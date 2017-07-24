import os
import json
import sys
def extract_imports(test_file):
	list=[]
	for test_function in test_file['test_functions']:
		for to_test_function in test_function['to_test_functions']:
			if to_test_function['to_test_file_name'] not in list:
				list.append(to_test_function['to_test_file_name'])
	return list

def extract_specific_mode(test_file,mode):
	list=[]
	for test_function in test_file['test_functions']:
		if test_function['operation'] == mode:
			list.append(test_function['test_function_name'])
	return list

def sync_file(add,delete,update,file_name):
	file = open(file_name, 'r')
	temp = open("temp_"+file_name,'w')
	imp = []
	add_line = False
	delete_line = False
	update_line = False
	for line in file:
		new_line = line.strip(' \t\n\r').split("def ")
		is_import = line.split("import ")
		if(len(is_import)>1):
			temp.write(line)
			imp.append(is_import[1].strip(' \t\n\r'))
		is_method_line = False
		if len(new_line)>1:
			is_method_line = True
		
		if is_method_line:
			add_line = False
			delete_line = False
			update_line = False
			func_name = new_line[1].strip(' \t\n\r').split("(")[0]
			
			for add_func in add:
				if add_func == func_name.split("test_")[1]:
					add_line = True
			if add_line:
				temp.write(line)
			else:
				for del_func in delete:
					if del_func == func_name.split("test_")[1]:
						delete_line = True
				if delete_line == False:
					for upd_func in update:
						if upd_func == func_name.split("test_")[1]:
							update_line = True
					if(update_line == False):
						temp.write(line)
						add_line = True
		else:
			if add_line:
				temp.write(line)
	temp.close()
	return imp
	
def read_test(file_name):
	file = open(file_name).read()
	data = json.loads(file)
	ex_imp=[]
	existed = False
	for test_file in data['test_files']:
		existed = False
		list_of_imports = extract_imports(test_file)
		if os.path.exists("test_"+test_file['test_file_name']+".py"):
			existed = True
			ex_imp = sync_file(extract_specific_mode(test_file,0),extract_specific_mode(test_file,1),extract_specific_mode(test_file,2),"test_"+test_file['test_file_name']+".py")
		
		test = open("test_"+test_file['test_file_name']+".py","w")
		counter = 0
		

		for imp in list_of_imports:
			if(imp not in ex_imp):
				if counter == 0:
					test.write("import "+imp)
				else:
					test.write("\nimport "+imp)
				counter+=1
				
		if existed:
			if(counter > 0):
				test.write("\n")
			temp = open("temp_"+"test_"+test_file['test_file_name']+".py",'r')
			prev ="\n"
			for line in temp:
				if line == "\n" and prev != "\n":
					test.write(line)
				elif line != "\n":
					test.write(line)
				prev = line

			temp.close()
			os.remove("temp_"+"test_"+test_file['test_file_name']+".py")
		counter = 0	
		for test_function in test_file['test_functions']:
			if existed == False or ( existed == True and test_function['operation']==2):
				if (existed == False or (existed == True and counter!=0)):
					test.write("\n")
					test.write("\n")
				counter += 1
				test.write("def test_"+test_function['test_function_name']+"():\n\t")
				for to_test_function in test_function['to_test_functions']:			
					for to_test_info in to_test_function['to_test_function_information']:
						test.write(to_test_info['result_variable_name']+ " = "+to_test_function['to_test_file_name']+"."+to_test_info['to_test_function_name']+"(")
						cnt=0
						for param in to_test_info['parameters']:
							if cnt!=0:
								test.write(",")
								try:
									test.write(param["value"])
								except Exception:
									test.write(str(param["value"]))
									
							else:
								try:
									test.write(param["value"])
								except Exception:
									test.write(str(param["value"]))
							cnt+=1
						test.write(")\n\t")
				test.write("assert")
				for add_assert in test_function['to_test_functions']:
					for val in add_assert['to_test_function_information']:
						if val['operator'] != "":
							test.write(" "+val['result_variable_name']+" == "+str(val['result_expected'])+" "+val['operator'])
						else:
							test.write(" "+val['result_variable_name']+" == "+str(val['result_expected']))
		test.close()
if __name__ == '__main__':
	if(sys.argv[1]=="--create"):
		read_test(sys.argv[2])
	elif(sys.argv[1]=="--init"):
		test = open(sys.argv[2],"w")
		test.write("{\n\t")
		test.write('"test_files":\n\t')
		test.write("[\n\t\t")
		count = 0
		for x in range(0,int(sys.argv[3])):
			test.write("{\n\t\t\t")
			test.write('"test_file_name": "",\n\t\t\t')
			test.write('"test_functions":\n\t\t\t')
			test.write('[\n\t\t\t\t')
			
			for y in range(0,int(sys.argv[4+count])):
				
				test.write("{\n\t\t\t\t\t")
				test.write('"test_function_name": "",\n\t\t\t\t\t')
				test.write('"to_test_functions":\n\t\t\t\t\t')
				test.write('[\n\t\t\t\t\t\t')
				test.write('{\n\t\t\t\t\t\t\t')
				test.write('"to_test_file_name":"",\n\t\t\t\t\t\t\t')
				test.write('"to_test_function_information":\n\t\t\t\t\t\t\t')
				test.write('[\n\t\t\t\t\t\t\t\t')
				test.write('{\n\t\t\t\t\t\t\t\t\t')
				test.write('"to_test_function_name":"",\n\t\t\t\t\t\t\t\t\t')
				test.write('"parameters":\n\t\t\t\t\t\t\t\t\t')
				test.write('[\n\t\t\t\t\t\t\t\t\t\t')
				test.write('{\n\t\t\t\t\t\t\t\t\t\t\t')
				test.write('"value": 0\n\t\t\t\t\t\t\t\t\t\t')
				test.write('}\n\t\t\t\t\t\t\t\t\t')
				test.write('],\n\t\t\t\t\t\t\t\t\t')
				test.write('"result_variable_name": "",\n\t\t\t\t\t\t\t\t\t')
				test.write('"result_expected": ,\n\t\t\t\t\t\t\t\t\t')
				test.write('"operator": ""\n\t\t\t\t\t\t\t\t')
				test.write('}\n\t\t\t\t\t\t\t')
				test.write(']\n\t\t\t\t\t\t')
				test.write('}\n\t\t\t\t\t')
				test.write('],\n\t\t\t\t\t')
				test.write('"operation":\n\t\t\t\t')
				if y == (int(sys.argv[4+count]) - 1):
					test.write('}\n\t\t\t')
				else:
					test.write('},\n\t\t\t\t')
			count += 1
			test.write(']\n\t\t')

			if x == (int(sys.argv[3])-1):
				test.write('}\n\t')
			else:
				test.write('},\n\t\t')
			
		test.write("]\n")
		test.write("}")
		test.close()
	else:
		print("Error: Second argument must be --init or --create")