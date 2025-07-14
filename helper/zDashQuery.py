from helper.files import load_data,save_data
import re
def loadDataFile(filename: str):
    list = load_data(filename)
    return list
def saveDataFile(filename: str,files):
    saves = save_data(filename,files)
    return saves
 
def countUser(post: dict, filterMonth: None):
    dataList = loadDataFile("zuser.json")
    total = 0
    dataCount =[]
    if "user_account" in post:
        user = post['user_account']
        if "company_id" in user:
            for x in filterMonth:
                total = sum(1 for person in dataList['zuser']if  re.search(x.lower(),person['created_date'].lower()) and (person['company_id'] == user['company_id'] if "company_id" in person else 0))
                data = {"count":total,"month":x}
                dataCount.append(data)
        else:
            for x in filterMonth:
                total = sum(1 for person in dataList['zuser']if  re.search(x.lower(),person['created_date'].lower()))
                data = {"count":total,"month":x}
                dataCount.append(data)
    else:
        for x in filterMonth:
            total = sum(1 for person in dataList['zuser']if  re.search(x.lower(),person['created_date'].lower()))
            data = {"count":total,"month":x}
            dataCount.append(data)
    return dataCount

def countOutlet(post: dict, filename,filterMonth: None):
    dataList = loadDataFile("outlet/"+filename)
    total = 0
    dataCount =[]
    for x in filterMonth:
        total = sum(1 for person in dataList['zoutlet']if  re.search(x.lower(),person['created_date'].lower()))
        data = {"count":total,"month":x}
        dataCount.append(data)
    return dataCount

def countProduct(post: dict, filename,filterMonth: None):
    dataList = loadDataFile("product/"+filename)
    total = 0
    dataCount =[]
    for x in filterMonth:
        total = sum(1 for person in dataList['zproduct']if  re.search(x.lower(),person['created_date'].lower()))
        data = {"count":total,"month":x}
        dataCount.append(data)
    return dataCount

def countCompany():
    dataList = loadDataFile("zcompany.json")
    total = 0
    total = sum(1 for com in dataList['zcom'])
    return total

def countAuth():
    dataList = loadDataFile("zauth.json")
    total = 0
    total = sum(1 for com in dataList['zauth'])
    return total