import glob
import re
import subprocess

from docxlatex import Document
from tqdm import tqdm

from .utils import *


def docToDocx():
    """convert doc to docx format"""
    for path in tqdm(glob.glob("data/doc/*.doc")):
        subprocess.call(['soffice', '--headless', '--convert-to', 'docx', "--outdir", "data/doc/", path])
        os.remove(path)


def docxToText():
    """convert docx to txt format"""

    docToDocx()

    for path in tqdm(glob.glob("data/doc/*.docx")):

        new_path = path.replace("/doc/", "/text/").replace(".docx", ".txt")
        if isFile(new_path) == False:

            doc = Document(path)
            text = doc.get_text()

            text = [e for e in text.split("\n")]
            new_text = []

            for l in text:
                if any(char.isdigit() for char in l) and not l[-1].isnumeric():
                    # pour chaque ligne contenant des chiffres qui ne sont pas des nums de chapitre
                    l = re.sub(r"\d*", "", l)
                new_text.append(l)

            new_path = path.replace("/doc/", "/text/").replace(".docx", ".txt")
            with open(new_path, 'w', encoding='utf-8') as f:
                f.write("\n".join(new_text))
