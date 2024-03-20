from pymongo import MongoClient

CONNECTION_STRING = "mongodb+srv://plamenavgeorgieva2019:ZGQh6Z2y9qB52p5y@tues-iot.kgcueop.mongodb.net/?retryWrites=true&w=majority&appName=TUES-IoT"

DATABASE_NAME = "iot_mongo_db"

def get_database():
    # create connection using MongoCLient
    client = MongoClient(CONNECTION_STRING)
    
    # return the databes
    return client[DATABASE_NAME]