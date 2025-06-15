from flask import Flask, request, render_template, jsonify
import requests
import datetime
import random
import json


app = Flask(__name__)

@app.route("/")
def hello_world():
	return render_template('home.html')

@app.route("/create_bill")
def create_bill(full_name):
	todays_date = datetime.datetime.today()
	due_date = todays_date + datetime.timedelta(days=60)
	todays_date_string = todays_date.strftime('%Y-%m-%d')
	due_date_string = due_date.strftime('%Y-%m-%d')
	url = "https://demo-api.ramp.com/developer/v1/bills"
	payload={
		'due_at': due_date_string,
		'entity_id': 'bdbe9108-1d28-41f3-995e-eb4e1bde3c12',
		'invoice_currency': 'USD',
		'invoice_number': random.randint(3, 9),
		'issued_at': todays_date_string,
		'line_items': [ {
			'accounting_field_selections': [],
			'amount': 470,
			'memo': 'Custom Snowboard for ' + full_name
			}],
		'payment_method': 'PAID_MANUALLY',
		'vendor_contact_id': '69ecbbe1-330f-4bf0-bc25-27b8775113de',
		'vendor_id': '864d239e-f5de-4c4c-a107-a65b4a9ecc5c'
		}
	headers = {
	'Authorization': 'Bearer ramp_tok_VE6WxSDD8lEdtMYcSxjRboLkw30SwMKEunIusiMZ8L',
	'Content-Type': 'application/json'
	}
	response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
	print(request.json())
	print(response.json())
	return response.json()


@app.route("/import_from_shopify", methods = ['POST'])
def import_from_shopify():
	data = request.get_json()
	line_items = data.get("line_items")
	for x in line_items:
		print(x.get("product_id"))
		if str(x.get("product_id")) == "7819102093411":
			print("Compiling customer name")
			memo = "Custom snowboard for " + data.get("customer").get("first_name") + " " + data.get("customer").get("last_name") + ". Order Number: " + str(data.get("order_number"))
			create_bill(memo)
	return jsonify(data)