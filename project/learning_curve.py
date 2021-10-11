'''
This code does all the work required for the learning curve experiment.
The learning curve experiment works by taking one of the cross-validation training sets
in this case, it is Akkad_1-2-3-4.conllu
and splits it into 5 sets increasing exponentially (the biggest set is the entire file, 
and the smaller set is half of that, and so on...)
It also creates 5 other sets by concatenating PATB to each of previous 5 sets
then it trains models using these different sets
and parses the file Akkad_part_5.conllu using these models
then it runs malteval on the the parsed files to get the score
then it processes the raw score into a readable output

There are five main function here:
1. split_train, this one splits the training file into 5 different sets
2. train: runs maltparser in training mode to create the models
3. parse: runs maltparser using the different models to parse the 5th file
4. score: runs malteval to get the scores of each parsed file
5. score_process: processes the raw scores and stores them in ./scores/processed/lc
'''

import run_maltparser
import sys, os

current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_path + "/tools/")
import methods
from pprint import pprint

training_file = "./data/Akkad_only/Akkad_1-2-3-4.conllu"
test_file = "./data/Akkad_parts/Akkad_part_5.conllu"
number_of_sets = 5

data_path = "./data/learning_curve"
models_path = "./models/learning_curve"
parsed_path = "./parsed/learning_curve"

def split_train(file, n):
    count = methods.sentence_count_conllu(file)
    count_original = count  # variable to keep the original amount because count will change later
    
    with open(file, "r") as f:
        data = f.readlines()
    
    # initialize a list with all zeros, this set will be filled in the loop below
    # such that the number of sentences in set i equals the sum of sizes[:i+1]
    # for example, if sizes = [1,1,2,4,8], then the first set will contain 1 element,
    # the second will contain 1+1=2, the third will contain 1+1+2=4, and so on
    sizes = [0]*n
    # this variable stores how many sentences we accounted for, in case there are sentences 
    # unaccounted for, due to rounding errors, this will make sure we include them
    total = 0 
    
    # n is the number of sets
    for i in range(n):
        if i != n-1:
            sizes[n-i-1] = int(count - (count / 2))
            count = int(count / 2)
        else:
            sizes[0] = sizes[1]
        total += sizes[n-i-1]
    sizes[n-1] += count_original - total
    
    #print(original_count, sizes)
    
    # this set contains n strings, each one will contian a number of sentences, 
    # corresponding to the sizes list above
    sets = [''] * n
    
    #divide the sentences into groups based on the sizes list above
    sentence_id = 0
    set_id = 0
    for line in data:
        sets[set_id] += line
        if line == "\n":    # if you find an empty line, count one sentence
            sentence_id += 1
        
        # if you reach the limit of one size, start filling the next group, and reset the sentence counter
        if sentence_id == sizes[set_id]:    
            set_id += 1
            sentence_id = 0
    
    output_path = data_path
    methods.mkdir(output_path)
    
    # write the sets of sentences into the files
    # the first file will get the sentences in set[0]
    # the second file will get the sentences in set[0] and set[1], and so on...
    for i in range(n):
        with open(f"{output_path}/Akkad_set_{i+1}.conllu", "w") as f:
            for j in range(i+1):
                f.write(sets[j])
    
    # read the PATB training set      
    with open("./data/PATB/catib.train.conllu", "r") as f:
        PATB = "".join(f.readlines())
    
    # create another 5 sets with the PATB training sets concatinated to them
    for i in range(n):
        with open(f"{output_path}/PATB+Akkad_set_{i+1}.conllu", "w") as f:
            f.write(PATB)
            for j in range(i+1):
                f.write(sets[j])

# this function is straight forward
# it just prepares the arguments for maltparser and runs it
def train(n):
    
    config = methods.json_load('config.json')
    parser_file = config['parsers'][0]["path"] + config['parsers'][0]["file"]
    
    methods.mkdir("./models/learning_curve")
    working_space = models_path
    
    for i in range(n):
        model1 = f"model_Akkad_set_{i+1}"
        model2 = f"model_PATB+Akkad_set_{i+1}"
        
        input_path1 = f"./data/learning_curve/Akkad_set_{i+1}.conllu"
        input_path2 = f"./data/learning_curve/PATB+Akkad_set_{i+1}.conllu"
        
        run_maltparser.learn(parser_file, model1, working_space, input_path1)
        run_maltparser.learn(parser_file, model2, working_space, input_path2)

# similar to the previous function, this one prepares arguments for maltparser
# and parses the file Akkad_part_5.conllu using the models created in the previous parts
def parse(n, test_file):
    
    config = methods.json_load('config.json')
    parser_file = config['parsers'][0]["path"] + config['parsers'][0]["file"]
    
    working_space = "./models/learning_curve"
    
    output_path = parsed_path
    
    input_file = test_file
    
    methods.mkdir(output_path)
    
    for i in range(n):
        model1 = f"model_Akkad_set_{i+1}"
        model2 = f"model_PATB+Akkad_set_{i+1}"
        
        output_file1 = f"{output_path}/parsed_Akkad_set_{i+1}.conllu"
        output_file2 = f"{output_path}/parsed_PATB+Akkad_set_{i+1}.conllu"
        
        run_maltparser.parse(parser_file, model1, working_space, input_file, output_file1)
        run_maltparser.parse(parser_file, model2, working_space, input_file, output_file2)

# this function prepares the input for the malteval to get the scores of each parsed file
def score(n, test_file):
    
    config = methods.json_load('config.json')
    eval_file = config['evaluators'][0]["path"] + config['evaluators'][0]["file"]

    gold = [test_file]
    parsed = []
    
    for i in range(n):
        parsed.append(f"{parsed_path}/parsed_Akkad_set_{i+1}.conllu")
    for i in range(n):
        parsed.append(f"{parsed_path}/parsed_PATB+Akkad_set_{i+1}.conllu")
    
    methods.mkdir("./scores/raw/lc/")
    output_file = "./scores/raw/lc/score_learning_curve.txt"
    
    run_maltparser.eval(eval_file, gold, parsed, output_file)

def score_process():
    in_path = current_path + "/../scores/raw/lc/"
    out_path = current_path + "/../scores/processed/lc/"
    
    in_file = in_path + "score_learning_curve.txt"
    
    output = ""
    
    with open(in_file, "r") as f:
        lines = f.readlines()
    
    for i in range(10):
        parsed_file = lines[3 + 14 * i].strip().split("/")[-1] 
        
        output += "Akkad part 5" + "\t"
        
        output += parsed_file[7:] + "\t"
        
        output += lines[11 + 14 * i] + "\n"
    
    methods.mkdir(out_path)
    with open(out_path + "score_learning_curve.txt", "w") as f:
        f.write("Parsed file \ttraining set \tLabel \tUAS \tLAS \n")    # output header
        f.write(output)

split_b = True
train_b = True
parse_b = True
score_b = True
score_process_b = True

if split_b:
    split_train(training_file, number_of_sets)
if train_b:
    train(number_of_sets)
if parse_b:
    parse(number_of_sets, test_file)
if score_b:
    score(number_of_sets, test_file)
if score_process_b:
    score_process()