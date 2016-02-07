# Maja Svanberg
# classify.py
# USER THIS BY INVOKING THE getType(url) function on any url

import requests
import urllib
from bs4 import BeautifulSoup


def getText(url):
    """Takes a url and returns a string version of the html file"""
    html_text = urllib.urlopen(url).read()
    soup = BeautifulSoup(html_text, 'html.parser')
    # First get the meta description tag
    description = soup.findAll(attrs={"name":"description"}) 
    if  len(description) != 0:
        return description[0]['content'].encode('utf-8')
    

def getType(url):
    text = getText(url)
    prms = {'api_key': '837ea8ebf50b511d618341ad4fb15e88', \
                'text': text}
    r = requests.get('http://api.datumbox.com/1.0/TopicClassification.json', params =prms)
    if r.text[0] == '{':
        return r.text[31:-2]

