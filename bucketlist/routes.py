"""This module contains the routes for the application"""

import random, string, datetime
import jwt
from flask import request, jsonify, make_response
from functools import wraps
from .app import *

RANDOM_STRING = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(32))
# app.config['SECRET_KEY'] = RANDOM_STRING
app.config['SECRET_KEY'] = 'RANDOM_STRING'
app.config['TOKEN_NAME'] = 'x-token'
# public access

def authenticate(f):
    @wraps(f)
    def inner(*args, **kwargs):
        token = None
        if app.config['TOKEN_NAME'] in request.headers:
            token = request.headers[app.config['TOKEN_NAME']]

        if not token:
            token = request.args.get('token')

        if not token:
            return jsonify(message="Token is parameter"), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            
        except:
            return jsonify(message="Invalid token"), 401

        user = User.query.get(data['user_id'])
        now = datetime.datetime.utcnow()
        
        if not user:
            return jsonify(message="Invalid token"), 401

        if not token == user.token:
            return jsonify(message="Invalid token"), 401

        if now > user.token_expiry:
            return jsonify(message="Expired token"), 401

        if not user:
            return jsonify(message="Invalid token"), 401

        return f(user, *args, **kwargs)
    return inner

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

def get_pagination_params(request):
    limit = request.args.get('limit')
    page = request.args.get('page')
    
    try:
        limit = int(limit)
    except:
        limit = 12

    try:
        page = int(page)
    except:
         page = 0
    
    limit = 12 if limit < 0 else limit
    page = 0 if page < 0 else page

    return limit, page

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
        return jsonify(message = 'Duplicate parameter', parameter = 'email'), 409

    username_exists = User.has_username(username)

    if username_exists:
        return jsonify(message = 'Duplicate parameter', parameter = 'username'), 409

    user = User(first_name, last_name, username, email, password)
    db.session.add(user)
    db.session.commit()

    created_user = User.query.filter_by(email = email).first()
    
    return jsonify(created_user.dict()), 201

@app.route("/auth/login", methods=['POST'])
def login():
    """Login application user"""
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate':'Basic Realm="Login required"'})

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        user = User.query.filter_by(email=auth.username).first()

    if not user:
        return make_response('Invalid login credentials', 401, {'WWW-Authenticate':'Basic Realm="Login required"'})

    password_matches = user.verify_password(auth.password)

    if not password_matches:
        return make_response('Invalid login credentials', 401, {'WWW-Authenticate':'Basic Realm="Login required"'})

    # password matched login user
    expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=24*60*7)
    token = jwt.encode({'user_id':user.id, 'expiry':str(expiry)}, app.config['SECRET_KEY'])
    token = token.decode('UTF-8')

    user.token = token
    user.token_expiry = expiry
    db.session.commit()

    return jsonify(token=token, user = user.dict())

@app.route("/auth/logout", methods=['POST'])
@authenticate
def logout(user):
    """Logout application user"""
    expiry = datetime.datetime.utcnow() - datetime.timedelta(minutes=20)
    #user.token = ''
    user.token_expiry = expiry
    db.session.commit()
    return jsonify()

@app.route("/auth/reset-password", methods=['POST'])
@authenticate
def reset_password(user):
    """Reset application user's password"""
    body = get_request_body(request)
    old_password = body.get('old_password')
    new_password = body.get('new_password')

    if not old_password:
        return jsonify(message = 'You must provide old password', parameter='old_password'), 400

    if not new_password:
        return jsonify(message = 'You must provide new password', parameter='new_password'), 400

    if not user.verify_password(old_password):
        return jsonify(message = 'Invalid old password')

    user.set_password(new_password)
    db.session.commit()

    return jsonify()

