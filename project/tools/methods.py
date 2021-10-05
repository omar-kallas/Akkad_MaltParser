'''
This file includes simple methods that are used in different parts of the code

'''

import json, os

# The "load" method loads data from a json file
def json_load(file_name):
    file = open(file_name,)
    data = json.load(file)
    file.close()
    return data

# The "mkdir" method gets a path and creates it if it doesn't exist
def mkdir(dir_path):
    path = ""
    for dir in dir_path.split("/"):
        path += f"{dir}/"
        if not os.path.exists(path):
            os.mkdir(path)

# The "percentage" method takes a ratio and returns it as a percentage
def percentage(ratio):
    return "{:.2f}%".format(ratio*100)

#The "sentence count" methdo counts the number of sentences in a conllu file
def sentence_count_conllu(file):
    
    with open(file, "r") as inFile:
        lines = inFile.readlines()
        
    count = 0
    for line in lines:
        if line == "\n":
            count += 1
    
    return count