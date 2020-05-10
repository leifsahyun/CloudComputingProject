#! /usr/bin/env python2

#is moving sys under __main__ a common practice?
import sys
import time
if sys.version_info[0] < 3:
    import BaseHTTPServer, cgi
else:
    print("web.py classes for python3 are not supported yet ")
    #import http.server etc etc
    exit()

import json
#import DBclient

API_Key = "c3d4e51234sa5" #clearly not implemented yet

DEF_HOST_NAME = "localhost" # !!!REMEMBER TO CHANGE THIS!!!
DEF_PORT_NUMBER = 8080 # Maybe set this to 9000.

dummy_metrics={"provider":"AWS",
            "type":"m1",
            "tier":"micro",
            "cpu":16,
            "RAM":32,
            "something": 75}

class MetricsServer(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(100)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
    
    
    def do_GET(self):
        """Respond to a GET request."""
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()

    def do_POST(self):
   # Parse the form data posted
     
        hdr=self.headers
        
        # Begin the response
        # this is where we use get_latest
        clength = int(hdr.getheader('content-length'))
        ctype, pdict = cgi.parse_header(hdr.getheader("content-type"))
        
        if ctype != "application/json":

            post_data = json.loads(self.rfile.read(clength)) # <--- Gets the data itself
            

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
        #### Body here

            # Note: writing the json dump each iteration might be more efficient, but looks less clean
            # so that's  something to consider later
            # like  
            #  for instkey ... :
            #   self.wfile.write("\'{")
            #   self.wfile.write("\"" +instkey + '\":' + json.dumps(dummy_metrics)) 
            #   ...

            metricdata={} #class object?
            #FUTURE: prevent race condition for DB access
            if post_data.has_key("instances"):
                for instkey in post_data["instances"]: 
                    #metricdata[instkey]=dummy_metrics  # 
                    metricdata[instkey] = self.dbc.get_last(instkey)
                
                self.wfile.write(json.dumps(metricdata)) 

            #TODO: request might be for updating the instance list database
            #elif has_key(something else) 

            # couldn't find the key we are looking for
            else:
                self.err_resp("Bad value in data")

        # we need a JSON
        else:
            self.err_resp("Bad content type")


        return
    
    def err_resp(self, msg, code=400):
        self.send_response(code)
        self.send_header("Error", msg)
        self.end_headers()
        return



def main():
    #TODO: parameterize
    HOST_NAME = DEF_HOST_NAME
    PORT_NUMBER = DEF_PORT_NUMBER
    server_class = BaseHTTPServer.HTTPServer #nice touch they did in the examples

    metricd = server_class((HOST_NAME, PORT_NUMBER), MetricsServer)
    print(time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))

    try:
        ### MAIN LOOP will make it a step
        metricd.serve_forever()
        ###


    except KeyboardInterrupt:
        pass
    metricd.server_close()
    print(time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))


    # print command line arguments
    #client = DBClient(args[1:])
    #TODO: if len(argv)==1 read server.cfg, if 2 with cfg use specified file,  file or revert then def

    # For now, backup and wipe database in Bash 
    # Perfkit calls add_entry
    # DBClient
    # TODO a http-server
    # on POST request, retrieve metric data


if __name__ == "__main__":
    main()