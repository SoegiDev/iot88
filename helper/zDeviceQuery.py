from helper.files import load_data,save_data
import re
def loadDataFile(filename):
    list = load_data(filename)
    return list

def saveDataFile(filename,files):
    saves = save_data(filename,files)
    return saves
    
    
# FOR GENERATE SETUP ID
def checkCount(filename):
    dataList = loadDataFile("device_esl/"+filename)
    totalData = len(dataList['zESL'])
    return totalData

def checkCountSequence(post: dict,filename):
    dataList = loadDataFile("device_esl/"+filename)
    if post['year'] is not None :
      filtered_data = list(filter(
          lambda item:re.search(post['year'].lower(),item['id'].lower()), dataList['zESL']))
    totalData = len(filtered_data)
    return totalData

def checkID(post: dict,filename):
    dataList = loadDataFile("device_esl/"+filename)
    filtered_data = []
    if "id" in post :
        filtered_data = list(filter(
        lambda item: item['id'] == post['id'] , dataList['zESL']))
    totalData = len(filtered_data)
    if len(totalData) > 0:
        return False
    return True

def checkExist(post: dict,filename):
    dataList = loadDataFile("device_esl/"+filename)
    print(f"Post {post}")
    print(f"DataList {dataList['zESL']}")
    filtered_data = []
    if "id" in post :
        filtered_data = list(filter(
        lambda item: item['id'] == post['id'] , dataList['zESL']))
    if "id" not in post :
        return None
    if not filtered_data:
        return None
    return filtered_data

def queryListUsingSearch(post: dict,filename):
    dataList = loadDataFile("device_esl/"+filename)
    print(f"List {dataList['zESL']}")
    if post['client_owner_id'] is not None :
        filtered_data = list(filter(
        lambda item: item['client_owner_id'] == post['client_owner_id'], dataList['zESL']))
    if post['client_owner_id'] is None:
        return dataList['zESL']
    if not filtered_data:
        return None
    return filtered_data

def insert(data: dict,filename):
    filename = "device_esl/"+filename
    get_load = loadDataFile(filename)
    get_load['zESL'].append(data)
    return saveDataFile(filename,get_load)
    
def change(id,data,filename,dateTime):
    filename = "device_esl/"+filename
    get_load = loadDataFile(filename)
    list_data = get_load['zESL']
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
