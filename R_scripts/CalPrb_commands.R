library(DMBC)
data(training)
idx <- sample(1:nrow(training),1)
test <- training[idx,]
train <- training[-idx,]
CalPrb(FS(train),test)