import requests
import uuid
import sys
from matplotlib import pyplot as plt

# Add your subscription key and endpoint
subscription_key = "USE UR KEY API"
endpoint = "https://api.cognitive.microsofttranslator.com/"

# Add your location, also known as region. The default is global.
# This is required if using a Cognitive Services resource.
location = "francecentral"

path = '/detect?api-version=3.0'
constructed_url = endpoint + path

params = {
    'api-version': '3.0',
    'to': ['de', 'it', 'ar']
}

headers = {
    'Ocp-Apim-Subscription-Key': subscription_key,
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

mon_fichier_x = open("x_train.txt", "r", encoding="utf8")
mon_fichier_y = open("y_train.txt", "r", encoding="utf8")
contenu_x = mon_fichier_x.readlines()
contenu_y = mon_fichier_y.readlines()


def recup_texte(label, nb_para):
    print('Détection du label :', label, ' et chargement de ', nb_para, ' paragraphes')
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

    len(paragraphes)
    taux_success.append(detect_lang(label, *paragraphes))


def detect_lang(label, *param):
    i_succ = 0
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
lang_label = ['zho', 'spa', 'eng', 'hin', 'ara']
taux_success = []

for lab in lang_label:
    recup_texte(lab, 1)

print(taux_success)

mon_fichier_x.close()
mon_fichier_y.close()

languages = ['zh', 'es', 'en', 'hi', 'ar']
xs = [i + 0.1 for i, _ in enumerate(languages)]

print(sys.executable)

plt.bar(xs, taux_success)
plt.title("Success rates for the 5 most spoken languages")
plt.ylabel("Success rate")
plt.xlabel("Language code ISO 6391")
#plt.xticks([i + 0.1 for i, _ in enumerate(languages)], languages)
plt.show()
