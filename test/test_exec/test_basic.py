import requests, json, jwt, pytest
#from rdf_json import RDF_JSON_Encoder, RDF_JSON_Document, rdf_json_decoder

def test_server_running():
    test_result = do_get_test("http://localhost:3005/")
    assert test_result == True


def test_account_get():
	assert do_get_test("http://localhost:3005/account") == True

def test_ac_get():
	assert do_get_test("http://localhost:3005/ac") == True

def test_mt_get():
	assert do_get_test("http://localhost:3005/mt") == True

def do_get_test(url):
	r = requests.get(url, headers={}, verify=False)
	print "status code: %s" % r.status_code
	print r.text
	if r.status_code != 200:		
		return False
	return True

# this is for working with tests while building them 
if __name__ == "__main__":	
	#test_server_running()
	pass