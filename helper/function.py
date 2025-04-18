from datetime import datetime
from uuid import uuid4
import random

eventid = datetime.now().strftime('%y%m-%d%H-%M%S-') + str(uuid4())
eventid
def generate_userId():
    # generate a random UUID
    eventid = datetime.now().strftime('%Y%m-%d%H-%M%S-')
    random_id = str(uuid4())
    get_id = eventid+random_id
    # print the UUIDs
    return get_id

def generate_device_id():
    # generate a random UUID
    eventid = datetime.now().strftime('%d%H-%M%S-')
    random_id = str(uuid4())
    get_id = eventid+random_id
    # print the UUIDs
    return get_id

def generate_key():
    # generate a random UUID
    eventid = datetime.now().strftime('%Y%m%d%H%M%S')
    strs = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    random_get = eventid+strs
    random_id = ''.join(random.choices(random_get, k=10))
    return random_id