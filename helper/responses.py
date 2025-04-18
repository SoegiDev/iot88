from flask import jsonify

def bad_request(message,code):
        response = jsonify({'message': message,"code":code})
        response.status_code = code
        return response
    
def success_request(message,code,data : None):
        datas = {"message":message,"code":code}
        if data is not None:
            datas = {"message":message,"data":data,"code":code}
        response = jsonify(datas)
        response.status_code = code
        return response