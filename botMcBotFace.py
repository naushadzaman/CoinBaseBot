#!/usr/bin/env python
# encoding: utf-8

__author__      = "Naushad UzZaman (@naushadzaman)"

import os 
import sys 
import time
import json 

import gdax

filepath = os.path.abspath(os.path.dirname(__file__)) + "/"

# define files, change names here. 
trade_file = filepath + "trade_queue.txt"
history_file = filepath + "history.txt"
config_file = filepath + "config"

# index, mappings, accepted variables 
index = {0:"currency", 1:"action", 2:"gte_or_lte", 3:"target", 4:"budget"}
reverse_index = {index[x]:x for x in index}
accepted_currencies = ["BTC", "ETH", "LTC"]
accepted_actions = ["BUY", "SELL"]
gte_or_lte = ["<", ">", "<=", ">="]

debug = False 

# coinbase params 
currency_code = 'USD' 

public_client = gdax.PublicClient()

def get_spot_price(crypto_currency, currency_code): 
	try: 
		return public_client.get_product_ticker(product_id=crypto_currency+'-'+currency_code)
	except: 
		None 


def get_config_line_info(line): 
	return ":".join(line.split(":")[1:]).strip()


def load_config(config_file): 
	config_text = open(config_file).read().strip().split("\n")
	config = {"coinbase":{
		"Key":get_config_line_info(config_text[0]), 
		"Secret":get_config_line_info(config_text[1])
		},
		"twilio":
		{
		"Key":get_config_line_info(config_text[2]), 
		"Secret":get_config_line_info(config_text[3]),
		"Message":get_config_line_info(config_text[4]),
		"Param1":get_config_line_info(config_text[5]),
		"Param2":get_config_line_info(config_text[6]),
		}
	}
	return config


def send_text(config, message): 
	# curl1 = "curl 'https://api.twilio.com/2010-04-01/Accounts/AC312e5fddb054379c65c099339db9d102/Messages.json' -X POST --data-urlencode 'To=+15857481778' --data-urlencode 'From=+15859783469' --data-urlencode 'Body=Buy LTC' -u AC312e5fddb054379c65c099339db9d102:61246dd6050fac4570e1abeaed5c68e1"
	# message = "Buy LTC"
	curl2 = "curl '"+ config["twilio"]["Message"] + config["twilio"]["Param1"] + message + config["twilio"]["Param2"]
	# print(curl1)
	print(curl2)
	# if(curl1 == curl2): 
	os.system(curl2)


def get_client(): 
	config = load_config(config_file)
	client = Client(config["coinbase"]["Key"], config["coinbase"]["Secret"])
	return client

def read_trade_line(line): 
	line_split = [x.strip() for x in line.split(",")]
	max_index = max(index.keys())
	found_error = False 

	# check if contains at least expected number of entries 
	if len(line_split) - 1 < max_index: 
		found_error = "does not contain expected number of entries "

	# check if contains accepted currencies 
	elif not line_split[reverse_index["currency"]] in accepted_currencies: 
		found_error = "does not contain accepted currencies" 

	# check if contains accepted actions 
	elif not line_split[reverse_index["action"]] in accepted_actions: 
		found_error = "doest not contain accepted actions" 

	# check gte_or_lte operations 	
	elif not line_split[reverse_index["gte_or_lte"]] in gte_or_lte: 
		found_error = "does not contain proper gte / lte operations" 

	try: 
		if line_split[reverse_index["gte_or_lte"]] in ["<", '<=']: 
			line_split[reverse_index["gte_or_lte"]] = "lte"
		elif line_split[reverse_index["gte_or_lte"]] in [">", '>=']: 
			line_split[reverse_index["gte_or_lte"]] = "gte"

		line_split[reverse_index["target"]] = float(line_split[reverse_index["target"]])
		line_split[reverse_index["budget"]] = float(line_split[reverse_index["budget"]])
	except: 
		found_error = True 

	if found_error: 
		if debug: 
			print("Line error:", line)
			print(found_error)
			print("Expected format: currency, action, gte_or_lte, targer, budget")
			print("\n")
		return None 

	return line_split


def get_trade_queue(trade_file): 
	trade_queue = []
	file = open(trade_file)
	for line in file: 
		line = line.strip() 
		trade = read_trade_line(line)
		if not trade is None: 
			trade_queue.append(trade)
	file.close()
	return trade_queue


def match_trade_criteria(trade, spot_price): 
	target_price = trade[reverse_index["target"]] 
	budget = trade[reverse_index["budget"]] 

	trading = False 
	if trade[reverse_index["gte_or_lte"]] == "lte": 
		if spot_price < target_price: 
			trading = True 
	elif trade[reverse_index["gte_or_lte"]] == "gte": 
		if spot_price > target_price: 
			trading = True 

	if trading: 
		message = trade[reverse_index["action"]] + " " + str(trade[reverse_index["budget"]]) + " " + currency_code + " of " + str(trade[reverse_index["currency"]]) + " NOW!!! at " + str(spot_price) 
		return message
	return None 


def McBotFaceLetsRoll(): 
	config = load_config(config_file)
	# client = get_client()
	# print(json.dumps(config, indent=3))
	count = 0 
	time_sleep = 3
	print_interval = 10
	
	while True:
	# if True: 
		price_dict = {}
		trade_queue = get_trade_queue(trade_file)
		for trade in trade_queue: 
			crypto_currency = trade[reverse_index["currency"]]
			try: 
				spot = get_spot_price(crypto_currency, currency_code)
				spot_price = float(spot["price"])
				if spot_price is None: continue 
			except: 
				continue
			price_dict[crypto_currency] = spot_price
			price_dict["time"] = spot[u'time']
			if debug and count % print_interval == 0: 
				print(trade)
				print("Spot price:", spot_price)
				print("")
				print(spot)
			
			message = match_trade_criteria(trade, spot_price)
			if message: 
				print(message)
				send_text(config, message)
				exit()
			
		time.sleep(time_sleep)
		spot = get_spot_price(crypto_currency, currency_code)

		if count % print_interval == 0: 
			print(json.dumps(price_dict, indent=3))

		count += 1 
		
if __name__ == "__main__": 
	McBotFaceLetsRoll()
	