from helper.files import load_data,save_data
import re
def loadDataFile(filename):
    list = load_data(filename)
    return list
def saveDataFile(filename,files):
    saves = save_data(filename,files)
    return saves

# FOR GENERATE PRODUCT ID
def checkCount(filename):
    dataList = loadDataFile("product/"+filename)
    totalData = len(dataList['zproduct'])
    return totalData

def checkCountSequence(post: dict,filename):
    dataList = loadDataFile("product/"+filename)
    if post['year'] is not None :
      filtered_data = list(filter(
          lambda item:re.search(post['year'].lower(),item['id'].lower()), dataList['zproduct']))
    totalData = len(filtered_data)
    return totalData

def checkID(post: dict,filename):
    dataList = loadDataFile("product/"+filename)
    filtered_data = []
    if "id" in post :
        filtered_data = list(filter(
        lambda item: item['id'] == post['id'] , dataList['zproduct']))
    totalData = len(filtered_data)
    if len(totalData) > 0:
        return False
    return True

    
def checkExist(post: dict,filename):
    dataList = loadDataFile("product/"+filename)
    print(f" product {dataList['zproduct']}")
    if "item_name" in post :
        filtered_data = list(filter(
        lambda item: item['item_name'] == post['item_name'], dataList['zproduct']))
    if "sku" in post :
        filtered_data = list(filter(
        lambda item: item['sku'] == post['sku'], dataList['zproduct']))
    if "id" in post :
        filtered_data = list(filter(
        lambda item: item['id'] == post['id'] , dataList['zproduct']))
    if "item_name" in post and "id" in post and "sku" in post :
        filtered_data = list(filter(
        lambda item: item['sku'] == post['sku'] and item['item_name'] == post['item_name'] and item['id'] == post['id'] , dataList['zproduct']))
    if "item_name" not in post and "id" not in post and "sku" not in post :
        return None
    if not filtered_data:
        return None
    return filtered_data

def queryListUsingSearch(post: dict,filename):
    print(f" POST {post}")
    dataList = loadDataFile("product/"+filename)   
    if post['query'] is not None :
      filtered_data = list(filter(
          lambda item:re.search(post['query'].lower(),item['item_name'].lower()) or re.search(post['query'].lower(),item['sku'].lower()), dataList['zproduct']))
    if post['query'] is None:
        return dataList['zproduct']
    if not filtered_data:
        return None
    return filtered_data

def insert(data: dict,filename):
    filename = "product/"+filename
    get_load = loadDataFile(filename)
    get_load['zproduct'].append(data)
    return saveDataFile(filename,get_load)
    
def change(id,data,filename,dateTime):
    filename = "product/"+filename
    get_load = loadDataFile(filename)
    list_data = get_load['zproduct']
    for x in list_data:
        if x.get("id")==id:
            for key in data:
                x[key] = data[key]
                x['last_updated'] = dateTime
                print()
        else:
            continue
    return saveDataFile(filename,get_load)

def getList(post: dict):
    get_load = loadDataFile()
    sorted_by_Date = sorted(get_load, key=lambda item: item['created_date'])
    
    #descending
    #sorted_by_age = sorted(get_load, key=lambda item: item['created_date'],reverse=True)
    return sorted_by_Date
