"""This module contains database configurations for the app"""
import os

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:su@postgressdb@localhost/bucketlist')
