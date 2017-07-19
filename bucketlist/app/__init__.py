"""This module contains the routes for the application"""

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../data/database.db'
db = SQLAlchemy(app)

# public access

@app.route("/auth/register", methods=['POST'])
def register():
    """register new application user"""
    return json.dumps(dict(status=200, code="OK")), 200

@app.route("/auth/login", methods=['POST'])
def login():
    """login application user"""
    pass
@app.route("/auth/logout", methods=['POST'])
def logout():
    """logout application user"""
    pass
@app.route("/auth/reset-password", methods=['POST'])
def reset_password():
    """reset application user's password"""
    pass

# private access
@app.route("/bucketlists", methods = ['GET', 'POST'])
def bucketlists():
    """do sth"""
    pass
@app.route("/bucketlists/<_id>", methods = ['GET', 'POST', 'PUT', 'DELETE'])
def bucketlists_id(_id):
    pass
@app.route("/bucketlists/<_id>/items", methods=['POST'])
def edit_bucket_item(_id):
    """edits a bucket list item"""
    pass
@app.route("/bucketlists/<_id>/items/<item_id>", methods=['PUT', 'DELETE'])
def main(_id, item_id):
    """do sth"""
    pass
