import os
import json

def isFile(path):
  "check if a file exist"
  return os.path.isfile(path)

def openJson(path):
  "open a json file"
  with open(path,'r',encoding='utf-8') as f:
    data = json.load(f)
  return data
