from pathlib import Path

from tqdm.auto import tqdm
import pandas as pd

from io import StringIO

def csv2connlu(csv: Path, output: Path):
    assert csv.exists(), f"{csv} does not exist"
    assert csv.is_file(), f"{csv} is not a file"
    if output.exists():
        print(f"Warning: {output} already exists and will be overwritten")
    if not output.parent.exists():
        output.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(csv).fillna("_")

    sents = []
    sent = []
    prev = None
    for i, row in df.iterrows():
        if len(sent) > 1 and row['word'].strip() not in "!؟.!?" and prev in "!؟.!?":
            sents.append(sent)
            sent = []
        sent.append((row['word'].strip(), row["pos_rimane"], row["pos_rimane2"]))
        prev = row['word'].strip()
    if sent:
        sents.append(sent)

    connlu = StringIO()
    connlu.write("# global.columns = ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC\n\n")
    for i, sent in enumerate(sents, 1):
        connlu.write(f"# sent_id = {i}\n# text = {' '.join(w for w, _, _ in sent)}\n")
        for j, (w, pos, xpos) in enumerate(sent, 1):
            connlu.write(f"{j}\t{w}\t_\t{pos}\t{xpos}\t_\t_\t_\t_\t_\n")
        connlu.write("\n")

    connlu.seek(0)

    with open(output, "w", encoding="utf-8") as f:
        f.write(connlu.getvalue())

if __name__ == '__main__':
    csv2connlu(Path("../data/camelschema_vol1.csv"), Path("../output/CorpusConllU/Rimane_ver/01.conllu"))

