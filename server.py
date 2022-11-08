import configparser
import socket
import base64
import csv

def opencsv(username, password):                                                # รับค่า username กับ password มาเพื่อตรวจสอบ
    file = open('user_pass.csv')                                                     # เปิดไฟล์ .csv
    type(file)
    userhead = csv.reader(file)
    header = []
    header = next(userhead)
    user = []
    for x in userhead:
        user.append(x)
    i = 0
    UsernameList = []
    PasswordList = []
    while i < len(user):                                                        # แยกเก็บข้อมูล username กับ password
        UsernameList.append(user[i][0])
        PasswordList.append(user[i][1])
        i += 1
    i = 0
    while i < len(UsernameList):                                                # วนลูปเพื่อตรวจสอบ username กับ password
        if username == UsernameList[i] and password == PasswordList[i]:
            return True                                                         # ถ้าตรงกันให้ส่งกลับว่าเป็นจริง
            break
        i += 1
        if i == len(UsernameList):
            return False                                                        # ถ้าไม่ตรงกันให้ส่งกลับว่าเป็นเท็จ

def encodeBase64(message):
    token = base64.b64encode(message)                                           # รับข้อความมาเพื่อเข้ารหัส base64
    token = token.decode()
    return token


def decodeBase64(token):
    message = base64.b64decode(token)                                           # รับ token มาเพื่อถอดรหัส base64
    message = message.decode()
    return message


def authenticated(token):
    if len(token) % 4 != 0:  # check if multiple of 4                           # ตรวจสอบความถูกต้องของรูปแบบ base64
        return False                                                            # ส่งคืนค่า flase
    else:
        message = decodeBase64(token)                                           # ส่ง token ไปถอดรหัส

    message = message.split(".")                                                # แยกข้อความ username กับ password
    username = message[0]                                                       # เก็บ username ไว้ในตัวแปร username
    password = message[1]                                                       # เก็บ password ไว้ในตัวแปร password
    check = opencsv(username, password)                                         # ส่ง username กับ password ไปตรวจสอบ
    return check


