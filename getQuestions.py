def getQuestions(questions,solutions):
	file = open("quizquestions.txt","r")
	print("File has been opened for reading questions...")

	# reading until beginning of Quesitons.
	line = file.readline()
	while line:
		if line.strip().split(" ")[0] == "BEGIN":
			break
		line = file.readline()

	# ignoring a line
	file.readline()

	# starting to read the questions
	while(1):
		line = file.readline().strip().split(" ")
		#if end of questions received exit the test
		if(line[0] == "END"):
			break

		ques = file.readline().strip()
		file.readline()
		optionList = []
		for i in range(4):
			options = file.readline().strip()
			#checking for correct option...
			if(options.split(" ")[0] == "Correct:"):
				solutions.append(chr(97 + i))
				options = ' '.join(map(str, options.split(" ")[1:])) 
			optionList.append(options)
		ques_str = ques + "\n a. "+optionList[0] + "\n b. "+optionList[1] + "\n c. "+optionList[2]+"\n d. "+optionList[3]
		questions.append(ques_str)

		# ignore line
		file.readline()
		
	print("questions and solutions have been updated...")

def main():
	questions = []
	solutions = []
	getQuestions(questions,solutions)

if __name__ == "__main__":
	main()