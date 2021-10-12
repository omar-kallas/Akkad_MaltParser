import methods

files_words = {}
methods.mkdir("./scores/")
output_file = "./scores/out_of_vocab.txt"
output = ("parsed file \t# of words \t# of unique words "
          "\ttraining set \t# of words \t# of unique words"
          "\t# of out-of-vocab \t# of unique out-of-vocab\n")

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

def out_of_voc(file1, file2):   #file2 is the one used for the training model, file1 is the parsed one
    global files_words, output
    
    if not file1 in files_words.keys():
        files_words[file1] = get_words_uniq(file1)
    if not file2 in files_words.keys():
        files_words[file2] = get_words_uniq(file2)

    '''uniq_count = 0
    all_words =  list(set(files_words[file1][1] + files_words[file2][1]))
    uniq_count = len(all_words) - len(files_words[file2][1])'''
            
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

for p_set in config['parse_sets']:
    for pair in p_set['model_input_pairs']:
        file1 = p_set['data_path'] + pair[1]
        
        file2_path = p_set['model_path'].replace("models", "data")
        file2_name = pair[0].replace("model_", "")
        file2_name = file2_name.replace(".mco", "")
        file2 = file2_path + "/" + file2_name
        
        print(f"running for files {file1} and {file2}")
        out_of_voc(file1, file2)

with open(output_file, "w") as f:
    f.write(output)