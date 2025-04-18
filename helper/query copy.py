from helper.files import load_data,save_data

def get_login_username(username,l,columns : None):
    len_data = 0
    total_data = len(l['authentication'])
    for x in l['authentication']:
        len_data = len_data + 1
        if x.get("username")==username:
            if columns == None:
                return x
            return x.get(columns)
        else:
            if len_data == total_data:
                return None
            else:
                continue
            
# Get Password using Status
def get_password(l,status : bool):
    len_data = 0
    total_data = len(l)
    for x in l:
        len_data = len_data + 1
        if x.get("primary")==status:
            return x   
        else:
            if len_data == total_data:
                return None
            else:
                continue

# Check Username Default False
def check_username(username,l)->bool:
    check = False
    len_data = 0
    total_data = len(l['authentication'])
    for x in l['authentication']:
        len_data = len_data + 1
        if x.get("username")==username:
            check = True  
        else:
            if len_data == total_data:
                check = False
            else:
                continue
    return check

# Check Level Admin
def check_admin(username,l)->bool:
    check = False
    len_data = 0
    total_data = len(l['authentication'])
    for x in l['authentication']:
        len_data = len_data + 1
        if x.get("username")==username:
            if x.get("role") == "admin":
                return True
        else:
            if len_data == total_data:
                check = False
            else:
                continue
    return check
# Check Email Default False
def check_email(email,l)->bool:
    check = False
    len_data = 0
    total_data = len(l['authentication'])
    for x in l['authentication']:
        len_data = len_data + 1
        if x.get("email")==email:
            check = True  
        else:
            if len_data == total_data:
                check = False
            else:
                continue
    return check

# Get Data Users
def data_users(username,l,columns : None):
    len_data = 0
    total_data = len(l['authentication'])
    raw = {}
    for x in l['authentication']:
        len_data = len_data + 1
        if x.get("username")==username:
            if columns == None:
                raw = x
            else:
                for word in columns:
                    value = x.get(word)
                    raw[word] = value
        else:
            if len_data == total_data:
                raw = None
            else:
                continue
    return raw

#============================CHANGE==========================#

# Action Not Active Password By Username
def change_password_md(username,password,l):
    password = {"password":password,"primary":True}
    for x in l['authentication']:
        if x.get("username")==username:
            for j in x.get("password"):
                if j.get("primary") == True:
                    j["primary"] = False
            x['password'].append(password)
    save_data("resources/auth.json",l)
    return l

#============================Register========================#

def r_device_admin(device):
    get_load = load_data("resources/device_list.json")
    get_load['device'].append(device)
    results = save_data("resources/device_list.json",get_load)
    return results

def r_device(username,device,l):
    device ={"id":device['id']
             ,"device_id":device['device_id']
             ,"device_name":device['device_name']
             ,"device_model":device['device_model']
             ,"device_ip":device['device_ip']
             ,"device_status":device['device_status']
             ,"device_message":device['device_message']
             ,"device_location":device['device_location']
             ,"device_owned":device['device_owned']
             ,"device_key":device['device_key']}
    for x in l['authentication']:
        if x.get("username")==username:
            x['device'].append(device)
    save_data("resources/auth.json",l)
    device_list = get_login_username(username,l,"device")
    return device_list
