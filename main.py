from scripts.docToDocx import docToDocx
from scripts.docxToText import docxToText
from scripts.POStag import POStag

def proceed(args):

  if args.docToDocx:
    print("converting .doc to .docx ...")
    docToDocx()
    print("done !")

  if args.docxToText:
    print("converting .docx to .txt ...")
    docxToText()
    print("done !")

  if args.POStag:
    print("Applying POS tags ...")
    POStag()
    print("done !")

if __name__ == "__main__":
	
  import argparse
  parser = argparse.ArgumentParser()

  parser.add_argument("-x", "--docToDocx", action="store_true", help="Convert .doc files to .docx")
  parser.add_argument("-t", "--docxToText", action="store_true", help="Convert .docx files to .txt")
  parser.add_argument("-p","--POStag",action="store_true", help="Apply POS tags to every .txt files")

  args = parser.parse_args()
  proceed(args)