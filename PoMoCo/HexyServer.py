import string, cgi, time, json
import threading
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from ConfigParser import *
from servotorComm import runMovement

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            self.send_response(200)
            op = self.path[1:]
            if op == "index.html" or op == "":
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write("<html><head>" + 
                                 "<meta http-equiv='Content-Type'" +
                                 "content='text/html; charset=utf-8' />" +
                                 "<script type='text/javascript' src='//ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js'></script>" +
                                 "<script type='text/javascript'>" +
                                 "function runCommand(name){ $.get(name, '' , " +
                                 "function(data){ /*alert(data);*/ }); } "+
                                 "</script>" +
                                 "</head><body>" +
                                 "<h1>Available commands</h1>")
                for moveName in moves:
                    self.wfile.write("<a style='min-width:20em;margin:1em;font-size:120%;' href='javascript:" +
                                     "runCommand(\""+moveName+"\")" +
                                     "'>"+moveName+"</a><br>")
                self.wfile.write("</body></html>")
            else:
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                moveName = op.replace('%20',' ')
                if moveName in moves:
                    self.wfile.write(json.dumps({'operation': op}))
                    runMovement(move,moveName)
                else:
                    self.wfile.write(json.dumps({'operation': 'not found'}))

            return
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)


class httpThread(threading.Thread):

    def __init__(self, server):
        threading.Thread.__init__(self)
        self.function=self.run
        self.server = server
        self.start()

    def run(self):
        try:
            print 'started http server...'
            self.server.serve_forever()
        except KeyboardInterrupt:
            print '^C received, shutting down http server'
            self.server.socket.close()

def startHttpServer(port):
    server = HTTPServer(('', port), MyHandler)
    httpThread(server)
    print "Shutting down http server"

