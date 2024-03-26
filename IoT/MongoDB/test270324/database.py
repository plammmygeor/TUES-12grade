from pymongo import MongoClient

CONNECTION_STRING = "mongodb+srv://plamenavgeorgieva2019:ZGQh6Z2y9qB52p5y@tues-iot.kgcueop.mongodb.net/?retryWrites=true&w=majority&appName=TUES-IoT"

DATABASE_NAME = ""


def get_database():
    client = MongoClient(CONNECTION_STRING)
    return client[DATABASE_NAME]