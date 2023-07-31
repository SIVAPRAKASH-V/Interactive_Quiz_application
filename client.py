import socket
import sys
import select
import os

sys.path.append(os.path.normpath("../ui/"))
from question import *


HEADER = 64
PORT = 9009
SERVER = "999.99.99.9"
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = "Game Over"


def connClose(client):
    # Before closing connection print the leaderboard
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~LEADERBOARD~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("...........................................................................")
    playerNumbers = client.recv(4096).decode(FORMAT)
    playerNumbers = int(playerNumbers)
    print("%-10s %-15s %-10s %-10s %-10s" %("Player Num","Name","Rank","Points","Total Time"))
    for i in range(playerNumbers):
        rankMssg = client.recv(4096).decode(FORMAT).split("-")
        print("%-10s %-15s %-10s %-10s %-10s" %(rankMssg[0],rankMssg[1],rankMssg[2],rankMssg[3],rankMssg[4]))

    finalMssg = client.recv(4096).decode(FORMAT)
    print("___________________________________________________________________________")
    print(finalMssg)
    print("___________________________________________________________________________")
    client.close()
    sys.exit()

def recvMessage(client):
    # receiving the question
    queMssg = client.recv(4096).decode(FORMAT)
    print(queMssg)

    # if "game over " received then stop the quiz
    if(queMssg == DISCONNECT_MSG):
        connClose(client)

    # taking question and option from the message.
    queMssg = queMssg.split("\n")
    question = queMssg[0]
    options = queMssg[1:]

    # Application Creation.
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow1()
    
    # setting UI according to received question.
    ui.setupUi_1(MainWindow,question,options,client,ui)
    MainWindow.setWindowTitle("Quiz")
    MainWindow.show()
    sys.exit(app.exec_())

def recvMessageF(client,ui,MainWindow):
    # Receiving the question. 
    queMssg = client.recv(4096).decode(FORMAT)
    print(queMssg)

   # If "game over" message is received stop the quiz
    if(queMssg == DISCONNECT_MSG):
        MainWindow.close()
        connClose(client)

    # Extract question and options from the message.
    queMssg = queMssg.split("\n")
    question = queMssg[0]
    options = queMssg[1:]
    
    # set the UI according to the new question receieved.
    ui.setupUi_1(MainWindow,question,options,client,ui)
    ui.updateQuestionIndex()
   

if __name__ == "__main__":

    # Give UserName
    print("Enter a username to login: ")
    username = input().strip()
    
    clientS = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    clientS.connect(ADDR)
    # receiving welcome message and rules..
    welcomeMssg = clientS.recv(4096).decode(FORMAT)
    print(welcomeMssg)

     # for printing name in leaderboard send name to server
    clientS.send(username.encode(FORMAT))

    # closing the application
    recvMessage(clientS)
