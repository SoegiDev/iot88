from datetime import datetime, timezone, timedelta
from uuid import uuid4
import string
import random
import jwt
from helper.files import check_File
from .zProductQuery import checkCount as productCount,checkCountSequence as productSeq
from .zAuthQuery import checkCount as authCount, checkCountSequence as authSeq
from .zCompanyQuery import checkCount as comCount, checkCountSequence as comSeq
from .zSetupQuery import checkCount as setupCount, checkCountSequence as setupSeq
from .zOutletQuery import checkCount as storeCount, checkCountSequence as storeSeq
from .zUserQuery import checkCount as userCount, checkCountSequence as userSeq
from .zDeviceQuery import checkCount as deviceCount, checkCountSequence as deviceSeq
expireTime = 30000
expireTimeHours = 730000
expireTimeDays = 90 #3 bulan
eventid = datetime.now().strftime('%y%m-%d%H-%M%S-') + str(uuid4())
eventid

def generate_auth_id():
    next_sequence = 0
    get_year = datetime.now().strftime('%Y')
    filenames_create = "zauth.json"
    if check_File(filenames_create) is False:
        next_sequence = 1
    else:
        next_sequence = authCount()+1
    # Pad the sequence number with leading zeros (e.g., 00001)
    padded_sequence = str(next_sequence).zfill(5)
    #prefix = "ITEM-"
    prefix = generate_random_string(5)
    year = f"{get_year}-"
    post = {}
    post['id'] =f"{prefix}{year}{padded_sequence}"
    return f"{prefix}{year}{padded_sequence}"

def generate_company_id():
    next_sequence = 0
    get_year = datetime.now().strftime('%Y')
    filenames_create = "zcompany.json"
    if check_File(filenames_create) is False:
        next_sequence = 1
    else:
        next_sequence = comCount()+1
    # Pad the sequence number with leading zeros (e.g., 00001)
    padded_sequence = str(next_sequence).zfill(5)
    #prefix = "ITEM-"
    prefix = generate_random_string(5)
    year = f"{get_year}-"
    post = {}
    post['id'] =f"{prefix}{year}{padded_sequence}"
    return f"{prefix}{year}{padded_sequence}"

def generate_setup_id():
    next_sequence = 0
    get_year = datetime.now().strftime('%Y')
    filenames_create = "zsetup.json"
    if check_File(filenames_create) is False:
        next_sequence = 1
    else:
        next_sequence = setupCount()+1
    # Pad the sequence number with leading zeros (e.g., 00001)
    padded_sequence = str(next_sequence).zfill(5)
    #prefix = "ITEM-"
    prefix = generate_random_string(5)
    year = f"{get_year}-"
    post = {}
    post['id'] =f"{prefix}{year}{padded_sequence}"
    return f"{prefix}{year}{padded_sequence}"

def generate_user_id():
    next_sequence = 0
    get_year = datetime.now().strftime('%Y')
    filenames_create = "zuser.json"
    if check_File(filenames_create) is False:
        next_sequence = 1
    else:
        next_sequence = setupCount()+1
    # Pad the sequence number with leading zeros (e.g., 00001)
    padded_sequence = str(next_sequence).zfill(5)
    #prefix = "ITEM-"
    prefix = f"USR-{generate_random_string(5)}"
    year = f"{get_year}-"
    post = {}
    post['id'] =f"{prefix}{year}{padded_sequence}"
    return f"{prefix}{year}{padded_sequence}"

def generate_store_id(fileName):
    next_sequence = 0
    get_year = datetime.now().strftime('%Y')
    if check_File(fileName) is False:
        next_sequence = 1
    else:
        next_sequence = storeCount(fileName)+1
    # Pad the sequence number with leading zeros (e.g., 00001)
    padded_sequence = str(next_sequence).zfill(5)
    #prefix = "ITEM-"
    prefix = f"STORE-{generate_random_string(5)}"
    year = f"{get_year}-"
    post = {}
    post['id'] =f"{prefix}{year}{padded_sequence}"
    return f"{prefix}{year}{padded_sequence}"

def generate_product_id(fileName):
    next_sequence = 0
    get_year = datetime.now().strftime('%Y')
    if check_File(fileName) is False:
        next_sequence = 1
    else:
        next_sequence = productCount(fileName)+1
    # Pad the sequence number with leading zeros (e.g., 00001)
    padded_sequence = str(next_sequence).zfill(5)
    prefix = "ITEM-"
    year = f"{get_year}-"
    post = {}
    post['id'] =f"{prefix}{year}{padded_sequence}"
    return f"{prefix}{year}{padded_sequence}"

def generate_device_id(fileName):
    next_sequence = 0
    get_year = datetime.now().strftime('%Y')
    if check_File(fileName) is False:
        next_sequence = 1
    else:
        next_sequence = deviceCount(fileName)+1
    # Pad the sequence number with leading zeros (e.g., 00001)
    padded_sequence = str(next_sequence).zfill(5)
    prefix = generate_random_string(5)
    year = f"{get_year}-"
    post = {}
    post['id'] =f"{prefix}{year}{padded_sequence}"
    return f"{prefix}{year}{padded_sequence}"

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
       
#
def generate_random_string(length):
    """Generates a random string of a given length."""
    # Define the set of characters to choose from
    characters = string.ascii_uppercase + string.digits
    
    # Use random.choices to pick 'length' characters with replacement
    # and then join them to form the string
    random_string = ''.join(random.choices(characters, k=length))
    return random_string

def random_capitalize_string(input_string):
    """
    Randomly capitalizes letters within a given string.
    """
    result_chars = []
    for char in input_string:
        if char.isalpha():  # Only consider alphabetic characters for capitalization
            if random.choice([True, False]):  # Randomly choose to capitalize or not
                result_chars.append(char.upper())
            else:
                result_chars.append(char.lower()) # Ensure consistency if not capitalizing
        else:
            result_chars.append(char)  # Keep non-alphabetic characters as they are
    return "".join(result_chars)
