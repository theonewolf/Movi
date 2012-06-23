#!/usr/bin/env python
#
#   Authors: Wolfgang Richter <wolf@cs.cmu.edu>
#            Debjani Biswas   <dbiswas@cmu.edu>
#
#
#   Description: This is a web app that serves a group of video files from a
#                directory.


### Imports ###
from flask import Flask
from flask import render_template


from sys import argv
import os 




### App Configuration ###
USAGE='Usage: %s <path to movie files folder>'
HOST='0.0.0.0'
PORT=31415
app=Flask(__name__)
app.debug=True

__movies = dict()

### Helper functions ###
def die(msg):
    print 'ERROR: %s' % (msg)
    exit(1)

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
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/info')
def info():
    global __movies
    sorted_movies = sorted(__movies.items())
    return 'Display configuration and list of videos (%s)' % (str(sorted_movies))

@app.route('/movies')
def movies():
    return 'Show movie form...'

@app.route('/serve/<name>')
def serve(name=None):
    return 'Trying to serve: "%s"' % name


@app.route('/watch/<name>')
def watch(name=None):
    return 'Trying to watch: "%s"' % name

### Main ###
if __name__ == '__main__':
    
    if len(argv) != 2:
        print USAGE % (argv[0])
        die('Not enough arguments.')

    if not os.path.isdir(argv[1]):
        print USAGE % (argv[1])
        die('First argument is not a valid directory.')

  
    find_movies(argv[1])

    app.run(host=HOST, port=PORT)
