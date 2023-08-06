import asyncio
import gzip
import json
import pickle
from datetime import datetime, timedelta, timezone
from typing import Union

import pandas as pd
from powerbot_client import ApiClient, ContractApi

from powerbot_backtesting.data_acquisition import get_public_trades_by_days
from powerbot_backtesting.exceptions import NotInCacheError
from powerbot_backtesting.utils import _find_cache, _cache_data, _orderbook_data_transformation, _delta_filter
from powerbot_backtesting.utils.constants import *


def get_orders(contract_hist_data: dict[str, pd.DataFrame]) -> dict[str, list[dict]]:
	"""
	Extracts all order data from contract history as is, without performing any quality control.

	Args:
		contract_hist_data (dict): Dictionary of Dataframes containing Contract History Data

	Returns:
		dict{key: [orders]}: Dictionary of Lists of Orders
	"""
	order_list = {}

	for key, value in contract_hist_data.items():
		bids_asks = []
		orders_all = value["orders"].to_list()
		for nr, orders in enumerate(orders_all):
			for k, v in orders.items():
				if v:
					if k == "bid":
						for x in v:
							x["type"] = "bid"
							x["best_bid_price"] = value.loc[nr, "best_bid_price"]
							x["best_bid_quantity"] = value.loc[nr, "best_bid_quantity"]
							x["vwap"] = value.loc[nr, "vwap"]
							bids_asks.append(x)
					if k == "ask":
						for x in v:
							x["type"] = "ask"
							x["best_ask_price"] = value.loc[nr, "best_ask_price"]
							x["best_ask_quantity"] = value.loc[nr, "best_ask_quantity"]
							x["vwap"] = value.loc[nr, "vwap"]
							bids_asks.append(x)

		order_list[key] = bids_asks

	return order_list


