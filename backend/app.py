import os
import psycopg2
import requests
import json
from datetime import datetime
from functools import wraps
from flask import Flask,request, redirect, jsonify,  render_template, flash, session
from lib.database_connection import get_flask_database_connection


app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')