from pathlib import Path

import pandas as pd
from tqdm.auto import tqdm

input = Path("/home/marceau/PycharmProjects/ArabicToTXM/output/CorpusCSV_sents")
output = Path("/home/marceau/PycharmProjects/ArabicToTXM/output/CorpusCSV_sents_oneletter/")
output.mkdir(exist_ok=True, parents=True)

corresp = {
    "PART": "P",
    "NOUN": "N",
    "PUNC": "Z",
    "VERB": "V",
    "DIGIT": "D",
    "NOUN_OR_PART": "N",
}


def transform(liste):
    return " ".join([corresp.get(tag, "X") for tag in liste.split()])


for csv in tqdm(list(input.glob("*.csv"))):
    df = pd.read_csv(csv).fillna("")

    df["tags"] = df["tags"].apply(transform)

    df.to_csv(output / csv.name, index=False)
    tqdm.write(f"{csv} converted to {output / csv.name}")
