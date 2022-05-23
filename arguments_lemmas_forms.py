#this function finds lemmas and wordforms (together with adpositions) of A and P arguments for computation of semantic tightness, as well as for computation of overlap between forms.

import glob
from collections import OrderedDict
from collections import defaultdict
import re
from random import sample 

languages_news = ["eng", "ara", "bul", "ces", "ell", "dan", "est", "fra", "ita", "hun",  "lav", "lit",  "nld", "nob", "por", "ron", "slv", "spa",  "swe", "vie", "rus", "deu", "fin", "tur", "jpn", "ind", "hin", "tam", "fas", "hrv", "kor"]
languages_with_cases = ["ara", "bul", "ces", "ell", "est", "hun", "lav", "lit", "por", "ron", "slv", "spa", "rus", "fin", "tur", "jpn", "hin", "tam", "fas", "hrv", "kor"]

def findArguments(compounds = False):
    directory = "E:/MyCorpusDirectory/"
    language_list = languages_news
    args = ["nsubj", "obj", "iobj", "obl"]
    for language in language_list:
        print (language)
        path = directory + language + "_*"
        files = glob.glob(path)
        if compounds == False:
            outfilename = "arguments_" + language + "_new.txt"
        else:
            outfilename = "arguments_" + language + "_compounds_new.txt"
        outfile = open(outfilename, "wb")
        for filename in files:
            print (filename)
            file = open(filename, "rb")
            corpus = file.read()
            corpus = str(corpus, "UTF-8", errors = "ignore")
            file.close()
            sentences = corpus.split("\n\n") # I had some problems with separators because the corpora had been created inconsistently. Please check this.
            if len(sentences) == 1:
                sentences = corpus.split("\n\r")
            print (len(sentences))
            for sentence in sentences:
                lines = sentence.strip().split("\n")
                line_tuples = []
                for line in lines:
                    linelist = line.strip().split("\t")
                    if len(linelist) > 7:
                        dep = linelist[7]
                        dep_original = linelist[7]
                        head_id = linelist[6] 
                        if ":" in dep:
                            dep = dep.split(":")[0]
                        if dep == "conj":
                            dep, head_id = coordination(head_id, lines)
                        if dep in args:
                            POS = linelist[3]
                            if POS in ["NOUN", "PROPN", "VERB", "ADJ", "NUM", "SYM"]:     
                                token_id = linelist[0]
                                lemma = linelist[2].lower()
                                if lemma == "_":
                                    lemma = linelist[1].lower() 
                                if compounds == True:
                                    lemma = checkCompounds(lemma, token_id, lines)
                                if dep == "nsubj":                            
                                    if checkTrans(head_id, lines):
                                        dep = "nsubj_tr"
                                    else:   
                                        dep = "nsubj_intr" 
                                wordform = linelist[1].lower()
                                wordform = check_adposition(wordform, token_id, lines, language)                             
                                out = lemma + "\t" + POS + "\t" + dep + "\t" + dep_original + "\t" + wordform + "\n"
                                outfile.write(bytes(out, "UTF-8"))
        outfile.close()

# we won't need this function. Just added for completeness. The results based on compounds and bare nouns are similar.
def checkCompounds(lemma, token_id, lines):
    compound_dict = {int(token_id) : lemma}
    compound_deps = ["compound", "fixed", "flat"]
    for line in lines:
        linelist = line.split("\t")
        if len(linelist) == 10:
            dep = linelist[7]
            if ":" in dep:
                dep = dep.split(":")[0]
            if dep in compound_deps:
                head_id = linelist[6]
                if head_id == token_id:
                    new_lemma = linelist[2].lower()
                    if new_lemma == "_":
                        new_lemma = linelist[1].lower()
                    new_token_id = linelist[0]    
                    compound_dict[int(new_token_id)] = new_lemma    
                    for line1 in lines:
                        linelist1 = line1.split("\t")
                        if len(linelist1) == 10:
                            dep1 = linelist1[7]
                            if ":" in dep1:
                                dep1 = dep1.split(":")[0]
                            if dep1 in compound_deps:
                                head_id1 = linelist1[6]
                                if head_id1 == new_token_id:
                                    new_new_lemma = linelist1[2].lower()
                                    if new_new_lemma == "_":
                                        new_new_lemma = linelist1[1].lower()
                                        new_new_token_id = linelist1[0]    
                                        compound_dict[int(new_new_token_id)] = new_new_lemma     
    ordered = OrderedDict(sorted(compound_dict.items()))
    compound_lemma = ""
    for key in ordered.keys():
        compound_lemma = compound_lemma + "_" + ordered[key]
    compound_lemma = compound_lemma.strip("_")
    return compound_lemma

