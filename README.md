# Disclaimer

This project was created during the "CERES Hackathon" event. 

# ArabicToTXM

The goal was to create a script that can convert an arabic corpus (.docx or .txt format) to a [TXM](https://txm.gitpages.huma-num.fr/textometrie/) compatible file  (.xml format). We use the work presented in [Camelira: An Arabic Multi-Dialect Morphological Disambiguator](https://aclanthology.org/2022.emnlp-demos.32/)(Ossama Obeid, Go Inoue, Nizar Habash, 2022) to apply multiple POS tags for each word of the corpus. 

# Installation

To install ArabicToTXM, you must have  **Python 3.x** and  **pip** installed. Clone this repository on your computer. Open your terminal and go to the ArabicToTXM folder (where **main.py** is). Once in the indicated folder, use this command :

```
pip install -r requirements.txt
```

# How to use

The program contains two command lines. The first one retrieves the contents of word files (.docx) and places them in text files (.txt), one for each word document to be processed. The command is as follows:

```
python main.py --docxToText
```

The word files must be placed in the **data/doc/**. The text files resulting from this command are stored in **data/text/**.

The second command line will tokenize each text file and apply POS tags for each token. The result is a xml file containing one word per line with its POS tags. The command is as follows : 

```
python main.py --POStag
```

The applied POS tags list can be found in  **scripts/tags_list.json**. For more informations about the tags you can add to the list, please refer to [Camelira's online documentation](https://camel-tools.readthedocs.io/en/latest/api/tagger/default.html).