import sys
sys.path.append('../../lda')
sys.path.append('../../../lda-serverlib')
sys.path.append('../../../lda-serverlib/logiclibrary')
sys.path.append('../../../lda-serverlib/mongodbstorage')
sys.path.append('../../../lda-clientlib/python')
sys.path.append('../../../lda-clientlib/python/test')
sys.path.append('../../src')
sys.path.append('../../test')

from os import walk
from inspect import getmembers, isfunction

test_result = 0
test_count = 0
failed_count = 0
failed_names = ""

def execute_test(test_module_name, func_info):
	global test_result
	global test_count
	global failed_count
	global failed_names
	test_count += 1
	
	func_name = func_info[0]
	func = func_info[1]
	full_name = "%s.%s" % (test_module_name, func_name)
	
	print "travis_fold:start:%s" % full_name
	print full_name
	passed = True
	try:
		passed = func()		
	except Exception as e:
		print "Exception: %s" % e	
		passed = False
	print "travis_fold:end:%s" % full_name
	print "                                                  ",
	if passed:
		print "passed"		
	else:
		print "failed"
		failed_count += 1
		failed_names += "\n    %s" % full_name
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
	
	print "========================================================="
	print "test results"
	print " total count: %s" % test_count
	print "failed count: %s" % failed_count
	if failed_count > 0:
		print "failed names: %s" % failed_names	
	exit(test_result)

