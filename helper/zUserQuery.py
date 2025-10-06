from helper.files import load_data,save_data
import re
filename = "zuser.json"
def loadDataFile():
    list = load_data(filename)
    return list
def saveDataFile(files):
    saves = save_data(filename,files)
    return saves
    
# FOR GENERATE USER ID
def checkCount():
    dataList = loadDataFile()
    totalData = len(dataList['zuser'])
    return totalData

def checkCountSequence(post: dict):
    dataList = loadDataFile()
    if post['year'] is not None :
      filtered_data = list(filter(
          lambda item:re.search(post['year'].lower(),item['id'].lower()), dataList['zuser']))
    totalData = len(filtered_data)
    return totalData

def checkID(post: dict):
    dataList = loadDataFile()
    filtered_data = []
    if "id" in post :
        filtered_data = list(filter(
        lambda item: item['id'] == post['id'] , dataList['zuser']))
    totalData = len(filtered_data)
    if len(totalData) > 0:
        return False
    return True

def checkExist(post: dict):
    dataList = loadDataFile()
    filtered_data = []
    if "username" in post:
        print(f"User 1")
        filtered_data = list(filter(
        lambda item: item['username'] == post['username'], dataList['zuser']))
    if "email" in post:
        print(f"User 2")
        filtered_data = list(filter(
        lambda item: item['email'] == post['email'] , dataList['zuser']))
    if "id" in post:
        print(f"User 3")
        filtered_data = list(filter(
        lambda item: item['id'] == post['id'] , dataList['zuser']))
    if not filtered_data:
        return None
    return filtered_data

def queryListUsingSearch(post: dict):
    dataList = loadDataFile()
    if post['company_id'] is not None and post['query'] is not None :
        print("1")
        filtered_data = list(filter(
        lambda item: item['company_id'] == post['company_id'] 
        and (re.search(post['query'].lower(),item['username'].lower()) or re.search(post['query'].lower(),item['email'].lower())), dataList['zuser']))
    if post['company_id'] is None and post['query'] is not None :
        print("2")
        filtered_data = list(filter(
        lambda item: re.search(post['query'].lower(),item['username'].lower())
        or re.search(post['query'].lower(),item['fullname'].lower()), dataList['zuser']))
    if post['company_id'] is None and post['query'] is None :
        print("3")
        return dataList['zuser']
    if not filtered_data:
        return None
    return filtered_data

def insert(data: dict):
    get_load = loadDataFile()
    get_load['zuser'].append(data)
    return saveDataFile(get_load)
    
def change(id,data,dateTime):
    get_load = loadDataFile()
    list_data = get_load['zuser']
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
