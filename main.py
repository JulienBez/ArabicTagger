import argparse

from scripts.POStag import POStag
from scripts.docxToText import docxToText

parser = argparse.ArgumentParser()

parser.add_argument("-t", "--docxToText", action="store_true", help="Convert .docx files to .txt")
parser.add_argument("-p", "--POStag", action="store_true", help="Apply POS tags to every .txt files")


def proceed(docx, pos):
    if docx:
        print("converting .docx to .txt ...")
        docxToText()
        print("done !")

    if pos:
        print("Applying POS tags ...")
        POStag()
        print("done !")


if __name__ == "__main__":
    args = parser.parse_args()
    proceed(
        args.docxToText,
        args.POStag,
    )