def get_ohlc_data(trade_data: dict[str, pd.DataFrame],
                  delivery_area: str,
                  timesteps: int,
                  time_unit: str,
                  api_client: ApiClient = None,
                  sql_export: bool = False,
                  use_cached_data: bool = True,
                  caching: bool = True,
                  gzip_files: bool = True,
                  one_file: bool = False) -> dict[str, pd.DataFrame]:
	"""
	Converts trade data into Open-High-Low-Close format in the specified timesteps.

	Args:
		trade_data (dict{key: DataFrame}): Dictionary of Dataframes containing Contract Trade Data
		delivery_area (str): Area Code for Delivery Area
		timesteps (int): Timesteps to group Trades by
		time_unit (str): Time units for timesteps (either hours, minutes or seconds)
		api_client: PowerBot ApiClient
		sql_export (bool): True if data was exported from SQL
		use_cached_data (bool): If True, function tries to load data from cache wherever possible
		caching (bool): True if data should be cached
		gzip_files (bool): True if cached files should be gzipped
		one_file (bool): True if data should be cached in a single JSON file

	Returns:
		dict{key: DataFrame}: Dictionary of DataFrames
	"""
	if not api_client and not sql_export:
		raise Exception("API data exports need a valid API client")

	# Setup Parameters
	all_ohlc_data = {}
	host = api_client.configuration.host if api_client else None
	environment = host.split("/")[2].split(".")[0] if host else "sql"
	exchange = host.split("/")[4] if host else list(trade_data.values())[0].exchange[0]
	file_ending = ".gz" if gzip_files else ""

	# Check if __cache__ already exists
	cache_path = _find_cache()

	for key, value in trade_data.items():
		# Check If Data Already Cached
		delivery_date = datetime.strptime(key.split(" ")[0], DATE_YMD)
		year_month = delivery_date.strftime(DATE_YM)
		day_month = delivery_date.strftime(DATE_MD)
		file_name = key.replace(f"{str(key).split(' ')[0]}", "").replace(":", "-")
		data_ohlc = None

		if use_cached_data:
			for i in [".json.gz", ".json"]:
				if cache_path.joinpath(f'{environment}\\{exchange}_{delivery_area}\\{year_month}\\{day_month}'
				                       f'\\processed\\{file_name}_ohlc_{timesteps}{time_unit[0]}{i}').exists():
					data_ohlc = pd.read_json(cache_path.joinpath(f'{environment}\\{exchange}_{delivery_area}\\'
					                                             f'{year_month}\\{day_month}\\processed\\'
					                                             f'{file_name}_ohlc_{timesteps}{time_unit[0]}{i}'),
					                         dtype=False)

		if isinstance(data_ohlc, pd.DataFrame):
			data_ohlc.rename(columns={0: 'exec_time'}, inplace=True)
			all_ohlc_data[key] = data_ohlc

		else:
			data_ohlc = value.set_index('exec_time')
			data_ohlc = data_ohlc['price'].resample(f'{timesteps}{time_unit[0]}').ohlc() if time_unit != "minutes" \
				else data_ohlc['price'].resample(f'{timesteps}{time_unit[:3]}').ohlc()
			data_ohlc = data_ohlc.dropna(how='all')

			# Append to complete OHLC collection
			all_ohlc_data[key] = data_ohlc

	# Cache Data as JSON
	if caching:
		_cache_data("ohlc", all_ohlc_data, delivery_area, exchange=exchange, api_client=api_client,
					gzip_files=gzip_files, timesteps=timesteps, time_unit=time_unit[0], as_csv=False)

	# Cache Data as JSON
	if caching:
		_cache_data("ohlc", all_ohlc_data, delivery_area, exchange=exchange, api_client=api_client,
		            gzip_files=gzip_files, timesteps=timesteps, time_unit=time_unit[0], as_csv=False)

	# Saving Complete OHLC Data as JSON
	if one_file and trade_data:
		# Take Day of Delivery Start
		# Parameters
		contract_times = sorted([i for i in [*trade_data]])
		first_contract = datetime.strptime(
			contract_times[0].replace(f"{str(contract_times[0]).split(' - ')[1]}", "").replace(" - ", ":00"),
			DATE_YMD_TIME_HMS)
		last_contract = datetime.strptime(
			contract_times[-1].replace(f"{str(contract_times[-1]).split(' ')[1]}", "").replace(" - ", "") + ":00",
			DATE_YMD_TIME_HMS)

		year_month = first_contract.strftime(DATE_YM)
		day_month = first_contract.strftime(DATE_MD)

		if len(contract_times) == 1:
			first_contract = first_contract.strftime(DATE_YMD_TIME_HMS_ALT)
			last_contract = None
		else:
			if first_contract.strftime(DATE_D) != last_contract.strftime(DATE_D):
				first_contract = first_contract.strftime(DATE_YMD_TIME_HM_ALT)
				last_contract = last_contract.strftime(DATE_YMD_TIME_HM_ALT)
			else:
				first_contract = first_contract.strftime(TIME_HM_ALT)
				last_contract = last_contract.strftime(TIME_HM_ALT)

		filename = f'all_ohlc_{first_contract} - {last_contract}_{timesteps}{time_unit[0]}.json.gz' \
			if last_contract else f'all_ohlc_{first_contract}_{timesteps}{time_unit[0]}.json{file_ending}'

		if not cache_path.joinpath(
				f"{environment}\\{exchange}_{delivery_area}\\{year_month}\\{day_month}\\processed\\{filename}").exists():
			if "gz" in file_ending:
				with gzip.open(cache_path.joinpath(
						f"{environment}\\{exchange}_{delivery_area}\\{year_month}\\{day_month}\\processed\\{filename}"),
						'wt', encoding="ascii") as f:
					json.dump(
						{key: {k: v.to_json() for (k, v) in value.items()} for (key, value) in all_ohlc_data.items()},
						f, default=str)
			else:
				with open(cache_path.joinpath(
						f"{environment}\\{exchange}_{delivery_area}\\{year_month}\\"
						f"{day_month}\\processed\\{filename}"), 'wt',
						encoding="ascii") as f:
					json.dump(
						{key: {k: v.to_json() for (k, v) in value.items()} for (key, value) in all_ohlc_data.items()},
						f, default=str)

	return all_ohlc_data


