import os
import json

def isFile(path):
    """check if a file exist"""
    return os.path.isfile(path)


def openJson(path):
    """open a json file"""
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def writeJson(path,data):
  "create a json file"
  with open(path,"w",encoding='utf-8') as f:
    json.dump(data,f,indent=4,ensure_ascii=False)


def createFolders(path):
  "create several folders"
  if not os.path.exists(path):
    os.makedirs(path)