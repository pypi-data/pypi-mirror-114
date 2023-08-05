from replit import db as rdb
import json
from typing import Union, List

def pass_function():
  pass

class ScarletDB:
  def __init__(self, list, commit_function = pass_function):
    self.list = list
    self.commit = commit_function
  
  def lstructure(self) -> None:
    self.struct = {}
    keys = []
    for i, dict in enumerate(self.list):
      dict["_index"] = i
      self.list[i] = dict
    for dict in self.list:
      for key in dict.keys():
        if key not in keys:
          keys.append(key)
    for key in keys:
      self.struct[key] = {}
      for i, dict in enumerate(self.list):
        if self.list[i].get(key, None) not in self.struct[key]:
          self.struct[key][self.list[i].get(key, None)] = []
        self.struct[key][self.list[i].get(key, None)].append(self.list[i])
      
  def structure(self) -> None:
    self.struct = {}
    keys = []
    for i, doc in enumerate(self.list):
      doc["_index"] = i
      self.list[i] = doc
    for doc in self.list:
      for key in doc.keys():
        if key not in keys:
          keys.append(key)
    for key in keys:
      self.struct[key] = {}
      for i, doc in enumerate(self.list):
        if self.list[i].get(key, None) not in self.struct[key]:
          self.struct[key][self.list[i].get(key, None)] = []
        self.struct[key][self.list[i].get(key, None)].append(i)

  def insert(self, dict: dict) -> None:
    self.list.append(dict)
    self.structure()
    self.commit()
    return self.list[-1]
  
  def insert_many(self, dicts: List[dict]):
    indexes = []
    for dict in dicts:
      indexes.append(self.insert(dict)["_index"])
    retval = []
    for i in indexes:
      retval.append(self.list[i])

  
  '''def get(self, key, value) -> dict:
    indexes = []
    for index in self.struct[key][value]:
      indexes.append(index)
    retval = []
    for index in indexes:
      retval.append(self.list[index])
    return retval'''

  def get(self, query: Union[dict, int], one: bool = False, return_indicies=False, query_by_index=False):
    fresult = []
    indexes = []
    result = []
    done_indexes=[]
    for key in query.keys():
      for index in self.struct[key][query[key]]:
        indexes.append(index)
    for index in indexes:
      if index not in done_indexes:
        fresult.append(self.list[index])
        done_indexes.append(index)
    if not one:
      for res in fresult:
        has_failed = False
        for key in query.keys():
          if res.get(key, NotImplemented) != query[key]:
            has_failed = True
        if not has_failed:
          result.append(res)
    else:
      result = fresult
    if not return_indicies:
      return result
    else:
      return done_indexes

    


  def remove(self, query: Union[dict, int], query_by_index=False, one=False) -> None:
    if isinstance(query, dict) and query_by_index==True:
      raise TypeError("When querying by index, you must pass an integer that is and index of the list property on the DB.")
    if isinstance(query, int) and query_by_index==False:
      raise TypeError("When querying by value, you must pass a dict containing the values that you want and the keys associated with them.")
    if query_by_index:
      self.list.pop(query)
    else:
      self.list.pop(self.get(query, one=one))
    self.structure()
    self.commit()

  def update(self, query: Union[dict, int], value: dict, query_by_index=False) -> None:
    if isinstance(query, dict) and query_by_index==True:
      raise TypeError("When querying by index, you must pass an integer that is and index of the list property on the DB.")
    if isinstance(query, int) and query_by_index==False:
      raise TypeError("When querying by value, you must pass a dict containing the values that you want and the keys associated with them.")
    if query_by_index:
      inds = [self.list[query]]
    else:
      inds = self.get(query, return_indicies=True)
    for i in inds:
      for key in value.keys():
        self.list[i][key] = value[key]
    self.structure()
    self.commit()
  
  def replit(self, name: str):
    self.commit = self._replit_commit
    self._replit_name = name
    if name not in rdb.keys():
      rdb[name] = []
    self.list = json.loads(rdb.get_raw(name))
    self.commit()

  def clear(self):
    self.list = []
    self.structure()

  def _replit_commit(self):
    rdb[self._replit_name] = self.list

