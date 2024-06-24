from pathlib import Path

import pandas as pd
from tqdm.auto import tqdm

input = Path("/home/marceau/PycharmProjects/ArabicToTXM/output/CorpusCSV/")
output = Path("/home/marceau/PycharmProjects/ArabicToTXM/output/CorpusCSV_sents/")
output.mkdir(exist_ok=True, parents=True)

for csv in tqdm(list(input.glob("*.csv"))):
    df = pd.read_csv(csv)

    sents = []
    sent = []
    pos = []
    for i, row in df.iterrows():
        sent.append(row.word.strip())
        pos.append(row.pos)
        if row.word.strip() in "!؟.!?" and sent and sent[-1] not in "!؟.!?":
            sents.append((" ".join(sent), " ".join(pos)))
            sent = []
            pos = []

    if sent:
        sents.append((" ".join(sent), " ".join(pos)))

    df = pd.DataFrame(sents, columns=["sentence", "tags"])
    df.to_csv(output / csv.with_suffix(".csv").name, index=False)
