import glob
from tqdm import tqdm

from .utils import *

def toASMR():
    "to asmr read json files"
    createFolders("output/asmr")
    counter = 0
    for path in tqdm(glob.glob("output/sentences/json/*.json")):
        data = openJson(path)
        new_data = []
        for k,v in data.items():
            entry = {
                "sent":k,
                "metadata": {"id":counter,"volume":path.split(" ")[-1].replace(".json","")},
                "paired_with":{"seed":"","distance":-1},
                "parsing": {
                    "TOK": v["TOK"],
                    "LEM": v["LEM"],
                    "POS": v["POS"]
                }
            }
            new_data.append(entry)
            counter += 1
        writeJson(path.replace("sentences/json/","asmr/"),new_data)