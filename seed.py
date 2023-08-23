# File for seeding the database
import json
from models import *
from crud import *



def get_users():
    users_data = []
    with open('users.json', 'r') as file:
        users_data = json.load(file)
    for user in users_data:
        User(user['name'], user['email'], user['password'], user['zipcode'], user['address'], user['age'])


