    ########################## IN PROGRESSSSSSS #######################
    ########################## IN PROGRESSSSSSS #######################
    ########################## IN PROGRESSSSSSS #######################
    ########################## IN PROGRESSSSSSS #######################
    ########################## IN PROGRESSSSSSS #######################
    ########################## IN PROGRESSSSSSS #######################
    ########################## IN PROGRESSSSSSS #######################
    ########################## IN PROGRESSSSSSS #######################
    ########################## IN PROGRESSSSSSS #######################
    ########################## IN PROGRESSSSSSS #######################

# -*- coding: utf-8 -*-
import requests
import time
from datetime        import datetime, timedelta, timezone
from datetime        import datetime
from bs4             import BeautifulSoup
import pymongo
from pymongo      import UpdateOne


currentSession = requests.session() 

def get_bsoup():
    # self.currentSession = requests.session() 
    url = "https://www.crossover-comics.com.ar/"
    response = currentSession.get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    # print(html_soup)

    return html_soup


def get_lists(html_soup):    
    # categories = titles.find_all('div', {'class': 'js-desktop-dropdown desktop-dropdown'})
    get_nav = html_soup.find('div', {'class': 'row align-items-center nav-row d-none d-md-block'})
    get_subcategories = get_nav.find_all('a', {'class': 'nav-list-link'})
    
    subcat_deeplinks = []
    for subcat in get_subcategories:               
        print(subcat['href'])        
        subcat_deeplinks.append(subcat['href'])

    return subcat_deeplinks

    # subcat_deeplinks = []
    # for subcat in get_subcategories:               
    #     print(subcat['href'])        
    #     subcat_deeplinks.append(subcat['href'])

    # return subcat_deeplinks

        
def payload(li):
    # Guarda dependiendo cada campo, la informacion tomada de la pagina.

    payload = {
        'PageId': "Crossover Comics Store",
        'Id'    : None,
        'Title' : None,
        'Link'  : None,
        'Image' : None,
        'Price' : None,
        'Date'  : None,
    }

    return payload


def save(payloads):
    # Función básica para insertar todos los payloads de los productos

    with pymongo.MongoClient('mongodb://localhost:27017/', connect=False) as client:
        db = client.suika
        db['scraping'].insert_many(payloads)

        client.close()


def scraping():    
    pass
#     print('total products:', total_products)

#     end_timestamp = get_datetime()
#     duration = str(end_timestamp - start_timestamp)

#     print(len(payloads))
#     print("Saving...")
#     save(payloads)
#     print(duration)


scraping()
currentSession.close()

# html_soup = get_bsoup()
# get_lists(html_soup)

