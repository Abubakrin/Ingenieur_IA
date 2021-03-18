import requests, uuid, json

# Add your subscription key and endpoint
subscription_key = "c0861480097049cfaadc8ce4d827039c"
endpoint = "https://api.cognitive.microsofttranslator.com/"

# Add your location, also known as region. The default is global.
# This is required if using a Cognitive Services resource.
location = "francecentral"

path = '/detect'
constructed_url = endpoint + path

params = {
    'api-version': '3.0',
    'to': ['de', 'it', 'ar']
}
constructed_url = endpoint + path

headers = {
    'Ocp-Apim-Subscription-Key': subscription_key,
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

mon_fichier_x      = open("x_train.txt","r", encoding= "utf8")
mon_fichier_y      = open("y_train.txt","r", encoding= "utf8")
contenu_x          = mon_fichier_x.readlines()
contenu_y          = mon_fichier_y.readlines()


def recup_texte(label, nb_para):
    print('Détection du label :', label,' et chargement de ', nb_para,' paragraphes')
    i = 0
    j = 0
    global taux_success
    paragraphes = []
    for ligne_y in contenu_y:
        ligne_y = ligne_y.strip(' \n\t')
        if label == ligne_y:
            if j < nb_para:
                paragraphes.append(contenu_x[i])
                j += 1
        i += 1
        
    i_lang = len(paragraphes)
    taux_success.append(detectLang(label,*paragraphes))


def detectLang(label, *param):
    i_succ = 0
    tx_success = 0
    i_lang = len(param)

    for elt in param:
        body = [{
            'text': elt
        }]

        request = requests.post(constructed_url, headers=headers, json=body)
        response = request.json()
        sc = response[0]
        if sc['language'] == 'zh-Hant' and label == 'zho':
            i_succ += 1
        if sc['language'] == 'es' and label == 'spa':
            i_succ += 1
        if sc['language'] == 'en' and label == 'eng':
            i_succ += 1
        if sc['language'] == 'hi' and label == 'hin':
            i_succ += 1
        if sc['language'] == 'ar' and label == 'ara':
            i_succ += 1
    #   print(i_succ)
    if i_lang != 0:
        tx_success = i_succ / i_lang * 100
        return tx_success

# You can pass more than one object in body.
body = [{
    'text': 'Hello World!'
}]

request = requests.post(constructed_url, params=params, headers=headers, json=body)
response = request.json()

print(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))