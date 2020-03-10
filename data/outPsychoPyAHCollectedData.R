rm(list=ls())
library(ggplot2)
library(car)
library(dbplyr)
library(lattice)
library(reshape2)

myData <- read.csv("collectedAHData.csv")

shapiro.test(myData$RT)
# Shapiro-Wilk normality test
# data:  myData$RT
# W = 0.78745, p-value < 2.2e-16
# Data is not normally distributed. I think RT usually isn't.

qplot(sample = myData$RT, stat = "qq")
# the line sags, so the kurtosis differs from normality

leveneTest(myData$RT, myData$condition, center = median)

## Trim Data ####
## remove values that are less than 5 ms or more than 5 sec (Baayen & Milin 2009:15).
myData <- myData[myData$RT > 0.005 & myData$RT <= 5.00,]

## Clean Data
myData <-  subset(myData, myData$correct)

write.csv(myData, file="cleanAHData.csv",row.names = T)

# ## Density Plot all RT
# d <- density(x) # returns the density data
# plot(d) # plots the results 
# polygon(d, col="red", border="blue")
# ## 

ggplot(myData, aes(RT, fill = condition)) + geom_density(alpha = 0.25)
ggsave("pics/AHDensity.png")

## Comparing Groups via Kernal Density
library(hrbrthemes)
library(dplyr)
library(tidyr)
library(viridis)
ggplot(myData, aes(RT, fill = condition)) + 
      geom_density(alpha = 0.25) +
      theme_ipsum() +
      facet_wrap(~subject) +
      theme()
ggsave("pics/AHDensityFacet.png")

boxplot(RT~condition,data=myData, main="RT by Condition",
   xlab="Condition", ylab="RT in ms")
## ggsave("pics/AHBoxplot.png")


