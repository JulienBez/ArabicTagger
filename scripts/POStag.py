import re
from io import StringIO
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

from camel_tools.disambig.bert.unfactored import BERTUnfactoredDisambiguator
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


def POStag(disambiguator="mled_msa"):
    """apply camel-tools POS tagging according to tags listed in tags_list.json"""

    disambiguators = {
        "mled_msa": [MLEDisambiguator.pretrained, {"model_name": "calima-msa-r13"}],
        "mled_egy": [MLEDisambiguator.pretrained, {"model_name": "calima-egy-r13"}],

        "bert_msa": [BERTUnfactoredDisambiguator.pretrained, {"model_name": "msa"}],
        "bert_egy": [BERTUnfactoredDisambiguator.pretrained, {"model_name": "egy"}],
        "bert_glf": [BERTUnfactoredDisambiguator.pretrained, {"model_name": "glf"}],
    }

    try:
        mled = disambiguators[disambiguator]
        mled = mled[0](**mled[1])
    except KeyError:
        raise ValueError(f"disambiguator must be one of {list(disambiguators.keys())}")


    tags_list = openJson("scripts/tags_list.json")

    folder = Path("data/text")
    output = Path("output")

    # taggers = {tag: DefaultTagger(mled, tag) for tag in tags_list}

    for path in tqdm(list(folder.glob("*.txt"))):
        new_path = output / path.with_suffix(".xml").name
        new_path.parent.mkdir(parents=True, exist_ok=True)

        if new_path.exists():
            print(f"{new_path} already exists, skipping")
            continue

        with path.open('r', encoding='utf-8') as f:
            file = f.read()

        tokens = simple_word_tokenize(file)  # split_digits

        disambig = mled.disambiguate(tokens)

        liste = [
            {"word": tok,
             **{k: d.analyses[0].analysis[k] for k in tags_list if d.analyses and k in d.analyses[0].analysis}}
            for i, (tok, d) in enumerate(zip(tokens, disambig))
        ]

        with new_path.open('w') as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\n')
            f.write('<root>\n')
            with StringIO() as s:
                for jointure in liste:
                    s.write(f'<w ')
                    s.write(' '.join(
                        f'{k}="{quoteattr(v)}"' if v is not None else f'{k}="{None}"' for k, v in jointure.items() if
                        k != "word"))
                    s.write(f'>{escape(jointure["word"])}</w>\n')
                f.write(s.getvalue())
            f.write('</root>\n')
