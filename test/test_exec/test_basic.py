import requests, json, jwt
#from rdf_json import RDF_JSON_Encoder, RDF_JSON_Document, rdf_json_decoder

def test_server_running():
	GET_HEADERS = {
    'Accept': 'application/rdf+json+ce'
    } 
	r = requests.get("http://localhost:3005/", headers={}, verify=False)
	if r.status_code != 200:
		return False
	return True

def test_2():
	# do something
	return True

