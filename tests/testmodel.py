import unittest
from bucketlist import *

db.drop_all()
db.create_all()

class TestUserModel(unittest.TestCase):

    def setUp(self):
        first_name = "John"
        last_name = 'Doe'
        username = 'jdoe'
        email = 'jdoe@example.com'
        password = 'theSecurePassword'
        
        user = User.query.filter_by(email = email).first()

        if user == None:
            user = User(first_name, last_name, username, email, password)

            db.session.add(user)
            db.session.commit()

            self.user = User.query.filter_by(email=user.email).first()
        else:
            self.user = user

        # Add a Bucket
        self.bucket_name = "Bucket 1"
        bucket_description = "Bucket 1's description"
        bucket = Bucket(self.bucket_name, bucket_description, owner = self.user)

        db.session.add(bucket)
        db.session.commit()

        self.bucket = Bucket.query.filter_by(user_id = self.user.id).first()
        # Add a BucketItem
        self.title = "To do 1"
        description="To do description"
        item = BucketItem(self.title, description, bucket=self.bucket)

        db.session.add(item)
        db.session.commit()

        self.item = BucketItem.query.filter_by(bucket_id = self.bucket.id).first()


    def tearDown(self):
        pass
        
    # User

    def test_can_create_user(self):
        created_user = User.query.get(self.user.id)
        self.assertEqual(self.user.email, created_user.email)
    
    def test_can_delete_user(self):
        user = User.query.get(self.user.id)
        db.session.delete(user)
        db.session.commit()

        deleted_user = User.query.get(self.user.id)
        
        self.assertIsNone(deleted_user)

    def test_can_update_user(self):
        self.user.first_name = 'Benjamin'
        db.session.commit()

        modified_user = User.query.get(self.user.id)

        self.assertEqual('Benjamin', modified_user.first_name)

    # Bucket

    def test_can_add_bucket(self):
        self.assertEqual(self.bucket_name, self.bucket.name)

    def test_can_edit_bucket(self):
        name2 = "Some random name"
        description2 = "Some random description"
        bucket = Bucket.query.filter_by(user_id=self.user.id).first()
        bucket.name = name2
        bucket.description = description2

        db.session.commit();

        edited_bucket = Bucket.query.get(bucket.id)

        self.assertEqual(name2, edited_bucket.name)
        self.assertEqual(description2, edited_bucket.description)
    
    def test_can_delete_bucket(self):
        bucket_id = self.bucket.id

        db.session.delete(self.bucket)
        db.session.commit()

        bucket = Bucket.query.get(bucket_id)

        self.assertIsNone(bucket)
    
    # BucketItem

    def test_can_add_bucket_item(self):
        self.assertEqual(self.title, self.item.title)
    
    def test_can_edit_bucket_item(self):
        self.item.title = "Another title"

        db.session.commit()

        editted_item = BucketItem.query.get(self.item.id)
        self.assertEqual("Another title", editted_item.title)
    
    def test_can_delete_bucket_item(self):
        item_id = self.item.id

        db.session.delete(self.item)
        db.session.commit()

        item = BucketItem.query.get(item_id)
