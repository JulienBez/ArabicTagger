from pathlib import Path

import pandas as pd
from tqdm.auto import tqdm

input = Path("/home/marceau/PycharmProjects/ArabicToTXM/output/test.csv")
output = Path("/home/marceau/PycharmProjects/ArabicToTXM/output/test_word.csv")

df = pd.read_csv(input)

words = []
pos = []

for i, row in df.iterrows():
    words_tmp = row.sentence.split()
    pos_tmp = row.predicted_tags.split()
    try:
        assert len(words_tmp) == len(pos_tmp)
    except AssertionError:
        print(i)
        print(words_tmp)
        print(pos_tmp)
    words.extend(words_tmp)
    pos.extend(pos_tmp)

df = pd.DataFrame({"word": words, "pos": pos})
df.to_csv(output, index=False)


