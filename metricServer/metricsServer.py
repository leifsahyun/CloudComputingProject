#! /usr/bin/env python

#is moving sys under __main__ a common practice?
import sys
import time
import BaseHTTPServer, cgi
import json
#import DBclient

API_Key = 'c3d4e51234sa5'

DEF_HOST_NAME = 'localhost' # !!!REMEMBER TO CHANGE THIS!!!
DEF_PORT_NUMBER = 8080 # Maybe set this to 9000.

dummy_metrics={'provider':'AWS',
            'type':'m1',
            'tier':'micro',
            'cpu':16,
            'RAM':32,
            'something': 75}

class MetricsServer(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
    
    
    def do_GET(self):
        """Respond to a GET request."""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_POST(self):
   # Parse the form data posted
        form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })

        # Begin the response
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        #### Body here


        #if ctype != 'application/json':
        message={}
        message['received'] = 'ok'
        self.wfile.write(json.dumps(dummy_metrics))


      

        return

def main():
    #TODO: parameterize
    HOST_NAME = DEF_HOST_NAME
    PORT_NUMBER = DEF_PORT_NUMBER
    server_class = BaseHTTPServer.HTTPServer #nice touch they did in the examples

    httpd = server_class((HOST_NAME, PORT_NUMBER), MetricsServer)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)

    try:
        ### MAIN LOOP will make it a step
        httpd.serve_forever()
        ###


    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)


    # print command line arguments
    #client = DBClient(args[1:])
    #TODO: if len(argv)==1 read server.cfg, if 2 with cfg use specified file,  file or revert then def

    # For now, backup and wipe database in Bash 
    # Perfkit calls add_entry
    # DBClient
    # TODO a http-server
    # on GET request, retrieve metric


if __name__ == "__main__":
    main()