from helper.files import load_data,save_data
import re
filename = "zauth.json"
def loadDataFile():
    list = load_data(filename)
    return list
def saveDataFile(files):
    saves = save_data(filename,files)
    return saves
    
# FOR GENERATE AUTH ID
def checkCount():
    dataList = loadDataFile()
    totalData = len(dataList['zauth'])
    return totalData

def checkCountSequence(post: dict):
    dataList = loadDataFile()
    if post['year'] is not None :
      filtered_data = list(filter(
          lambda item:re.search(post['year'].lower(),item['id'].lower()), dataList['zauth']))
    totalData = len(filtered_data)
    return totalData

def checkID(post: dict):
    dataList = loadDataFile()
    filtered_data = []
    if "id" in post :
        filtered_data = list(filter(
        lambda item: item['id'] == post['id'] , dataList['zauth']))
    totalData = len(filtered_data)
    if len(totalData) > 0:
        return False
    return True

def checkExist(post: dict):
    dataList = loadDataFile()
    filtered_data = []
    if "username" in post :
        print("1")
        filtered_data = list(filter(
        lambda item: item['username'] == post['username'], dataList['zauth']))
    if "email" in post :
        print(f"2")
        filtered_data = list(filter(
        lambda item: item['email'] == post['email'] , dataList['zauth']))
    if "id" in post :
        print("3")
        filtered_data = list(filter(
        lambda item: item['id'] == post['id'] , dataList['zauth']))
    if "username" in post and "email" in post :
        print("4")
        filtered_data = list(filter(
        lambda item: item['email'] == post['email'] and item['username'] == post['username'] , dataList['zauth']))
    if "username" in post and "id" in post :
        print("5")
        filtered_data = list(filter(
        lambda item: item['id'] == post['id'] and item['username'] == post['username'] , dataList['zauth']))
    if "id" in post and "email" in post :
        print("6")
        filtered_data = list(filter(
        lambda item: item['email'] == post['email'] and item['id'] == post['id'] , dataList['zauth']))
    if "email" not in post or "username" not in post or "id" not in post :
        print("7")
        return filtered_data
    return filtered_data

def checkExistUserId(post: dict):
    dataList = loadDataFile()
    if "id" in post:
        filtered_data = list(filter(
        lambda item: item['user_id'] == post['id'] if "user_id" in item else None, dataList['zauth']))
    if not filtered_data:
        return None
    return filtered_data

def queryListUsingSearch(post: dict):
    dataList = loadDataFile()
    if post['query'] is not None :
        print("1")
        filtered_data = list(filter(
        lambda item: re.search(post['query'].lower(),item['username'].lower())
        or re.search(post['query'].lower(),item['email'].lower()), dataList['zauth']))
    if post['query'] is None :
        print("2")
        return dataList['zauth']
    if not filtered_data:
        return None
    return filtered_data


def insert(data: dict):
    get_load = loadDataFile()
    get_load['zauth'].append(data)
    return saveDataFile(get_load)
    
def change(id,data,dateTime):
    get_load = loadDataFile()
    list_data = get_load['zauth']
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
