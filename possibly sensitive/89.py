Created on Mon Jul  3 18:59:05 2017

@author: Ayush Vatsyayan


import os
import sys
import pyparsing as pp
import re
import pandas as pd
import locale
import ConfigParser


def pdf_to_text():
    global config


    cmd = config.get("PDF","PDFBOX_COMMAND") + " " + config.get("PDF","PASSWORD")
    cmd += " " + config.get("PDF","PDF_FILE_PATH") + " tmp.txt"

    resp = os.system(cmd)
    
    if resp != 0:
        print "Error converting PDF to txt"
        sys.exit(resp)
    

    textfile = open("tmp.txt")
    lines = textfile.readlines()
    textfile.close() #close file
    
    os.remove("tmp.txt")
    
    return lines


def init():
    #Read configuration
    global config
    config = ConfigParser.ConfigParser()
    config.read("config.ini")
    
    transaction_id = pp.Word(pp.nums) + pp.Suppress(pp.White())
    balance = pp.Combine(pp.Word(pp.nums + ",") + "." + pp.Word(pp.nums, exact=2) + pp.Optional('CR'))
    date_pattern = pp.Word(pp.nums, exact=6)
    merchant = pp.restOfLine()

    global transactional_pattern
    global non_transactional_pattern
    transactional_pattern = transaction_id + balance + date_pattern + merchant
    non_transactional_pattern = balance + date_pattern + merchant

def parse_transactions(lines):
    global transactional_pattern
    global non_transactional_pattern
    
 
    stmt_dict = {'transaction_id':[], 'balance':[], 'date':[],'merchant':[] }
    
    for line in lines:
        try:
            result = pp.OneOrMore(transactional_pattern).parseString(line)
            
  
            stmt_dict['transaction_id'].append(result[0])
            stmt_dict['balance'].append(result[1])
            stmt_dict['date'].append(result[2])
            stmt_dict['merchant'].append(result[3])
        except pp.ParseException:

            try:
                result = non_transactional_pattern.parseString(line)
                stmt_dict['transaction_id'].append('')
                stmt_dict['balance'].append(result[0])
                stmt_dict['date'].append(result[1])
                stmt_dict['merchant'].append(result[2])
            except pp.ParseException:
                pass
    

    stmt_df = pd.DataFrame(stmt_dict)

    stmt_df.balance = [ '-' + v.replace('CR','').strip() if v.endswith('CR') else v.strip() for v in stmt_df.balance]

    stmt_df.merchant = [re.sub("\s\s+" , " ",v) for v in stmt_df.merchant]
    