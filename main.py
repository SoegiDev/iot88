from utils import AuthParse
import json
import sys

path = "resources/auth.json"
aP = AuthParse()
aP.parse(path)
allData = aP.get_result()
for ij in allData['authentication']:
    print(ij['email'])

def parse_json(data):
    result = {}
    for key, value in data.items():
        if isinstance(value, dict):
            result[key] = parse_json(value)
        else:
            result[key] = value
    return result

def register_user():
    a = str(sys.argv[1])
    password = str(sys.argv[2])

# Parsing JSON data using recursion
#parsed_data = parse_json(json.load s(str(allData)))
# print(parsed_data['authentication'])