def get_orderbooks(contract_hist_data: dict[str, pd.DataFrame],
				   delivery_area: str,
				   timesteps: int = 15,
				   time_unit: str = "minutes",
				   timestamp: list[datetime] = None,
				   from_timestamp: bool = False,
				   api_client: ApiClient = None,
				   use_cached_data: bool = True,
				   caching: bool = True,
				   as_json: bool = False) -> dict[str, pd.DataFrame]:
	"""
	Converts contract history data into orderbooks in the specified timesteps. If no API client is passed, the function
	will automatically assume that the data is production data.

	Please be aware that optimally only data from one exchange at a time should be used (e.g. only EPEX).

	To generate specific orderbooks for a position closing algorithm, the timestamp and from_timestamp parameters can
	be used.

	Args:
		contract_hist_data (dict{key: DataFrame}): Dictionary of Dataframes containing Contract History Data
		delivery_area (str): Area Code for Delivery Area
		timesteps (int): Timesteps to group Orderbooks by
		time_unit (str): Time units for timesteps (either hours, minutes or seconds)
		timestamp (list[datetime]): List of timestamps to generate orderbooks at/ from
		from_timestamp (bool): True if timestamp serves as starting point for orderbook generation
		api_client: PowerBot ApiClient
		use_cached_data (bool): If True, function tries to load data from cache wherever possible
		caching (bool): True if single orderbooks should be cached as JSON
		as_json (bool): True if complete orderbook should be cached as JSON

	Returns:
		dict{key: DataFrame}: Dictionary of DataFrames
	"""
	# Setup
	all_order_books = {}

	host = api_client.configuration.host if api_client else None
	environment = host.split("/")[2].split(".")[0] if host else "prod"
	exchange = host.split("/")[4] if host else list(contract_hist_data.values())[0].exchange[0]

	# Parameters
	contract_times = sorted([i for i in [*contract_hist_data]])
	first_contract = datetime.strptime(
		contract_times[0].replace(f"{str(contract_times[0]).split(' - ')[1]}", "").replace(" - ", ":00"),
		DATE_YMD_TIME_HMS)
	last_contract = datetime.strptime(
		contract_times[-1].replace(f"{str(contract_times[-1]).split(' ')[1]}", "").replace(" - ", "") + ":00",
		DATE_YMD_TIME_HMS)

	year_month = first_contract.strftime(DATE_YM)
	day_month = first_contract.strftime(DATE_MD)

	if len(contract_times) == 1:
		first_contract = first_contract.strftime(DATE_YMD_TIME_HM_ALT)
		last_contract = None
	else:
		if first_contract.strftime(DATE_D) != last_contract.strftime(DATE_D):
			first_contract = first_contract.strftime(DATE_YMD_TIME_HM)
			last_contract = last_contract.strftime(DATE_MD_TIME_HM)
		else:
			first_contract = first_contract.strftime(TIME_HM_ALT)
			last_contract = last_contract.strftime(TIME_HM_ALT)

	# Check if __cache__ already exists
	cache_path = _find_cache()
	new_dir = cache_path.joinpath(f"{environment}\\{exchange}_{delivery_area}\\{year_month}\\{day_month}\\processed")

	# Processing Concurrently With Asyncio
	async def main():
		function_list = []
		for nr, (key, value) in enumerate(contract_hist_data.items()):
			function_list.append(
				__process_orderbook(key, value, str(new_dir), timesteps, time_unit,
				                    timestamp[nr] if timestamp else None, from_timestamp,
				                    all_order_books, use_cached_data))

		await asyncio.gather(*function_list)

	asyncio.run(main())

	# Cache Data as pickle
	if caching:
		_cache_data("orderbook", all_order_books, delivery_area, exchange=exchange, api_client=api_client,
		            gzip_files=False, timesteps=timesteps, time_unit=time_unit[0], as_json=False, as_pickle=True)

	# Saving Complete Orderbook as JSON
	if as_json:
		new_dir.mkdir(parents=True, exist_ok=True)

		filename = f'orderbook_{first_contract} - {last_contract}_{timesteps}{time_unit[0]}.json.gz' \
			if last_contract else f'orderbook_{first_contract}_{timesteps}{time_unit[0]}.json.gz'
		with gzip.open(new_dir.joinpath(filename), 'wt', encoding="ascii") as f:
			json.dump({key: {k: v.to_json() for (k, v) in value.items()} for (key, value) in all_order_books.items()},
			          f, default=str)

	return all_order_books


