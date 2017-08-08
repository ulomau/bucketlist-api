[![Build Status](https://travis-ci.org/john555/bucketlist-api.svg?branch=master)](https://travis-ci.org/john555/bucketlist-api)

# Bucketlist API (Challenge 3)

This project is an API for a bucket list app, that enables you to keep track of your goals or dreams.

## How to run the app

- Install Python version >= 3.5
- Clone the repository.
- Cd into the root the project root folder.
- Install required packages using `pip install -r requirements.txt`.
- Configure the `DATABASE_URI` environment variable. This is the database connection string.
- Run the app using the `python run.py` command.

## How to run migration script
- Run `python dbmigration.py db <command>`

For more info on what commands are available, run `python dbmigration.py db --help`

### How to run tests

The tests are written using the unittest module. To execute tests,

- Run `python -m unittest` while in the project's root folder. 

__Note__:
Make sure to install all required dependencies and configure the app environment.

## Documentation
Documentation can be found at `/apidocs` when the app is running.
