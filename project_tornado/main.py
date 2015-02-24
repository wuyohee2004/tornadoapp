import os
import signal
import logging

from tornado import web,ioloop
from tornado import options


is_closing = False

def signal_handler(signum, frame):
    global is_closing
    logging.info('exiting...')
    is_closing = True

def try_exit():
    global is_closing
    if is_closing:
        # clean up here
        ioloop.IOLoop.instance().stop()
        logging.info('exit success')
class MainHandler(web.RequestHandler):
    def get(self):
        self.write("Hello get")

    def post(self):
        self.write("Hello post")

    def put(self):
        self.write("Hello put")

        # def delete(self):
        #     self.write("Hello delete")

if __name__ == "__main__":
    settings = {
        'debug':True,
        'static_path':os.path.join(os.path.dirname(__file__),"static"),
        'template_path':os.path.join(os.path.dirname(__file__),"templates"),
        }

    application = web.Application([
                                      (r"/",MainHandler),
                                      ],**settings)
    options.parse_command_line()
    signal.signal(signal.SIGINT, signal_handler)
    application.listen(8888)
    ioloop.PeriodicCallback(try_exit, 100).start()
    ioloop.IOLoop.instance().start()
