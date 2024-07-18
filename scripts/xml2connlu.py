from pathlib import Path

from bs4 import BeautifulSoup
from tqdm.auto import tqdm

from io import StringIO



file = Path("/home/marceau/PycharmProjects/ArabicToTXM/output/CorpusKARAMED/")
output = Path("/home/marceau/PycharmProjects/ArabicToTXM/output/CorpusConllU/")
output.mkdir(exist_ok=True, parents=True)


for xml in tqdm(list(file.glob("*.xml"))):
    with xml.open("r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "xml")

    w_s = soup.find_all("w")

    data = [
        (i, w.text, w["pos"])
        for i, w in enumerate(w_s)
    ]

    sents = []
    sent = []
    prev = None
    for w in w_s:
        if len(sent) > 1 and w.text.strip() not in "!؟.!?" and prev in "!؟.!?":
            sents.append(sent)
            sent = []
        sent.append((w.text, w["pos"], w["atbtok"]))
        prev = w.text.strip()
    if sent:
        sents.append(sent)


    connlu = StringIO()
    connlu.write("# global.columns = ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC\n")
    for i, sent in enumerate(sents, 1):
        connlu.write(f"# sent_id = {i}\n# text = {' '.join(w for w, _, _ in sent)}\n")
        for j, (w, pos, atbtok) in enumerate(sent, 1):
            connlu.write(f"{j}\t{w}\t{atbtok}\t{pos}\t_\t_\t_\t_\t_\t_\n")
        connlu.write("\n")

    connlu.seek(0)

    with open(output / f"{xml.stem}.conllu", "w", encoding="utf-8") as f:
        f.write(connlu.getvalue())




