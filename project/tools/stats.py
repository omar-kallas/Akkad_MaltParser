'''
This file runs shell commands to run malteval with specific parameters to get some statistics
The output is several files stored under ./scores/stats

The commands below are very similar and they only differ in the GroupBy option
All commands evaluate the Akkad_part5 parsed using Akkad folds (1-2-3-4)
(Except for the forth one, more explanation before the command)
Their output is specified by the output's file name

The output of these calls is not very tidy due to the limited formatting options offered by malteval
The output can be understood better by pasting it on an excel sheet, and moving the columns around

For more explanation on the commands check out the malteval documentation
'''

import os
import methods

output_path = "./scores/stats/"
methods.mkdir(output_path)

os.system(f'java -jar ./external_libraries/malteval/lib/MaltEval.jar \
          -s ./parsed/Akkad_on_Akkad_only/5_parsed_Akkad_on_Akkad_only_Akkad_part_5.conllu \
          -g ./data/Akkad_parts/Akkad_part_5.conllu \
          --details 1 --Metric "LAS;LA;UAS" --tab 1 --header-info 0 --row-header 1 --pattern 0.0000%\
          --GroupBy "Sentence:accuracy|sentencelength"  \
          > {output_path}/groupBySentence.txt')

os.system(f'java -jar ./external_libraries/malteval/lib/MaltEval.jar \
          -s ./parsed/Akkad_on_Akkad_only/5_parsed_Akkad_on_Akkad_only_Akkad_part_5.conllu \
          -g ./data/Akkad_parts/Akkad_part_5.conllu \
          --details 1 --Metric "LAS;LA;UAS" --tab 1 --header-info 0 --row-header 1 --pattern 0.0000% \
          --GroupBy "Postag:counter|accuracy" \
          > {output_path}/groupByPostag.txt')

os.system(f'java -jar ./external_libraries/malteval/lib/MaltEval.jar \
          -s ./parsed/Akkad_on_Akkad_only/5_parsed_Akkad_on_Akkad_only_Akkad_part_5.conllu \
          -g ./data/Akkad_parts/Akkad_part_5.conllu \
          --details 1 --Metric "LAS;LA;UAS" --tab 1 --header-info 0 --row-header 1 --pattern 0.0000% \
          --GroupBy "Cpostag:counter|accuracy" \
          > {output_path}/groupByCpostag.txt')

# this command evaluates the Akkad_part 5 parsed not only using the Akkad folds
# but also parsed using the PATB training set and the combination of both
# this is why the flag -s is given 3 arguments
os.system(f'java -jar ./external_libraries/malteval/lib/MaltEval.jar \
          -s ./parsed/Akkad_on_PATB/5_parsed_Akkad_on_PATB_Akkad_part_5.conllu \
          ./parsed/Akkad_on_Akkad_only/5_parsed_Akkad_on_Akkad_only_Akkad_part_5.conllu \
          ./parsed/Akkad_on_PATB_train_and_Akkad/5_parsed_Akkad_on_PATB_train_and_Akkad_Akkad_part_5.conllu \
          -g ./data/Akkad_parts/Akkad_part_5.conllu \
          --Metric "LAS;LA;UAS" --tab 1 --header-info 1 --row-header 1 --pattern 0.000% \
          --ExcludeCpostags PNX \
          > {output_path}/withoutPNX.txt')

os.system(f'java -jar ./external_libraries/malteval/lib/MaltEval.jar \
            -s ./parsed/Akkad_on_Akkad_only/5_parsed_Akkad_on_Akkad_only_Akkad_part_5.conllu \
            -g ./data/Akkad_parts/Akkad_part_5.conllu \
            --details 1 --Metric "LAS;LA;UAS" --tab 1 --header-info 0 --row-header 1 --pattern 0.000% \
            --GroupBy "RelationLength:parsercounter|treebankcounter|treebankaccuracy|parseraccuracy" \
            > {output_path}/distance_to_parent.txt')

os.system(f'java -jar ./external_libraries/malteval/lib/MaltEval.jar \
            -s ./parsed/Akkad_on_Akkad_only/5_parsed_Akkad_on_Akkad_only_Akkad_part_5.conllu \
            -g ./data/Akkad_parts/Akkad_part_5.conllu \
            --details 1 --Metric "LAS;LA;UAS" --tab 1 --header-info 0 --row-header 1 --pattern 0.000% \
            --GroupBy "ArcDepth:parsercounter|treebankcounter|treebankaccuracy|parseraccuracy" \
            > {output_path}/ArcDepth.txt')