def mainRun():

    parser = configparser.ConfigParser()                                        # เปิดไฟล์config
    parser.read("config.ini")

    host = "127.0.0.1"

    port = parser.get('Serverconfig', 'Server_port')                            # ตั้งค่าportจากconfig

    port = int(port)                                                            # แปลงให้อยู่ในรูปint

    key = parser.get("Serverconfig", "Secret_Key")                              # ตั้งค่าkeyจากconfig

    server = socket.socket()                                                    # รอการเชื่อมต่อจาก client
    server.bind((host, port))
    server.listen(5)
    print("รอการเชื่อมต่อ")

    client, addr = server.accept()                                              # รับการเชื่อมต่อจากclient
    print("connect from :" + str(addr))

    data = client.recv(1024).decode('utf-8')                                    # รับข้อควาจาก client
    text = data.split(":")                                                      # แบ่งข้อความโดยใช้ semi collon
    Username = text[0]                                                          # สร้างตัวแปรเก็บ username
    Pass = text[1]                                                              # สร้างตัวแปรเก็บ password
    check = opencsv(Username, Pass)                                             # ส่งusernameกับpasswordไปตรวจสอบ
    wrong = 0                                                                   # ใช้ตรวจสอบจำนวนครั้งที่ผิด
    while wrong < 2:                                                            # วนลูปเพื่อตรวจสอบจำนวนครั้งที่กรอกข้อมูลผิด
        if check is True:                                                       # ตรวจสอบว่าถ้า username และ password ถูกต้อง
            data = data.replace(":", ".") + "." + key                           # ให้เปลี่ยนจาก : ในข้อความเป็น . และเพิ่ม secret key เข้าไป
            message = data.encode()                                             # แปลงให้เป็น byte
            token = encodeBase64(message)                                       # ส่งข้อความไปเข้ารหัส base64 และเก็บไว้ใน token
            client.send(token.encode('utf-8'))                                  # ส่ง token ให้ client
            wrong = 0
            break                                                               #ออกจากลูป

        else:                                                                   # ถ้า username และ password ไม่ถูกต้อง
            wrong += 1                                                          # เพิ่มค่า wrong ขึ้น1
            txt = "Please try agian " + str(wrong) + "/3"                       # ข้อความที่จะส่งหา client
            client.send(txt.encode('utf-8'))                                    # ส่งข้อความให้ client

            data = client.recv(1024).decode('utf-8')
            text = data.split(":")
            Username = text[0]
            Pass = text[1]
            check = opencsv(Username, Pass)

    if wrong == 2:                                                              # ตรวจสอบว่าถ้าผิดครบ 3 ครั้งให้ตัดการเชื่อมต่อกับ client
        txt = "Connection refused!! you’ve exceeded maximum number of attempts"
        client.send(txt.encode('utf-8'))
        client.close()

    while True:
        data = client.recv(1024).decode('utf-8')                                # รับtokenและคำสั่งจาก client
        message = data.split(":")                                               # แบ่งข้อความโดยใช้ :
        token = message[0]                                                      # เก็บtokenไว้ในตัวแปรtoken
        token = token.encode('utf-8')
        command = message[1]                                                    # เก็บคำสั่งไว้ในตัวแปร command
        authen = authenticated(token)                                           # ส่ง token ไปเพื่อยืนยันตัวตน

        username = decodeBase64(token)                                          # ทำการสร้าง secret number
        username = username.split(".")                                          # ถอดรหัส token และเก็บเฉพาะ username ไว้ในตัวแปร uname
        uname = username[0]
        secretnum = 0
        i = 0
        while i <= len(uname) - 1:                                              #วนลูปเพื่อบวกแต่ละหลักของ username และเก็บไว้ใน secretnum
            secretnum = secretnum + int(uname[i])
            i += 1

        if authen is True:                                                      # ยืนยันตัวตนถูกต้อง
            txt = "Authenticated : True \n"                                     # ข้อความบอกว่ายืนยันตัวตนถูกต้อง
            wrong = 0
            if command == "request secret number":                              # ถ้าคำสั่งเป็น request secret number
                if len(message) != 4:                                           # ตรวจสอบมีการส่ง public key มาด้วยหรือไม่
                    text = "Connection refused !! Invalid Action."              # ถ้าไม่มีให้ส่องข้อความว่า"Connection refused !! Invalid Action."
                    client.send(text.encode('utf-8'))
                    client.close()                                              # ตัดการเชื่อมต่อ
                else:
                    e = int(message[2])
                    n = int(message[3])
                    cipherText = pow(secretnum,e,n)                             # คำนวนหา cipher text
                    text = "Encrypted Secret Number : "+str(cipherText)
                    client.send(txt.encode('utf-8')+text.encode('utf-8'))       # ส่งให้ client

            elif command == "check secret number":                              # ถ้าคำสั่งเป็น check secret number
                if len(message) != 3:                                           # ตรวจสอบความถูกต้องของรูปแบบคำสั่ง
                    text = "Connection refused !! Invalid Action."              # ถ้าผิดให้ส่งข้อความหา client และตัดการเชื่อมต่อ
                    client.send(text.encode('utf-8'))
                    client.close()
                else:                                                           # รูปแบบคำสั่งถูกต้อง
                    ChecksecretNum = int(message[2])
                    if ChecksecretNum == secretnum:                             # ตรวจสอบค่า secret number
                        text = "Secret Number Verification : True"
                    else:
                        text = "Secret Number Verification : False"
                    client.send(txt.encode('utf-8')+text.encode('utf-8'))       # ส่งผลลัพธ์กลับไปหา client

            elif command == "quit":                                             # ถ้าคำสั่งเป็น quit
                text = "Session is closed."                                     # ส่งข้อความหา client และตัดการเชื่อมต่อ
                client.send(txt.encode('utf-8')+text.encode('utf-8'))
                client.close()
            else:
                text = "Connection refused !! Invalid Action."                  # ถ้าคำสั่งผิดให้ส่งข้อความหา client และตัดการเชื่อมต่อ
                client.send(text.encode('utf-8'))
                client.close()
        elif wrong == 2:                                                        # ตรวจสอบว่าถ้าใส่ token ผิดครบ 3 ครั้งให้ตัดการเชื่อมต่อกับ client
            text = "Session closed"
            client.send(text.encode('utf-8'))
            client.close()
        else:
            text = "Authenticated : False"
            client.send(text.encode('utf-8'))
            wrong += 1



if __name__ == "__main__":
    mainRun()