def strip_punct(word): 
    clean_lemma = re.sub('[^\w]','', word, re.UNICODE)
    return clean_lemma

def coordination(head_id, lines): 
    head_dep = "NA"
    head_id1 = "NA"
    for line in lines:
        linelist = line.split("\t")
        if len(linelist) == 10:
            token_id = linelist[0]
            if token_id == head_id:
                head_dep = linelist[7]
                head_id1 = linelist[6]
    return head_dep, head_id1    
    
    
def checkTrans(head_id, lines): 
    trans = False
    for line in lines:
        linelist = line.split("\t")
        if len(linelist) == 10:
            dep = linelist[7]
            if ":" in dep:
                dep = dep.split(":")[0]
            if dep == "obj":
                head_id_new = linelist[6]
                if head_id_new == head_id:
                    trans = True
    return trans  

def check_adposition(wordform, token_id, lines, language):
    wordform_full = wordform
    for line in lines:
        linelist = line.split("\t")
        if len(linelist) == 10:
            head_id = linelist[6]
            if head_id == token_id:
                dep = linelist[7]
                if ":" in dep:
                    dep = dep.split(":")[0]
                if dep == "case": 
                    adpos = linelist[1].lower()
                    if language in ["spa", "es", "pt", "por"]:
                        if adpos == "a":
                            wordform_full = wordform_full + "_" + adpos
                    else:
                        wordform_full = wordform_full + "_" + adpos #because there were many PPs that were erroneously treated as obj
    return wordform_full

#An additional round of clearning is necessary. I also think there should be more 

def cleanArguments(compounds = False):
    directory = "E:/MyDirectory/"
    language_list = languages_with_cases
    for language in language_list:
        print (language)
        if compounds == False: 
            #filename = directory + "arguments_" + language + "_new.txt"
            #outfilename = directory + "arguments_" + language + "_clean.txt"
            filename = directory + language + "_forms.txt"
            outfilename = directory + language + "_forms_clean.txt"
        else:
            filename = directory + "arguments_" + language + "_compounds_new.txt"
            outfilename = directory + "arguments_" + language + "_compounds_clean.txt"
        outfile = open(outfilename, "wb")
        file = open(filename, "rb")
        lines = file.readlines()
        file.close()
        print (len(lines))
        for line in lines:
            line_UTF = str(line, "UTF-8", errors = "ignore")
            linelist = line_UTF.strip().split("\t")
            if len(linelist) == 5:
                POS = linelist[1]
                dep = linelist[2]
                wordform = linelist[4]
                dep_detailed = linelist[3]
                if dep == "nsubj_tr": #please double-check that
                #if dep == "nsubj":
                    coreArg = True
                    if dep_detailed == "nsubj:pass":
                        coreArg = False
                    elif "_" in wordform: #no adpositions by default are allowed for subjects, except for Hindi, Japanese and Korean. We might need to extend that.
                        if len(wordform.split("_")) > 2:
                            coreArg = False
                        casemarker = wordform.split("_")[1]
                        if language == "hin":
                            if casemarker!= u"ने":
                                coreArg = False 
                        elif language == "jpn":
                            if casemarker not in [u"が", u"は"]:
                                coreArg = False                        
                        elif language == "kor":
                            if casemarker not in [u"는", u"은", u"도"]:
                                coreArg = False    
                        else:
                            coreArg = False 
                    if coreArg:
                        outfile.write(line)                       
                elif dep == "obj":
                    coreArg = True
                    if "_" in wordform: 
                        if len(wordform.split("_")) > 2:
                            coreArg = False
                        casemarker = wordform.split("_")[1]
                        if language in ["spa", "por"]: #here, too: we'll need to change it
                            if casemarker != "a":
                                coreArg = False
                        elif language == "ita":
                            if casemarker != "di":
                                coreArg = False
                        elif language == "ron":
                            if casemarker != "pe":
                                coreArg = False
                        elif language == "fra":
                            if casemarker not in ["de", "d'", "d’", "du", "des"]:
                                coreArg = False
                        elif language == "fas":
                            if casemarker != u"را":
                                coreArg = False
                        elif language == "hin":
                            if casemarker != u"को":
                                coreArg = False
                        elif language == "jpn":
                            if casemarker != u"を":
                                coreArg = False
                        elif language == "kor":
                            if casemarker not in [u"는", u"은", u"도"]:
                                coreArg = False
                        elif language == "urd":
                            if casemarker not in [u"نے", u"کو"]:
                                coreArg = False
                        else:
                            coreArg = False 
                    if coreArg:
                        outfile.write(line)                           
        outfile.close()