async def __process_orderbook(key: str,
							  value: pd.DataFrame,
							  directory: str,
							  timesteps: int,
							  time_unit: str,
							  timestamp: Union[datetime, None],
							  from_timestamp: bool,
							  orderbook_dict: dict[str, pd.DataFrame],
							  use_cached_data: bool):
	"""
	Asyncio function to process single order book. Return value is appended to collection of order books.

	Returns:
		pd.Dataframe: single order book
	"""
	# Setup Parameters
	units = {"hours": 0, "minutes": 0, "seconds": 0, time_unit: timesteps}
	delivery_start = datetime.strptime(key.replace(f"{str(key).split(' - ')[1]}", "").replace(" - ", ":00"),
	                                   DATE_YMD_TIME_HMS).replace(tzinfo=timezone.utc)
	timestamp = timestamp.replace(tzinfo=timezone.utc) if timestamp else None
	file_name = key.replace(f"{str(key).split(' ')[0]}", "").replace(":", "-")
	directory = directory.split('\\')
	directory = '\\'.join(directory)

	try:
		if not use_cached_data:
			raise NotInCacheError("Not loading from cache")
		# Check If Data Already Cached
		order_book_clean = pickle.load(open(f"{directory}\\{file_name}_orderbook_{timesteps}{time_unit[0]}.p", "rb"))
		orderbook_dict[key] = order_book_clean

	except (NotInCacheError, FileNotFoundError):
		# Filter out emtpy revisions
		order_filter = value.orders.map(lambda x: x if x["bid"] or x["ask"] else None)
		value = value.loc[~value.index.isin(order_filter[order_filter.isna()].index)]

		# Setting Either Starting Point or Specific Timestamp
		start_time = value.as_of.min().replace(minute=0, second=0, microsecond=0, tzinfo=timezone.utc)
		time = timestamp if timestamp and from_timestamp \
			else timestamp + timedelta(**{time_unit: timesteps}) if timestamp and not from_timestamp \
			else start_time + timedelta(**{time_unit: timesteps})
		time = start_time + timedelta(**{time_unit: timesteps}) if start_time > time else time

		order_book = {}

		# Transform orders
		df_bid_asks = _orderbook_data_transformation(value)

		if not df_bid_asks.empty:
			# Create a filter to shorten dataframe
			orders_del = set()

			# Main Loop
			while time <= delivery_start:
				# Shorten Bids_Asks
				if len(orders_del) != 0:
					df_bid_asks = df_bid_asks.loc[~df_bid_asks.order_id.isin(orders_del)]

				# Create New Temporary Dataframe
				if timestamp and not from_timestamp:
					df_temp = df_bid_asks.loc[df_bid_asks.as_of <= f'{timestamp}']

				else:
					df_temp = df_bid_asks.loc[(df_bid_asks.as_of >= f'{start_time}') & (df_bid_asks.as_of <= f'{time}')]

				# Delete all orders before the last delta == False
				df_temp = _delta_filter(df_temp)

				if not df_temp.empty:
					# Extract Order IDs for Quantity = 0 & Update Set Of Order IDs
					contract_ids = df_temp.contract_id.unique().tolist()
					orders_del.update(df_temp.loc[df_temp.quantity == 0].order_id.tolist())

					# Check For Uniformity of Contract ID
					if len(contract_ids) == 1:
						# QC For Temporary Dataframe
						# Add Filtered Df To Orderbook
						if timestamp and not from_timestamp:
							order_book[f"{timestamp}"] = df_temp.loc[~df_temp.order_id.isin(orders_del)]
						else:
							order_book[f"{time}"] = df_temp.loc[~df_temp.order_id.isin(orders_del)]

					else:
						# If There Are Multiple Contracts In The Same Orderbook -> Create 2 Separate Orderbooks
						dataframes = []
						df_check_1 = df_temp.loc[df_temp.contract_id == contract_ids[0]]
						dataframes.append(df_check_1)
						df_check_2 = df_temp.loc[df_temp.contract_id == contract_ids[1]]
						df_check_2 = df_check_2.loc[df_check_2.as_of > f'{time - timedelta(**units)}']
						dataframes.append(df_check_2)

						# Quality Control For Temporary Dataframe
						temp_dataframe_list = []

						for nr, val in enumerate(dataframes):
							# Quality Control For Temporary Dataframe
							df_check = val.loc[~val.order_id.isin(orders_del)]

							if not df_check.empty:
								temp_dataframe_list.append(df_check)  # Add Filtered Df To List

						if len(temp_dataframe_list) == 1:
							order_book[f"{timestamp if timestamp and not from_timestamp else time}"] = \
								temp_dataframe_list[0]
						else:
							for nr, val in enumerate(temp_dataframe_list):
								if not nr:
									order_book[
										f"{(timestamp if timestamp and not from_timestamp else time) - timedelta(seconds=1)}"] = val
								else:
									order_book[f"{timestamp if timestamp and not from_timestamp else time}"] = val

				# Progress In Time Or Break Loop If Timestamp Exists
				if timestamp and not from_timestamp:
					break

				# Adjust Start Time To New Contract if necessary
				if time == (delivery_start - timedelta(hours=1)):
					start_time = time

				# Time Progression
				time += timedelta(**units)

			# General Quality Control
			# Delete All Order ID Duplicates & Empty Timesteps
			order_book_clean = {
				key: value.sort_values(by=['as_of'], ascending=False).drop_duplicates(subset="order_id", keep="first",
				                                                                      inplace=False) for (key, value) in
				order_book.items()}
			order_book_clean = {key: value for (key, value) in order_book_clean.items() if not value.empty}

		else:
			order_book_clean = df_bid_asks

	orderbook_dict[key] = order_book_clean


