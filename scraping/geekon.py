# -*- coding: utf-8 -*-
import requests
import time
from datetime        import datetime, timedelta, timezone
from datetime        import datetime
from bs4             import BeautifulSoup
import pymongo
from pymongo      import UpdateOne


currentSession = requests.session()

page = 1
payloads = []
while(True):
    response = currentSession.get(f"https://www.geekon.com.ar/categoria/series/page/{page}/")
    html_soup = BeautifulSoup(response.text, 'html.parser')

    products = html_soup.find_all('div',{'class': 'product-small box'})

    if products:
        for item in products:
            if item.find('span',{'class':'woocommerce-Price-amount amount'}):
                payload = {
                    'PageId': "Geekon",
                    'Id'    : item.find('a',{'class':'quick-view'}).get('data-prod'),
                    'Title' : item.find('p',{'class':'name product-title'}).text,
                    'Link'  : item.find('div',{'class':'image-fade_in_back'}).a.get('href'),
                    'Image' : item.find('img',{'class':'attachment-woocommerce_thumbnail size-woocommerce_thumbnail'}).get('src').replace('-300x300',''),
                    'Price' : int(item.find('span',{'class':'woocommerce-Price-amount amount'}).text.replace('$','').split(',')[0].replace('.','')),
                    'Date'  : time.strftime('%Y-%m-%d'),
                }
                print(payload)
                payloads.append(payload)
        
        page += 1
    else:
        break

with pymongo.MongoClient('mongodb://localhost:27017/', connect=False) as client:
    db = client.suika_api
    cursor = db['historial'].find_one(projection={'Date':1},sort=[(u"Date", 1)])

    if not cursor:
        db['historial'].insert_many(payloads)
        db['contenidos'].delete_many({'PageId': "Geekon"})
        db['contenidos'].insert_many(payloads)
    else:
        if cursor['Date'] > payloads[0]['Date']:
            db['historial'].insert_many(payloads)
            db['contenidos'].delete_many({'PageId': "Geekon"})
            db['contenidos'].insert_many(payloads)
    
    client.close()
