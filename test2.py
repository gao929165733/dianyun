import os
from publicMethod import mkdir, converter, segRoot, LASmerge, wayTxtToJson, wayTxtToJson2
from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import send_from_directory
from flask import send_file
from flask import make_response
from werkzeug import secure_filename
from flask import redirect
from flask import json, jsonify
import shutil

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!', 201, {'Content-Type': 'application/json'}



if __name__ == '__main__':
    port = 5001
    app.debug = True
    app.run('',port)