library(ggplot2)
library(dplyr)
library(reshape2)
library(stringr)
library(viridis)
library(colourvalues)
library(entropy)


r <- read.csv("SO_rigidity/so_rigidity-freq.tsv",sep="\t")

r$nouns.rigidity <- NA
r$all.rigidity <- NA


for(i in 1:nrow(r)) {
	r[i, ]$nouns.rigidity <- 1- entropy(c(r[i, ]$SO.nouns,r[i, ]$OS.nouns),method="ML",unit="log2")
	r[i, ]$all.rigidity <- 1- entropy(c(r[i, ]$SO.all,r[i, ]$OS.all),method="ML",unit="log2")
				}

write.csv(r,"SO_rigidity/so_rigidity-entropy.tsv", row.names = FALSE)

rnoun <- r %>% select(Language,nouns.rigidity)
rall <- r %>% select(Language,all.rigidity)
ggplot(data=rnoun) +
   geom_point(size=4,mapping = aes(y = reorder(Language,+nouns.rigidity), x = nouns.rigidity)) +##
   theme_bw() +##
   theme(legend.position = "right", legend.text = element_text(face="bold"), axis.text.x = element_text(angle = 45, vjust = 0.5, hjust=0.5)) +
   labs(title = "", x = "Rigidity (Anti-Entropy) of Subject-Object order (NOUN)", y = "Language", fill = "\n")
  ggsave("SO_rigidity/SO_rigidity_noun.png")
ggplot(data=rall) +
   geom_point(size=4,mapping = aes(y = reorder(Language,+all.rigidity), x = all.rigidity)) +##
   theme_bw() +##
   theme(legend.position = "right", legend.text = element_text(face="bold"), axis.text.x = element_text(angle = 45, vjust = 0.5, hjust=0.5)) +
   labs(title = "", x = "Rigidity (Anti-Entropy) of Subject-Object order (any UPOS)", y = "Language", fill = "\n")
  ggsave("SO_rigidity/SO_rigidity_all.png")