def calc_trade_vwap(api_client: ApiClient,
                    contract_time: str,
                    delivery_area: str,
                    trade_data: dict[str, pd.DataFrame] = None,
                    time_from: datetime = None,
                    previous_days: int = 10,
                    contract_id: str = None,
                    index: str = "ID3") -> pd.DataFrame:
	"""
	Function gets trades for a certain contract for X previous days in the same delivery period and calculates their
	VWAP for ID3 or ID1 or all. Generates a new list of trades for these contracts.
	Can take either a time period or a specific contract ID to load data for.

	If previous days is 0, only the trades for the original time period/ contract will be loaded.

	Can also be called directly from get_public_trades with parameter 'add_vwap' to add VWAP to loaded trades.

	Args:
		api_client: PowerBot ApiClient
		contract_time (str): hourly, half-hourly or quarter-hourly
		delivery_area (str): Area Code for Delivery Area
		trade_data (dict[str, pd.DataFrame]: Dictionary of Dataframes containing Contract Trade Data
		time_from (str/ datetime): yyyy-mm-dd hh:mm:ss
		previous_days (int): Amount of previous days to load data
		contract_id (str): ID of specific Contract
		index (str): all, ID3, ID1

	Returns:
		DataFrame: Trade Data with added calculated fields
	"""
	# Setup
	indices = {"all": 1980, "ID3": 180, "ID1": 60}
	contract_api = ContractApi(api_client)

	# Create Empty Dataframe
	all_trade_data = pd.DataFrame(
		{'trade_id': [], 'buy_delivery_area': [], 'sell_delivery_area': [], 'api_timestamp': [],
		 'exec_time': [], 'contract_id': [], 'price': [], 'quantity': [], 'self_trade': [], 'time_diff': []})

	# Get Delivery Start If Contract ID was passed
	if contract_id:
		if not isinstance(contract_id, str):
			raise TypeError("contract_id has to be a string")
		time_from = str(contract_api.find_contracts(contract_id=[contract_id])[0].delivery_start).replace("+00:00", "")

	# Get Trade Data
	trade_data = trade_data if trade_data else get_public_trades_by_days(api_client=api_client,
	                                                                     time_from=time_from,
	                                                                     previous_days=previous_days,
	                                                                     delivery_area=delivery_area,
	                                                                     contract_time=contract_time)

	# Processing
	for key, value in trade_data.items():
		# Time Difference In Minutes
		time = datetime.strptime(key.replace(f"{str(key).split(' - ')[1]}", "").replace(" - ", ":00"),
		                         DATE_YMD_TIME_HMS)
		time_diff = [round((time.replace(tzinfo=None) - i.replace(tzinfo=None)).total_seconds() / 60, 2) for i in
		             value.exec_time]
		value["time_diff"] = time_diff
		all_trade_data = all_trade_data.append(value)

	all_trade_data = all_trade_data.loc[all_trade_data["time_diff"] <= indices[index]].sort_values(by=['time_diff'],
	                                                                                               ascending=False)
	total_quantity = all_trade_data.quantity.sum()
	all_quantities = all_trade_data.quantity.tolist()
	all_prices = all_trade_data.price.tolist()

	target_volume = []
	cumulated_quantities = []
	calculated_vwaps = []
	cum_weighted_price = 0

	for nr, item in enumerate(all_quantities):
		cum_sum = round(sum(all_quantities[:nr + 1]), 2)
		cum_weighted_price += all_prices[nr] * all_quantities[nr]
		calculated_vwaps.append(round(cum_weighted_price / cum_sum, 2))
		cumulated_quantities.append(cum_sum)
		target_volume.append(round(cum_sum / total_quantity, 4))

	all_trade_data["cumulated_quantity"] = cumulated_quantities
	all_trade_data["target_volume"] = target_volume
	all_trade_data["vwap"] = calculated_vwaps

	return all_trade_data.reset_index(drop=True)


