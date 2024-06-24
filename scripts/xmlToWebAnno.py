from pathlib import Path
from typing import List, Set, Dict, Optional, Iterable
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from bs4 import BeautifulSoup
from tqdm.auto import tqdm

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
            self.layer_defs = [("webanno.custom.KARAMLayer", ["pos"]), ]
            self.layers = {"webanno.custom.KARAMLayer", }

    def transform(self, soup: BeautifulSoup | str):
        if isinstance(soup, str):
            soup = BeautifulSoup(soup, "xml")
        elif not isinstance(soup, BeautifulSoup):
            raise ValueError(f"soup should be a `bs4.BeautifulSoup` or a `str`, not a {type(soup)}")

        w_s = soup.find_all("w")

        # print(*w_s[50:100], sep="\n")

        points_index = [i for i, w in enumerate(w_s) if w.text.casefold().strip() in self.points]

        sentences = [
            [w.text.strip() for w in w_s[:points_index[i]]] if i == 0
            else [w.text.strip() for w in w_s[points_index[i-1]:points_index[i]]] if i != len(points_index)
            else [w.text.strip() for w in w_s[points_index[i-1]:]]
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
                # print(i)
                # print(w.text)
                # print(doc.tokens[i:i+1])
                # print(attr_field)
                # print(attr_value)
                # 1/0
                annotations.append(
                    Annotation(
                        tokens=doc.tokens[i:i+1],
                        layer=layer,
                        field=attr_field,
                        label=attr_value,
                    )
                )

        doc = replace(doc, annotations=annotations, layer_defs=self.layer_defs)
        return doc.tsv()

    def transform_file(self, file: Path | str):
        if isinstance(file, str):
            file = Path(file)
        elif not isinstance(file, Path):
            raise ValueError(f"file should be a `pathlib.Path` or a `str`, not a {type(file)}")

        with file.open(mode="r", encoding="utf-8") as f:
            return self.transform(f.read())

    def transform_folder(self, folder: Path | str):
        if isinstance(folder, str):
            folder = Path(folder)
        elif not isinstance(folder, Path):
            raise ValueError(f"folder should be a `pathlib.Path` or a `str`, not a {type(folder)}")

        # for file in folder.glob("*.xml"):
        #     yield self.transform_file(file)
        with ProcessPoolExecutor() as executor:
            return executor.map(self.transform_file, folder.glob("*.xml"))

    def transform_folder_to_tsv(self, folder: Path | str, output_folder: Path | str):
        if isinstance(folder, str):
            folder = Path(folder)
        elif not isinstance(folder, Path):
            raise ValueError(f"folder should be a `pathlib.Path` or a `str`, not a {type(folder)}")

        if isinstance(output_folder, str):
            output_folder = Path(output_folder)
        elif not isinstance(output_folder, Path):
            raise ValueError(f"output_folder should be a `pathlib.Path` or a `str`, not a {type(output_folder)}")

        output_folder.mkdir(exist_ok=True, parents=True)

        with ProcessPoolExecutor() as executor:
            xmls = list(folder.glob("*.xml"))
            tsvs = tqdm(executor.map(self.transform_file, xmls), total=len(xmls))
            for tsv, xml in zip(tsvs, xmls):
                with (output_folder / xml.with_suffix(".tsv").name).open("w") as f:
                    f.write(tsv)


if __name__ == "__main__":
    file = Path("/home/marceau/PycharmProjects/ArabicToTXM/output/CorpusKARAMED/")
    output = Path("/home/marceau/PycharmProjects/ArabicToTXM/output/CorpusKARAMED_WA/")
    output.parent.mkdir(exist_ok=True, parents=True)

    wat = WebAnnoTransformer()

    wat.transform_folder_to_tsv(file, output)

