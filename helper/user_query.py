from helper.files import load_data,save_data


#==================== CHECK USER =================#
def user_check_admin(current_user):
    admin = False if current_user is None else True
    if admin == True :
        admin = True if current_user['role'] == "admin" or current_user['role'] == "superadmin" else False 
    return admin

#================ GET DATA ===============#

# GET DEVICE (GET TOKEN)
def user_get_token(key : None,columns : None):
    get_load = load_data("resources/device_list.json")
    list_data = get_load['device']
    process_data = 0
    raw = {}
    data = []
    total_data = len(list_data)
    for x in list_data:
        if key is not None : 
            process_data = process_data + 1
            if x.get("key")==key:
                if columns == None:
                    return x
                else:
                    for word in columns:
                        value = x.get(word)
                        raw[word] = value
                    return raw                  
            else:
                if process_data == total_data:
                    return None
                else:
                    continue
        else:
            if process_data == total_data:
                return None
            else:
                continue
    return data

#LOGIN BY USERNAME
def user_get_by_username(user,columns : None):
    get_load = load_data("resources/auth.json")
    auth = get_load['authentication']
    process_data = 0
    raw = {}
    total_data = len(auth)
    for x in auth:
        process_data = process_data + 1
        if x.get("username")==user['username']:
            if columns == None:
                    return x
            else:
                for word in columns:
                    value = x.get(word)
                    raw[word] = value
                return raw              
        else:
            if process_data == total_data:
                return None
            else:
                continue
       
# Get Password using Status
def user_get_password(user,status : bool):
    password = user['password']
    process_data = 0
    total_data = len(password)
    for x in password:
        process_data = process_data + 1
        if x.get("primary")==status:
            return x   
        else:
            if process_data == total_data:
                return None
            else:
                continue

#GET USER BY ID
def user_get_by_id(user,columns : None):
    get_load = load_data("resources/auth.json")
    auth = get_load['authentication']
    process_data = 0
    raw = {}
    total_data = len(auth)
    for x in auth:
        process_data = process_data + 1
        if x.get("id")==user['id']:
            if columns == None:
                    return x
            else:
                for word in columns:
                    value = x.get(word)
                    raw[word] = value
                return raw              
        else:
            if process_data == total_data:
                return None
            else:
                continue

# ======================= CHANGE =================#