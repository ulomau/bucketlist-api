"""This module contains database configurations for the app"""
import os

DATABASE_URI = os.environ.get('DATABASE_URI')

if not DATABASE_URI:
    DATABASE_URI = 'postgresql://postgres:su@postgressdb@localhost/bucketlist'
