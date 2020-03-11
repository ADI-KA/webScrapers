import requests
from bs4 import BeautifulSoup
import json

def getWebsiteAndReturnContent(URL):
    page = requests.get(URL)
    return BeautifulSoup(page.content, 'html.parser')

def getFirstHrefFromAnchorInDiv(soup):
    try:
        return soup.find('a')['href']
    except:
        print("")

def getArticles(soup):
    return soup.findAll("div", {"class": "articleHolder"})

def getURLsFromArticles(articles):
    URLs = []
    for article in articles:
        URLs.append(getFirstHrefFromAnchorInDiv(article))
    return URLs

def getBaseArticle(articlesURL):
    return getWebsiteAndReturnContent(articlesURL).find("div",{"class": "block-dyn"})

def getDictDataFromArticle(baseArticle):
    dictData = {       
    }
    try:
        if baseArticle.find("div", {"class": "nadnaslov"}) is not None:
            dictData['subtitle'] = baseArticle.find("div", {"class": "nadnaslov"}).div.span.get_text()

        if baseArticle.find("div", {"class": "uvod-clanka"}) is not None:
            dictData['intro'] = baseArticle.find("div", {"class": "uvod-clanka"}).get_text()

        if baseArticle.find("div", {"class": "naslov"}) is not None:
            dictData['title'] = baseArticle.find("div", {"class": "naslov"}).h1.get_text()

        if baseArticle.find("div", {"class": "tekst"}) is not None:
            dictData['article'] = baseArticle.find("div", {"class": "tekst"}) .get_text()
    except:
        print(baseArticle)    
    return dictData




URL = 'https://www.klix.ba'

welcomePage = getWebsiteAndReturnContent(URL)

articles = getArticles(welcomePage)


articlesURL = getURLsFromArticles(articles)

data = {}
data['articles'] = []
for articleURL in articlesURL:
    if articleURL is not None:
        data['articles'].append(getDictDataFromArticle(getBaseArticle(URL + articleURL)))

with open('klix.json', 'w') as outfile:
    json.dump(data, outfile)
