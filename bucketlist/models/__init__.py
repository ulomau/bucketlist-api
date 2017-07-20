""""""
import datetime
from passlib.hash import sha256_crypt
from bucketlist.app import app, db

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(255), nullable = False)
    last_name = db.Column(db.String(255), nullable = False)
    username = db.Column(db.String(255), unique = True, nullable = False)
    email = db.Column(db.String(255), unique = True, nullable = False)
    password_hash = db.Column(db.String(255), nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    buckets = db.relationship('Bucket', backref=db.backref('owner', lazy=True))
    
    def __init__(self, first_name, last_name, username, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password_hash = sha256_crypt.hash(password)

class Bucket(db.Model):
    __tablename__ = "bucket"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(140), nullable = False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    items = db.relationship('BucketItem', backref = db.backref("bucket", lazy = True))

    def __init__(self, name, description, owner = None):
        self.name = name
        self.description = description
        self.owner = owner
        
class BucketItem(db.Model):
    __tablename__ = "bucket_item"
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(140))
    description = db.Column(db.String(250))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    bucket_id = db.Column(db.Integer, db.ForeignKey('bucket.id'))
    
    def __init__(self, title, description, bucket = None):
        self.title = title
        self.description = description
        self.bucket = bucket
        
