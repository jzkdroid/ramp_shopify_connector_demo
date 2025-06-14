from flask import Flask, request, render_template, jsonify
import requests


app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('home.html')

@app.route("/create_bill")
def create_bill():
	url = "https://demo-api.ramp.com/developer/v1/bills"
	payload="{\n    \"due_at\": \"2025-06-14\",\n    \"entity_id\": \"bdbe9108-1d28-41f3-995e-eb4e1bde3c12\",\n    \"invoice_currency\": \"USD\",\n    \"invoice_number\": \"12345676543\",\n    \"issued_at\": \"2025-06-13\",\n    \"payment_method\": \"PAID_MANUALLY\",\n    \"vendor_contact_id\": \"2b355861-0305-4505-947c-9b8bb66f61c1\",\n    \"vendor_id\": \"ea58ca32-984a-4187-9fb7-ad8ba85b185b\",\n    \"line_items\": [\n        {\n            \"accounting_field_selections\": [],\n            \"amount\": 100,\n            \"memo\": \"Printing services\"\n        }\n    ]\n}"
	headers = {
	'Authorization': 'Bearer ramp_tok_VE6WxSDD8lEdtMYcSxjRboLkw30SwMKEunIusiMZ8L',
	'Content-Type': 'application/json'
	}
	response = requests.request("POST", url, headers=headers, data=payload)
	print(response.json())
	return response.json()


@app.route("/import_from_shopify", methods = ['POST'])
def import_from_shopify():
	data = request.get_json()
	line_items = data.get("line_items")
	for x in line_items:
		print(x.get("product_id"))
		if str(x.get("product_id")) == "7819102093411":
			print("We are calling ramp")
			create_bill()
	return jsonify(data)