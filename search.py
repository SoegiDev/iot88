from utils import AuthParse
from helper.query import get_login_username,get_password
import sys

path = "resources/auth.json"
aP = AuthParse()
aP.parse(path)
allData = aP.get_result()
dataObject = allData

if __name__ == '__main__':
    a = str(sys.argv[1])
    password = str(sys.argv[2])
    get_data = get_login_username(a,dataObject,"password")
    get_password = get_password(password,get_data)
    print(get_data)
    print(get_password)