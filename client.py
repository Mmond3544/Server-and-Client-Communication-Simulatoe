import socket

def mainRun():
    host="127.0.0.1"
    port=8080
    server=socket.socket()
    server.connect((host,port))
    data = input("login : ")

    while data != 'q':
        server.send(data.encode('utf-8'))
        data = server.recv(1024).decode('utf-8')
        print(data)
        data=input(">")

    server.close()

if __name__ == "__main__":
    mainRun()