# private access
@app.route("/bucketlists", methods = ['GET', 'POST'])
@authenticate
def bucketlists(user):
    """Adds or retrieves buckets"""
    if request.method == 'POST':
        body = get_request_body(request)
        name = body.get('name')
        description = body.get('description')

        if not name:
            return jsonify(message='Missing required parameter', parameter='name'), 400
        
        if not description:
            return jsonify(message='Missing required parameter', parameter='description'), 400
        
        bucket = Bucket(name, description, owner = user)
        db.session.add(bucket)
        db.session.commit()

        result = dict(id = bucket.id, name = bucket.name, description=bucket.description)

        return jsonify(result), 201

    # request.method == 'GET'
    limit, page = get_pagination_params(request)

    offset = page * limit

    buckets = Bucket.query.filter(Bucket.user_id == user.id).limit(limit).offset(offset)
    bucket_list = list()

    for bucket in buckets:
        _bucket = dict(id=bucket.id, name=bucket.name, description=bucket.description)
        bucket_list.append(_bucket)

    return jsonify(bucket_list)

@app.route("/bucketlists/<int:id>", methods = ['GET', 'PUT', 'DELETE'])
@authenticate
def bucketlists_id(user, id):
    
    bucket = Bucket.query.filter_by(user_id = user.id, id = id).first()

    if bucket == None:
        return jsonify(message = 'Bucket does not exist'), 404

    if request.method == 'PUT':
        body = get_request_body(request)
        bucket.name = body.get('name')
        bucket.description = body.get('description')
        db.session.commit()
    
    if request.method == 'DELETE':
        db.session.delete(bucket)
        db.session.commit()
        return jsonify(id=bucket.id)

    bucket_result = dict(id=bucket.id, name=bucket.name, description=bucket.description)
    bucket_result['items'] = list()
    limit, page = get_pagination_params(request)
    items = BucketItem.query.filter(BucketItem.bucket_id == bucket.id).limit(limit).offset(limit * page)
    
    for item in items:
        bucket_result['items'].append(item.dict())

    return jsonify(bucket_result)

@app.route("/bucketlists/<int:id>/items", methods=['POST'])
@authenticate
def add_bucket_item(user, id):
    """Creates a bucket item"""
    bucket = Bucket.query.filter_by(user_id = user.id, id = id).first()
    
    if bucket == None:
        return jsonify(error='Bucket does not extist'), 404

    body = get_request_body(request)
    title = body.get('title')
    description = body.get('description')
    due_date = body.get('due_date')

    if title == None:
        return jsonify(message='Missing required parameter', parameter="title"), 400

    if description == None:
        return jsonify(message='Missing required parameter', parameter="description"), 400

    if due_date == None:
        return jsonify(message='Missing required parameter', parameter="due_date"), 400

    item = BucketItem(title, description, due_date, bucket = bucket)
    db.session.add(item)
    db.session.commit()

    result = dict()
    result['id'] = item.id 
    result['title'] = item.title 
    result['description'] = item.description
    result['is_complete'] = item.is_complete
    result['due_date'] = item.due_date
    
    return jsonify(result), 201

@app.route("/bucketlists/<int:bucket_id>/items/<int:item_id>", methods=['PUT', 'DELETE'])
@authenticate
def bucket_items(user, bucket_id, item_id):
    """do sth"""
    bucket = Bucket.query.filter_by(user_id = user.id, id = bucket_id).first()
    
    if bucket == None:
        return jsonify(error='Bucket does not extist'), 404

    item = BucketItem.query.filter_by(bucket_id = bucket.id, id = item_id).first()

    if item == None:
        return jsonify(error='BucketItem does not extist'), 404

    if request.method == 'DELETE':
        db.session.delete(item)
        db.session.commit()
        return jsonify(id=item.id)

    # request.method == 'PUT':
    body = get_request_body(request)
    title = body.get('title')
    description = body.get('description')
    is_complete = body.get('is_complete')
    due_date = body.get('due_date')

    try:
        is_complete = int(is_complete)
    except:
        is_complete = False

    if not title == None:
        item.title = title

    if not description == None:
        item.description = description

    if not due_date == None:
        item.due_date = due_date
    
    if not is_complete == None:
        item.is_complete = bool(is_complete)

    db.session.commit()

    result = dict()
    result['id'] = item.id 
    result['title'] = item.title 
    result['description'] = item.description
    result['is_complete'] = item.is_complete
    result['due_date'] = item.due_date
    
    return jsonify(result)
