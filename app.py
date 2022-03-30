#!/usr/bin/env python
from urllib import request
import random
import requests
import urllib
import time
from datetime import date
import sys
import re
import json
from flask_wtf import FlaskForm
from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

class Film:
    def __init__(self, name, year):
        self.name = name
        self.year = year


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


def get_posters(page):
    filmList = []
    if page.ready == False:
        page.Load();
    # read posters
    posterContainer = page.soup.find(class_='poster-list')
    if posterContainer:
    #<img alt="John Wick: Chapter 2" class="image" height="105" src="https://s1.ltrbxd.com/static/img/empty-poster-70.84a.png" width="70"/>
        nameList = posterContainer.find_all('img')
        for film in range(0, len(nameList)):
            nameEntry = nameList[film]
            name = nameEntry.get('alt')
            name.encode('utf8')
            year = page.year;
            filmList.append(Film(name, year))
            # print('filmList: '+name)
    return filmList


@app.route("/handle_data", methods =['GET', 'POST'])
def handle_data():
    if request.method == 'POST':
        #OGurl = request.form.get("url")
        #print(OGurl)
        
        urls = []
        for key, val in request.form.items():
            if key.startswith("url"):
                if val:
                    urls.append(val)

        randomList = random.randint(0,len(urls)-1) # make random number
        OGurl = urls[randomList] #choose random list
        print("OGurl: "+OGurl)

        pageList = []
        filmList = []

        class Page():
            def __init__(self, url, num):
                self.url = url
                self.num = num
                self.page = None
                self.soup = None
                self.year = 0
                self.ready = False
            def Load(self):
                self.page = requests.get(self.url)
                self.soup = BeautifulSoup(self.page.text,'html.parser')
                self.ready = True

        class Film():
            def __init__(self, name, rating, year):
                self.name = name
                self.rating = rating
                self.year = year

        # Find needed pages
        firstPage = Page(OGurl, 1)
        firstPage.Load()
        pageList.append(firstPage)
        pageDiscoveryList = firstPage.soup.find_all('li', class_='paginate-page')

        # If only 1 page exists
        if len(pageDiscoveryList) == 0:
            filmList = get_posters(pageList[0])
        else:
            # find last page number
            pageCount = int(pageDiscoveryList[len(pageDiscoveryList)-1].a.get_text())

            # add range to search list
            for pageNum in range(2, pageCount + 1):
                pageTemp = Page(OGurl+ '/page/' + str(pageNum) + '/', str(pageNum))
                pageList.append(pageTemp)

            # choose a random page
            randomPage = random.randint(0,len(pageList)-1) # make random number
            filmList = get_posters(pageList[randomPage])

            # find films on pages
            #for i in range(0, len(pageList)):
                #page = pageList[i]
                # print('PAGE '+str(i))
                #filmList = filmList + get_posters(page)
            
        randomNumber = random.randint(0,len(filmList)-1) # make random number
        filmRandom = filmList[randomNumber]			     # variable 'films' is a random movie poster
        filmsRandomString = str(filmRandom.name)
        print('RANDOM CHOICE: '+filmsRandomString)
        movieLinkString = filmsRandomString.replace(" ", "-")
        movieLink = 'https://letterboxd.com/film/' + movieLinkString.lower().replace(",", "").replace(":", "").replace("'", "").replace("?", "").replace("!", "").replace("&", "") + '/'
        return render_template('home.html', movieLink= movieLink, films = filmsRandomString)

if __name__ == '__main__':
    app.run(debug=True)
