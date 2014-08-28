from os import walk
from inspect import getmembers, isfunction

test_result = 0

def execute_test(test_module_name, func_info):
	global test_result
	
	func_name = func_info[0]
	func = func_info[1]
	print("running %s.%s..." % (test_module_name, func_name)),	
	try:		
		passed = func()
		if passed:
			print "passed"
		else:
			raise		 
	except:
		print "failed"
		test_result = 1	

def find_and_execute_tests(dirpath, test_module_name):
	global test_result
	try:
		test_module_name = test_module_name.replace('.py','')
		test_module = __import__(test_module_name)
		functions_list = [o for o in getmembers(test_module) if isfunction(o[1])]
		functions_list.reverse() # try to make them run in the same order as they are in the file
		for func_info in functions_list:
			if func_info[0].startswith('test_'):
				execute_test(test_module_name, func_info)		
				    
	except ImportError as e:		
		print "couldn't import %s: %s" % (test_module_name, e)
		test_result = 1	

if __name__ == "__main__":	
	
	for (dirpath, dirnames, fnames) in walk("."):
		for fname in fnames:
			if fname.startswith('test_') and fname.endswith('.py'):
				find_and_execute_tests(dirpath, fname)
	print "test_result: %s" % test_result
	exit(test_result)