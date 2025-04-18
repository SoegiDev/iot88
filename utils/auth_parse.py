import json
import pandas as pd
from random import choice

class AuthParse:
    def __init__(self):
        self.username = []
        self.email = []
        self.password = []
        self.authentication = []
        self.device = []

    def parse(self, json_path):
        with open(json_path) as data_file:
            self.data = json.load(data_file)

        for intent in self.data['authentication']:
                self.username.append(intent['username'])
                self.email.append(intent['email'])
                self.password.append(intent['password'])
                self.device.append(intent['device'])
                
    def get_result(self):
        return self.data
    
    def get_username(self):
        return self.username