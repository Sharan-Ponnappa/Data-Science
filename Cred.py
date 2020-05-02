import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import random
from factor_analyzer import FactorAnalyzer
from sklearn.decomposition import *
from sklearn.cluster import KMeans

os.chdir("F:/proj1")

#read data
raw_dat=pd.read_csv("credit-card-data.csv")

#find missing value and its percentage
miss_val=pd.DataFrame(raw_dat.isnull().sum())
miss_val=miss_val.reset_index()
miss_val=miss_val.rename(columns={'index': 'Variables',0:'missing_percentage'})
miss_val['missing_percentage']=(miss_val['missing_percentage']/len(raw_dat))*100

miss_val=miss_val.rename(columns={'index': 'Variables',0:'missing_percentage'})

#collection of numeric columns
c=['BALANCE','BALANCE_FREQUENCY','PURCHASES','ONEOFF_PURCHASES','INSTALLMENTS_PURCHASES','CASH_ADVANCE','PURCHASES_FREQUENCY',
   'ONEOFF_PURCHASES_FREQUENCY','PURCHASES_INSTALLMENTS_FREQUENCY','CASH_ADVANCE_FREQUENCY','CASH_ADVANCE_TRX','PURCHASES_TRX',
   'CREDIT_LIMIT','PAYMENTS','MINIMUM_PAYMENTS','PRC_FULL_PAYMENT','TENURE']


#finding and removing outliers
for i in c:
    q75,q25=np.percentile(raw_dat.loc[:,i],[75,25])
    iqr=q75-q25
    min=q25-(iqr*1.5)
    max=q75+(iqr*1.5)
    print(min)
    print(max)
    raw_dat=raw_dat.drop(raw_dat[raw_dat.loc[:,i]<min].index)
    raw_dat=raw_dat.drop(raw_dat[raw_dat.loc[:,i]>max].index)
    raw_dat=raw_dat.reset_index(drop=True)


f,ax=plt.subplots(figsize=(7,5))
corr=raw_dat.corr()
sns.heatmap(corr,mask=np.zeros_like(corr,dtype=np.bool),cmap=sns.diverging_palette(220,10,as_cmap=True),square=True,ax=ax)


#derving data from the original data according to KPI
derived_data={'CUST_ID':raw_dat['CUST_ID'],'monthly_average_purchase':raw_dat['PURCHASES'],'CASH_ADVANCE':raw_dat['CASH_ADVANCE'],
             'ONEOFF_PURCHASES':raw_dat['ONEOFF_PURCHASES'],'INSTALLMENTS_PURCHASES':raw_dat['INSTALLMENTS_PURCHASES'],
              'PURCHASES_TRX':raw_dat['PURCHASES_TRX'],'CASH_ADVANCE_TRX':raw_dat['CASH_ADVANCE_TRX'],
              'LIMIT_USAGE':raw_dat['BALANCE']/raw_dat['CREDIT_LIMIT'],
              'PAYMENTS_TO_MIN_PAYMENTS_RATIO':raw_dat['PAYMENTS']/raw_dat['MINIMUM_PAYMENTS']}

derived_data=pd.DataFrame(derived_data)

#plot boxplot to visualize outliers
sns.boxplot(derived_data['monthly_average_purchase'])
plt.boxplot(derived_data['CASH_ADVANCE'])
plt.boxplot(derived_data['ONEOFF_PURCHASES'])
plt.boxplot(derived_data['INSTALLMENTS_PURCHASES'])
plt.boxplot(derived_data['PURCHASES_TRX'])
plt.boxplot(derived_data['CASH_ADVANCE_TRX'])
plt.boxplot(derived_data['LIMIT_USAGE'])
sns.boxplot(derived_data['PAYMENTS_TO_MIN_PAYMENTS_RATIO'])

#removing variable "CUST_ID" as it is in factor type and not usefull for building a model.
derived_data=derived_data.drop(columns=['CUST_ID'])


#PLotting correlation map
f,ax=plt.subplots(figsize=(7,5))
corr=derived_data.corr()
sns.heatmap(corr,mask=np.zeros_like(corr,dtype=np.bool),cmap=sns.diverging_palette(220,10,as_cmap=True),square=True,ax=ax)

#normality check
plt.hist(derived_data['PURCHASES_TRX'],bins='auto')

#normalization
for i in cols:
    print(i)
    derived_data[i]=(derived_data[i]-derived_data[i].min())/(derived_data[i].max()-derived_data[i].min())

#standarization
for i in cols:
    print(i)
    derived_data[i]=(derived_data[i]-derived_data[i].mean())/(derived_data[i].std())


#factor analysis for getting ideal number factors to select
fa = FactorAnalyzer(rotation=None)
fa.fit(derived_data)
ev ,v= fa.get_eigenvalues()

#eigen values
ev


#plot a elbow graph for getting number factors
plt.plot(range(1,derived_data.shape[1]+1),ev)
plt.title('Scree Plot')
plt.xlabel('Factors')
plt.ylabel('Eigenvalue')
plt.grid()
plt.show()	


#factor analysis with number factors =4
fa = FactorAnalyzer(n_factors=2,rotation="varimax")
fa.fit(derived_data)


fa.get_factor_variance()
#cummuilative variance=47%

#loadings per each factor
fa.loadings_

#Kmeans clustering


clusters=KMeans(init="random",n_clusters=2)
clusters.fit(derived_data)
