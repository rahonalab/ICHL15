library(rstatix)
library(DescTools)#for yet another sanity check, an alternative way of computing MI

language_code_add <- c("ga", "hy", "no", "pl", "sk", "uk", "ur")

MI_lemmas_add <- numeric(length = 7)
lemmas_add <- numeric(length = 7)

MI_check_lemmas_add <- numeric(length = 7)

MI_value <- function(data){
  prop_data <- prop.table(data)
  prop_data <- as.matrix(prop_data)
 
  Q_dist <- chisq.test(data)$expected
  Q_dist <- prop.table(Q_dist)
 
  MI <- sum(prop_data*ifelse(prop_data > 0, log2(prop_data/Q_dist), 0))
  return (MI)
}


for (i in 1:7){
  lang <- language_code_add[i]
  print (lang)
  infilename <- paste("arguments-Leipzig/arguments_", lang, sep = "")
  infilename <- paste(infilename, "_clean.txt", sep = "")
  data <- read.table(infilename, header = F, sep  ="\t", quote = "", comment = "", encoding = "UTF-8")
  print (dim(data))
  colnames(data) <- c("Lexeme", "Features", "POS", "Role", "Role_full", "Wordform")
  strip_beginning <- grep("^[[:punct:]]+[[:alnum:]]", data$Lexeme) 
  strip_end <- grep("[[:alnum:]][[:punct:]]+$", data$Lexeme) 
  strip_all <- c(strip_beginning, strip_end)
  print(length(strip_all))
  if (length(strip_all) > 0){
    data <- data[-strip_all,]
  }
  data <- data[nchar(as.character(data$Lexeme)) > 0,]
  data$LexemePOS <- paste(data$Lexeme, data$POS, sep = "/")
  data_nouns <- data[data$POS == "NOUN",]
  mytable <- table(data_nouns$LexemePOS, data_nouns$Role)
  rm(data_nouns)
  mytable <- mytable[rowSums(mytable) > 10,]
  hyphen <- grep("^-", rownames(mytable))
  if (length(hyphen) > 0){
    mytable <- mytable[-hyphen,]
  }
  lemmas_add[i] <- nrow(mytable)
  MI_lemmas_add[i] <- MI_value(mytable)
  print (MI_lemmas_add[i])
  data_restore <- countsToCases(as.data.frame(mytable))
  MI_check_lemmas_add[i] <- MutInf(data_restore[, 1], data_restore[, 2])
  print (MI_check_lemmas_add[i])
}


#Results:
#ga 0.09571849
#hy 0.1038157
#no 0.2307286
#pl 0.2129873
#sk 0.1620755
#uk 0.1636959
#ur 0.1335202