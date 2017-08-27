"""This module initializes the app"""

from .app import create_app
from .models import db, User, BucketList, BucketItem

app = create_app()

from .views import *
