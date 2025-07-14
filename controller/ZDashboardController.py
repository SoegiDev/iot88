from flask import current_app
from datetime import datetime
from helper.enum import LevelRole
from helper.responses import bad_request,success_request
from helper.zDashQuery import countUser,countOutlet,countProduct
from helper.zOutletQuery import queryListUsingSearch as outletListSearch
from itertools import islice
from datetime import date
from dateutil.relativedelta import relativedelta
from helper.files import get_listResources_files,check_dir,check_File

superadmin = [LevelRole.SuperAdmin.value]
adminTeam = [LevelRole.SuperAdmin.value,LevelRole.adminTeam.value]
supportTeam = [LevelRole.SuperAdmin.value,LevelRole.adminTeam.value,LevelRole.supportTeam.value]
admin = [LevelRole.Admin.value]
clientStaff = [LevelRole.Manager.value,LevelRole.Supervisor.value,LevelRole.Staff.value]
# REGISTER
def team_dashboard(current_user):
    result = {}
    user_result = None
    outlet_result = None
    checkFileUser = check_File("zuser.json")
    if checkFileUser:
        user_result = cal_user(current_user)
    checkFileOutlet = check_dir("resources/outlet")
    if checkFileOutlet:
        length_outlet = get_listResources_files("outlet")
        if len(length_outlet) > 0:
            outlet_result = cal_outlet(current_user)
    checkFileProduct = check_dir("resources/product")
    if checkFileProduct:
        length_product = get_listResources_files("product")
        if len(length_product) > 0:
            product_result = cal_product(current_user)
    result['user'] = user_result
    result['outlet'] = outlet_result
    result['product'] = outlet_result
    return success_request("Successfully",200,result)

def cal_user(current_user):
    today = datetime.now()
    user = {}
    result = {}
    filterdate = []
    for x in range(12):
        month = str(x+1)
        if len(month)<2:
            month = "0"+month
        date = datetime.now().strftime("%Y")+"-"
        strDate = str(date+str(month))
        filterdate.append(strDate)
    user['data']= countUser(current_user,filterdate)
    user_data_prev_month = 0
    user_data_now = 0
    total_all = 0
    for jo in user['data']:
        next_month_date = today + relativedelta(months=1)
        if jo['month'] == next_month_date.strftime('%Y-%m'):
            user_data_prev_month = jo['count']
        if jo['month'] == today.strftime('%Y-%m'):
            user_data_now = jo['count']
        total_all += jo['count']
        datetime_object = datetime.strptime(jo['month'], "%Y-%m")
        full_month_name = datetime_object.strftime("%B")
        jo['month'] = full_month_name
    user['prev_month_total'] = user_data_prev_month
    user['now_month_total'] = user_data_now
    user['total_all'] = total_all
    percentage = 0
    try:
        percentage = round(((user_data_now-user_data_prev_month)/user_data_prev_month)*100)
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed. USER")
    user['percentage'] = percentage
    return user

def cal_outlet(current_user):
    today = datetime.now()
    outlet = {}
    filterdate = []
    for x in range(12):
        month = str(x+1)
        if len(month)<2:
            month = "0"+month
        date = datetime.now().strftime("%Y")+"-"
        strDate = str(date+str(month))
        filterdate.append(strDate)
    tempList = []
    if "user_account" in current_user:
        if "company_id" in current_user["user_account"]:
            user_account = current_user['user_account']
            if "company_id" in user_account:
                fileStore = "outlet"+user_account['company_id']+".json"
                tempList = countOutlet(current_user,fileStore,filterdate)
    else:
        listfiles = get_listResources_files("outlet")
        for tmp in filterdate:
                set = {}
                set['month'] = tmp
                set['count'] = 0
                tempList.append(set)
        for out in listfiles:
            adData = countOutlet(current_user,out,filterdate)
            for t in tempList:
                for x in adData:
                    if x['month'] == t['month']:
                        t['count'] += x['count']
    outlet['data'] = tempList
    user_data_prev_month = 0
    user_data_now = 0
    total_all = 0
    for jo in outlet['data']:
        next_month_date = today + relativedelta(months=1)
        if jo['month'] == next_month_date.strftime('%Y-%m'):
            user_data_prev_month = jo['count']
        if jo['month'] == today.strftime('%Y-%m'):
            user_data_now = jo['count']
        total_all += jo['count']
        datetime_object = datetime.strptime(jo['month'], "%Y-%m")
        full_month_name = datetime_object.strftime("%B")
        jo['month'] = full_month_name
    outlet['prev_month_total'] = user_data_prev_month
    outlet['now_month_total'] = user_data_now
    outlet['total_all'] = total_all
    percentage = 0
    try:
        percentage = round(((user_data_now-user_data_prev_month)/user_data_prev_month)*100)
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed. OUTLET")
    outlet['percentage'] = percentage
    return outlet


