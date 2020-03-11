import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime


def getWebsiteAndReturnContent(URL):
    page = requests.get(URL)
    return BeautifulSoup(page.content, 'html.parser')

def getFirstHrefFromAnchorInDiv(soup):
    return soup.find('a')['href']

def getArticles(soup):
    return soup.findAll("article", {"class": "b-article"})

def getURLsFromArticles(articles):
    URLs = []
    for article in articles:
        URLs.append(getFirstHrefFromAnchorInDiv(article))
    return URLs

def getBaseArticle(articlesURL):
    return getWebsiteAndReturnContent(articlesURL).find("article",{"class": "b-article-detail"})

def getDictDataFromArticle(baseArticle):
    dictData = {       
    }

    try:
        if baseArticle.find("h2", {"class": "subtitle"}) is not None:
            dictData['subtitle'] = baseArticle.find("h2", {"class": "subtitle"}).get_text()

        if baseArticle.find("div", {"class": "intro"}) is not None:
            dictData['intro'] = baseArticle.find("div", {"class": "intro"}).get_text()

        if  baseArticle.find("div", {"class": "info"}) is not None:
            dictData['info'] = baseArticle.find("div", {"class": "info"}).get_text()

        if baseArticle.find("h1", {"class": "title"}) is not None:
            dictData['title'] = baseArticle.find("h1", {"class": "title"}).get_text()

        if baseArticle.find("div", {"id": "__xclaimwords_wrapper"}) is not None:
            dictData['article'] = baseArticle.find("div", {"id": "__xclaimwords_wrapper"}).get_text()
    except:
        print(baseArticle)    
    return dictData




URL = 'https://www.bljesak.info'

welcomePage = getWebsiteAndReturnContent(URL)

articles = getArticles(welcomePage)

articlesURL = getURLsFromArticles(articles)

dt_string = datetime.now().strftime("%H%M%S_%d%m%Y")

data = {}
data['articles'] = []
# print(getDictDataFromArticle(getBaseArticle(articlesURL[0])))
for articleURL in articlesURL:
    data['articles'].append(getDictDataFromArticle(getBaseArticle(articleURL)))

with open('bljesak_'+dt_string+'.json', 'w') as outfile:
    json.dump(data, outfile)
