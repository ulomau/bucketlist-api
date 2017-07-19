""""""
from bucketlist.app import app, db

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(50), primary_key = True)
    last_name = db.Column(db.String(50), primary_key = True)
    username = db.Column(db.String(50), primary_key = True)
    email = db.Column(db.String(50), primary_key = True)
    password_hash = db.Column(db.String(50), primary_key = True)
    created_at = db.Column(db.DateTime)
    
    def __init__(self, first_name, last_name, username, email):
        self.username = username
        self.email = email

class Bucket(db.Model):
    __tablename__ = "bucket"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(140))
    created_at = db.Column(db.DateTime)

    def __init__(self):
        pass
        
class BucketItem(db.Model):
    __tablename__ = "bucket_item"
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(140))
    description = db.Column(db.String(250))
    created_at = db.Column(db.DateTime)
    
    def __init__(self):
        pass

