from helper.files import load_data,save_data
import re

# Get data #
def queryGetRow(sku : None,status : False,columns : None):
    get_load = load_data("resources/log_update.json")
    list_data = get_load['log']
    process_data = 0
    raw = {}
    total_data = len(list_data)
    if total_data == 0:
        return None
    for x in list_data:
        process_data = process_data + 1
        if x.get("item_sku") == sku and x.get("status") == status:
            if columns == None:
                return x
            else:
                for word in columns:
                    value = x.get(word)
                    raw[word] = value
                return raw
        if process_data == total_data:
            return None
        else:
            continue


# Get LIST #
def queryGetList(post_data: dict,columns : None):
    get_load = load_data("resources/log_update.json")
    list_data = get_load['log']
    process_data = 0
    raw = {}
    data = []
    total_data = len(list_data)
    if total_data == 0:
        return None
    for x in list_data:
        process_data = process_data + 1
        if post_data['query'] is not None :
            if re.search(post_data['query'].lower(),x.get("id").lower()):
                if columns == None:
                    data.append(x)
                else:
                    for word in columns:
                        value = x.get(word)
                        raw[word] = value
                    data.append(raw)
                if process_data == total_data:
                    return data
                else:
                    continue
            else:
                if process_data == total_data:
                    return data
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
            if process_data == total_data:
                return data
            else:
                continue
            
# Get data By Company #
def queryGetByCompany(post_data : dict,company_id: None,store_id : None,columns : None):
    get_load = load_data("resources/log_update.json")
    list_data = get_load['log']
    process_data = 0
    raw = {}
    data = []
    total_data = len(list_data)
    if total_data == 0:
        return None
    if company_id is None:
        return None
    for x in list_data:
        process_data = process_data + 1
        if post_data['query'] is not None:
            if store_id is None:
                if x.get("client_owner_id")==company_id and re.search(post_data['query'].lower(),x.get("id").lower()):
                    if columns == None:
                        data.append(x)
                    else:
                        for word in columns:
                            value = x.get(word)
                            raw[word] = value
                        data.append(raw)
                if process_data == total_data:
                    return data
                else:
                    continue
            else:
                if x.get("client_owner_id")==company_id and x.get("client_store_id")==store_id and re.search(post_data['query'].lower(),x.get("id").lower()):
                    if columns == None:
                        data.append(x)
                    else:
                        for word in columns:
                            value = x.get(word)
                            raw[word] = value
                        data.append(raw)
                if process_data == total_data:
                    return data
                else:
                    continue
        else:
            if store_id is not None:
                if x.get("client_owner_id")==company_id and x.get("client_store_id")==store_id:
                    if columns == None:
                        data.append(x)
                    else:
                        for word in columns:
                            value = x.get(word)
                            raw[word] = value
                        data.append(raw)
                if process_data == total_data:
                    return data
                else:
                    continue
            else:
                if x.get("client_owner_id")==company_id:
                    if columns == None:
                        data.append(x)
                    else:
                        for word in columns:
                            value = x.get(word)
                            raw[word] = value
                        data.append(raw)
                if process_data == total_data:
                    return data
                else:
                    continue
            
# REGISTER #
def queryInsert(data):
    get_load = load_data("resources/log_update.json")
    get_load['log'].append(data)
    results = save_data("resources/log_update.json",get_load)
    return results

# CHANGE #
def queryChange(id,data,dateTime):
    get_load = load_data("resources/log_update.json")
    list_data = get_load['log']
    for x in list_data:
        if x.get("id")==id:
            for key in data:
                x[key] = data[key]
                x['last_updated'] = dateTime
    device_list = save_data("resources/log_update.json",get_load)
    return device_list