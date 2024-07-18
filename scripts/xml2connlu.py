from pathlib import Path

from bs4 import BeautifulSoup
from bs4.element import Tag
from tqdm.auto import tqdm

from io import StringIO



file = Path("/home/marceau/PycharmProjects/ArabicToTXM/output/CorpusRimane/")
output = Path("/home/marceau/PycharmProjects/ArabicToTXM/output/CorpusConllU/CamelFusion/")
output.mkdir(exist_ok=True, parents=True)


tagset_file = Path("/home/marceau/PycharmProjects/ArabicToTXM/tagset.txt")

with tagset_file.open("r") as f:
    tagset = f.readlines()

tagset = [[e[0].strip(), e[1].strip()] for e in [e.split("=", 1) for e in tagset]]
tagset = {e[0]: e[1] for e in tagset}

def replace(tag):
    return tagset.get(tag.upper(), tagset.get(tag, tag.upper()))

def from_w_to_xpos(w: Tag) -> str:
    # part1 = ''.join((w["asp"], w["per"], w["gen"], w["num"]))
    # part2 = ''.join((w["stt"], w["cas"], w["vox"], w["mod"]))
    # return f"{w['pos']}{f'.{part1}.{part2}' if part1 or part2 else ''}".upper()
    return f"{w['pos']}{f'.{w['asp']}{w['per']}{w['gen']}{w['num']}.{w['stt']}{w['vox']}' if any(w[k] for k in ["asp", "per", "gen", "num", "stt", "cas", "vox", "mod"]) else ''}".upper()



for xml in tqdm(list(file.glob("*.xml"))):
    with xml.open("r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "xml")

    w_s = soup.find_all("w")

    sents = []
    sent = []
    prev = None
    for w in w_s:
        if len(sent) > 1 and w.text.strip() not in "!؟.!?" and prev in "!؟.!?":
            sents.append(sent)
            sent = []
        sent.append((w.text.strip(), replace(w["pos"]), w["atbtok"], from_w_to_xpos(w)))
        prev = w.text.strip()
    if sent:
        sents.append(sent)


    connlu = StringIO()
    connlu.write("# global.columns = ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC\n\n")
    for i, sent in enumerate(sents, 1):
        connlu.write(f"# sent_id = {i}\n# text = {' '.join(w for w, _, _, _ in sent)}\n")
        for j, (w, pos, atbtok, xpos) in enumerate(sent, 1):
            connlu.write(f"{j}\t{w}\t{atbtok}\t{pos}\t{xpos}\t_\t_\t_\t_\t_\n")
        connlu.write("\n")

    connlu.seek(0)

    with open(output / f"{xml.stem}.conllu", "w", encoding="utf-8") as f:
        f.write(connlu.getvalue())




