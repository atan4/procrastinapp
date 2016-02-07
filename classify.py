# Maja Svanberg
# classify.py
# USER THIS BY INVOKING THE getType(url) function on any url

import requests
import urllib
from bs4 import BeautifulSoup
import Procrastinapp


def getText(url):
    """Takes a url and returns a string version of the html file"""
    html_text = urllib.urlopen(url).read()
    soup = BeautifulSoup(html_text, 'html.parser')
    # First get the meta description tag
    description = soup.findAll(attrs={"name":["description", "Description"]}) 
    if  len(description) != 0:
        # if such exists, return the content of the first description
        return description[0]['content'].encode('utf-8')
    

def getType(url):
    '''takes a url as an input and returns the category it belongs to
    based on meta description'''
    text = getText(url)
    # calls the datumbox API to categorize content
    prms = {'api_key': '837ea8ebf50b511d618341ad4fb15e88', \
                'text': text}
    r = requests.get('http://api.datumbox.com/1.0/TopicClassification.json', params =prms)
    # if text starts with {, returns the category
    if r.text[0] == '{':
        return r.text[31:-2]


#print getType('http://www.huffingtonpost.com/')

#print 'x'
def top3categories(df):
    '''takes a dataframe and changes it, adds category'''
    df['category'] = df['url'].apply(classify.getType)
    grouped = df['visit_count'].groupby('category').sum()

    
#dataf = Procrastinapp.fromTextToPickle('msvanberg@wellesley.edu', 'History.txt') 

#print top3categories(dataf)
