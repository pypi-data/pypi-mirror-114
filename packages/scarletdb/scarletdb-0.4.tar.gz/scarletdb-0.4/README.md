# [Docs](https://github.com/Xd-pro/ScarletDB/wiki/ScarletDB)

Basic document database mostly intended for use on [replit](https://replit.com).
```py
db = ScarletDB([])
db.replit("data") # data is replit db the key that the database is stored in

db.clear() # empty the db for testing purposes

db.insert_many([
  {
    "name": "AJ",
    "pet": "Rabbit"
  },
  {
    "name": "Jack",
    "pet": "Dog"
  }
]) # insert some documents

db.update({"name": "Jack"}, {"name": "Tom"}) # update some documents, while querying them by a value (does not loop over them, uses a data structure to save them in a way where they can be queried)

print(db.get({
  "pet": "Dog"
})) # get a document by another key than before
```

Docs are on [github](https://github.com/xd-pro/ScarletDB)