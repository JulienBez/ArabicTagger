import re
import glob
from docxlatex import Document
from .utils import *
from tqdm import tqdm

def docxToText():
    "convert docx to txt format"

    for path in tqdm(glob.glob("data/doc/*.docx")):

        new_path = path.replace("/doc/","/text/").replace(".docx",".txt")
        if isFile(new_path) == False:
            
            doc = Document(path)
            text = doc.get_text()

            text = [e for e in text.split("\n")]
            new_text = []
            
            for l in text:
                if any(char.isdigit() for char in l) and l[-1].isnumeric() == False: 
                    #pour chaque ligne contenant des chiffres qui ne sont pas des nums de chapitre
                    l = re.sub(r"\d*","",l)
                new_text.append(l)

            new_path = path.replace("/doc/","/text/").replace(".docx",".txt")
            with open(new_path,'w',encoding='utf-8') as f:
                f.write("\n".join(new_text))
        