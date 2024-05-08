from pathlib import Path
from typing import List, Set, Dict, Optional, Iterable

from bs4 import BeautifulSoup

from webanno_tsv import Document, Annotation
from dataclasses import replace


class WebAnnoTransformer:
    points: Set[str] = {"!", "?", "."}

    def __init__(
            self,
            *args,
            fields_dict: Optional[Dict[str, Iterable[str]]] = None
    ):
        if fields_dict is not None:
            assert isinstance(fields_dict, dict), f"The kw argument `fields_dict` should be a dict (or None) !"

            self.layer_def = []
            for layer, fields in fields_dict.items():
                assert isinstance(layer, str)
                assert isinstance(fields, Iterable)
                fields = list(fields) if not isinstance(fields, list) else fields

                self.layer_defs.append((layer, fields))

            self.layers = set(fields_dict)
        else:
            self.layer_defs = [("KARAMLayer", ["pos"]), ]
            self.layers = {"KARAMLayer", }

    def transform(self, soup: BeautifulSoup | str):
        if isinstance(soup, str):
            soup = BeautifulSoup(soup, "xml")
        elif not isinstance(soup, BeautifulSoup):
            raise ValueError(f"soup should be a `bs4.BeautifulSoup` or a `str`, not a {type(soup)}")

        w_s = soup.find_all("w")[:100]

        # print(*w_s[50:100], sep="\n")

        points_index = [i for i, w in enumerate(w_s) if w.text.casefold().strip() in self.points]

        sentences = [
            [w.text for w in w_s[:points_index[i]]] if i == 0
            else [w.text for w in w_s[points_index[i-1]:points_index[i]]] if i != len(points_index)
            else [w.text for w in w_s[points_index[i]:]]
            for i in range(len(points_index) + 1)
        ]

        doc = Document.from_token_lists(sentences)

        annotations = []

        for i, w in enumerate(w_s):
            for attr_field, attr_value in w.attrs.items():
                for layer, fields in self.layer_defs:
                    if attr_field in fields:
                        break
                else:
                    continue

                annotations.append(
                    Annotation(
                        tokens=doc.tokens[i:i],
                        layer=layer,
                        field=attr_field,
                        label=attr_value,
                    )
                )

        doc = replace(doc, annotations=annotations, layer_defs=self.layer_defs)
        return doc.tsv()



if __name__ == "__main__":
    file = Path("/home/marceau/PycharmProjects/ArabicToTXM/output/CorpusRimane/01.xml")

    wat = WebAnnoTransformer()

    wat_t = wat.transform(file.open().read())

    print(wat_t)
