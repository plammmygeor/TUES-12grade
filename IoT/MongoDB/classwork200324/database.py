from pymongo import MongoClient

CONNECTION_STRING = "mongodb+srv://plamenavgeorgieva2019:ZGQh6Z2y9qB52p5y@tues-iot.kgcueop.mongodb.net/?retryWrites=true&w=majority&appName=TUES-IoT"

DATABASE_NAME = "iot_database"


def get_database():
    # create a connection using MongoClient
    client = MongoClient(CONNECTION_STRING)

    # return the database
    return client[DATABASE_NAME]