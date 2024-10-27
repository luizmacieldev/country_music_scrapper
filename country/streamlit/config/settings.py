from pymongo import MongoClient

def load_data_from_mongo(uri, db_name, collection_name):
    client = MongoClient(uri) 
    db = client[db_name]
    collection = db[collection_name]
    return list(collection.find())
