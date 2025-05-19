from helper.files import load_data,save_data
import locale
#================ GET DATA ===============#

def esl_get_token(key : None,columns : None):
    get_load = load_data("resources/esl_list.json")
    list_data = get_load['esl']
    process_data = 0
    raw = {}
    data = []
    total_data = len(list_data)
    for x in list_data:
        if key is not None : 
            process_data = process_data + 1
            if x.get("device_key") == key or x.get['id'] == key:
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
def esl_get_by_id(device_id : None,columns : None):
    get_load = load_data("resources/esl_list.json")
    list_data = get_load['esl']
    process_data = 0
    raw = {}
    data = []
    total_data = len(list_data)
    if total_data == 0:
        return None
    for x in list_data:
        if device_id is not None : 
            process_data = process_data + 1
            if x.get("id")==device_id or x.get("device_id")==device_id:
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
            if columns == None:
                data.append(x)
            else:
                for word in columns:
                    value = x.get(word)
                    raw[word] = value
                data.append(x)
    return data

# GET DEVICEBYUSER
def esl_get_by_user(user: dict,device_id :None,columns : None):
    get_load = load_data("resources/esl_list.json")
    list_data = get_load['esl']
    process_data = 0
    raw = {}
    data = []
    total_data = len(list_data)
    for x in list_data: 
        process_data = process_data + 1
        if x.get("client_owner")==user['username']:
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
def esl_change(device,dateTime):
    get_load = load_data("resources/esl_list.json")
    list_data = get_load['esl']
    print(device)
    for x in list_data:
        if x.get("id")==device['id']:
            for key in device:
                x[key] = device[key]
                x['last_updated'] = dateTime
    device_list = save_data("resources/esl_list.json",get_load)
    return device_list


#=========================Register======================#

#CREATE PUSH NOTIFY
def esl_push_notif(sensor):
    getNotif = load_data("resources/esl_notif.json")
    getNotif['notif'].append(sensor)
    results = save_data("resources/esl_notif.json",getNotif)
    return results

#REGISTER ESL
def esl_register(esl):
    get_load = load_data("resources/esl_list.json")
    get_load['esl'].append(esl)
    results = save_data("resources/esl_list.json",get_load)
    return results

def rupiah_format(angka, with_prefix=False, desimal=2):
    locale.setlocale(locale.LC_NUMERIC, 'IND')
    rupiah = locale.format("%.*f", (desimal, angka), True)
    if with_prefix:
        return "Rp. {}".format(rupiah)
    return rupiah