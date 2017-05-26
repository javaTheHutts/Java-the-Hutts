import os
class MyFiles:

	def __init__(self,first,name):
		self.list = [first]
		self.name = name

def readTest(file):
	file = open(file, "r") 
	counter2 = 0
	for line2 in file:
		counter = 0
		params = ""
		append = 'a'
		checkVal = "defVal"
		assertVal = "True"
		splitted = line2.split("#")
		line=splitted[0]
		if(len(splitted)>1):
			checkVal = splitted[1].split("?")[0]
			assertVal = splitted[1].split("?")[1]
		for word in line.split(" "):
			if counter == 0:
				testFile = "test_" + word
			elif counter == 1:
				testFunction = word
			elif counter == 2:
				toTestFile = word
			elif counter == 3:
				toTestFunction = word
			elif counter == 4:
				params = word
			else:
				params = params + "," + word
			counter = counter + 1
		if(counter2 == 0):
			list = [MyFiles(toTestFile,testFile)]
			append = 'w'
		else:
			for m in list:
				shouldAdd = True
				if m.name == testFile:
					shouldAdd = False
					check = False
					for n in m.list:
						if n == toTestFile:
							check = True
					if check == False:
						m.list.append(toTestFile)
			if shouldAdd == True:
				append = 'w'
				list.append(MyFiles(toTestFile,testFile))
		#if os.path.exists(testFile) and counter2 != 0:
		#	append = 'a'
		#else:
			
		test = open(testFile,append)
		test.write("def test_"+testFunction+"():\n\t")
	
		test.write(checkVal+" = " + toTestFile + "." + toTestFunction + "(" +params.split("\n")[0]+")\n\t")
		test.write("assert "+checkVal+" == "+assertVal+"\n")
		
		test.close()
		counter2 =counter2 + 1
	file.close()
	for k in list:
		myp = open("temp"+k.name,'w')
		for l in k.list:
			myp.write("import "+l+"\n")
		myf = open(k.name, 'r')
		for cline in myf:
			myp.write(cline)
		myp.close()
		myf.close()
		os.remove(k.name)
		os.rename("temp"+k.name,k.name)
readTest("autotestmaker.txt")