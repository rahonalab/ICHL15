language_list = []#please add the language list

def count_overlap_lemmas():
    outfilename = "lemmas_overlap.txt"
    outfile = open(outfilename, "w")
    language_list = languages_news
    for language in language_list:
        print (language)
        lemmas_overlap = 0
        lemmas_total = 0
        lemmas_overlap_weighted = 0
        lemmas_total_weighted = 0
        dict_nsubj = defaultdict(list)
        dict_obj = defaultdict(list)
        infilename = "E:/Cleaning_up/SemTypology/TLT2020/" + language + "_forms_clean.txt"#please modify it as you need
        infile = open(infilename, "rb")
        lines = infile.readlines()
        for line in lines:
            line = str(line, "UTF-8",errors = 'ignore')
            linelist = line.strip().split("\t")           
            try:
                lemma = linelist[0].strip()
                if language in ["ko", "kor"]:
                    lemma = linelist[0].strip().split("+")[0].strip()
                if lemma != "_" and len(lemma) > 0:
                    lemmaPOS = lemma + "/" + linelist[1]
                    if only_nouns == True:
                        if linelist[1] == "NOUN":
                            if linelist[2] == "obj":
                                dict_obj[lemmaPOS].append(linelist[4].strip())
                            elif linelist[2] == "nsubj":
                                dict_nsubj[lemmaPOS].append(linelist[4].strip())
                    else: 
                        if linelist[2] == "obj":
                            dict_obj[lemmaPOS].append(linelist[4].strip())
                        elif linelist[3] == "nsubj":
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