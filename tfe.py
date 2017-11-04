from flask import Flask
from flask import request
from flask import render_template
from flask import make_response
from functools import wraps, update_wrapper
from datetime import datetime
import subprocess

application = Flask(__name__)

@application.route('/')
def my_form():
    #my_form.html is very basic html input form
    return render_template("my-form.html")

@application.route('/', methods=['POST'])
def my_form_post():
    #input from user
    text = request.form['text']
    
    #parse the space-separated input text into variables for chromosome, position,reference base, mutated base and HLA_type
    chromo,pos,ref,alt,hla = text.split()
    
    #processed text holds summary of output from running Topiary
    processed_text = ""

    #take the '*' out of HLA type since it may cause problems if included in output file name at some point 
    hla_file_term = hla.replace("*","_")
     
    #output file name is named based on input variables
    #currently all output files are saved /home/ec2-user/tfe/results/
    output_file = "/home/ec2-user/tfe/results/output_" + chromo + "_" + pos + "_" + ref + "_" + alt + "_" + hla_file_term + ".html"    
 
    try:
        #input_list is list of elements required forrunning topiary from command line
        input_list = ['topiary','--variant','7','55191822','T','G','--mhc-predictor','random','--mhc-alleles','HLA-A*02:01','--ic50-cutoff','500','--mhc-epitope-lengths','8-11','--genome','GRCh38','--output-html',output_file]  
        
        #placeholders in input_list are replaced with values input by user
        input_list[2] = str(chromo)
        input_list[3] = str(pos)
        input_list[4] = ref
        input_list[5] = alt
        input_list[9] = hla

        #subprocess actually runs topiary 
        processed_text = subprocess.check_output(input_list)
    except subprocess.CalledProcessError as e:
        processed_text = e.output
        return processed_text
    #read out and return contents of html output file
    myfile = open(output_file, 'r')
    results =myfile.read()
    return results
    
if __name__ == "__main__":
    #application.debug = True 
    application.run(host='0.0.0.0')
