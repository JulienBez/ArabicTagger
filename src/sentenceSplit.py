from pathlib import Path
import pandas as pd
import xml.etree.ElementTree as ET
from tqdm.auto import tqdm

from .utils import *


def sentenceSplit():
    """"""

    folder = Path("output/tagged/")
    output = Path("output/sentences/")
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

            if word in ["!", "؟", ".", "!"]:
                if sent and (len(sent) < 2 or sent[-2] not in ["!", "؟", ".", "!"]):
                    sents.append((" ".join(sent), " ".join(pos), " ".join(lem)))
                    sent = []
                    pos = []
                    lem = []

        if sent:
            sents.append((" ".join(sent), " ".join(pos), " ".join(lem)))

        df = pd.DataFrame(sents, columns=["sentence", "tags", "lem"])
        df.to_csv(output / xml_file.with_suffix(".csv").name, index=False)
