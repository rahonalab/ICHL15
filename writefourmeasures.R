#AggregVate results in a single file
library(ISOcodes)
#Modify according to the datasource
setwd("~/Desktop/linguistics/saarbruecken/natalia/results/treebanks/")
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
#Change column name for consistency
colnames(lemmaoverlap)[colnames(lemmaoverlap) == 'language'] <- 'Language'
lemmaoverlap[c("lemma.proportion")] <- lemmaoverlap[c("lemmas_overlap")]/lemmaoverlap[c("lemmas_total")]
lemmaoverlap[c("lemma.proportion.weighted")] <-  lemmaoverlap[c("lemmas_overlap_weighted")]/lemmaoverlap[c("lemmas_total_weighted")]

fourmeasures <- wordorder

#Aggregate data depending on the Language column

fourmeasures <- merge(fourmeasures, sorigidity, by.x = "Language", all.x = TRUE)
fourmeasures <- merge(fourmeasures, lemmaoverlap, by.x = "Language", all.x = TRUE)

#IF CIEP+ gets data straight from semantictightness
if (nchar(fourmeasures$Language[1]) < 3) {
fourmeasures <- merge(fourmeasures, semantictightness, by.x = "Language", all.x =  TRUE)
#then get language names
fourmeasures <- merge(fourmeasures, ISO_639_2, by.x="Language", by.y = "code", all.x=TRUE)
}

#If treebanks builds the language name
if (nchar(fourmeasures$Language[1]) > 3)
{
  colnames(fourmeasures)[colnames(fourmeasures) == 'Language'] <- 'Treebank'
  fourmeasures$Language <- str_replace_all(fourmeasures$Treebank,c("UD_" = "", "-.*" = ""))
  semantictightness <- merge(semantictightness,ISO_639_2, by.x = "Language", by.y = "code", all.x = TRUE)
  colnames(semantictightness)[colnames(semantictightness) == 'Language'] <- 'code'
  fourmeasures <- merge(fourmeasures, semantictightness, by.x = "Language", by.y = "Name", all.x =  TRUE)
}
write.table(fourmeasures,file="four-measures.tsv",sep="\t",row.names=FALSE)

