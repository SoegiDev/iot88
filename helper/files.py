import json

def load_data(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def save_data(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)
        
def get_auth_file():
    get_load = load_data("resources/auth.json")
    return get_load

def get_device_file():
    get_load = load_data("resources/device_list.json")
    return get_load

def get_device_notif():
    get_load = load_data("resources/device_notif.json")
    return get_load

def get_esl_file():
    get_load = load_data("resources/esl_list.json")
    return get_load