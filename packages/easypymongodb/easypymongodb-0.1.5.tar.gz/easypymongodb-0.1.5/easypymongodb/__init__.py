import pymongo
import dns


class DB:
  """
  Initialisation of the pymongo client.

  [client] is the string which is used to connect to Atlas.
  Make sure to include username & password in the string.
  Not optional; can only be set during initialisation.

  [dbname] is the name of the database.
  This is optional; can be set via .dbName = "".
  Will throw up an error if it isn't set and you try to insert data.

  [colname] is the name of the collection.
  This is optional; can be set via .colName = "".
  Will throw up an error if it isn't set and you try to insert data.
  """
  def __init__(self, client: str, dbname: str = "", colname: str = ""):
    self._pymongo = pymongo
    self._dns = dns
    self._client = self._pymongo.MongoClient(client)
    self._dbName = dbname
    self._colName = colname
  
  """
  Property.
  Returns the [list] list of database names if found.
  Use by .databases (print).
  """
  @property
  def databases(self):
    return self._client.list_database_names()

  """
  Property.
  Returns the [list] list of collection names if found.
  Use by .collections (print).
  """
  @property
  def collections(self):
    db = self._client[self._dbName]
    return db.list_collection_names()

  """
  Property.
  Returns the [string] name of the current database being used.
  Use by .dbName (print).
  """
  @property
  def dbName(self):
    return self._dbName

  """
  Property.
  Returns the [string] name of the current collection being used.
  Use by .colName (print).
  """
  @property
  def colName(self):
    return self.colName
  
  """
  Setter object.
  Set the [string] name of the database which you want to use.
  Use by .dbName = "".
  """
  @dbName.setter
  def dbName(self, name: str):
    self._dbName = name

  """
  Setter object.
  Set the [string] name of the collection which you want to use.
  Use by .colName = "".
  """
  @colName.setter
  def colName(self, name: str):
    self._colName = name

  """
  Internal method to create and return the database.
  """
  def __createDB(self):
    db = self._client[self._dbName]
    return db

  """
  Internal method to create and return the collection.
  """
  def __createCol(self):
    db = DB.__createDB(self)
    mycol = db[self._colName]
    return mycol
  
  """
  Method to insert [dict] data into the database.
  Data inserted as a dict and id is returned (print).
  """
  def insertOne(self, data: dict):
    mycol = DB.__createCol(self)
    x = mycol.insert_one(data)
    return f"Inserted data with id: {x.inserted_id}"
  
  """
  Method to insert [dict] multiple data into the database.
  Data inserted as a list and ids are returned (print).
  """
  def insertMany(self, data: list):
    mycol = DB.__createCol(self)
    x = mycol.insert_many(data)
    return f"Inserted datas with ids: {x.inserted_ids}"
  
  """
  Method to find first occurence in a collection in a database.
  Data is returned as a [dict] dict with the _id field.
  """
  def findOne(self):
    mycol = DB.__createCol(self)
    data = mycol.find_one()
    return data

  """
  Method to find all occurences in a collection in a database.
  Data is returned as a [list] dictionary with the _id field.
  """
  def findAll(self):
    mycol = DB.__createCol(self)
    lst = []
    for data in mycol.find():
      lst.append(data)
    return lst

  """
  Method to filter occurences in a collection in a database.
  Data inserted must be a dict.
  Values must be 1 if there is more than one:
    {"fname": 1, "lname": 1}
  If there is only one, that field will be omitted if there is a 0:
    {"job": 0}
  Data is returned as a [dict] dictionary, with ID if otherwise specified.

  A limit can be specified if you only want a certain number of documents returned.
  """
  def filter(self, data: dict, ID=True, limit: int = 0):
    mycol = DB.__createCol(self)
    lst = []
    ID = 1 if ID == True else 0
    find = {"_id": ID}
    find.update(data)
    for data in mycol.find({}, find).limit(limit):
      lst.append(data)
    return dict(lst[0])

  """
  Method to find all query the occurences in a collection in a database.
  Data is returned as a [dict] dictionary with the _id field.

  You can also query in these ways:
    {"name": {"$gt", "S"}} --> to find the occurences where the "name" field starts with the letter "S" or higher (alphabetically).
    Check the pymongo docs for more modifiers.

    {"name": {"$regex": "S"}} --> to find only the occurences where the "name" field starts with the letter "S".
    Check the pymongo docs for more modifiers.
  
  A limit can be specified if you only want a certain number of documents returned.
  """
  def query(self, query: dict, limit: int = 0):
    mycol = DB.__createCol(self)
    lst = []
    data = mycol.find(query).limit(limit)
    for each in data:
      lst.append(each)
    return dict(lst[0])

  """
  Method to sort the collections in a database by a fieldname [field].
  If [ascending] is not specified, a descending [dict] dictionary will be returned.

  A limit can be specified if you only want a certain number of documents returned.
  """
  def sort(self, field: str, ascending=True, limit: int = 0):
    mycol = DB.__createCol(self)
    lst = []
    asc = 1 if ascending == True else -1
    data = mycol.find().sort(field, asc).limit(limit)
    for each in data:
      lst.append(each)
    return dict(lst[0])

  """
  Method to delete one query from a collection in a database.
  Query must be a [dict] dict.
  """
  def deleteOne(self, query: dict):
    mycol = DB.__createCol(self)
    mycol.delete_one(query)
    return f"Deleted {query}!"

  """
  Method to delete many queries from a collection in a database.
  Query must be a [dict] dict.

  To delete all collections in a database, set query as en empty dict.
  """
  def deleteMany(self, query: dict):
    mycol = DB.__createCol(self)
    x = mycol.delete_many(query)
    return f"Deleted {x.deleted_count} documents!"

  """
  Method to drop a collection in a database.
  """
  def drop(self):
    mycol = DB.__createCol(self)
    mycol.drop()
    self._colName = ""
    return f"Dropped {mycol}"
  
  """
  Method to update one query from a collection in a database.
  oldquery & newquery must be a [dict] dict, with newquery being the data you want to replace of oldquery.

  Returns a [dict] dictionary of the updated collection.
  """
  def updateOne(self, oldquery: dict, newquery: dict):
    mycol = DB.__createCol(self)
    lst = []
    mycol.update_one(oldquery, newquery)
    for each in mycol.find():
      lst.append(each)
    return dict(lst[0])

  """
  Method to update many queries from a collection in a database (probably using regex or a modifier).
  oldquery & newquery must be a [dict] dict, with newquery being the data you want to replace of oldquery.
  """
  def updateMany(self, oldquery: dict, newquery: dict):
    mycol = DB.__createCol(self)
    lst = []
    x = mycol.update_many(oldquery, newquery)
    return f"{x.modified_count} documents modified"

  """
  Internal method to insert data transferred from [transfer] into the database.
  Data inserted as a list and ids are returned (print).
  """
  def _transferMany(self, data: dict):
    lst = []
    lst.append(data)
    mycol = DB.__createCol(self)
    x = mycol.insert_many(lst)
    return f"Inserted datas with ids: {x.inserted_ids}"

  """
  Method to transfer data from a dictionary to MongoDB Atlas. 
  Primarily created to transfer data from easypydb to MongoDB Atlas.
  """
  def transfer(self, data: dict):
    ids = []
    for x, y in data.items():
      self._dbName = x
      for a, b in y.items():
        self._colName = a
        if type(b) != dict:
          x = DB._transferMany(self, {a: b})
        else:
          x = DB._transferMany(self, b)
        ids.append(x)
    return x
