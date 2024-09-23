import argparse

from scripts.POStag import POStag
from scripts.docxToText import *

parser = argparse.ArgumentParser()


parser.add_argument("-t", "--docxToText", action="store_true", help="Convert .docx files to .txt")
parser.add_argument("-p", "--POStag", action="store_true", help="Apply POS tags to every .txt files")
parser.add_argument(
    "-m", "--model", type=str, help="Choose a model to apply POS tags"
    "\n mled_msa, mled_egy, bert_msa, bert_egy, bert_glf"
    "\n default: mled_msa"
)

def proceed(docx, pos, model):
    if docx:
        print("converting .docx to .txt ...")
        docToDocx()
        docxToText()
        print("done !")

    if pos:
        print("Applying POS tags ...")
        POStag(model)
        print("done !")


if __name__ == "__main__":
    args = parser.parse_args()
    proceed(
        args.docxToText,
        args.POStag,
        args.model
    )
