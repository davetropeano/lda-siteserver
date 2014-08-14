def test1():
	msg = "running test1... "
	# do something
	msg += "passed"
	print msg
	return True

def test2():
	msg = "running test2... "
	# do something
	msg += "passed"
	print msg
	return True


if __name__ == "__main__":
	
	result = 0
	result = result if test1() else 1
	result = result if test2() else 1
	
	exit(result)