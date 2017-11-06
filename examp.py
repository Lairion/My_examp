import requests
import json
js = json.dumps({"quote": {
        "shipper": {
          "country":"FR",
          "postal_code": "06100",
          "city": "Nice"
        },
        "recipient": {
          "is_a_company": "false",
          "country": "FR",
          # "postal_code": "06000",
          "city": "Nice"
        },
        "parcels": [
          {
            "weight": 10,
            "length": 10,
            "width": 10,
            "height": 10
          },
          {
            "weight": 10,
            "length": 10,
            "width": 10,
            "height": 10
          }
        ]
      }})
req = requests.get("https://api.myflyingbox.com/v2/quotes",
	auth = ('sas_catchingbox', '-mHd_z4AVy6YSPSYAtsSX1wjy4fj8uC-'), 
	data = js
      ) 
res = json.loads(req.text)

offers = res["data"][0]["offers"]

def sort_by_price(offer):
	return offer["total_price"]["amount_in_cents"]

def filter_offers(offers):
	new_offers = []
	for offer in offers:
		details_en = offer["product"]["details"]['en']
		details_en = details_en.split('\r\n')
		dict_details = {}
		for i in details_en:
			new_list = i.split(":")
			dict_details.update({new_list[0].strip().lower():new_list[1].strip()})
		in_office = dict_details.get('delivery in office',"NO").upper() == "NO"
		at_home = dict_details.get('delivery at home',"NO").upper() == "NO"
		if in_office and at_home:
			new_offers.append(offer)
	new_offers = sorted(new_offers, key=sort_by_price)
	return new_offers

new_offers = filter_offers(offers)


# for offer in new_offers:
# 	print(offer['id'])
# 	print(offer["total_price"]["amount_in_cents"])
# print(len(new_offers))


js = {'location[street]':" 44 Rue Vernier",'location[city]':"Nice"}
req = requests.get("https://api.myflyingbox.com/v2/offers/"+new_offers[0]["id"]+"/available_delivery_locations",
	auth = ('sas_catchingbox', '-mHd_z4AVy6YSPSYAtsSX1wjy4fj8uC-'),  
	data= js
      )

res = json.loads(req.text)
deliveries = res['data']
def get_addresses(deliveries):
	deliveries_addresses = []
	for delivery in deliveries:
		deliveries_addresses.append(
			{
			"street":delivery['street'],
			"city":delivery["city"],
			"postal_code":delivery['postal_code'],
			}
			)
	return deliveries_addresses
addresses = get_addresses(deliveries)
print(addresses)

