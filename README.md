# Akkad_MaltParser

This project uses MaltParser to train models using data from Al-Akkad novel "Sara", as well as the PATB, and different combinations of the two datasets. It then uses these models to parse the some of parts of the Akkad data, and uses malteval to get some statistical information about the accuracyc of the parser using differnet measures.

# ./data directory
the directory ./data contains the data that is used in the training and the modeling process. It has two conllu files that contain the parsed sentences of the Akkad novel, one of them with text (i.e with the full sentence preceeding its tokenization), and the other is without text. The one without text is the one used to split the data.

The directory also has the following diretories that contains the Akkad data and the PATB data split and merged in different ways:
- **Akkad_parts**: This contains the result of splitting the file AlAkkad_full_no_text.conllu into 5 parts with the same number of sentences in each.
- **Akkad_only**: this contains the sets that are used in training for the cross-validation experiments. For example, file Akkad_1-2-3-4.conllu contains the parts 1, 2, 3, 4 of Akkad data concatinated into one file (taken from Akkad_parts directory).
- **PATB**: this contains three files from the PATB, one used for training (train), onr for develeopment (dev), and one for testing (test).
- **PATB_train_and_Akkad**: this contains 5 files, each of them is the concatination of the PATB training set, with one of the files in Akkas_only (the ones used for cross-validation).
- **learning curve**: this file contains the files used to create a learning curve using the learning_curve.py code which is explained in a later part of this document.

# config.json
the config.json file is a file that includes the important information, and is used in many parts of the code to identify the files that should be used in training and parsing:
- **parser info**: file name and data_path
- **evaluator info**: file name and data_path

- **training sets**: the sets of data that will be used to traing the parser. It includes the path of the data files, a list of the names of the files, and the output folder where the model will be stored.
There are currently 3 training sets:
1. **PATB**: this one uses the PATB training set stored in catib.train.conllu
2. **Akkad_only**: this one uses 5 files, each one contains 4 out of 5 folds of the Akkad data. Example: Akkad_1-2-3-4.conllu which contains the 1st, 2nd, 3rd, and 4th folds.
3. **PATB_train_and_Akkad**: this one uses 5 files, each one contains the PATB training set plus a file from the Akkad_only set.

- **parsing sets**: the sets of data that will be parsed. It includes the paths of the data files and trained models, a list of the pairs of the models and input files that will be parsed, and the output folder where the parsed data will be stored. 
There are 9 parsing sets in total, coming frmo 3 models created by the 3 training sets, and 3 different sets that we want to parse. The 3 sets we want to parse are:
1. **Akkad**: This set contains 5 files we want to parse separately, which are the 5 folds of the Akkad data. When parsed using the PATB training set, all files are parsed with the same model. However, when parsed using the Akkad_only or PATB_train_and_Akkad set, each file will be parsed using the model that didn't use the file in the training. For example: when parsing the file Akkad_part_1.conllu using Akkad_only training set, we use the model model_Akkad_2-3-4-5.conllu.mco. This is configured in the model_input_pairs list.
2. **PATB_dev** this set has the file catib.dev.conllu which contains the PATB develeopment set. This is parsed using all the different models in the training sets.
2. **PATB_test** this set has the file catib.test.conllu which contains the PATB testing set. This is parsed using all the different models in the training sets.

# maltparser and malteval
This project uses the maltparser 1.9.2 and malteval software obtained from http://www.maltparser.org/download.html and http://www.maltparser.org/malteval.html

In order for the code to work, install maltparser and malteval and update their directories in the config.json file, under the parsers['path'] and evaluators['path']. You should enter the directories of the jar files.

# ./parsed directory
This directory contains 10 sub-directories. 9 of them correspond to the 9 parsing sets specified in the config file, and 1 corresponding to the learning curve experiment. Each sub-directory contains the parsed results of the parsing sets. These files are used to calculate the score of each parsing set.
The name of each of the 9 main sub directories specifies the parsed data and the training data. For example, the directory "Akkad_on_Akkad_only" contins the results of parsing Akkad parts using other parts of Akkad.

# ./project directory:
This directory contains the python code used in this project. There are five files directly under this directory which run the main experiments on the data. These are:
- **run_maltparser.py**: This file runs maltparser and malteval by running the terminal's call. It has differenet methods: one for training, one for parsing, and one for evaluating.
- **maltparser_train.py**: This code extracts the information about the training sets and models from the config file and runs maltparser on each file that is used for training. It stores the output under the ./models directory.
- **maltparser_parse.py**: This code extracts the information about the models and input files from the config file and runs maltparser to parse each file with the specified model. It stores the results under the ./parsed directory.
- **maltparser_score.py**: This code runs malteval on the 9 parsing sets specified in the config file. It stores the output under the ./scores/raw directory.
- **learning_curve.py**: This code does all the work required for the learning curve experiment.
The learning curve experiment works by taking one of the cross-validation training sets
in this case, it is Akkad_1-2-3-4.conllu, and splits it into 5 sets increasing exponentially (the biggest set is the entire file, and the smaller set is half of that, and so on...)
It also creates 5 other sets by concatenating PATB to each of previous 5 sets then it trains models using these different sets, and parses the file Akkad_part_5.conllu using these models.
Then it runs malteval on the the parsed files to get the score.
Then it processes the raw score into a readable output, stores it in ./scores/processed/lc

Other files are stored in the **/tools** directory which are used to produce more statistics. These files are:
- methods.py: This file includes simple methods that are used in different parts of the code
- process_score.py: This code processes the raw output of malteval for the general scores on the main experiments. The input are the files generated by malteval including the scores of parsing stored in ../../scores/raw/main. The output is a single files contains all the scores combined into one file stored in ../../scores/processed
- out_of_vocab.py: This function gets the word counts (unique and total) for all the pairs of files in the parsing sets of the config files. It also counts the number of out-of-vocab words (unique and total) of these pairs (out-of-vocab words are the ones present in the parsed file but not in the training file). It writes the output to ./scores/out_of_vocab.txt