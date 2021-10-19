import pymongo
from pymongo      import UpdateOne
import json

def fix():
    with pymongo.MongoClient('mongodb://localhost:27017/', connect=False) as client:
        cursor = client.suika['historial'].find(projection={'_id':0})
        query_result = list(cursor)                
            
    payloads = []
    for item in query_result:
        # print(item['Price'])
        
        try:
            item['Price'] = int(item['Price'])
        except:
            if ' ' in item['Price']:
                item['Price'] = item['Price'].replace('$', '')
                item['Price'] = item['Price'].split(' ')
                item['Price'] = item['Price'][0].split(',')
                item['Price'] = int(item['Price'][0].replace('.',''))
            else: 
                item['Price'] = item['Price'].replace('$', '')
                item['Price'] = item['Price'].split(',')
                item['Price'] = int(item['Price'][0].replace('.',''))
                # "2.600,00"
                
        # print(item['Price'])

        # payloads.append(
        #     UpdateOne(
        #         {'PlatformCode' : item},
        #         { u'$set':{'PlatformCode' : item, 'LastUpdate': isodate } },
        #         upsert=True
        #     )
        # )

    print(len(query_result))
    client.suika['historial'].delete_many()
    print('11111111111')
    client.suika['historial'].insert_many(query_result)
    print('222222222222')

    cursor.close()


    # bulk_api_result = result.bulk_api_result

    # print('Upserted: {} - Matched: {} - Modified: {}'.format(
    #         bulk_api_result['nUpserted'],
    #         bulk_api_result['nMatched'],
    #         bulk_api_result['nModified']
    #     )
    # )

fix()