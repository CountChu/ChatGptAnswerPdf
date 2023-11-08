import requests
import pdb
br = pdb.set_trace

def is_sensitive(text):
    API_KEY = "YOUR_API_KEY_HERE"
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=" + API_KEY
    data = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}}
    }
    response = requests.post(url, json=data)
    response_dict = response.json()
    br()
    toxicity_score = response_dict['attributeScores']['TOXICITY']['summaryScore']['value']
    if toxicity_score > 0.5:
        return "YES"
    else:
        return "NO"

text = '我們有3個人共同製作投影片。我是主要製作人和主講者，其他兩人SX和YP可以幫我製作投影片。該如何分工？'
is_sensitive(text)