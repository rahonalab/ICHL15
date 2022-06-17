import glob

languages_ciep = ["bg","br","cs","cy","da","de","el","en","es","fa","fr","ga","hbs","hi","hy","it","kmr","la","lt","lv","nl","no","pl","pt","ro","ru","sk","sv","uk","ur"]

#The function below extracts the data to compute word order rigidity (1 - entropy) and verb order metric.
#The output contains the following columns:
#"Language", "SOV", "SVO", "OSV", "OVS", "VSO", "VOS". All counts are provided only for S and O expressed by nouns, and for lexical verbs.

    
def find_all_orders(directory, outfilename): #e.g., directory = "D:/Corpora/ud-treebanks-v2.7/"
    outfile = open(outfilename, "w")
    outfile.write("Language\tSOV\tSVO\tOSV\tOVS\tVSO\tVOS\n")
    for language in languages_ciep: 
#        filenames = glob.glob(directory + language + "*") 
        filenames = glob.glob(directory + "*/" + language + "*.conllu")
        SOV = 0
        SVO = 0
        OSV = 0
        OVS = 0
        VSO = 0
        VOS = 0
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
        out = language + "\t" + str(SOV) + "\t" + str(SVO) + "\t" + str(OSV) + "\t" + str(OVS) + "\t" + str(VSO) + "\t" + str(VOS) + "\n"
        print (out)
        outfile.write(out)
    outfile.close()    