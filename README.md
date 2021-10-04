# Akkad_MaltParser

This project uses MaltParser to train models using data from Al-Akkad novel "Sara", as well as the PATB, and different combinations of the two datasets. It then uses these models to parse the some of parts of the Akkad data, and uses malteval to get some statistical information about the accuracyc of the parser using differnet measures.

# Data directory
the directory ./data contains the data that is used in the training and the modeling process. It has two conllu files that contain the parsed sentences of the Akkad novel, one of them with text (i.e with the full sentence preceeding its tokenization), and the other is without text. The one without text is the one used to split the data.

The directory also has the following diretories that contains the Akkad data and the PATB data split and merged in different ways:
- Akkad_parts: This contains the result of splitting the file AlAkkad_full_no_text.conllu into 5 parts with the same number of sentences in each.
- Akkad_only: this contains the sets that are used in training for the cross-validation experiments. For example, file Akkad_1-2-3-4.conllu contains the parts 1, 2, 3, 4 of Akkad data concatinated into one file (taken from Akkad_parts directory).
- PATB: this contains three files from the PATB, one used for training (train), onr for develeopment (dev), and one for testing (test).
- PATB_train_and_Akkad: this contains 5 files, each of them is the concatination of the PATB training set, with one of the files in Akkas_only (the ones used for cross-validation).
- learning curve: this file contains the files used to create a learning curve using the learning_curve.py code which is explained in a later part of this document.