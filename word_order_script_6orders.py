#!/usr/bin/env python3
import sys
import subprocess
import re
import pprint
import glob
import os
import random
import unicodedata
import collections
import csv
import string
import pyconll
import pyconll.util

try:
    import argparse
except ImportError:
    checkpkg.check(['python-argparse'])

import time
import socket

"""

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

USAGE = './word_order_script_6orders.py <source_directory> <target_directory> [-h]'

def build_parser():
    parser = argparse.ArgumentParser(description='word order script - six order version: The script extracts the data to compute the six word orders (SOV). The function below extracts the data to compute word order rigidity (1 - entropy) and verb order metric.\n The output contains the following columns:\n "Language", "SOV", "SVO", "OSV", "OVS", "VSO", "VOS". All counts are provided only for S and O expressed by nouns, and for lexical verbs. ')
    parser.add_argument('source',help='Source for conllu files. It should have conllu files organized in sub-directories, e.g. en uk hbs')
    parser.add_argument('target',help='Output file: tsv (tabular-separated value) file')

    return parser

def check_args(args):
    '''Exit if required arguments not specified'''
    check_flags = {}


import glob

languages_ciep = ["bg","br","cs","cy","da","de","el","en","es","fa","fr","ga","hbs","hi","hy","it","kmr","la","lt","lv","nl","no","pl","pt","ro","ru","sk","sv","uk","ur"]

#The function below extracts the data to compute word order rigidity (1 - entropy) and verb order metric.
#The output contains the following columns:
#"Language", "SOV", "SVO", "OSV", "OVS", "VSO", "VOS". All counts are provided only for S and O expressed by nouns, and for lexical verbs.

    
def find_all_orders(directory, outfilename): #e.g., directory = "D:/Corpora/ud-treebanks-v2.7/"
    outfile = open(outfilename, "w")
    outfile.write("Language\tSOV\tSVO\tOSV\tOVS\tVSO\tVOS\tVerbScore\n") 
    for language in sorted((f for f in os.listdir(directory) if not f.startswith(".")), key=str.lower):
        print(language)
#        filenames = glob.glob(directory + language + "*") 
        #filenames = glob.glob(directory + language + "/*.conllu")
        #print(filenames)
        SOV = 0
        SVO = 0
        OSV = 0
        OVS = 0
        VSO = 0
        VOS = 0
        for filename in glob.glob(directory + language + "/*.conllu"):
            print (filename)
            try:
                file = open(filename, "rb")
                corpus = file.read()
                corpus = str(corpus, "UTF-8", errors = "ignore")
                file.close()
            except:
                file = open(filename, "r")
                corpus = file.read()
            sentences = corpus.split("\n\n")
            if len(sentences) == 1:
                sentences = corpus.split("\n\r")#because of different formats and encodings in my corpora, probably not needed for CIEP
            print (len(sentences))
            for sentence in sentences:
                lines = sentence.strip().split("\n")
                for line in lines:
                    linelist = line.strip().split("\t")
                    if len(linelist) > 7:
                        POS = linelist[3]
                        if POS == "VERB":
                            obj = 0
                            subj = 0
                            token_id = linelist[0]
                            for line1 in lines:
                                linelist1 = line1.strip().split("\t")
                                if len(linelist1) > 7:
                                    head_id1 = linelist1[6]
                                    if head_id1 == token_id:
                                        dep1 = linelist1[7]
                                        if ":" in dep1:
                                            dep1 = dep1.split(":")[0]
                                        if dep1 == "obj" and linelist1[3] in ["NOUN", "PROPN"]:
                                            obj = 1
                                            token_id_obj = linelist1[0]
                                            if "-" in token_id_obj:
                                                token_id_obj = token_id_obj.split("-")[0]
                                        elif dep1 == "nsubj" and linelist1[3] in ["NOUN", "PROPN"]:
                                            subj = 1
                                            token_id_subj = linelist1[0]
                                            if "-" in token_id_subj:
                                                token_id_subj = token_id_subj.split("-")[0]
                            if obj == 1 and subj == 1:
                                token_id = int(token_id)
                                token_id_subj = int(token_id_subj)
                                token_id_obj = int(token_id_obj)
                                if token_id > token_id_subj and token_id < token_id_obj:
                                    SVO += 1
                                elif token_id_obj > token_id_subj and token_id > token_id_obj:
                                    SOV += 1
                                elif token_id > token_id_obj and token_id_subj > token_id:
                                    OVS += 1
                                elif token_id_subj > token_id_obj and token_id > token_id_subj:
                                    OSV += 1
                                elif token_id_subj > token_id and token_id_obj > token_id_subj:
                                    VSO += 1
                                elif token_id_obj > token_id and token_id_subj > token_id_obj:
                                    VOS += 1
                                else:
                                    print ("verb: " + str(token_id))
                                    print ("subject: " + str(token_id_subj))
                                    print ("object: " + str(token_id_obj))     
        try:
            verb_order_score = ((VSO + VOS) + (SVO + OVS)*2 + (SOV + OSV)*3)/(SOV + SVO + VSO + VOS + OVS + OSV)
        except:
            print("I cannot compute verb_order_score...")
            verb_order_score = "n/a"
        out = language + "\t" + str(SOV) + "\t" + str(SVO) + "\t" + str(OSV) + "\t" + str(OVS) + "\t" + str(VSO) + "\t" + str(VOS) + "\t" + str(verb_order_score) +"\n"
        print (out)
        outfile.write(out)
    outfile.close()    

def main():
    global debug
    global args
    global seppath
    parser = build_parser()
    args = parser.parse_args()
    seppath = '/'
    '''Check arguments'''    
    if check_args(args) is False:
     sys.stderr.write("There was a problem validating the arguments supplied. Please check your input and try again. Exiting...\n")
     sys.exit(1)
    find_all_orders(args.source,args.target) 
    print("Done! Happy corpus-based typological linguistics!\n")

if __name__ == "__main__":
    main()
    sys.exit(0)

