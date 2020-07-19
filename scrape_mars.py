#!/usr/bin/env python
# coding: utf-8

# # Mission to Mars
from bs4 import BeautifulSoup
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import pandas as pd
import requests
import pymongo
import flask
import time
# # NASA Mars News
def scrape():

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(news_url)
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    articles = soup.find('li', class_='slide')
    headlines = articles.find('div', class_="content_title")
    news_title = headlines.text.strip()

    body = articles.find('div', class_="article_teaser_body")
    news_p = body.text.strip()
    news = {"title":news_title,"para":news_p}
    #print("news_p")
    # print(news_p)

    # # JPL Mars Space Images - Featured Image
    feat_img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(feat_img_url)
    time.sleep(2)
    soup2 = BeautifulSoup(browser.html, 'html.parser')
    img = soup2.find('a', class_="button fancybox")
    img_url = img['data-fancybox-href']
    featured_image_url = 'https://www.jpl.nasa.gov' + img_url

    # # Mars Weather
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    time.sleep(2)
    soup3 = BeautifulSoup(browser.html, 'html.parser')
    tweet = soup3.find('div', class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0')
    #print(tweet)

    # # Mars Facts
    facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(facts_url)
    facts = tables[0]
    html_table = facts.to_html()
    # html_table
    #may want to strip unwanted newlines to clean up table
    #html_table.replace('\n', '')

    #can also save the table directly to a file
    #facts.to_html('file.html')


    # # Mars Hemispheres
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)
    time.sleep(2)
    soup4 = BeautifulSoup(browser.html, 'html.parser')
    container = soup4.find('div', class_="description")
    hemis =[]
    for i in soup4.findAll("div", class_="item"):
        #todo click url to get the full image and put in img_url, clean up soup4 and html4
        try:
            browser.visit("https://astrogeology.usgs.gov/"+i.find("a",class_="itemLink").get("href"))
            time.sleep(2)
            innerHtml = browser.html
            innerSoup = BeautifulSoup(innerHtml,'html.parser')
            innerDl = innerSoup.find("div",class_="downloads")
            innerjpeg=innerDl.find("a").get("href")          
            
        except Exception as e:
            print("Error getting full image browser page\n",e)    
        hemis.append({"title":i.find("h3").getText(),"img_url":innerjpeg,"desc":i.find("p").getText()})

    # print(hemis)
    final = {"hemis":hemis,"twitter":tweet.getText(),"table":html_table,"featured_img":featured_image_url,"news":news}
    browser.quit()

    return final
