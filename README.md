# ArabicTagger

This project was created during the **[CERES](https://ceres.sorbonne-universite.fr/) Hackathon** event with the participation of [Rimane Karam](https://www.orient-mediterranee.com/member/7215/) and [Marceau Hernandez](https://ceres.sorbonne-universite.fr/1c808d15-d54d-47cd-b831-7f5550f13483). The goal was to apply POS tags to an Arabic corpus. We use the work presented in [Camelira: An Arabic Multi-Dialect Morphological Disambiguator](https://aclanthology.org/2022.emnlp-demos.32/) (Ossama Obeid, Go Inoue, Nizar Habash, 2022) to apply multiple tags for each word of the corpus. 

## Installation

To install ArabicTagger, you must have  **Python 3.x** and  **pip** installed. You must first install some dependencies for Camel-Tools, which is the package used to apply multiple POS tags. Refer to [Camel-Tools](https://github.com/CAMeL-Lab/camel_tools) official documentation for more informations. Here is the command to install those dependencies (for Ubuntu):

```
sudo apt-get install cmake libboost-all-dev
camel_data -i light
```

Once all the dependencies installed, clone this repository on your computer. Open your terminal and go to the ArabicTagger folder (where **main.py** is). Once in the indicated folder, install required packages with the following command:

```
pip install -r requirements.txt
```

## How to use

This script takes raw text files (.txt) as input. It will tokenize each file and apply POS tags for each token in them. The result is a **.xml** file in **output/tagged** containing one word per line with its POS tags. This file is compatible with [TXM](https://txm.gitpages.huma-num.fr/textometrie/). The command is as follows: 

```
python main.py --tag --model [MODEL_NAME]
```

The applied POS tags list can be found in  **src/tags_list.json**. For more informations about the tags you can add to the list, please refer to [Camelira's online documentation](https://camel-tools.readthedocs.io/en/latest/api/tagger/default.html) and [Camelira's tag list](https://camel-tools.readthedocs.io/en/v1.2.0/reference/camel_morphology_features.html). If you want to segment your corpus in sentences, you can use the following command:

```
python main.py --sentence
```

It will create a **.csv** file in **output/sentence** containing three columns: **sentence** (raw sentence), **tags** (POS tagsof each word in this sentence) and **lem** (canonical form of each word in this sentence). You can also generate **.json** files instead of csv by specifying the desired output:

```
python main.py --sentence -f json
```