def cal_product(current_user):
    today = datetime.now()
    product = {}
    roleType = 0
    if current_user['role'] in supportTeam:
        roleType = 0
    if current_user['role'] in admin:
        roleType = 1
    if current_user['role'] in clientStaff:
        roleType = 2
    filterdate = []
    for x in range(12):
        month = str(x+1)
        if len(month)<2:
            month = "0"+month
        date = datetime.now().strftime("%Y")+"-"
        strDate = str(date+str(month))
        filterdate.append(strDate)
    tempList = []
    if "user_account" in current_user:
        if "company_id" in current_user["user_account"]:
            user_account = current_user['user_account']
            print(f"Type {roleType}")
            if roleType == 1:
                fileStore = "outlet"+user_account['company_id']+".json"
                checkFile = check_File("outlet/"+fileStore)
                if checkFile is False:
                    print(f"Check File {checkFile}")
                    tempList = []
                else:
                    companySearch = {}
                    companySearch['query'] = None
                    companySearch['company_id'] = user_account['company_id']
                    getOutlet = outletListSearch(companySearch,fileStore)
                    print(f"Get Outlet {getOutlet}")
                    if getOutlet:
                        for out in getOutlet:
                            fileStore = "product"+out['id']+".json"
                            checkFile = check_File("product/"+fileStore)
                            if checkFile:
                                for tmp in filterdate:
                                    set = {}
                                    set['month'] = tmp
                                    set['count'] = 0
                                    tempList.append(set)
                                adData = countProduct(current_user,fileStore,filterdate)
                                for t in tempList:
                                    for x in adData:
                                        if x['month'] == t['month']:
                                            t['count'] += x['count']
            if roleType == 2:
                storeList = current_user['user_account']['store']
                for x in storeList:
                    fileStore = "product"+x['store_id']+".json"
                    checkFile = check_File("product/"+fileStore)
                    if checkFile:
                        for tmp in filterdate:
                            set = {}
                            set['month'] = tmp
                            set['count'] = 0
                            tempList.append(set)
                        adData = countProduct(current_user,fileStore,filterdate)
                        for t in tempList:
                            for x in adData:
                                if x['month'] == t['month']:
                                    t['count'] += x['count']
                    else:
                        continue
    else:
        listfiles = get_listResources_files("product")
        for tmp in filterdate:
                set = {}
                set['month'] = tmp
                set['count'] = 0
                tempList.append(set)
        for out in listfiles:
            adData = countProduct(current_user,out,filterdate)
            for t in tempList:
                for x in adData:
                    if x['month'] == t['month']:
                        t['count'] += x['count']
    product['data'] = tempList
    user_data_prev_month = 0
    user_data_now = 0
    total_all = 0
    for jo in product['data']:
        next_month_date = today + relativedelta(months=1)
        if jo['month'] == next_month_date.strftime('%Y-%m'):
            user_data_prev_month = jo['count']
        if jo['month'] == today.strftime('%Y-%m'):
            user_data_now = jo['count']
        total_all += jo['count']
        datetime_object = datetime.strptime(jo['month'], "%Y-%m")
        full_month_name = datetime_object.strftime("%B")
        jo['month'] = full_month_name
    product['prev_month_total'] = user_data_prev_month
    product['now_month_total'] = user_data_now
    product['total_all'] = total_all
    percentage = 0
    try:
        percentage = round(((user_data_now-user_data_prev_month)/user_data_prev_month)*100)
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed. OUTLET")
    product['percentage'] = percentage
    return product