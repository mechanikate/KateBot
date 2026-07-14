import json
def daily():
	print("Clearing odds exp")
	data = {"odds_power": 3, "balances": {}}
	try:
		with open("econ.json", "r") as f:
			data = json.load(f)
	except:
		pass
	data["odds_power"] = 3
	with open("econ.json", "w+") as f:
		json.dump(data, f)
daily()
