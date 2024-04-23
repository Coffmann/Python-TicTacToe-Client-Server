from threading import Thread
from time import sleep
import socket as so
import os

def connectToGame():
    MySocket.connect(("IP-ADRESS-HERE", 45545))
    print("Connected to Game")

def handleSocketResponse(text):
    global doEnd
    if "C_" in text:
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
    if "P_" in text:
        print(text[2:].replace("P_",""))
    if "I_" in text:
        temp_data = input(text[2:].replace("I_",""))
        MySocket.send(temp_data.encode())
    if "X_" in text:
        doEnd = True       
        
def receive_messages(soc:so.socket):
    global doEnd
    while True:
        try:
            data = soc.recv(1024)
            if not data:
                continue
            if doEnd:
                return
            handleSocketResponse(data.decode())
        except Exception as e:
            print(e)
            break

doEnd = False
MySocket = so.socket(so.AF_INET, so.SOCK_STREAM)
connectToGame()
receive_thread = Thread(target=receive_messages, args=(MySocket,))
receive_thread.start()
while True:
    if doEnd:
        receive_thread.join()
        MySocket.close()
        input("Press Enter to exit!")
        break

