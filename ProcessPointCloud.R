rm(list = ls())
fnCumDays <- function(intMonth, intDay) {
  if (intMonth == 1) intCumMonthDays = 0                                                 #January
  else if (intMonth == 2) intCumMonthDays = 31                                           #February
  else if (intMonth == 3) intCumMonthDays = 59                                           #March
  else if (intMonth == 4) intCumMonthDays = 90                                           #April
  else if (intMonth == 5) intCumMonthDays = 120                                          #May
  else if (intMonth == 6) intCumMonthDays = 151                                          #June
  else if (intMonth == 7) intCumMonthDays = 181                                          #July
  else if (intMonth == 8) intCumMonthDays = 212                                          #August
  else if (intMonth == 9) intCumMonthDays = 243                                          #September
  else if (intMonth == 10) intCumMonthDays = 273                                         #October
  else if (intMonth == 11) intCumMonthDays = 304                                         #November
  else if (intMonth == 12) intCumMonthDays = 334                                         #December
  else intCumMonthDays = NA                                                              #ERROR  
  return(intCumMonthDays + intDay)
}


fnQuantile <- function(vctInput, intNumberDivisions) {
    #returns a factor. Slices up vctInput into intNumberDivisions. Each slice contains approx same number of observations
    vctDivisions <- seq(0,1, by = 1 / intNumberDivisions)
    vctQuantile <- quantile(vctInput, probs = vctDivisions)
    vctFactor <- cut(vctInput, vctQuantile, labels = 1:intNumberDivisions, include.lowest=TRUE)
    return(vctFactor)
}

fnFuzz <- function(intValue) {
    return(intValue + runif(1,-0.5,0.5))
}


setwd('/Users/zurich/Google Drive/SITES/FactMachine-Final/3D-Histogram')
origData <- read.csv('SydneyCleanData.csv', header = FALSE)
names(origData) <- c('day','month','year','date','temp')
origData <- subset(origData, !(year==2012))                                             #exclude partial year (134 obs) [tot: 5]
origData <- subset(origData, !(month==2 & day ==29))                                    #get rid of 29.02.yy (38 obs) Post 55845 observations
origData$cumDay <- mapply(fnCumDays, origData$month, origData$day)                      #vectorised application of a function
origData$yearNumber <- sapply(origData$year, function(x) x-1858)                        #anonymous function Pst: Year is 1 to 153
origData$factor <- fnQuantile(origData$temp, 11)                                        #splits temp into 11 quantiles
dfDataExport <- origData[, c(5,7,6,8)]                                                  #output temp, year, day factor

dfDataExport$yearNumber <- sapply(dfDataExport$yearNumber, fnFuzz)                      #fuzz up discrete values
dfDataExport$cumDay <- sapply(dfDataExport$cumDay, fnFuzz)                             

dfDataExport$yearNumber <- as.vector(scale(dfDataExport$yearNumber))                    #mean = 0, sd = 1
dfDataExport$cumDay <- as.vector(scale(dfDataExport$cumDay))
dfDataExport$temp <- as.vector(scale(dfDataExport$temp))

sampleRows <- sample(1:nrow(dfDataExport), nrow(dfDataExport), replace=F)               #jumble up rows. 
dfDataExport <- dfDataExport[sampleRows,]
write.table(dfDataExport, "dataNew.csv", row.names=FALSE, col.names=FALSE, sep=",")
