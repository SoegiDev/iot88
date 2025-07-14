from datetime import datetime, timezone, timedelta
from uuid import uuid4
import random
import jwt
expireTime = 30000
expireTimeHours = 730000
expireTimeDays = 90 #3 bulan
eventid = datetime.now().strftime('%y%m-%d%H-%M%S-') + str(uuid4())
eventid

def generate_corporateId():
    # generate a random UUID
    eventid = datetime.now().strftime('%Y%m-%d%H-')
    random_id = str(uuid4())
    get_id = "cp"+eventid+random_id[0:5]
    # print the UUIDs
    return get_id

def generate_storeId(companyId):
    # generate a random UUID
    eventid = datetime.now().strftime('%Y%m-%d%H')
    random_id = str(uuid4())
    get_id = "outlet"+companyId+"."+eventid+"."+random_id[0:5]
    # print the UUIDs
    return get_id

def generate_productId(companyId,storeId):
    # generate a random UUID
    eventid = datetime.now().strftime('%Y%m-%d%H-%M%S')
    random_id = str(uuid4())
    get_id = "products"+companyId+"."+storeId+"."+random_id[0:5]
    # print the UUIDs
    return get_id

def generate_userId():
    eventid = datetime.now().strftime('%Y%m.%d%H.%M%S.')
    random_id = str(uuid4())
    get_id = eventid+random_id[0:5]
    return get_id

def generate_device_id():
    # generate a random UUID
    eventid = datetime.now().strftime('%d%H-%M%S-')
    random_id = str(uuid4())
    get_id = eventid+random_id[0:5]
    # print the UUIDs
    return get_id

def generate_token(data: dict,current_app):
    token = jwt.encode({
            'id': data['id'],'role': data['role'],
            'exp': datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(minutes=expireTime),
            'expDate': str(datetime.now() + timedelta(days=expireTimeDays))}, \
                current_app.config['SECRET_KEY'], algorithm='HS256')
    return token
    

def generate_key():
    # generate a random UUID
    eventid = datetime.now().strftime('%Y%m%d%H%M%S')
    strs = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    random_get = eventid+strs
    random_id = ''.join(random.choices(random_get, k=10))
    return random_id

def pagination(page: int,total_data: int,per_page: int):
    page = int(page)
    total_data = int(total_data)
    per_page = int(per_page)
    start = 0
    stop = 0
    previous_page = 0
    next_page = 0
    current_page = 0
    if page == 1 or page == 0:
        start = 0
        stop = per_page
        total_page = int(total_data / per_page)
        previous_page = 0
        current_page = 1
    else:
        bagi = 1 if per_page < page else int(per_page/page)
        start = page - (bagi)
        stop = per_page * page
        total_page = int(total_data / per_page)
        previous_page = page - 1
        current_page = page
    next_page = page+1 if (total_page > 1 and total_page >= page+1 ) else 0  
    if next_page == 0 and previous_page == 0:
        return {"start":start,"stop":stop,"current_page":current_page,"total_data":total_data,"total_page":total_page}
    if next_page == 0 and previous_page > 0:
        return {"start":start,"stop":stop,"current_page":current_page,"total_data":total_data,"total_page":total_page,"previous_page":previous_page}
    if next_page > 0 and previous_page == 0:
        return {"start":start,"stop":stop,"current_page":current_page,"total_data":total_data,"total_page":total_page,"next_page":next_page}
    if next_page > 0 and previous_page > 0:
        return {"start":start,"stop":stop,"current_page":current_page,"total_data":total_data,"total_page":total_page,"previous_page":previous_page,"next_page":next_page}        