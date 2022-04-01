import glob

languages_news = ["eng", "ara", "bul", "ces", "ell", "dan", "est", "fra", "ita", "hun",  "lav", "lit",  "nld", "nob", "por", "ron", "slv", "spa",  "swe", "vie", "rus", "deu", "fin", "tur", "jpn", "ind", "hin", "tam", "fas", "hrv", "kor"]

#The function below extracts the data to compute word order rigidity (1 - entropy) and verb-medial order.
#The output contains the following columns:
#"Language", 
#"total_sent_nouns": number of clauses with both NOUN nsubj and obj
#"total_sent_all": total number of all transitive clauses
#"verb_middle_nouns": number of transitive clauses with NOUN nsubj and obj and the verb between them
#"verb_middle_all": total number of transitive clauses with the verb between nsubj and obj
#"SO_nouns": number of SO clauses with NOUN nsubj and obj
#"SO_all" total number of all SO clauses

def word_order(directory, outfilename): #e.g., directory = "E:/LeipzigCorpora/Parsed/"
    outfile = open(outfilename, "w")
    outfile.write("Language\ttotal_sent_nouns\ttotal_sent_all\tverb_middle_nouns\tverb_middle_all\tSO_nouns\tSO_all\n")
    for language in languages_news: 
        filenames = glob.glob(directory + language + "*") 
        total_sentences_nouns = 0 #when both arguments are nouns
        total_sentences_all = 0
        verb_middle_nouns = 0
        verb_middle_all = 0
        SO_nouns = 0
        SO_all = 0
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
                                total_sentences_all +=1
                                token_id = int(token_id)
                                token_id_subj = int(token_id_subj)
                                token_id_obj = int(token_id_obj)
                                if token_id < token_id_subj and token_id > token_id_obj:
                                    verb_middle_all +=1
                                elif token_id > token_id_subj and token_id < token_id_obj: 
                                    verb_middle_all += 1 
                                if token_id_subj < token_id_obj:
                                    SO_all += 1
                                if POS_subj == "NOUN" and POS_obj == "NOUN":
                                    total_sentences_nouns += 1   
                                    if token_id < token_id_subj and token_id > token_id_obj:
                                        verb_middle_nouns +=1
                                    elif token_id > token_id_subj and token_id < token_id_obj: 
                                        verb_middle_nouns += 1                                     
                                    if token_id_subj < token_id_obj:
                                        SO_nouns += 1
        out = language + "\t" + str(total_sentences_nouns) + "\t" + str(total_sentences_all) + "\t" + str(verb_middle_nouns) + "\t" + str(verb_middle_all) + "\t" + str(SO_nouns) + "\t" + str(SO_all) + "\n"
        print (out)
        outfile.write(out)
    outfile.close()  