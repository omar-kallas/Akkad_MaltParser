'''
This code runs malteval on the 9 parsing sets specified in the config file. 
It stores the output under the ./scores/raw directory.
'''

import sys, os

# the following command is to import files from the tools directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/tools')
import methods
import run_maltparser

config = methods.json_load("config.json")

# this loop goes through the evaluators (now there is only matleval)
for eval in config['evaluators']:
    
    eval_file = f"{eval['path']}{eval['file']}"
    
    # this loop goes through the parsing sets, to  collect the names of the golden and parsed files 
    # and runs the malteval code on them to evaluate parsing
    for set in config['parse_sets']:
        gold = []
        parsed = []
        
        # add input files to the gold list and parsed files to the parsed list
        for (i, pair) in enumerate(set['model_input_pairs']):
            if f"{set['data_path']}{pair[1]}" not in gold:
                gold.append(f"{set['data_path']}{pair[1]}")
            parsed.append(f"{set['output_path']}{set['name']}/{i+1}_parsed_{set['name']}_{pair[1]}")
        
        methods.mkdir("./scores/raw")
        output_file = f"./scores/raw/score_{set['name']}.txt"
        
        print("evaluating the following files:\n{:s}...".format('\n'.join(parsed)))
        run_maltparser.eval(eval_file, gold, parsed, output_file)