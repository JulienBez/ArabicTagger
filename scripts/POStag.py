import re
import glob
from tqdm import tqdm

from .utils import *

from camel_tools.tagger.default import DefaultTagger
from camel_tools.disambig.mle import MLEDisambiguator
from camel_tools.tokenizers.word import simple_word_tokenize

def checkMarkup(lines):
    "check for markup characters to replace to avoid errors in TXM"
    new_lines = []
    for line in lines:
        new_line = line.replace("=\">","=\"&gt;").replace("=\"<","=\"&lt;")
        new_line = re.sub("=\"(na)|(None)\"","=\"",new_line)
        new_lines.append(new_line)
    return new_lines

def POStag():
    "apply camel-tools POS tagging according to tags listed in tags_list.json"

    mled = MLEDisambiguator.pretrained()
    tags_list = openJson("scripts/tags_list.json")

    taggers = {}
    for tag in tags_list:
        if tag not in taggers:
            taggers[tag] = DefaultTagger(mled, tag)

    for path in tqdm(glob.glob("data/text/*.txt")):

        new_path = path.replace("data/text/","output/").replace(".txt",".xml")
        if isFile(new_path) == False:

            with open(path,'r',encoding='utf-8') as f:
                file = f.read()
            
            tokens = simple_word_tokenize(file) #split_digits

            dic_tagged = {}
            for k, v in tqdm(taggers.items()):
                if k not in dic_tagged:
                    dic_tagged[k] = v.tag(" ".join(tokens).split())

            liste = []
            for i,tok in enumerate(tokens):
                jointure = {"word":tok}
                for k, v in dic_tagged.items():
                    if k not in jointure:
                        jointure[k] = v[i]
                liste.append(jointure)

            lines = ["""<?xml version="1.0" encoding="utf-8"?>""","<root>"]

            for jointure in liste:
                line = "<w"
                for k,v in jointure.items():
                    if k != 'word':
                        line = line + (f""" {k}="{v}" """)
                line = line + "> " + jointure['word'].replace(">","&gt;").replace("<","&lt;") + " </w>"
                lines.append(line)
            lines.append("</root>")

            with open(new_path, 'w') as f:
                for line in checkMarkup(lines):
                    f.write(f"{line}\n")
