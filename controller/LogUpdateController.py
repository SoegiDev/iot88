from datetime import datetime
from helper.function import generate_key,pagination
from helper.log_query import queryInsert as logInsert,queryGetList as logList,\
    queryGetRow as logRow, queryChange as logChange
from helper.responses import bad_request,success_request
from itertools import islice

def log_create(post : dict,current_app):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    id = generate_key()
    data : dict = {}
    data['id'] = id
    data['created_date'] = date_time
    data['last_updated'] = date_time
    logInsert(data)
    return True


def esl_list(post_data: dict, current_user):
    per_page = 10
    get_data = logList(post_data,None)
    total_data = 0 if get_data is None else len(get_data)
    page = 0 if post_data['page'] is None else post_data['page'] 
    getPage = pagination(page,total_data,per_page)
    if get_data is None:
        result = {"data":[],"pagination":getPage}
        return success_request("Successfully Get Data",200,result)
    if getPage['start'] < 0:
        result = {"data":[],"pagination":getPage}
        return success_request("Successfully Get Data",200,result)
    filtered_data = [item for item in islice(get_data, getPage['start'], getPage['stop'])]
    result = {"data":filtered_data,"pagination":getPage}
    return success_request("Successfully Get Data",200,result)

def esl_change(data : dict,current_user):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    get_ = logRow(data['id'],None)
    data['updated_by'] = current_user['username']
    if get_ is None:
        return bad_request("Not Found or Forbidden For Data Owned",403)
    updated = logChange(data['id'],data,date_time)
    return success_request(message="Successfully Changed",code=200,data=updated)