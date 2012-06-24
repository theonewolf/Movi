#!/usr/bin/env python
#
#   Authors: Wolfgang Richter <wolf@cs.cmu.edu>
#            Debjani Biswas   <dbiswas@cmu.edu>
#
#
#   Description: This is a web app that serves a group of video files from a
#                directory.


### Imports ###
from flask import __version__
from flask import Flask
from flask import render_template
from flask import request
from flask import send_file
from flask import send_from_directory

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

import os 
from sys import argv
from sys import version




### App Configuration ###
USAGE='Usage: %s <path to movie files folder>'
HOST='0.0.0.0'
PORT=31415
app=Flask(__name__)
app.debug=True

__movies = dict()
__root = ''

### Helper functions ###
def die(msg):
    print 'ERROR: %s' % (msg)
    exit(1)

def log_info(msg):
    print 'INFO: %s' % msg

def find_movies(path):
    global __movies
    for (dirpath, dirnames, filenames) in os.walk(path):
        for d in dirnames:
            find_movies(d)
        for f in filenames:
            split = os.path.splitext(f)
            if split[1] == '.avi':
                __movies[split[0]] = os.path.join(dirpath, f)




### Routes ###
@app.route('/favicon.ico')
def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),
                            'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/info')
def info():
    global __movies
    sorted_movies = sorted(__movies.items())
    server = os.environ.get('SERVER_SOFTWARE', 'Unknown')
    return render_template('info.html', movies=sorted_movies,
                                        ip=HOST,
                                        port=PORT,
                                        server=server,
                                        python=version,
                                        flask=__version__,
                                        root=__root)

@app.route('/movies')
def movies():
    global __movies
    global __root

    sorted_movies = sorted(__movies.keys())
    return render_template('movies.html', movies=sorted_movies,
                                          root=__root)

@app.route('/serve')
def serve():
    path = request.args.get('path')
    ext = os.path.splitext(path)[1]
    return send_file(path, mimetype='video/%s' % ext[1:]) 

@app.route('/watch')
def watch():
    global __movies
    path = __movies[request.args.get('movie')]
    ext = os.path.splitext(path)[1][1:]
    return render_template('watch.html', path=path, type=ext)

### Main ###
if __name__ == '__main__':
    
    if len(argv) != 2:
        print USAGE % (argv[0])
        die('Not enough arguments.')

    if not os.path.isdir(argv[1]):
        print USAGE % (argv[1])
        die('First argument is not a valid directory.')

    __root = argv[1]
  
    find_movies(__root)

    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(PORT)
    IOLoop.instance().start()
