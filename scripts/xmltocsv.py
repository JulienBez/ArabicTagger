from pathlib import Path

from bs4 import BeautifulSoup
import pandas as pd
from tqdm.auto import tqdm


file = Path("/home/marceau/PycharmProjects/ArabicToTXM/output/CorpusKARAMED/")
output = Path("/home/marceau/PycharmProjects/ArabicToTXM/output/CorpusCSV/")
output.mkdir(exist_ok=True, parents=True)

for xml in tqdm(list(file.glob("*.xml"))):
    with xml.open("r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "xml")

    w_s = soup.find_all("w")

    data = [
        (i, w.text, w["pos"])
        for i, w in enumerate(w_s)
    ]

    # data = []
    # for i, w in enumerate(w_s):
    #     try:
    #         data.append((i, w.text,w["pos"]))
    #     except KeyError:
    #         print(f"Error in {xml} at line {i}, {w = }")
    #         raise

    df = pd.DataFrame(data, columns=["id", "word", "pos"])

    df.to_csv(output / xml.with_suffix(".csv").name, index=False)

    tqdm.write(f"{xml} converted to {output / xml.with_suffix('.csv').name}")

