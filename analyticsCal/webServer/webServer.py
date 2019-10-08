from flask import Flask, request, json, send_from_directory, send_file, jsonify, render_template, Response
import sys
import pymysql

'''
Created on 05-Oct-2019

@author: archit
'''


# -*- coding: UTF-8 -*-
"""
hello_flask: First Python-Flask webapp
"""

#from flask import Flask  # From module flask import class Flask
app = Flask(__name__)    # Construct an instance of Flask class for our webapp

@app.route('/')   # URL '/' to be handled by main() route handler
def main():
    """Say hello"""
    return 'Hello, world!'

@app.route("/FixItFast/<path:path>", methods=['GET'])
def static_resource(path):    
    return send_from_directory('./FixItFast/', path)


if __name__ == '__main__':  # Script executed directly?
    app.run(debug=True)  # Launch built-in web server and run this Flask webapp
