import json

from flask import Flask, request, jsonify
from database import get_database
from time import time
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)