import string, cgi, time, json
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import ConfigParser
from HexyPresetController import BotPresetControl

bot = BotPresetControl()
__builtins__.hexy = bot.hexy # sets 'hexy' to be a gobal variable common to all modules
__builtins__.floor = 60  # this is the minimum level the legs will reach

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            op = self.path[1:]
            self.end_headers()
            if op == "index.html":
                self.wfile.write("<h1>Available commands</h1>")
            else:
                self.wfile.write(json.dumps({'operation': op}))
                #bot.parseTextCommand(op)
                bot.runCommand(op)
            return
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)


def main():
    try:
        server = HTTPServer(('', 8080), MyHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()
        bot.estop()

if __name__ == '__main__':
    main()

