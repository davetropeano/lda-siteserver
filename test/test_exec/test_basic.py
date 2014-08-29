import requests, json, jwt
#from rdf_json import RDF_JSON_Encoder, RDF_JSON_Document, rdf_json_decoder

def test_server_running():	 
	return do_get_test("http://localhost:3005/")	

def test_account_get():
	return do_get_test("http://localhost:3005/account")

def test_ac_get():
	return do_get_test("http://localhost:3005/ac")

def test_mt_get():
	return do_get_test("http://localhost:3005/mt")	

def do_get_test(url):
	r = requests.get(url, headers={}, verify=False)
	print "status code: %s" % r.status_code
	print r.text
	if r.status_code != 200:		
		return False
	return True

# this is for working with tests while building them 
if __name__ == "__main__":	
	#glob = globals()
	#print 'done'
	pass