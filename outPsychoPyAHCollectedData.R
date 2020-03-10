rm(list=ls())
library(ggplot2)
library(car)
library(dbplyr)
library(lattice)
library(reshape2)

myData <- read.csv("collectedAHData.csv")

##
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
## myData <- myData %>% filter(RT > 0.005 & RT <= 5.00) ## doesn't work
myData <- myData[myData$RT > 0.005 & myData$RT <= 5.00,]
## !any(myData$RT > 0.005 & myData$RT <= 5.00)

## Clean Data
myData <-  subset(myData, myData$correct)

write.csv(myData, file="cleanAHData.csv",row.names = T)

x <- myData$RT
h<-hist(x, breaks=12, col="red", xlab="RT in ms",
   main="Histogram with Normal Curve")
xfit<-seq(min(x),max(x),length=40)
yfit<-dnorm(xfit,mean=mean(x),sd=sd(x))
yfit <- yfit*diff(h$mids[1:2])*length(x)
lines(xfit, yfit, col="blue", lwd=2) 

# ## Density Plot all RT
# d <- density(x) # returns the density data
# plot(d) # plots the results 
# polygon(d, col="red", border="blue")
# ## 

ggplot(myData, aes(myData$RT, fill = myData$condition)) + geom_density(alpha = 0.25)
ggsave("pics/RTbyCondition.png")

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
ggsave("pics/AHDensityRTbyConditionbyTime.png")


boxplot(RT~condition,data=myData, main="RT by Condition",
   xlab="Condition", ylab="RT in ms")
ggsave("pics/testDataBoxplotRTbyCondition.png")




