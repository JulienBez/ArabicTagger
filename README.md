# Disclaimer

This project was created during the **[CERES](https://ceres.sorbonne-universite.fr/) Hackathon** event with the participation of [Rimane Karam](https://www.orient-mediterranee.com/member/7215/).

# ArabicToTXM

The goal was to create a script that can convert an arabic corpus (.doc, .docx or .txt format) to a [TXM](https://txm.gitpages.huma-num.fr/textometrie/) compatible file  (.xml format). We use the work presented in [Camelira: An Arabic Multi-Dialect Morphological Disambiguator](https://aclanthology.org/2022.emnlp-demos.32/) (Ossama Obeid, Go Inoue, Nizar Habash, 2022) to apply multiple POS tags for each word of the corpus. 

# Installation

To install ArabicToTXM, you must have  **Python 3.x** and  **pip** installed. You must first install some dependencies for Camel-Tools, which is the package used to apply multiple POS tags. Refer to [Camel-Tools](https://github.com/CAMeL-Lab/camel_tools) official documentation for more informations. Here is the command to install those dependencies (for Ubuntu):

```
sudo apt-get install cmake libboost-all-dev
```

In case you want to convert .doc files, you must have LibreOffice installed:

```
sudo apt-get install libreoffice
```

 Once all the dependencies installed, clone this repository on your computer. Open your terminal and go to the ArabicToTXM folder (where **main.py** is). Once in the indicated folder, install required packages with the following command:

```
pip install -r requirements.txt
```

Next execute this command to install Camel data:

```
camel_data -i light
```

# How to use

The program contains two command lines. The first one retrieves the contents of word files (.doc and .docx) and places them in text files (.txt), one for each word document to be processed. The command is as follows:

```
python main.py --docxToText
```

The word files must be placed in the **data/doc/**. The text files resulting from this command are stored in **data/text/**. If your corpus is already in text format, just place the text files in **data/text/** and ignore the first command.

The second command line will tokenize each text file and apply POS tags for each token. The result is a xml file containing one word per line with its POS tags. The command is as follows: 

```
python main.py --POStag
```

The applied POS tags list can be found in  **scripts/tags_list.json**. For more informations about the tags you can add to the list, please refer to [Camelira's online documentation](https://camel-tools.readthedocs.io/en/latest/api/tagger/default.html) and [Camelira's tag list](https://camel-tools.readthedocs.io/en/v1.2.0/reference/camel_morphology_features.html). 
