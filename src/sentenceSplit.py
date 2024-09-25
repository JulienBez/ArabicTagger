import pandas as pd
from pathlib import Path
from tqdm.auto import tqdm
import xml.etree.ElementTree as ET

from .utils import *


def sentenceSplit(format="csv"):
    """Divide a text in sentences from its xml POS tags output. Can be saved in csv or json"""

    folder = Path("output/tagged/")
    output = Path("output/sentences/csv/")
    if format == "json":
        output = Path("output/sentences/json/")
    createFolders(output)

    for xml_file in tqdm(list(folder.glob("*.xml"))):
        tree = ET.parse(xml_file)
        root = tree.getroot()

        sents = [] 
        sent = [] 
        pos = []
        lem = []

        for word_element in root.findall('w'):
            word = word_element.text.strip() 
            pos_tag = word_element.attrib.get('pos', '')
            lem_tag = word_element.attrib.get('lex', '')

            sent.append(word)
            pos.append(pos_tag)
            lem.append(lem_tag)

            if word in ["!", "؟", ".", "!","\n"]:
                if sent and (len(sent) < 2 or sent[-2] not in ["!", "؟", ".", "!"]):
                    sents.append((" ".join(sent), " ".join(pos), " ".join(lem)))
                    sent = []
                    pos = []
                    lem = []

        if sent:
            sents.append((" ".join(sent), " ".join(pos), " ".join(lem)))

        if format == "json":
            dict_sent = {}
            for tup in sents:
                dict_sent[tup[0]] = {"TOK":tup[0].split(),"POS":tup[1].split(),"LEM":tup[2].split()}
            writeJson(output / xml_file.with_suffix(".json").name,dict_sent)

        else:
            df = pd.DataFrame(sents, columns=["sentence", "POS", "LEM"])
            df.to_csv(output / xml_file.with_suffix(".csv").name, index=False)
