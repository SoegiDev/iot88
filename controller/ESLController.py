from datetime import datetime
from helper.function import generate_device_id,generate_token,generate_key
from helper.esl_query import esl_get_token,esl_get_by_id,esl_change,esl_push_notif,esl_get_by_user,esl_register
from helper.responses import bad_request,success_request
import locale

def money_format(value):
    value = str(value).split('.')
    money = ''
    count = 1

    for digit in value[0][::-1]:
        if count != 3:
            money += digit
            count += 1
        else:
            money += f'{digit},'
            count = 1

    if len(value) == 1:
        money = (money[::-1]).replace('','')
    else:
        money = (money[::-1] + '.' + value[1]).replace('','')

    return money

def rupiah_format(angka, with_prefix=False, desimal=0):
    locale.setlocale(locale.LC_NUMERIC, 'IND')
    rupiah = locale.format_string("%.*f", (desimal, angka), True)
    if with_prefix:
        return "Rp. {}".format(rupiah)
    return rupiah

def create_esl(post : dict):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    id = generate_device_id()
    mac = post['mac_address'].replace(":", "")
    device : dict = {}
    device['id'] = mac
    device['device_id'] = id
    device['device_name'] = "ESL_Name"
    device['device_category'] = "device_category"
    device['device_name'] = "ESL_Name"
    device['device_type']="ESL_Type"
    device['device_model'] = post['model']
    device['device_location'] = "device_location"
    device['device_connected'] = False
    device["device_screen"] = True
    device['device_key'] = generate_key()
    device['base_mac_address'] = mac
    device['base_ip_address'] = post['ip_address']
    device['base_server'] = post['server']
    device['base_endpoint'] = post['endpoint']
    device['base_server_connected'] = True
    device['client_wifi_ssid'] = ""
    device['client_wifi_password'] = ""
    device['client_owner'] = ""
    device['client_ip_address'] = ""
    device['client_server'] = ""
    device['client_endpoint'] = ""
    device['client_server_connected'] = False
    device['deleted'] = False
    device['status'] =  0
    device["item_name"] = "Item Name"
    device["item_desc"] = "Item Description"
    device["item_content"] = "Item Content"
    device["item_category"] = "Item Content"
    device["item_uom"] = ""
    device["item_code"] = "0"
    device["item_price"] = "0"
    device["item_disc_status"] = False
    device["item_disc"] = "20"
    device["item_berat"] = "200"
    device["item_image"] = ""
    device["item_promo"] =""
    device["item_active"] = False
    device["item_qris"] = "https://www.google.com"
    device["item_qris_status"]= False
    device["idle_start"] = ""
    device['idle_end'] = ""
    device['live_date'] = date_time
    device['live_end'] = date_time
    device['created_date'] = date_time
    device['last_updated'] = date_time
    device['created_by'] = "hardware"
    get_ = esl_get_by_id(mac,None)
    if get_ is not None:
        return bad_request("Your Mac Address was Registered",400)
    esl_process = esl_register(device)
    return success_request(message="Successfully Registered",code=201,data=esl_process)

def e_identity_token(current_app,key : str):
    get_ = esl_get_token(key,['id','device_key'])
    if get_ is None:
        message = f"Data Not Found"
        return bad_request(message=message,code=404)
    if key is None:
        message = f"Your Request Rejected cause Forbidden {key}"
        return bad_request(message=message,code=401)
    get_['role'] = "device_ESL"
    message = f"Successfully Get Data {key}"
    token = generate_token(get_,current_app)
    return success_request(message=message,code=200,data=token)
    

def e_device_get(id : str):
    if id is not None:
        get_ = esl_get_by_id(id,None)
        price = int(get_['item_price'])
        get_['item_price'] = money_format(price)
        message = f"Successfully Get Device {id}"
        return success_request(message=message,code=200,data=get_)
    get_ = esl_get_by_id(None,None)
    message = "Successfully Get All Device"
    return success_request(message=message,code=200,data=get_)

def e_device_getByUser(user: dict, deviceId: None):
    get_ = esl_get_by_user(user,deviceId,None)
    message = f"Successfully Get Device"
    if get_ is None:
        message = "Data Not Found"
        return success_request(message=message,code=404,data=get_)
    return success_request(message=message,code=200,data=get_)

def e_push_active(current_user):
    print(f"Push Active {current_user}")
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    results = esl_change(current_user,date_time)
    return success_request(message="Successfully Push",code=200,data=results)

def e_push_notif(device_notif,current_user):
    push_id = generate_device_id()
    print(f"Id device {current_user}")
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    device_notif['id'] = push_id
    device_notif['device_id'] = current_user['id']
    device_notif['created_time'] = date_time
    results = esl_push_notif(device_notif)
    return success_request(message="Successfully Push",code=200,data=results)

def e_change(esl : dict):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    get_ = esl_get_by_id(esl['id'],None)
    if get_ is None:
        return bad_request("Not Found or Forbidden For Data Owned",403)
    updated = esl_change(esl,date_time)
    return success_request(message="Successfully Changed",code=200,data=updated)
