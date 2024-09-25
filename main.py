
import time
import argparse
from src.POStag import *
from src.sentenceSplit import *

def proceed(args):

    start = time.time()

    if args.tag:
        print("Applying POS tags ...")
        POStag(args.model)

    if args.sentence:
        print("splitting the text in sentences ...")
        sentenceSplit(format=args.file)

    end = time.time()
    print(f"executed in {round(end - start,2)}")


if __name__ == "__main__":
	
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--tag", action="store_true", help="Apply POS tags to every .txt files.")
    parser.add_argument("-m", "--model", type=str, help="Choose a model to apply POS tags" 
                        "\n mled_msa, mled_egy, bert_msa, bert_egy, bert_glf" 
                        "\n default: mled_msa"
                        )
    
    parser.add_argument("-s","--sentence",action="store_true", help="Convert .txt files to sentences in .csv files.")
    parser.add_argument("-f", "--file", type=str, help="Choose a file format to save your sentences"
                        "\n csv, json"
                        "\n default: csv"
                        )

    args = parser.parse_args()
    proceed(args)
