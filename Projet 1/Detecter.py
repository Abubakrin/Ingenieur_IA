import json
import requests
import uuid

# Add your subscription key and endpoint
subscription_key = "USE UR KEY API"
endpoint = "https://api.cognitive.microsofttranslator.com"

# Add your location, also known as region. The default is global.
# This is required if using a Cognitive Services resource.
location = "francecentral"

path = '/detect'
constructed_url = endpoint + path

params = {
    'api-version': '3.0'
}
constructed_url = endpoint + path

headers = {
    'Ocp-Apim-Subscription-Key': subscription_key,
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

print("\nBonjour ici le chatbot de la banque Credit")
textADetecter = str(input("Entrez votre requête dans la langue que vous souhaitez:\n"))
# You can pass more than one object in body.
body = [{
    'text': textADetecter
}]

request = requests.post(constructed_url, params=params, headers=headers, json=body)
response = request.json()

print(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))
