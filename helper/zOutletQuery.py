from helper.files import load_data,save_data
import re
def loadDataFile(filename):
    list = load_data(filename)
    return list
def saveDataFile(filename,files):
    saves = save_data(filename,files)
    return saves
    
def checkExist(post: dict,filename):
    dataList = loadDataFile("outlet/"+filename)
    if "store_name" in post :
        filtered_data = list(filter(
        lambda item: item['store_name'] == post['store_name'], dataList['zoutlet']))
    if "id" in post :
        filtered_data = list(filter(
        lambda item: item['id'] == post['id'] , dataList['zoutlet']))
    if "store_name" in post and "id" in post :
        filtered_data = list(filter(
        lambda item: item['store_name'] == post['store_name'] and item['id'] == post['id'] , dataList['zoutlet']))
    if "store_name" not in post and "id" not in post :
        return None
    if not filtered_data:
        return None
    return filtered_data

def queryListUsingSearch(post: dict,filename):
    dataList = loadDataFile("outlet/"+filename)
    if post['company_id'] is not None and post['query'] is not None :
        print("1")
        filtered_data = list(filter(
        lambda item: item['company_id'] == post['company_id'] 
        and (re.search(post['query'].lower(),item['store_email'].lower()) or re.search(post['query'].lower(),item['store_name'].lower())), dataList['zoutlet']))
    if post['company_id'] is None and post['query'] is not None :
        print("2")
        filtered_data = list(filter(
        lambda item: re.search(post['query'].lower(),item['store_email'].lower())
        or re.search(post['query'].lower(),item['store_name'].lower()), dataList['zoutlet']))
    if post['company_id'] is not None and post['query'] is None :
        print("3")
        filtered_data = list(filter(
        lambda item: item['company_id'] == post['company_id'], dataList['zoutlet']))
    if post['company_id'] is None and post['query'] is None :
        print("4")
        return dataList['zoutlet']
    if not filtered_data:
        return None
    return filtered_data

def insert(data: dict,filename):
    filename = "outlet/"+filename
    get_load = loadDataFile(filename)
    get_load['zoutlet'].append(data)
    return saveDataFile(filename,get_load)
    
def change(id,data,filename,dateTime):
    filename = "outlet/"+filename
    get_load = loadDataFile(filename)
    list_data = get_load['zoutlet']
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
