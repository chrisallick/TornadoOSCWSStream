from threading import Thread
import time
import signal
import sys
import OSC
import Queue

import logging
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import os.path

import json

from tornado.options import define, options

define( "port", default=8888, help="run on the given port", type=int )

queue = Queue.Queue()

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/websocket", OSCWebSocketHandler),
        ]
        settings = dict(
            cookie_secret="43oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            autoescape=None,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class OSCWebSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()

    def open(self):
        OSCWebSocketHandler.waiters.add(self)
        OSCWebSocketHandler.update_coords()

    def on_close(self):
        OSCWebSocketHandler.waiters.remove(self)

    @classmethod
    def update_coords( self ):
        global queue
        if not queue.empty():
            OSCWebSocketHandler.send_updates(json.dumps({"msg": queue.get() }))

    @classmethod
    def send_updates(cls, msg ):
        for waiter in cls.waiters:
            try:
                waiter.write_message( msg )
            except:
                pass

    def on_message(self, message):
        pass

def osc_handler( addr, tags, stuff, source):
    global queue
    print stuff
    queue.put( stuff[0] )


def signal_handler(signal, frame):
    print 'You pressed Ctrl+C!'
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)

    s = OSC.ThreadingOSCServer(("localhost",5444)) # threading
    print "Creating OSCServer on port 5444..."
    s.addMsgHandler("/OSC", osc_handler) # adding our function
    st = Thread( target = s.serve_forever )
    st.start()

    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    io_loop = tornado.ioloop.IOLoop.instance()
    tornado.ioloop.PeriodicCallback( OSCWebSocketHandler.update_coords, 10.0, io_loop=io_loop ).start()
    io_loop.start()

if __name__ == "__main__":
    main()