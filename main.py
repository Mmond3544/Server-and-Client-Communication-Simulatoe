# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import base64
import configparser
import csv
"""
data = "mond"
message = data.encode()
token = base64.b64encode(message)
token = token.decode()

print(token)

file = open('name.csv')
type(file)
userhead = csv.reader(file)
header = []
header = next(userhead)
print(header)
user = []
for x in userhead:
    user.append(x)
i = 0
name = []
pw = []
while i < len(user):
    name.append(user[i][0])
    pw.append(user[i][1])
    i+=1
username = str(input("Username : "))
password = str(input("Password : "))
i = 0
while i < len(name):
    if username == name[i] and password == pw[i]:
        print("corret")
        break
    i+=1

parser = configparser.ConfigParser()
parser.read("config.ini")
port = parser.get('Serverconfig','Server_port')
key = parser.get("Serverconfig","Secret_Key")

print(port,key)

"""

a = 6
b = 5
c = 200
out = pow(a,b) % 200
print(out)