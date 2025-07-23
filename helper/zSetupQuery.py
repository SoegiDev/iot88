from helper.files import load_data,save_data
import re
filename = "zsetup.json"
def loadDataFile():
    list = load_data(filename)
    return list
def saveDataFile(files):
    saves = save_data(filename,files)
    return saves
    
# FOR GENERATE SETUP ID
def checkCount():
    dataList = loadDataFile()
    totalData = len(dataList['zset'])
    return totalData

def checkCountSequence(post: dict):
    dataList = loadDataFile()
    if post['year'] is not None :
      filtered_data = list(filter(
          lambda item:re.search(post['year'].lower(),item['id'].lower()), dataList['zset']))
    totalData = len(filtered_data)
    return totalData

def checkID(post: dict):
    dataList = loadDataFile()
    filtered_data = []
    if "id" in post :
        filtered_data = list(filter(
        lambda item: item['id'] == post['id'] , dataList['zset']))
    totalData = len(filtered_data)
    if len(totalData) > 0:
        return False
    return True

def checkExist(post: dict):
    dataList = loadDataFile()
    if "company_id" in post :
        filtered_data = list(filter(
        lambda item: item['company_id'] == post['company_id'], dataList['zset']))
    if "id" in post :
        filtered_data = list(filter(
        lambda item: item['id'] == post['id'] , dataList['zset']))
    if "id" in post and "company_id" in post :
        filtered_data = list(filter(
        lambda item: item['company_id'] == post['company_id'] and item['id'] == post['id'] , dataList['zset']))
    if  "company_id" not in post and "id" not in post :
        return None
    if not filtered_data:
        return None
    return filtered_data

def queryListUsingSearch(post: dict):
    dataList = loadDataFile()
    if post['company_id'] is not None and post['query'] is not None :
        filtered_data = list(filter(
        lambda item: item['company_id'] == post['company_id'] 
        and (re.search(post['query'].lower(),item['company_name'].lower()) or re.search(post['query'].lower(),item['company_email'].lower())), dataList['zset']))
    if post['company_id'] is None and post['query'] is not None :
        filtered_data = list(filter(
        lambda item: re.search(post['query'].lower(),item['company_name'].lower())
        or re.search(post['query'].lower(),item['company_email'].lower()), dataList['zset']))
    if post['company_id'] is None and post['query'] is None :
        return dataList['zset']
    if not filtered_data:
        return None
    return filtered_data

def insert(data: dict):
    get_load = loadDataFile()
    get_load['zset'].append(data)
    return saveDataFile(get_load)
    
def change(id,data,dateTime):
    get_load = loadDataFile()
    list_data = get_load['zset']
    for x in list_data:
        if x.get("id")==id:
            for key in data:
                x[key] = data[key]
                x['last_updated'] = dateTime
        else:
            continue
    return saveDataFile(get_load)

    
def getList(post: dict):
    get_load = loadDataFile()
    sorted_by_Date = sorted(get_load, key=lambda item: item['created_date'])
    
    #descending
    #sorted_by_age = sorted(get_load, key=lambda item: item['created_date'],reverse=True)
    return sorted_by_Date
