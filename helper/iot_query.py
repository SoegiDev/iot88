from helper.files import load_data,save_data

#================ GET DATA ===============#

# GET DEVICE (GET TOKEN)
def iot_get_token(key : None,columns : None):
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

# GET DEVICE
def iot_get_by_id(device_id : None,columns : None):
    get_load = load_data("resources/device_list.json")
    list_data = get_load['device']
    process_data = 0
    raw = {}
    data = []
    total_data = len(list_data)
    for x in list_data:
        if device_id is not None : 
            if x.get("id")==device_id or x.get("device_id")==device_id:
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
            if columns == None:
                data.append(x)
            else:
                for word in columns:
                    value = x.get(word)
                    raw[word] = value
                data.append(x)
    return data


# GET DEVICE
def iot_get_by_user(user: dict,device_id :None,columns : None):
    get_load = load_data("resources/device_list.json")
    list_data = get_load['device']
    process_data = 0
    raw = {}
    data = []
    total_data = len(list_data)
    for x in list_data: 
        process_data = process_data + 1
        if x.get("user_owner")==user['username']:
            if x.get("id")==device_id or x.get("device_id")==device_id:
                if columns == None:
                    return x
                else:
                    for word in columns:
                        value = x.get(word)
                        raw[word] = value
                    return raw                  
            else:
                if columns == None:
                    data.append(x)
                else:
                    for word in columns:
                        value = x.get(word)
                        raw[word] = value
                    data.append(raw)     
        else:
            if process_data == total_data:
                return data
            else:
                continue
    return data

# ======================= CHANGE =================#
# CHANGE DEVICE
def iot_change(device,dateTime):
    get_load = load_data("resources/device_list.json")
    list_data = get_load['device']
    for x in list_data:
        if x.get("id")==device['id']:
            for key in device:
                x[key] = device[key]
                x['last_updated'] = dateTime
    device_list = save_data("resources/device_list.json",get_load)
    return device_list

def iot_change_sensor(device,sensor,time):
    get_load = load_data("resources/device_list.json")
    list_data = get_load['device']
    for x in list_data:
        if (x.get("id")==device['id'] or x.get("device_id")==device['id']):
            for key in device:
                x['last_updated'] = time
                for sensor_x in x['sensor']:
                    if sensor_x['name'] == sensor['name']:
                        for key1 in sensor:
                            sensor_x[key1] = sensor[key1]
    device_list = save_data("resources/device_list.json",get_load)
    return device_list


#=========================Register======================#

#CREATE PUSH NOTIFY
def iot_push_notif(sensor):
    getNotif = load_data("resources/device_notif.json")
    getNotif['notif'].append(sensor)
    results = save_data("resources/device_notif.json",getNotif)
    return results

#REGISTER IOT
def iot_register(esl):
    get_load = load_data("resources/device_list.json")
    get_load['device'].append(esl)
    results = save_data("resources/device_list.json",get_load)
    return results