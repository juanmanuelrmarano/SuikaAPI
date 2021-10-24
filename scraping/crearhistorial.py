import pymongo
from pymongo      import UpdateOne
import json
import random

def crearhistorial():
    with pymongo.MongoClient('mongodb://localhost:27017/', connect=False) as client:
        cursor = client.suika_api['historial'].find({'PageId': 'Geekon'}, projection={'_id':0}) #{'_id': False},
        query_result = list(cursor)
            
        i = 1

        payloads = []

        for item in query_result:        
            payloads.append(item)
            # if i == 1:
            #     print(item)    
            # else:
            #     break
            
            # print(item['Price'])

            if i < 55:
                print('i',i)
                price = item['Price'] - random.randrange(250) - 200
                item['Date'] = "2021-10-15"
                # print(item['Price'])

                print(item)
                payloads.append(item)

                item['Price'] = price - random.randrange(250) - 100
                item['Date'] = "2021-10-12"
                # date = "2021-10-12"
                # print(item['Price'])

                print(item)
                payloads.append(item)

                item['Price'] = price - random.randrange(250)
                item['Date'] = "2021-10-10"
                # print(item['Price'])

                print(item)
                payloads.append(item)  

            else:
                item['Date'] = "2021-10-15"
                payloads.append(item)
                print(item)
            
                item['Date'] = "2021-10-12"
                payloads.append(item)
                print(item)

                item['Date'] = "2021-10-10"
                payloads.append(item)
                print(item)
            
            i+=1

        print('len', len(payloads))
        # print(payloads)

        client.suika_api['historial'].delete_many({'PageId': "Geekon"})
        client.suika_api['historial'].insert_many(payloads)
        

    cursor.close()


crearhistorial()