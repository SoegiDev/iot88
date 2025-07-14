from flask import jsonify

def bad_request(message,code):
    response = jsonify({'message': message,"code":code})
    response.status_code = code
    return response
    
def success_request(message,code,data : None):
    if data is None:
        datas = {"message":message,"code":code}
        response = jsonify(datas)
        response.status_code = code
        return response
    data['message'] = message
    data['code'] = code
    datas = data
    response = jsonify(datas)
    response.status_code = code
    return response