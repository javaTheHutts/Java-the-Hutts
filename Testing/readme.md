Using automatetesting.py:
	- Creating a skeleton JSON file:
		python automatetesting.py --init "filename.json" param1 param2 ... paramN
		Where param1 is the number of testing files you need.
		param2 ... paramN each specifies the number of functions inside
		each of the testing files.
		For example let's say you want 3 test files with 3 1 2 functions 
		respectively your command would be:
		python automatetesting.py --init example.json 3 3 1 2
	- Creating your testing file:
		python automatetesting.py --create "filename.json"
	-JSON file format:
		You can use the --init to give you the skeleton for the format 
		but to be thorough I will explain it a bit.
		
		The JSON file is opened with the following:
		
			{
				"test_files":
				[
				]
			}
			
		test_files: is an array of your test files to create.
		
		Let's look at the contents of test_files:
			
			{
				"test_function_name": "validate",
				"to_test_functions":
				[
				],
				"operation":1
			}
			
		test_function_name: is the name of the test function that
							should be created for your testing.
		to_test_functions: is an array containing all the functions
						   you want your testing function to test
						   operation: can have the following values
						   
				           0: keep the test function specified by test_function_name
						      if it exists. If it doesn't exist do nothing.
				           1: delete the test function specified by test_function_name 
				              if it exists. If it doesn't exist do nothing.
				           2: update the existing test function specified by 
						      test_function_name if it exists. If it doesn't add it.
		
		Let's look at the content of to_test_functions:
			{
				"to_test_file_name":"pytester",
				"to_test_function_information":
				[
				]
			}
			
		to_test_file_name: is the file containg your function you want to test.
		                   Thus for each different file you would need its own 
						   object in to_test_functions
		to_test_function_information: This is an array containing the info for 
		                              which function to test in to_test_file_name
									  and which parameters it will contain
		
		Let's look at the content of to_test_function_information:
			
			{
				"to_test_function_name":"summation",
				"parameters": 
				[
					{
						"value": 4
					},
					{
						"value": 5
					}
				],
				"result_variable_name": "sum_value",
				"result_expected": 9,
				"operator": ""
			}
		to_test_function_name: is the name of the function you want to test
		parameters: is an array of parameters you want to test with.
		result_variable_name: a variable name to store the result of to_test_file_name
		result_expected: The result you expect with the given parameters
		operator: can be and\or\"" this is used to combine your assert statement
		          the last object in to_test_function_information's operator will
				  always be "". You can also specify '(' or ')' to enforce precedence
				  throughout.
		An example can be found in test.json
								
		
	
	
