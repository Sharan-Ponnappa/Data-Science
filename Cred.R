#install.packages("DMwR")
#install.packages("caret")
#install.packages("unbalanced")
#install.packages("c50")
#install.packages("dummies")
#install.packages("gridExtra")
#install.packages("psych")


setwd("F:/proj1")
#library list
libs=c("ggplot2","corrgram","DMwR","caret","randomForest","unbalanced","c50","dummies","MASS","gridExtra","psych")

#load Libraries
lapply(libs,require,character.only=TRUE)

#read data
raw_dat=read.csv("credit-card-data.csv",header = T,na.strings = c(" ","","NA"))       

#missing value analysis
miss_val=data.frame(apply(raw_dat,2,function(x){sum(is.na(x))}))

miss_val$columns=row.names(miss_val)
row.names(miss_val)=NULL
names(miss_val)[1]="percentage"
miss_val$percentage = (miss_val$percentage/nrow(raw_dat))*100
miss_val$percentage =miss_val[order(-miss_val$percentage),]


#1 - 139.50979
#9 - 311.96341
#mean =	864.35442
#raw_dat$MINIMUM_PAYMENTS[is.na(raw_dat$MINIMUM_PAYMENTS)]=mean(raw_dat$MINIMUM_PAYMENTS,na.rm = T)

#median = 312.56064
#impute Missing values with median
raw_dat$MINIMUM_PAYMENTS[is.na(raw_dat$MINIMUM_PAYMENTS)]=median(raw_dat$MINIMUM_PAYMENTS,na.rm = T)


#outlier analysis

indx_val = sapply(raw_dat, is.numeric)
num_data = raw_dat[,indx_val]

cols= colnames(num_data)
#plot ggplot
for (i in 1:length(cols)) {
  assign(paste0("plot",i),ggplot(aes_string(y=(cols[i]),x="CUST_ID"),dat=subset(raw_dat))+
           stat_boxplot(geom='errorbar',width=0.5)+
  geom_boxplot(outlier.colour="red",fill="blue",outlier.shape=18,outlier.size=1,notch=F)+
    theme(legend.position="bottom")+
    labs(y=cols[i],x="CUST_ID"))
}

gridExtra::grid.arrange(plot1,plot2,plot3,ncol=3)



#remove outliers
for (i in cols) {
  
  val=raw_dat[,i][raw_dat[,i]%in%boxplot.stats(raw_dat[,i])$out]
  raw_dat=raw_dat[which(!raw_dat[,i]%in%val),]
}

#derive an enriched data frame as per KPI's

new_data=data.frame("CUST_ID"=raw_dat$CUST_ID,"monthly_average_purchase"= raw_dat$PURCHASES,
                        "CASH_ADVANCE"=raw_dat$CASH_ADVANCE,"ONEOFF_PURCHASES"=raw_dat$ONEOFF_PURCHASES,
                        "INSTALLMENTS_PURCHASES"=raw_dat$INSTALLMENTS_PURCHASES,
                        "average_amount_per_purchase"=raw_dat$PURCHASES_TRX,"CASH_ADVANCE_TRX"=raw_dat$CASH_ADVANCE_TRX,
                        "LIMIT_usage"=raw_dat$BALANCE/raw_dat$CREDIT_LIMIT,
                        "payments_to_minimum_payments_ratio"= raw_dat$PAYMENTS/raw_dat$MINIMUM_PAYMENTS )
#get only the numeric variables
indx_val = sapply(new_data, is.numeric)
num_data = new_data[,indx_val]



#correlation
corrgram(new_data[,indx_val],order = F,upper.panel = panel.shade,text.panel = panel.text,main="correlation")


#removing variable "CUST_ID" as it is in factor type and not usefull for building a model.
new_data=subset(new_data,select=-c(CUST_ID))

cols=colnames(new_data)

#normalization
for (i in cols) {
  new_data[,i]=(new_data[,i]-min(new_data[,i]))/(max(new_data[,i])-min(new_data[,i]))
}


#standardization
for (i in cols) {
  new_data[,i]=(new_data[,i]-mean(new_data[,i]))/sd(new_data[,i])
}
rmExcept("new_data")

#FACTOR ANALYSIS

# find principle component to get the no. of factors to select

pc=princomp(new_data)

summary(pc)

#plot a bar graph to conform the number the factors
plot(pc)



fa=factanal(new_data,factors = 4 )

print(fa,cutoff=.3,sort=T)

#temp=data.frame(scale(new_data[-5]))

#Kmeans Clustering

library(NbClust)
km=kmeans(new_data,4,nstart = 25)

acc=table(temp$average_amount_per_purchase,km$cluster)




