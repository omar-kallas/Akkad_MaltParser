'''
This file runs  maltparser and malteval by running the terminal's call
For more info on the parameters of the call checkout the maltparser and malteval documentation
'''

from subprocess import call

def learn(parser_file, model, working_space, input_file):
    call(["java",
          "-jar", parser_file,
          "-c", model,
          "-w", working_space,
          "-i", input_file,
          "-m", "learn"])
    
def parse(parser_file, model, working_space, input_file, output_file):
    call(["java",
          "-jar", parser_file,
          "-c", model,
          "-w", working_space,
          "-i", input_file,
          "-o", output_file])
    
def eval(eval_file, gold, parsed, output_file, metric = "LAS;UAS;LA", tab = "1", header = "0", pattern = "0.0000%"):
    call(["java",
          "-jar", eval_file,
          "-s", *parsed,
          "-g", *gold,
          "--output", output_file,
          "--Metric", metric,
          "--tab", tab,
          "--row-header", header,
          "--pattern", pattern])