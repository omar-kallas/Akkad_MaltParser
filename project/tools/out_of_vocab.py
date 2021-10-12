import methods

files_words = {} # dictionary to store the words of files to save time an not look them up later
methods.mkdir("./scores/")
output_file = "./scores/out_of_vocab.txt"
output = ("parsed file \t# of words \t# of unique words "
          "\ttraining set \t# of words \t# of unique words"
          "\t# of out-of-vocab \t# of unique out-of-vocab\n")

# a function that takes a conllu file name as an input
# it returns two lists, the first one contains all the words (tokens) of the file
# the second one contains the unique words of the file
def get_words_uniq(file):
    words_list = []
    with open(file, "r") as f:
        lines = f.readlines()
    
    for line in lines:
        if line != "\n" and line != "":
            line = line.split("\t")
            words_list.append(line[1])
    
    unique = set(words_list)
    u_words_list = (list(unique))
    
    return [words_list, u_words_list]

# a function that calculates the out-of-vocab and unique out-of-vocab and adds them to the output
# file1 is the parsed file, file2 is the one used for the training model
def out_of_voc(file1, file2):   
    global files_words, output
    
    # if the list of words is not found in the dictionary, use the above function to get it
    if not file1 in files_words.keys():
        files_words[file1] = get_words_uniq(file1)
    if not file2 in files_words.keys():
        files_words[file2] = get_words_uniq(file2)
    
    # this part goes through the list of words for the parsed file
    # and checks if it is available in the training file
    # keep in mind: files_words[file1][0] is the number of words in file1
    # files_words[file1][1] is the number of unique words in file1
    count = 0
    in_vocab = []
    out_vocab = []
    for word in files_words[file1][0]:
        if word in out_vocab:
            count += 1
        elif word in in_vocab:
            pass
        elif not word in files_words[file2][1]:
            count += 1
            out_vocab.append(word)
        else:
            in_vocab.append(word)
    
    uniq_count = len(list(set(out_vocab)))
    
    file1_name = file1.split('/')[-1]
    file2_name = file2.split('/')[-1]
    
    output += (f"{file1_name} \t{len(files_words[file1][0])} \t{len(files_words[file1][1])}" 
                f"\t{file2_name} \t{len(files_words[file2][0])} \t{len(files_words[file2][1])}" 
                f"\t{count} \t{uniq_count}\n")

config = methods.json_load("./config.json")

# go through all the parsing sets and run the above function on their parsing-training pairs
for p_set in config['parse_sets']:
    for pair in p_set['model_input_pairs']:
        file1 = p_set['data_path'] + pair[1]
        
        file2_path = p_set['model_path'].replace("models", "data")
        file2_name = pair[0].replace("model_", "")
        file2_name = file2_name.replace(".mco", "")
        file2 = file2_path + "/" + file2_name
        
        print(f"running for files {file1} and {file2}")
        out_of_voc(file1, file2)

#write the output to a file
with open(output_file, "w") as f:
    f.write(output)