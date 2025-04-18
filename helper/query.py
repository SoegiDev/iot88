from helper.files import load_data,save_data

#=============== CHECK ================== #

#CEK SUPER ADMIN DEFAULT FALSE
def check_super(username)->bool:
    l = load_data("resources/auth.json")
    len_data = 0
    total_data = len(l['authentication'])
    for x in l['authentication']:
        len_data = len_data + 1
        if x.get("username")==username:
            if x.get("role") == "superadmin":
                return True
        else:
            if len_data == total_data:
                return False
            else:
                continue
    return False

#CEK ADMIN DEFAULT FALSE
def check_admin(username)->bool:
    l = load_data("resources/auth.json")
    len_data = 0
    total_data = len(l['authentication'])
    for x in l['authentication']:
        len_data = len_data + 1
        if x.get("username")==username:
            if x.get("role") == "superadmin" or x.get("role") == "admin":
                return True
        else:
            if len_data == total_data:
                return False
            else:
                continue

#CEK OWNER DEFAULT FALSE
def check_owner(username)->bool:
    l = load_data("resources/auth.json")
    len_data = 0
    total_data = len(l['authentication'])
    for x in l['authentication']:
        len_data = len_data + 1
        if x.get("username")==username:
            if x.get("role") == "user":
                return True
        else:
            if len_data == total_data:
                return False
            else:
                continue
            
# CEK USER EXIST OR NO BY USERNAME DEFAULT FALSE
def check_username(username,l)->bool:
    len_data = 0
    total_data = len(l['authentication'])
    for x in l['authentication']:
        len_data = len_data + 1
        if x.get("username")==username:
            return True 
        else:
            if len_data == total_data:
                return False
            else:
                continue

# CEK USER EXIST OR NO BY EMAIL DEFAULT FALSE
def check_email(email,l)->bool:
    len_data = 0
    total_data = len(l['authentication'])
    for x in l['authentication']:
        len_data = len_data + 1
        if x.get("email")==email:
            return True  
        else:
            if len_data == total_data:
                return False
            else:
                continue


#=================== GET QUERY ===================#
#GET LOGIN USERNAME
def get_login_username(username,l,role : str,columns : None):
    len_data = 0
    raw = {}
    total_data = len(l['authentication'])
    for x in l['authentication']:
        len_data = len_data + 1
        if x.get("username")==username:
            if x.get("role") == role:
                if columns == None:
                    return x
                else:
                    for word in columns:
                        value = x.get(word)
                        raw[word] = value
                    return raw
            else:
                return None                    
        else:
            if len_data == total_data:
                return None
            else:
                continue


# GET DEVICE ADMIN
def get_device_admin(id,devices,current_user,columns : None):
    len_data = 0
    raw = {}
    data = []
    total_data = len(devices['device'])
    print(f"Total data {total_data}")
    for x in devices['device']:
        len_data = len_data + 1
        if id is None :
            if columns == None:
                data.append(x)
            else:
                for word in columns:
                    value = x.get(word)
                    raw[word] = value
                data.append(raw)
        else:
            if x.get("id")==id or x.get("device_id")==id:
                if columns == None:
                    return x
                else:
                    for word in columns:
                        value = x.get(word)
                        raw[word] = value
                    return raw             
            else:
                if len_data == total_data:
                    return None
                else:
                    continue
    return data
            
# GET DEVICE
def get_device(id,devices,current_user,columns : None):
    len_data = 0
    raw = {}
    data = []
    total_data = len(devices['device'])
    admin = True if current_user['role'] == "admin" or current_user['role'] == "superadmin" else False 
    for x in devices['device']:
        len_data = len_data + 1
        if id is None :
            if admin :
                if columns == None:
                    data.append(x)
                else:
                    for word in columns:
                        value = x.get(word)
                        raw[word] = value
                    data.append(x)
            else:
                if x.get("user_owner")==current_user['username']:
                    if columns == None:
                        data.append(x)
                    else:
                        for word in columns:
                            value = x.get(word)
                            raw[word] = value
                        data.append(raw)            
                else:
                    if len_data == total_data:
                        return None
                    else:
                        continue
        else:
            if admin :
                if x.get("id")==id or x.get("device_id")==id:
                    if columns == None:
                        return x
                    else:
                        for word in columns:
                            value = x.get(word)
                            raw[word] = value
                        return raw                  
                else:
                    if len_data == total_data:
                        return None
                    else:
                        continue
            else:
                if (x.get("id")==id or x.get("device_id")==id) and x.get("user_owner")==current_user['username']:
                    if columns == None:
                        return x
                    else:
                        for word in columns:
                            value = x.get(word)
                            raw[word] = value
                        return raw                  
                else:
                    if len_data == total_data:
                        return None
                    else:
                        continue
    return data    
       
