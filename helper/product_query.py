from helper.files import load_data,save_data

#================ GET DATA ===============#

# GET DEVICE
def product_get_by_id(id : None,columns : None):
    get_load = load_data("resources/product_list.json")
    list_data = get_load['product']
    process_data = 0
    raw = {}
    data = []
    total_data = len(list_data)
    for x in list_data:
        if id is not None : 
            if x.get("id")==id:
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

# ======================= CHANGE =================#
# CHANGE DEVICE
def product_change(product,dateTime):
    get_load = load_data("resources/product_list.json")
    list_data = get_load['product']
    for x in list_data:
        if x.get("id")==product['id']:
            for key in product:
                x[key] = product[key]
                x['last_updated'] = dateTime
    device_list = save_data("resources/product_list.json",get_load)
    return device_list