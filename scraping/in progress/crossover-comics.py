# -*- coding: utf-8 -*-
import requests
import time
from datetime        import datetime, timedelta, timezone
from datetime        import datetime
from bs4             import BeautifulSoup
import pymongo
from pymongo      import UpdateOne


currentSession = requests.session() 

def get_bsoup(url):
    # self.currentSession = requests.session() 
    response = currentSession.get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    # print(html_soup)

    return html_soup


def get_lists(html_soup):    
    # categories = titles.find_all('div', {'class': 'js-desktop-dropdown desktop-dropdown'})
    get_nav = html_soup.find('div', {'class': 'row align-items-center nav-row d-none d-md-block'})
    get_div_containers = get_nav.find_all('li', {'class': 'nav-item js-item-subitems-desktop nav-item-desktop item-with-subitems'})
    # print(get_div_containers)
    cat_links = []
    for cat in get_div_containers:
        # print('cat', cat)
        cat_links.append(cat.a['href'])

    return cat_links


def get_products(cat_links):
    ids = []
    for cat in cat_links:
        
        product_list = []

        page = 1
        
        while True:
            page_url = (f'{cat}?mpage={page}')
            print (page_url)
            html_soup = get_bsoup(url=page_url)
            get_container = html_soup.find('div', {'class': 'js-product-table row'})
            get_product = get_container.find_all('div', {'class': 'js-item-product col-6 col-md-4 col-lg-3'})

            for product in get_product:
                # if product == get_product[0]:
                #     print(product.a['title'], ' --- ', product.a['href'])

                if product.a['href'].split('/')[-2] in ids:
                    continue
                else:
                    ids.append(product.a['href'].split('/')[-2])

                    product_list.append(payload(product))

            print('!!!!! page:', page, "len product list: ", len(product_list))
            
            for title in product_list:
                print(title['Title'])


            page+= 1
            print('Next Page: ', page)
            
            # if page == 3:
            #     break


     
def payload(product):
    # Guarda dependiendo cada campo, la informacion tomada de la pagina.
    print( "IMAGEEEEEEEEEEEEEEEEEEE", product.a.img['src'])
    payload = {
        'PageId': "Crossover Comics Store",
        'Id'    : product.a['href'].split('/')[-2],
        'Title' : product.a['title'],
        'Link'  : product.a['href'],
        'Image' : product.a.img['src'],
        'Price' : product.find('span', {'class': 'js-price-display item-price'}).text.strip(),
        'Date'  : time.strftime('%Y-%m-%d'),
    }

    # print(payload)
    
    return payload


def save(payloads):
    # Función básica para insertar los payloads de los productos

    with pymongo.MongoClient('mongodb://localhost:27017/', connect=False) as client:
        db = client.suika_api

        # Guarda en la coleccion 'historial'
        find_history = db['historial'].find_one({'PageId': "Crossover Comics Store", 'Date': time.strftime('%Y-%m-%d')})
        if find_history:
            print("Ya hay historial para esta fecha")
            # print(find_history)
        else:
            db['historial'].insert_many(payloads)

        # Guarda todos los payloads en la base 'contenidos', eliminando primero los anteriores.
        db['contenidos'].delete_many({'PageId': "Crossover Comics Store"})
        db['contenidos'].insert_many(payloads)

        client.close()


def scraping():   
    start_timestamp = datetime.now()
    print(start_timestamp)

    html_soup = get_bsoup(url = "https://www.crossover-comics.com.ar/") 
    cat_links = get_lists(html_soup)
    get_products(cat_links)


#     print('total products:', total_products)

#     end_timestamp = get_datetime()
#     duration = str(end_timestamp - start_timestamp)

#     print(len(payloads))
#     print("Saving...")
#     save(payloads)
#     print(duration)

    # print(len(payloads))
    # print("Saving...")
    # save(payloads)
    end_timestamp = datetime.now()
    duration = str(end_timestamp - start_timestamp)
    print('Scraping Duration:', end_timestamp - start_timestamp)
    print(duration)


scraping()
currentSession.close()

# html_soup = get_bsoup()
# get_lists(html_soup)



'''
TODO:
cambiar idealmente por requests + paginado. En este link tienen los casos especificos de cada pagina en vez de ir sumandolos todos
https://www.crossover-comics.com/materia-principal/mangas/page/2/?results_only=true&limit=12&theme=amazonas
'''


# {
#     'PageId': 'Crossover Comics Store', 
#     'Id': 'haikyu-04', 
#     'Title': 'HAIKYU!! # 04', 
#     'Link': 'https://www.crossover-comics.com/productos/haikyu-04/', 
#     'Image': '//d3ugyf2ht6aenh.cloudfront.net/assets/themes/amazonas/static/images/empty-placeholder.png?1685972405', 
#     'Price': '\n                            $495\n                        ', 
#     'Date': '2021-09-28'    
# }

# {'PageId': 'Crossover Comics Store', 'Id': 'jujutsu-kaisen-03', 'Title': 'JUJUTSU KAISEN # 03', 'Link': 'https://www.crossover-comics.com/productos/jujutsu-kaisen-03/', 'Image': '//d3ugyf2ht6aenh.cloudfront.net/assets/themes/amazonas/static/images/empty-placeholder.png?1685972405', 'Price': '\n                            $575\n                        ', 'Date': '2021-09-28'}


# {'PageId': 'Crossover Comics Store', 'Id': 'haikyu-01', 'Title': 'HAIKYU!! # 01', 'Link': 'https://www.crossover-comics.com/productos/haikyu-01/', 'Image': '//d3ugyf2ht6aenh.cloudfront.net/assets/themes/amazonas/static/images/empty-placeholder.png?1685972405', 'Price': '$495', 'Date': '2021-09-28'}