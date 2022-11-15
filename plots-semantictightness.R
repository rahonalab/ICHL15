library(ggplot2)
library(dplyr)
library(reshape2)
library(stringr)
library(viridis)
library(colourvalues)
library(entropy)
library(infotheo)

dftot <- setNames(data.frame(matrix(ncol = 2, nrow = 0)),c("language","mi"))

MI_value <- function(data){
  prop_data <- prop.table(data)
  prop_data <- as.matrix(prop_data)
 
  Q_dist <- chisq.test(data)$expected
  Q_dist <- prop.table(Q_dist)
 
  MI <- sum(prop_data*ifelse(prop_data > 0, log2(prop_data/Q_dist), 0))
  return (MI)
}


for (i in list("ga","no","hy","uk","ur","pl","sk")){ 	
   csv <- read.csv(gsub(" ", "",paste("arguments-Leipzig/arguments_",i,"_clean.txt")),sep="\t",header=FALSE,quote="")
   print(i)
   #csv$V1 <- gsub('[[:digit:]]+', '', csv$V1)
   cont <- table(csv$V1,csv$V4)
   #mi <- MI_value(cont)
   df <- as.matrix(cont)
   mutinformation(df$nsubj_tr,df$obj)
   print(mi)
   row <- data.frame(language=i,mi=mi)
   dftot <- rbind(dftot,row)
}

ggplot(data=dftot) +
   geom_point(size=4,mapping = aes(y = reorder(language,+mi), x = mi)) +##
   theme_bw() +##
   theme(legend.position = "right", legend.text = element_text(face="bold"), axis.text.x = element_text(angle = 45, vjust = 0.5, hjust=0.5)) +
   labs(title = "", x = "Semantic Tightness (Mutual Information)", y = "Language", fill = "\n")
  ggsave("semantic_tightness.png")


write.csv(dftot,"semantic_tightness.tsv", row.names = FALSE)


