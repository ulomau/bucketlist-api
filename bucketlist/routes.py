"""This module contains the routes for the application"""

from flask import request, json
from .app import *

# public access

def get_request_body(request):
    """Returns the request body."""
    content_type = request.content_type
   
    if content_type == 'application/json':
        return request.json
    return request.form

def get_user_id(request):
    """Gets user_id from the query string or from the request body, for POST requests."""
    if request.method == 'POST':
        return get_request_body(request).get('user_id')
    
    return request.args.get('user_id')

@app.route("/auth/register", methods=['POST'])
def register():
    """Register new application user"""
    body = get_request_body(request)

    first_name = body.get("first_name")
    last_name = body.get("last_name")
    username = body.get("username")
    email = body.get("email")
    password = body.get("password")

    email_exists = User.has_email(email)

    if email_exists:
        return json.jsonify(error = 'email'), 409

    username_exists = User.has_username(username)

    if username_exists:
        return json.jsonify(error = 'username'), 409

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
    if request.method == 'POST':
        body = get_request_body(request)
        user_id = body.get('user_id')
        name = body.get('name')
        description = body.get('description')

        if user_id == None:
            return json.jsonify(error = 'Unknown user. you must provide the `user_id`'), 400

        user = User.query.get(user_id)

        if user == None:
            return json.jsonify(error = 'Unknown user'), 404

        bucket = Bucket(name, description, owner = user)
        db.session.add(bucket)
        db.session.commit()

        return json.jsonify(id = bucket.id, name = bucket.name, description=bucket.description), 201

    user_id = get_user_id(request)

    if user_id == None:
        return json.jsonify(error = 'You should specify user_id in the query string'), 400
    
    if not User.user_exists(user_id):
        return json.jsonify(error = 'Unknown user'), 404

    buckets = Bucket.query.filter_by(user_id = user_id)
    result = list()

    for bucket in buckets:
        result.append(dict(id=bucket.id, name=bucket.name, description=bucket.description))
    
    return json.jsonify(result)

@app.route("/bucketlists/<int:id>", methods = ['GET', 'PUT', 'DELETE'])
def bucketlists_id(id):
    bucket = Bucket.query.get(id)

    if bucket == None:
        return json.jsonify(error = 'Bucket does not exist'), 404

    if request.method == 'PUT':
        body = get_request_body(request)
        bucket.name = body.get('name')
        bucket.description = body.get('description')
        db.session.commit()
    
    if request.method == 'DELETE':
        db.session.delete(bucket)
        db.session.commit()
        return json.jsonify(id=bucket.id)

    return json.jsonify(id=bucket.id, name=bucket.name, description=bucket.description)


@app.route("/bucketlists/<_id>/items", methods=['POST'])
def edit_bucket_item(_id):
    """edits a bucket list item"""
    pass
@app.route("/bucketlists/<_id>/items/<item_id>", methods=['PUT', 'DELETE'])
def main(_id, item_id):
    """do sth"""
    pass
