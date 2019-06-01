# 4

# 1) root 81 17 absent (0.79012346 0.20987654)  
# 2) Start>=8.5 62  6 absent (0.90322581 0.09677419)  
# 4) Age=old,young 48  2 absent (0.95833333 0.04166667)  
# 8) Start>=13.5 25  0 absent (1.00000000 0.00000000) *
#   9) Start< 13.5 23  2 absent (0.91304348 0.08695652) *
#   5) Age=middle 14  4 absent (0.71428571 0.28571429)  
#   10) Start>=12.5 10  1 absent (0.90000000 0.10000000) *
#   11) Start< 12.5 4  1 present (0.25000000 0.75000000) *
#   3) Start< 8.5 19  8 present (0.42105263 0.57894737)  
# 6) Start< 4 10  4 absent (0.60000000 0.40000000)  
# 12) Number< 2.5 1  0 absent (1.00000000 0.00000000) *
#   13) Number>=2.5 9  4 absent (0.55555556 0.44444444) *
#   7) Start>=4 9  2 present (0.22222222 0.77777778)  
# 14) Number< 3.5 2  0 absent (1.00000000 0.00000000) *
#   15) Number>=3.5 7  0 present (0.00000000 1.00000000) * 

# Age     Number   Start   Prediction
# middle   5        10      present
# young    2        17      absent
# old     10         6      present
# young    2        17      absent
# old      4        15      absent
# middle   5        15      absent
# young    3        13      absent
# old      5         8      present
# young    7         9      absent
# middle   3        13      absent

# 5
install.packages("rpart")
library(rpart)

train<-read.csv("./data/sonar_train.csv",header=FALSE)
y<-as.factor(train[,61])
x<-train[,1:60]

test<-read.csv("data/sonar_test.csv",header=FALSE)
y_test<-as.factor(test[,61])
x_test<-test[,1:60]

train_error<-rep(0,6)
test_error<-rep(0,6)

for (dep in 1:6) {
  fit<-rpart(y~.,x,
             control=rpart.control(minsplit=0,minbucket=0,cp=-1,
                                   maxcompete=0, maxsurrogate=0, usesurrogate=0,
                                   xval=0,maxdepth=dep))
  train_error[dep]<-
    1-sum(y==predict(fit,x,type="class"))/length(y)
  test_error[dep]<-
    1- sum(y_test==predict(fit,x_test,type="class"))/length(y_test)
}