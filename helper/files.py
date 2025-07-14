import json
import os

def load_data(file_path: str):
    dirs = "resources/"
    with open(os.path.join(dirs,file_path), 'r') as file:
        data: dict = json.load(file)
    return data

def save_data(file_path: str, data: dict):
    dirs = "resources/"
    with open(os.path.join(dirs,file_path), 'w') as file:
        json.dump(data, file, indent=2)
        
def save_data_upload(file_path: str, data: dict):
    dirs = "uploads/"
    print(f"Save Data {os.path.join(dirs,file_path)} {data}")
    with open(os.path.join(dirs,file_path), 'w') as file:
        json.dump(data, file, indent=2)
        
def save_file(file, filename):
    dirs = "uploads/"
    file.save(os.path.join(dirs, filename))

def save_file_temps(file, filename,customFileName):
    extension = os.path.splitext(filename)[1]
    dirs = "uploads_temp/"
    file.save(os.path.join(dirs, customFileName+extension))
    
def delete_files(dirs,file):
    files = os.path.join(dirs, file)
    if os.path.exists(files):
        os.remove(files)
        return True
    else:
        return False
def open_uploads(filename):
    dirs = "uploads/"
    return os.path.join(dirs, filename)

def load_data_uploads(file_path: str):
    dirs = "uploads/"
    with open(os.path.join(dirs,file_path), 'r') as file:
        data: dict = json.load(file)
    return data
        
def check_File(file_path: str) -> bool:
    dirs = "resources/"
    if os.path.isfile(os.path.join(dirs,file_path)) and os.access(os.path.join(dirs,file_path), os.R_OK):
        return True
    else:
        return False

def check_dir(dir: str) ->bool:
    check = False
    check = os.path.isdir(dir)
    return check

def get_listResources_files(file: str) -> list:
    dirs = "resources/"
    file_path = os.path.join(dirs,file)
    dir_list = os.listdir(file_path)
    return dir_list

def get_listResources_uploads(file: str) -> list:
    dirs = "uploads/"
    file_path = os.path.join(dirs,file)
    dir_list = os.listdir(file_path)
    return dir_list

def create_dir(dir_name):
    try:
        os.mkdir(dir_name)
        return True
    except FileExistsError:
        return False

def get_esl_file():
    if check_File("resources/esl_list.json") is False:
        data = {}
        data['esl'] = []
        save_data("resources/esl_list.json",data)
    get_load = load_data("resources/esl_list.json")
    return get_load