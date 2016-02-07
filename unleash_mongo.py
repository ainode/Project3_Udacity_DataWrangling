#add site_packages, I already had Ipython Notebook installed in another directory.
sys.path.append("C:\\Users\\owner\\Anaconda3\\Lib\\site-packages")
import pymongo

def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

db = get_db('cities')

#Top 10 sources
sources = db.toronto.aggregate([{"$match":{"other_tags.source":{"$exists":1}}},
                               {"$group":{"_id":"$other_tags.source", "count":{"$sum":1}}},
                                                {"$sort":{"count":-1}}, {"$limit":10}])
for source in sources:
    print source

#Top 10 users
users = db.toronto.aggregate([{"$project":{"user":"$created.user","source":"$other_tags.source"}},
                               {"$group":{"_id":"$user", "count":{"$sum":1}}},
                               {"$project":{"count":"$count","user":"$created.user","source":"$source"}},
                                {"$sort":{"count":-1}}, {"$limit":10}])
for user in users:
    print user

#top 10 religious amenities
religions = db.toronto.aggregate([{"$match":{"other_tags.amenity":{"$exists":1}, "other_tags.amenity":"place_of_worship"}},                                                
                                    {"$group":{"_id":"$other_tags.religion", "count":{"$sum":1}}},                                                
                                    {"$sort":{"count":-1}}, {"$limit":10}])
                                                
for religion in religions:
    print religion

#top 10 leisure centers
leisures = db.toronto.aggregate([{"$match":{"other_tags.leisure":{"$exists":1}}},
                                                
{"$group":{"_id":"$other_tags.leisure", "count":{"$sum":1}}},
                                                
{"$sort":{"count":-1}}, {"$limit":10}])
                                                
for leisure in leisures:
    print leisure

"""Calculating proportion of roads with bicycle lane (the next 3 cells)"""
all_roads = db.toronto.aggregate([{"$match":{"other_tags.surface":"asphalt"}},
bicycle = db.toronto.aggregate([{"$match":{"other_tags.bicycle":"yes"}},
                                {"$group":{"_id":"$other_tags.bicycle", "count":{"$sum":1}}}])
print float(list(bicycle)[0]['count'])/float(list(all_roads)[0]['count'])

#Top 10 sport aminities. I thought there would be many more hokey rinks.
sports = db.toronto.aggregate([{"$match":{"other_tags.sport":{"$exists":"true"}}},
                                {"$group":{"_id":"$other_tags.sport", "count":{"$sum":1}}},{"$sort":{"count":-1}},{"$limit":10}])
for sport in sports:
    print sport

#Number of node elements in sample dataset
db.toronto.find({"type":"node"}).count()

#Number of way elements in sample dataset
db.toronto.find({"type":"way"}).count()

#Number of unique users
len(db.toronto.distinct("created.user"))

                                {"$group":{"_id":"$other_tags.surface", "count":{"$sum":1}}}])