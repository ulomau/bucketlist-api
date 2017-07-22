"""This module contains the routes for the application"""

from flask import request, json
from .app import *

db.drop_all()
db.create_all()

# public access

@app.route("/auth/register", methods=['POST'])
def register():
    """Register new application user"""
    first_name = request.json.get("first_name")
    last_name = request.json.get("last_name")
    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")

    user = User(first_name, last_name, username, email, password)
    db.session.add(user)
    db.session.commit()

    created_user = User.query.filter_by(email = email).first()
    
    return json.jsonify(id=created_user.id), 201

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
