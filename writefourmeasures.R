#Aggregate results in a single file

#Modify according to the datasource
setwd("~/Desktop/linguistics/saarbruecken/natalia/results/CIEP/")
lemmaoverlap <- read.csv("lemma-overlap.tsv",sep="\t")
sorigidity <- read.csv("SO_rigidity.tsv",sep="\t")
wordorder <- read.csv("word-order-6.tsv",sep="\t")
#Semantic tightness (outside CIEP/treebank dir, as it's calculated from Leipzig corpora)
semantictightness = read.csv("~/Desktop/linguistics/saarbruecken/natalia/results/semantic-tightness.tsv",sep="\t")

#Remove so/os.all and calculate entropy and then rigidity
sorigidity <- subset(sorigidity, select=c(Language,SO.nouns,OS.nouns))
sorigidity[c("SO.nouns.rigidity")]<- apply(sorigidity[c("SO.nouns", "OS.nouns")],1, entropy,unit=c("log2"))
sorigidity[c("SO.nouns.rigidity")]<- 1-sorigidity[c("SO.nouns.rigidity")]

#Lemma proportion
lemmaoverlap[c("lemma.proportion")] <- lemmaoverlap[c("lemmas_overlap")]/lemmaoverlap[c("lemmas_total")]
lemmaoverlap[c("lemma.proportion.weighted")] <-  lemmaoverlap[c("lemmas_overlap_weighted")]/lemmaoverlap[c("lemmas_total_weighted")]


#Aggregate data depending on the Language column
fourmeasures <- wordorder
fourmeasures <- merge(fourmeasures, sorigidity, by.x = "Language", all = TRUE)
colnames(lemmaoverlap)[colnames(lemmaoverlap) == 'language'] <- 'Language'
fourmeasures <- merge(fourmeasures, lemmaoverlap, by.x = "Language", all = TRUE)
fourmeasures <- merge(fourmeasures, semantictightness, by.x = "Language", all.x =  TRUE)

write.table(fourmeasures,file="four-measures.tsv",sep="\t",row.names=FALSE)

