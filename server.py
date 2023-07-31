import socket
import threading
import time
import sys
import numpy as np
from getQuestions import *

# defining constant parameters..
MAX_LEN = 64
PORT = 9009
SERVER = "999.99.99.99"
ADDR = (SERVER,PORT)
FORMAT = "utf-8"
DISCONNECT_MSG = "Game Over"
WAIT_TIME = 30
NUM_PLAYERS = 1

## declaring Global variables
clientList = []
clientNames = []
timeTaken = []
clientScore = []
clientLocked = []
threadLock = threading.Lock()

# creating server socket...
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

# defining the question set to be used..
questions = []
solutions = []

#  for concurrently handling client responses defining handleClient function..
def handleClient(conn,addr):
	print(f"[NEW CONNECTION] {addr} connected.")
	# printing Welcome Message
	msg = "Welcome to the Quiz!!! Waiting for other players..."
	msg = msg.encode(FORMAT)
	conn.send(msg)

	# # receiving the username of client
	username = conn.recv(1024).decode(FORMAT)
	index = clientList.index(conn)
	clientNames[index] = username
	print("Name of client: ",username)
	
	connected = True
	while connected:
		# receiving response from the client
		response = conn.recv(1024).decode(FORMAT)
		print(response)
		connIndex = clientList.index(conn)
		time.sleep(0.1)
		timeDuration = conn.recv(1024).decode(FORMAT)
		timeDuration_float = float(timeDuration)
		timeTaken[connIndex] =  timeTaken[connIndex] + timeDuration_float

		## Updating the score
		if(response == solutions[0]):
			clientScore[connIndex] = clientScore[connIndex] + 1

		clientLocked.append(conn)

		# waiting for a minute to end the process.
		while(len(clientLocked)%NUM_PLAYERS !=0):
			pass

		threadLock.acquire()
		if(clientLocked[-1] == conn):
			print("pop")
			questions.pop(0)
			solutions.pop(0)

			# Pop already asked question and ask another question	
			if len(questions) == 0:
				endQuiz()
				break
			else:
				startQuiz()
		threadLock.release()
	server.close()
# function defining to start the quiz
def startQuiz():
	if(len(questions)!=0):
		for connection in clientList:
			connection.send(questions[0].encode(FORMAT))
# function defining to end the quiz
def endQuiz():
	broadcast("Game Over")
	print(timeTaken)
	print(clientScore)

	time.sleep(1)

	# calculating the rank
	rank = [0]*NUM_PLAYERS
	
	# based on the key value rank is alloted
	# lowest key value gets highest rank
	indices = [i for i in range(NUM_PLAYERS)]
	negTime = [((-1) * i) for i in timeTaken]
	c = list(zip(clientScore,negTime,indices))
	c = sorted(c)
	for pos in range(len(c)):
		rank[c[pos][2]] = NUM_PLAYERS - pos
	print(rank)

	# Now broadcast the number of players
	broadcast(str(NUM_PLAYERS))
	time.sleep(1)

	for client in clientList:
		for player in clientList:
			index = clientList.index(player)
			rank_msg = "Player "+ str(index) + "-" + clientNames[index] 
			if(index == clientList.index(client)):
				rank_msg = rank_msg + " [YOU]"
			rank_msg = rank_msg + "-" + str(rank[index]) + "-" + str(clientScore[index]) + "-" + str(timeTaken[index])
			print(rank_msg)
			client.send(rank_msg.encode(FORMAT))
			time.sleep(0.1)
		time.sleep(0.3)
		finalMssg = "Sorry!!! You came in " + str(rank[clientList.index(client)]) + ". Better Luck next time!!!"
		if(rank[clientList.index(client)] == 1):
			finalMssg = "Congrats!!! You have won the quiz..."
		client.send(finalMssg.encode(FORMAT))

	# Closing all connections
	for clients in clientList:
		clients.close()
	sys.exit()

def broadcast(message):
    for clients in clientList:
    	clients.send(message.encode(FORMAT))

	
# server start listening
def start():
	# updating the questions and solutions by calling getQuestions python file.
	getQuestions(questions,solutions)

	server.listen()
	print(f"Server is listening on {SERVER}...")
	while True:
		conn,addr = server.accept()			
		clientList.append(conn)
		timeTaken.append(0)
		clientScore.append(0)
		clientNames.append("player")
		thread = threading.Thread(target=handleClient,args=(conn,addr))
		thread.start()
		# Once [NUM_PLAYERS] connections attained quiz will be started..
		if(len(clientList) == NUM_PLAYERS):						
			time.sleep(2)
			startQuiz()

	conn.close()
	server.close()

start()
