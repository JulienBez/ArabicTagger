import re
from pathlib import Path

from camel_tools.disambig.mle import MLEDisambiguator
from camel_tools.tagger.default import DefaultTagger
from camel_tools.tokenizers.word import simple_word_tokenize
from tqdm import tqdm

from .utils import *

markup = re.compile(r'="(na)|(None)"')


def checkMarkup(lines):
    """check for markup characters to replace to avoid errors in TXM"""
    new_lines = []
    for line in lines:
        new_line = line.replace("=\">", "=\"&gt;").replace("=\"<", "=\"&lt;")
        new_line = markup.sub("=\"", new_line)
        new_lines.append(new_line)
    return new_lines


def POStag():
    """apply camel-tools POS tagging according to tags listed in tags_list.json"""

    mled = MLEDisambiguator.pretrained()
    tags_list = openJson("scripts/tags_list.json")

    folder = Path("data/text")
    output = Path("output")

    # taggers = {}
    # for tag in tags_list:
    #     if tag not in taggers:
    #         taggers[tag] = DefaultTagger(mled, tag)

    taggers = {tag: DefaultTagger(mled, tag) for tag in tags_list}

    for path in tqdm(list(folder.glob("*.txt"))):
        new_path = output / path.with_suffix(".xml").name

        if new_path.exists():
            continue

        with path.open('r', encoding='utf-8') as f:
            file = f.read()

        tokens = simple_word_tokenize(file)  # split_digits

        dic_tagged = {}
        for k, v in taggers.items():
            if k not in dic_tagged:
                dic_tagged[k] = v.tag(" ".join(tokens).split())

        liste = []
        for i, tok in enumerate(tokens):
            jointure = {"word": tok}
            for k, v in dic_tagged.items():
                if k not in jointure:
                    jointure[k] = v[i]
            liste.append(jointure)

        lines = ["""<?xml version="1.0" encoding="utf-8"?>""", "<root>"]

        for jointure in liste:
            line = "<w"
            for k, v in jointure.items():
                if k != 'word':
                    line = line + f""" {k}="{v}" """
            line = line + "> " + jointure['word'].replace(">", "&gt;").replace("<", "&lt;") + " </w>"
            lines.append(line)
        lines.append("</root>")

        with new_path.open('w') as f:
            f.write("\n".join(lines))
