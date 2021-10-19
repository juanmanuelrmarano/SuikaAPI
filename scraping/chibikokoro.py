# -*- coding: utf-8 -*-
import requests
import time
from datetime        import datetime, timedelta, timezone
from datetime        import datetime
from bs4             import BeautifulSoup
import pymongo
from pymongo      import UpdateOne

#Iniciamos sesión de requests
currentSession = requests.session() 


def payload(li):
    # Guarda dependiendo cada campo, la informacion tomada de la pagina.
    # En este caso no se encontraron complicaciones ni fueron necesarias validaciones adicionales
    # TODO: Se encontraron algunos pocos casos de productos con un rango de precios. Un caso era venta de diferentes muñecos pokemon. Revisar para que agregue individualmente cada muñeco y su precio respectivo

    # Algunas imagenes a veces quedan cortadas, ver si es convenie cambiarlo
    # image = li.a.img['src'].replace('-300x300', '')

    strprice = li.find('span', {'class': 'price'}).text.replace('$', '')
    print(strprice)
    if ' ' in strprice:
        strprice = strprice.split(' ')
        strprice = strprice[0].split(',')
        strprice = int(strprice[0].replace('.',''))
    else: 
        strprice = strprice.split(',')
        strprice = int(strprice[0].replace('.',''))
        # "2.600,00"

    payload = {
        'PageId': "Chibi Kokoro",
        'Id'    : li.a['href'].split('/')[-2], #slug del link
        'Title' : li.a.h2.text, 
        'Link'  : li.a['href'], 
        'Image' : li.a.img['src'],
        'Price' : strprice,
        'Date'  : time.strftime('%Y-%m-%d'),
    }

    return payload


def get_products(html_soup, payloads):    
    # Se encuentra la caja principal contenedora del listado de productos.
    # A partir de cada listado, se obtiene la información necesaria de cada producto

    box = html_soup.find('ul', {'class': 'products columns-4'})
    lists = box.find_all('li')
    products = 1
    
    for li in lists:
        product = payload(li)
        payloads.append(product) 
        products+=1

    return products


def save(payloads):
    # Función básica para insertar todos los payloads de los productos

    with pymongo.MongoClient('mongodb://localhost:27017/', connect=False) as client:
        db = client.suika
        db['scraping'].insert_many(payloads)

        client.close()


def scraping():
    # A partir de la sección Anime, se enumeran las páginas para obtener cada listado
    # Traemos el html de cada página recorrida y comenzamos a guardar los datos necesarios

    start_timestamp = datetime.now()
    print(start_timestamp)

    base_url = "https://www.chibikokoro.com/categoria-producto/anime/page/{}/"

    payloads = []
    total_products = 0
    page = 1
    while True:        
        response = currentSession.get(base_url.format(page))
        if response.status_code == 200:
            print(base_url.format(page))
            html_soup = BeautifulSoup(response.text, 'html.parser')            
            products = get_products(html_soup, payloads)
            print(products, "products")
            total_products = total_products + products
            page+=1
            #save products        
        else:
            print('\n ~ No more pages ~ \n')
            break
    
    print('total products:', total_products)

    end_timestamp = datetime.now()
    duration = str(end_timestamp - start_timestamp)

    print(len(payloads))
    print("Saving...")
    save(payloads)
    print('Scraping Duration:', end_timestamp - start_timestamp)


scraping()
currentSession.close()
