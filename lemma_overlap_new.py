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

USAGE = './lemma_overlap_new.py <source_directory> <target_directory> [-h]'

def build_parser():

    parser = argparse.ArgumentParser(description='lemma overlap')


    parser.add_argument('source',help='Source for cleaned files')
    parser.add_argument('target',help='Target output file.')

    return parser

def check_args(args):
    '''Exit if required arguments not specified'''
    check_flags = {}


#this function finds lemmas and wordforms (together with adpositions) of A and P arguments for computation of semantic tightness, as well as for computation of overlap between forms.


import glob
from collections import OrderedDict
from collections import defaultdict
import re
from random import sample 


def count_overlap_lemmas(source,outfilename,language_list):
    outfile = open(outfilename, "w")
    outfile.write("language" + "\t" + "lemmas_overlap" + "\t" + "lemmas_total" + "\t" + "lemmas_overlap_weighted" + "\t" + "lemmas_total_weighted" + "\n")
    for language in language_list:
        print (language)
        lemmas_overlap = 0
        lemmas_total = 0
        lemmas_overlap_weighted = 0
        lemmas_total_weighted = 0
        dict_nsubj = defaultdict(list)
        dict_obj = defaultdict(list)
        infilename = source + "/arguments_" + language + "_clean.txt"#please modify it as you need
        infile = open(infilename, "rb")
        lines = infile.readlines()
        for line in lines:
            line = str(line, "UTF-8",errors = 'ignore')
            linelist = line.strip().split("\t")           
            try:
                lemma = linelist[0].strip()
                if lemma != "_" and len(lemma) > 0:
                    lemmaPOS = lemma + "/" + linelist[1]                    
                    if linelist[2] == "obj":
                        dict_obj[lemmaPOS].append(linelist[4].strip())
                    elif linelist[2] == "nsubj_tr":
                        dict_nsubj[lemmaPOS].append(linelist[4].strip())
            except:
                print (line)
        set_nsubj = set(dict_nsubj)
        set_obj = set(dict_obj)
        set_both = set_nsubj & set_obj 
        for key in set_both:
            list_obj = dict_obj[key]
            list_nsubj = dict_nsubj[key]
            freq = len(list_obj) + len(list_nsubj)
            if freq  > 0:
                obj_form = sample(list_obj, 1)
                nsubj_form = sample(list_nsubj, 1)
                if obj_form == nsubj_form:
                    lemmas_overlap_weighted += 1*freq
                    lemmas_overlap += 1
                lemmas_total_weighted += 1*freq
                lemmas_total += 1
        out = language + "\t" + str(lemmas_overlap) + "\t" + str(lemmas_total) + "\t" + str(lemmas_overlap_weighted) + "\t" + str(lemmas_total_weighted) + "\n"
        outfile.write(out)
        print(out)
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
    #We include languages with morphological and syntactic (adposition) case marking
    languages = ["cs","cy","da","de","el","es","fa","fr","hbs","hi","hy","it","kmr","la","lt","lv","no","pl","pt","ro","ru","sk","sv","uk","ur"]

    count_overlap_lemmas(args.source,args.target,languages)
    print("Done! Happy corpus-based typological linguistics!\n")

if __name__ == "__main__":
    main()
    sys.exit(0)

