import requests, json, jwt, pytest
#from rdf_json import RDF_JSON_Encoder, RDF_JSON_Document, rdf_json_decoder
account_container_url = 'http://%s/account' % 'localhost'

def test_server_running():
    test_result = do_get_test("http://localhost:3005/")
    assert test_result == True


def test_account_get():
	assert do_get_test("http://localhost:3005/account") == True

def test_ac_get():
	assert do_get_test("http://localhost:3005/ac") == True

def test_mt_get():
	assert do_get_test("http://localhost:3005/mt") == True
	
##account post and delete

def test_account_post():
	assert do_post_test(account_container_url)==True
	
def test_account_delete():
	assert do_delete_test()==True
	
def do_post_test(url):
	r= requests.post(url, headers={}, verify= False)
	print "stats code: %s" % r.status_code
	print r.text
	if r.status_code != 201:
		return false
	return True

def do_get_test(url):
	r = requests.get(url, headers={}, verify=False)
	print "status code: %s" % r.status_code
	print r.text
	if r.status_code != 200:		
		return False
	return True

def do_delete_test(url):
	#Delete something that just got posted
	requests.delete(url, headers={})

# this is for working with tests while building them 
if __name__ == "__main__":	
	#test_server_running()
	pass