def calc_single_vwap(objects: dict[str, pd.DataFrame],
                     desired_depth: float,
                     min_depth: float = None) -> dict[str, float]:
	"""
	This method can be used to calculate the weighted average price for a dictionary of dataframes (e.g. orders, trades)
	at a desired depth. The output is a singular value for each dataframe.
	This function does not load any data, therefore the already existing data object has to be passed as an argument.

	Args:
		objects (dict[str, DataFrame or list[str, dict]): A dictionary of dataframes, each of which needs to have a
		'quantity' and a 'price' field. Alternatively, a list of dictionaries can be passed as well.
		desired_depth (float): The depth (in MW) specifying how many of the objects should be taken into consideration.
		min_depth (float): The required minimum depth (in percent of the desired depth). If this requirement is not met,
		return value is 0.

	Returns:
		dict[str, float]: The weighted average price for the desired depth for each key in the dictionary.
	"""
	if min_depth and min_depth > 0.99:
		raise Exception("The minimum depth has to be given as percentage of the desired depth.")

	vwaps = {k: 0 for k in [*objects]}

	for key, obj in objects.items():
		if not isinstance(obj, pd.DataFrame):
			obj = pd.DataFrame(obj)
		available_depth = 0
		total_value = 0

		for ind, row in obj.iterrows():
			if available_depth + row.quantity < desired_depth:
				available_depth = available_depth + row.quantity
				total_value += row.quantity * row.price
			else:
				total_value += (desired_depth - available_depth) * row.price
				available_depth += desired_depth - available_depth
				available_depth = round(available_depth, 2)
				break

		# If the 'min_depth' parameter is set,
		# then the available depth on the market has to fulfill the minimum requirements.
		if min_depth and available_depth and available_depth > desired_depth * min_depth\
				or not min_depth and available_depth:
			vwaps[key] = round(total_value / available_depth, 2)

	return vwaps
