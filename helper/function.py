from datetime import datetime, timezone, timedelta
from uuid import uuid4
import random
import jwt
expireTime = 360
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

def generate_token(data: dict,current_app):
    token = jwt.encode({
            'id': data['id'],'role': data['role'],
            'exp': datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(minutes=expireTime),
            'expDate': str(datetime.now() + timedelta(minutes=expireTime))}, \
                current_app.config['SECRET_KEY'], algorithm='HS256')
    return token
    

def generate_key():
    # generate a random UUID
    eventid = datetime.now().strftime('%Y%m%d%H%M%S')
    strs = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    random_get = eventid+strs
    random_id = ''.join(random.choices(random_get, k=10))
    return random_id