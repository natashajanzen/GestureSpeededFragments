## The purpose of this script is to read in data from the csv files that PsychoPy creates in the data folder when gsf.py is run.
library(tidyverse)
library(plyr) ## without this ldply LOC 11 won't work
library(readr)
setwd("~/Documents/PhD/SpeededFragment/GestureSpeededFragments-development")
mydir = "data"
myfiles = list.files(path=mydir, pattern="*.csv", full.names=TRUE)
myfiles

## So far so good. I'm not sure about the next section
myData = ldply(myfiles, read_csv) 

rcsv <- function(fl){
      message(fl)
      dtx <- read_csv(fl)
      dtx$order <- NULL
      dtx$subject_1 <- NULL
      dtx
}
map_df(myfiles, rcsv) %>%
      mutate(gestures = gsub("gestures\\/(.*).mp4", "\\1",gestures),
             target = as.factor(target)) %>%
      separate(gestures, c("noun","Z")) %>%
      select(noun, Z, target, condition, gestureSet, RT, correct, subject, everything()) %>%
      select(-TrialNumber, -ran) %>% ## this is obviously how to get rid of variables you don't need
      filter(RT > 0)
myData

# x <- factor(1:3)
# levels(x) <- as.numeric(levels(x))+40

write.csv(myData, file="collectedData.csv",row.names = T)
