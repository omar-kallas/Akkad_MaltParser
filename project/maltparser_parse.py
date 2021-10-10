'''
This code extracts the information about the models and input files from the config file
and runs maltparser to parse each file with the specified model.
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
    
    # this loop goes over the parsing sets, gets the model name and the input file name
    # it creates a path for the output if it hasn't been already created
    # then it calls run_maltparser code to run the parser
    for set in config['parse_sets']:
        
        working_space = set['model_path']   #this is the path where the model was stored
        
        for (i, pair) in enumerate(set['model_input_pairs']):
            
            model = pair[0]
            input_path = f"{set['data_path']}{pair[1]}"
            output_path = f"{set['output_path']}{set['name']}/{i+1}_parsed_{set['name']}_{pair[1]}"
            
            methods.mkdir(f"{set['output_path']}{set['name']}")
            
            run_maltparser.parse(parser_file, model, working_space, input_path, output_path)