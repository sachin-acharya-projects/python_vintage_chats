from mysql import connector
from colorama import init, Fore
import json
import os

init(autoreset=True)
class Session:
    def __init__(self, file='session.json'):
        self.init(file)
    def init(self, file='session.json'):
        self.asked_file = file
        self.file = None
        if not os.path.exists(self.asked_file):
            self.file = open(file, "w+")
            self.file.seek(0)
            self.file.truncate()
            json.dump([{
                'session': "active"
            }], self.file, indent=4)
        else:
            self.file = open(file, "r+")
        self.array = json.load(self.file)
    def update(self, key, value):
        self.array[key] = str(value)
        self.file.seek(0)
        json.dump(self.array, self.file, indent=4)
        self.file.truncate()
    def get(self, key, default=None):
        value = self.array.get(key, default)
        if value == "True":
            return True
        elif value == 'False':
            return False
        elif value == 'None':
            return None
        else:
            return value
    def _update(self):
        self.array = {}
        self.raw_data = ""
        self.file.close()
        self.init()
def error(msg, sub="Error Occured"):
    print("""{}{}
        {}
    """.format(Fore.RED, sub, msg))
def database():
    """Database
    Returns database handle and cursor instance
    """
    mydb = connector.connect(
        host = "localhost", # "sql6.freemysqlhosting.net",
        user = "root", # "sql6412782",
        passwd = "", # "8aWUh4VNHs",
        port = "3306",
        database = "sql6415417"
    )
    cursor = mydb.cursor()
    return mydb, cursor
def userassign():
    session = Session()
    _, cursor = database()
    username = input("Enter Username(Receipent): ")
    cursor.execute("SELECT * FROM `user` WHERE `username`='{}'".format(username))
    result = cursor.fetchall()
    if len(result) > 0:
        uid = result[0][0]
        fullname = result[0][1]
        session.update("messagewith_id", uid)
        session.update("messagewith_name", fullname)
        return True
    else:
        error("UserExisitenceError", "Provide Username doesn't match any of available users\nUsername: {}".format(username))
