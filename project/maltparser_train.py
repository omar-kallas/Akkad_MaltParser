'''
This code extracts the information about the training sets and models from the config file
and runs maltparser on each file that is used for training
'''

import sys, os

# the following command is to import files from the tools directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/tools')
import methods
import run_maltparser

config = methods.json_load("config.json")

# a for loop that loops over parser, but curerntly there is only one
for parser in config['parsers']:
    
    parser_file = parser['path'] + parser ['file']
    
    # this loop goes over each training set and goes over the files in the set
    # it collects information about the names and pathes of the files
    # and runs maltparser to train models with the files
    for set in config['train_sets']:
        for file in set['files']:
            model = "model_" + file
            working_space = f"{set['output_path']}{set['name']}"    #this is the path where the model will be stored
            input_path = set['data_path'] + file
            
            # create output folder if it is not there
            methods.mkdir(f"{set['output_path']}{set['name']}")
            
            run_maltparser.learn(parser_file, model, working_space, input_path)
            