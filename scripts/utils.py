import os
import json

def isFile(path):
  "confirme si un fichier existe ou non"
  return os.path.isfile(path)

def openJson(path):
  "ouverture d'un fichier json"
  with open(path,'r',encoding='utf-8') as f:
    data = json.load(f)
  return data
