from anytree import Node, RenderTree, ZigZagGroupIter

input_files = ["./parsed/Akkad_on_Akkad_only/5_parsed_Akkad_on_Akkad_only_Akkad_part_5.conllu",
               "./parsed/Akkad_on_PATB/5_parsed_Akkad_on_PATB_Akkad_part_5.conllu",
               "./parsed/Akkad_on_PATB_train_and_Akkad/5_parsed_Akkad_on_PATB_train_and_Akkad_Akkad_part_5.conllu",
               "./data/Akkad_only/Akkad_1-2-3-4.conllu",
               "./data/Akkad_parts/Akkad_part_5.conllu",
               "./data/PATB/catib.train.conllu",
               "./data/PATB_train_and_Akkad/PATB_Akkad_1-2-3-4.conllu"]

def get_trees(input_file):
    with open(input_file, "r") as f:
        lines = f.readlines()

    trees = []

    current_nodes = [Node("0")]
    current_lines = []

    for line in lines:
        
        # reads an entire sentence, and adds the nodes to current nodes list
        if line != "\n":
            cols = line.split("\t")
            current_lines.append(cols)
            current_nodes.append(Node(cols[0]))
        
        # once the sentence is over, it attaches each node to its parent by reading the seventh column
        else:
            for (i, l) in enumerate(current_lines):
                try:
                    current_nodes[i+1].parent = current_nodes[int(l[6])]
                except:
                    print("Error: referenced node cannot be found", i, l)
            
            trees.append(current_nodes)
            
            current_nodes = [Node("0")]
            current_lines = []

    return trees

def average_depth(input_file):
    
    depth_sum = 0
    
    trees = get_trees(input_file)
    num_of_sentences = len(trees)

    for tree in trees:
        # subtracting 2 from the following length to not count the 0 node as part of the tree
        # change to - 1 if you want to count the 0 node
        depth = len(list(ZigZagGroupIter(tree[0]))) - 2
        depth_sum += depth

        # for debugging and seeing what the trees look like
        #print([[node.name for node in children] for children in ZigZagGroupIter(tree[0])])
        #print(depth)
        #print(RenderTree(tree[0]).by_attr())

    return depth_sum / num_of_sentences


for input_file in input_files:
    print(input_file, average_depth(input_file), sep="\t")
