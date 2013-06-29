import bson
import pprint
import pymongo
import sys

import cred_parser as credentials

## Server: "xxx@xxx.com, 
## Database: "PingPong"
## Write concern: 1 (acknowledge writes)
def get_creds():
    creds = credentials.parse()
    return creds

def get_connection(creds):
    db = 'mongodb://{0}:{1}@{2}:{3}/{4}?w=1'.format(creds['mongodb_user'],creds['mongodb_pass'],creds['mongodb_host'],creds['mongodb_port'],creds['mongodb_db'])

## Connect to MongoDB, create a handle for the "PingPong" database
    try:
        connection = pymongo.Connection(db)
        db = connection['PingPong']
    except Exception, ex:
        print "Couldn't connect, exception is: %s" % ex
    return db
    
def insert_into_collection_Players(Database,collection_name,record):
    
## Insert this document into the "Players" collection
    try:
        Database.Players.insert(record)
    except Exception, ex:
        print "Unable to insert, exception is: %s" % ex

def remove_from_collection_Players(Database,collection_name,record):

## Remove this document into the "Players" collection
    try:
        Database.Players.remove(record)
    except Exception, ex:
        print "Unable to insert, exception is: %s" % ex

def get_all_Players(Database):
    for post in Database.Players.find().limit(20):
        pprint.pprint(post)

def get_count_Players(Database):
    return Database.Players.count()

def create_leaderboard(Database,record):
    Database.LeaderBoard.insert(record)
