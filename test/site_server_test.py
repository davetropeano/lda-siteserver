import os, sys, logging
from wsgiref.simple_server import make_server
from wsgiref.simple_server import WSGIServer
from SocketServer import ThreadingMixIn

sys.path.append('../../lda-siteserver/src')
sys.path.append('../../lda-serverlib/logiclibrary')
sys.path.append('../../lda-serverlib/mongodbstorage')
sys.path.append('../../lda-clientlib/python')
sys.path.append('../../lda-clientlib/python/test')

class ThreadedWSGIServer(ThreadingMixIn, WSGIServer):
    """Handle requests in a separate thread."""

os.environ['APP_NAME'] = 'siteserver'
os.environ['MONGODB_DB_HOST'] = 'localhost'
os.environ['MONGODB_DB_PORT'] = '27017'    
#os.environ['DEBUG_HTML'] = 'True'    
os.environ['HOSTINGSITE_HOST'] = 'localhost:3001'
os.environ['SYSTEM_HOST'] = '127.0.0.1:3001'

from logic_server import application
from werkzeug.wsgi import SharedDataMiddleware

application = SharedDataMiddleware(application, {
    '/siteserver': os.path.join(os.path.dirname(__file__), '../wsgi/static/siteserver'),
    '/sitedesign': os.path.join(os.path.dirname(__file__), '../../lda-clientlib'),
})
 
SERVER_NAME = 'site server'
PORT = 3005
httpd = make_server('0.0.0.0', PORT, application, server_class=ThreadedWSGIServer)
print 'test %s initiated on host: localhost port: %d' % (SERVER_NAME, PORT)
logging.basicConfig(level=logging.DEBUG)
httpd.serve_forever()