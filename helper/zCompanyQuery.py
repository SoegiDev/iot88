from helper.files import load_data,save_data
import re
filename = "zcompany.json"
def loadDataFile():
    list = load_data(filename)
    return list
def saveDataFile(files):
    saves = save_data(filename,files)
    return saves
    
# FOR GENERATE COMPANY ID
def checkCount():
    dataList = loadDataFile()
    totalData = len(dataList['zcom'])
    return totalData

def checkCountSequence(post: dict):
    dataList = loadDataFile()
    if post['year'] is not None :
      filtered_data = list(filter(
          lambda item:re.search(post['year'].lower(),item['id'].lower()), dataList['zcom']))
    totalData = len(filtered_data)
    return totalData

def checkID(post: dict):
    dataList = loadDataFile()
    filtered_data = []
    if "id" in post :
        filtered_data = list(filter(
        lambda item: item['id'] == post['id'] , dataList['zcom']))
    totalData = len(filtered_data)
    if len(totalData) > 0:
        return False
    return True

def checkExist(post: dict):
    dataList = loadDataFile()
    if "company_name" in post :
        print("1")
        filtered_data = list(filter(
        lambda item: item['company_name'] == post['company_name'], dataList['zcom']))
    if "id" in post :
        print("3")
        filtered_data = list(filter(
        lambda item: item['id'] == post['id'] , dataList['zcom']))
    if not filtered_data:
        return None
    return filtered_data

def queryListUsingSearch(post: dict):
    dataList = loadDataFile()
    if  post['query'] is not None :
        print("1")
        filtered_data = list(filter(
        lambda item:re.search(post['query'].lower(),item['company_name'].lower()) or re.search(post['query'].lower(),item['company_email'].lower()), dataList['zcom']))
    if post['query'] is None :
        print("3")
        return dataList['zcom']
    if not filtered_data:
        return None
    return filtered_data

def insert(data: dict):
    get_load = loadDataFile()
    get_load['zcom'].append(data)
    return saveDataFile(get_load)
    
def change(id,data,dateTime):
    get_load = loadDataFile()
    list_data = get_load['zcom']
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
