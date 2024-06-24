from pathlib import Path

from bs4 import BeautifulSoup
from tqdm.auto import tqdm


file = Path("/home/marceau/PycharmProjects/ArabicToTXM/output/CorpusRimane/")
output = Path("/home/marceau/PycharmProjects/ArabicToTXM/output/CorpusKARAMED/")
output.mkdir(exist_ok=True, parents=True)

tagset_file = Path("/home/marceau/PycharmProjects/ArabicToTXM/tagset.txt")

with tagset_file.open("r") as f:
    tagset = f.readlines()

tagset = [[e[0].strip(), e[1].strip()] for e in [e.split("=", 1) for e in tagset]]
tagset = {e[0]: e[1] for e in tagset}

def replace(tag):
    return tagset.get(tag, tag)

for xml in tqdm(list(file.glob("*.xml"))):
    with xml.open("r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "xml")

    w_s = soup.find_all("w")

    for w in w_s:
        w["pos"] = replace(w["pos"])

    with (output / xml.name).open("w") as f:
        f.write(str(soup))
