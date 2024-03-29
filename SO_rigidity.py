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
import numpy as np
from scipy.stats import entropy

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

USAGE = './SO_rigidity.py <source_directory> <target_directory> [-h]'

def build_parser():

    parser = argparse.ArgumentParser(description='word order script: The script extracts the data to compute word order rigidity (1 - entropy)')


    parser.add_argument('source',help='Source for conllu files. It should have conllu files organized in sub-directories, e.g. en uk hbs')
    parser.add_argument('target',help='Output file: tsv (tabular-separated value) file')

    return parser

def check_args(args):
    '''Exit if required arguments not specified'''
    check_flags = {}

#The following dictionary should reflect source data directory
languages_ciep = ["bg","br","cs","cy","da","de","el","en","es","fa","fr","ga","hbs","hi","hy","it","kmr","la","lt","lv","nl","no","pl","pt","ro","ru","sk","sv","uk","ur"]

#The function below extracts the data to compute word order rigidity (1 - entropy) and verb-medial order.
#The output contains the following columns:
#"Language", SO/OS- nouns: occurrences of SO/OS as nouns, SO,OS- all: occurrences of SO/OS as all POSes


def so_rigidity(directory,outfilename): #e.g., directory = "E:/LeipzigCorpora/Parsed/"
    outfile = open(outfilename, "w")
    outfile.write("Language\tSO-nouns\tOS-nouns\tSO-all\tOS-all\n")
    for language in sorted((f for f in os.listdir(directory) if not f.startswith(".")), key=str.lower):
        filenames = glob.glob(directory+ language + "/*.conllu")
        print(filenames)
        SO_nouns = 0
        OS_nouns = 0
        SO_all = 0
        OS_all = 0
        for filename in filenames:
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
                sentences = corpus.split("\n\r")
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
                                        if dep1 == "obj":
                                            obj = 1
                                            token_id_obj = linelist1[0]
                                            if "-" in token_id_obj:
                                                token_id_obj = token_id_obj.split("-")[0]
                                            POS_obj = linelist1[3]
                                        elif dep1 == "nsubj":
                                            subj = 1
                                            token_id_subj = linelist1[0]
                                            if "-" in token_id_subj:
                                                token_id_subj = token_id_subj.split("-")[0]
                                            POS_subj = linelist1[3]
                            if obj == 1 and subj == 1:
                                token_id = int(token_id)
                                token_id_subj = int(token_id_subj)
                                token_id_obj = int(token_id_obj)
                                if token_id_subj < token_id_obj:
                                    SO_all += 1
                                if token_id_subj > token_id_obj:
                                    OS_all += 1
                                if POS_subj == "NOUN" and POS_obj == "NOUN":
                                    if token_id_subj < token_id_obj:
                                        SO_nouns += 1
                                    if token_id_subj > token_id_obj:
                                        OS_nouns += 1
        out = language + "\t" + str(SO_nouns) + "\t" + str(OS_nouns) + "\t" + str(SO_all) + "\t" + str(OS_all) + "\n"
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
    so_rigidity(args.source,args.target) 
    print("Done! Happy corpus-based typological linguistics!\n")

if __name__ == "__main__":
    main()
    sys.exit(0)