# Get Password using Status
def get_password(l,status : bool):
    len_data = 0
    total_data = len(l['password'])
    for x in l['password']:
        len_data = len_data + 1
        if x.get("primary")==status:
            return x   
        else:
            if len_data == total_data:
                return None
            else:
                continue
            
#============================CHANGE==========================#

# Change Password
def change_password(username,password,l):
    password = {"password":password,"primary":True}
    for x in l['authentication']:
        if x.get("username")==username:
            for j in x.get("password"):
                if j.get("primary") == True:
                    j["primary"] = False
            x['password'].append(password)
    save_data("resources/auth.json",l)
    return l

def change_device_by_user(current_user,device,time,device_list):
    for x in device_list['device']:
        if (x.get("id")==device['id'] or x.get("device_id")==device['id']) and x.get("user_owner")==current_user['username']:
            for key in device:
                x[key] = device[key]
                x['last_updated'] = time
    save_data("resources/device_list.json",device_list)
    return device_list

def change_device_sensor_by_user(current_user,device,sensor,time,device_list):
    for x in device_list['device']:
        if (x.get("id")==device['id'] or x.get("device_id")==device['id']) and x.get("user_owner")==current_user['username']:
            for key in device:
                x['last_updated'] = time
                for sensor_x in x['sensor']:
                    print(sensor_x)
                    if sensor_x['name'] == sensor['name']:
                        print(f"Sama {sensor_x['name']} {sensor['name']}")
                        for key1 in sensor:
                            print(f"Update {key1} {sensor[key1]}")
                            sensor_x[key1] = sensor[key1]
    save_data("resources/device_list.json",device_list)
    return device_list

def change_device_by_admin(device,time,device_list):
    for x in device_list['device']:
        if x.get("id")==device['id']:
            for key in device:
                x[key] = device[key]
                x['last_updated'] = time
    save_data("resources/device_list.json",device_list)
    return device_list

def change_device_sensor_by_admin(device,sensor,time,device_list):
    for x in device_list['device']:
        if x.get("id")==device['id']:
            for key in device:
                x['last_updated'] = time
                for sensor_x in x['sensor']:
                    print(sensor_x)
                    if sensor_x['name'] == sensor['name']:
                        print(f"Sama {sensor_x['name']} {sensor['name']}")
                        for key1 in sensor:
                            print(f"Update {key1} {sensor[key1]}")
                            sensor_x[key1] = sensor[key1]
                      
    save_data("resources/device_list.json",device_list)
    return device_list

def change_user(get_user,time,current_user,l):
    for x in l['authentication']:
        if x.get("username")==get_user['username']:
            for key in get_user:
                x[key] = get_user[key]
                x['last_updated'] = time
    save_data("resources/auth.json",l)
    return l

#============================Register========================#

def register_device_by_admin(device):
    get_load = load_data("resources/device_list.json")
    get_load['device'].append(device)
    results = save_data("resources/device_list.json",get_load)
    return results

def register_device_by_user(auths,formDevice,devices,time,current_user):
    for x in auths['authentication']:
        if x.get("username")==current_user['username']:
            if len(x.get("device")) == 0:
                devices['user_connected'] = formDevice['user_connected']
                devices['last_updated'] = time
                x['device'].append(devices)
            else:
                for key in devices:
                    x['last_updated'] = time
    save_data("resources/auth.json",auths)
    return devices