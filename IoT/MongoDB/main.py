import json
from flask import Flask, request, jsonify
from database import get_database
from time import time

database = get_database()
collection = database["newCollection"]
test = {
    "test": "testing value"
}
collection.insert_one(test)