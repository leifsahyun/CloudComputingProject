#! /usr/bin/env python

# is moving sys under __main__ a common practice?
import json
import cgi
import sys
import time

if sys.version_info[0] < 3:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

else:
    from http.server import BaseHTTPRequestHandler, HTTPServer
    #dict.__contains__=dict.__contains__

# import DBclient
from DBClient import DBClient


API_Key = "c3d4e51234sa5"  # clearly not implemented yet

DEF_HOST_NAME = "localhost"  # !!!REMEMBER TO CHANGE THIS!!!
DEF_PORT_NUMBER = 8080  # Maybe set this to 9000.

dummy_metrics = {"provider": "AWS",
            "type": "m1",
            "tier": "micro",
            "cpu": 16,
            "RAM": 32,
            "something": 75}


class MetricsServer(HTTPServer):
    def __init__(self, dbClient, *args, **kwargs):
         # Because HTTPServer is an old-style class, super() can't be used.
         HTTPServer.__init__(self, *args, **kwargs)
         print("Attached DB client")
         self.dbc = dbClient

class MetricsServerHandler(BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server):
        #print('Handling Request')
        # http://donghao.org/2015/06/18/override-the-__init__-of-basehttprequesthandler-in-python/?replytocom=151#respond
        #BaseHTTPRequestHandler.__init__(…) does NOT exit until a first request has been handled
        BaseHTTPRequestHandler.__init__(self,  request, client_address, server)

        if sys.version_info[0] < 3:
            self.headers.get = self.headers.getheader

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
        clength = int(hdr.get('content-length'))
        print(clength)
        ctype, pdict = cgi.parse_header(hdr.get("content-type"))

        if ctype == "application/json" and clength:

            post_data = json.loads(self.rfile.read(clength)) # <--- Gets the data itself


            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
        # Body here

            # Note: writing the json dump each iteration might be more efficient, but looks less clean
            # so that's  something to consider later
            # like
            #  for instkey ... :
            #   self.wfile.write("\'{")
            #   self.wfile.write("\"" +instkey + '\":' + json.dumps(dummy_metrics))
            #   ...

            metricdata={} #class object?
            # FUTURE: prevent race condition for DB access
            if post_data.__contains__("request"):
                print(post_data.get('request'))
                if  post_data.get('request') == 'metrics':
                    for instkey in post_data["instances"]:
                        #metricdata[instkey]=dummy_metrics  #
                        metricdata[instkey] =  self.server.dbc.pull_last(instkey)


                elif  post_data.get('request') == 'alternatives':
                    metricdata['instance_names'] = self.server.dbc.get_alternatives(post_data.get('instance'))

                elif  post_data.get('request') == 'candidates':
                    metricdata['instance_names'] = self.server.dbc.get_candidates(post_data.get('params'))

                print('POST:',metricdata)
                
                self.wfile.write(json.dumps(metricdata, default=str).encode())
            # TODO: request might be for updating the instance list database
            # elif __contains__(something else)

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
    # TODO: parameterize
    HOST_NAME = DEF_HOST_NAME
    PORT_NUMBER = DEF_PORT_NUMBER
    server_class = MetricsServer #nice touch they did in the examples
    dbc=DBClient()
    metricd = server_class(dbc,(HOST_NAME, PORT_NUMBER), MetricsServerHandler)
    print(time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
    try:
        # MAIN LOOP will make it a step
        metricd.serve_forever()
        ###


    except KeyboardInterrupt:
        pass
    metricd.server_close()
    print(time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))


    # print command line arguments
    # client = DBClient(args[1:])
    # TODO: if len(argv)==1 read server.cfg, if 2 with cfg use specified file,  file or revert then def

    # For now, backup and wipe database in Bash
    # Perfkit calls add_entry
    # DBClient
    # TODO a http-server
    # on POST request, retrieve metric data


if __name__ == "__main__":
    main()
