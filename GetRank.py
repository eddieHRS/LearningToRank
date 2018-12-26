import os
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame,Series
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
# from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.neural_network import BernoulliRBM
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn import tree
from sklearn import naive_bayes
# from sklearn.gaussian_process import GaussianProcess
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
# from sklearn.naive_bayes import GaussianNB
# from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

dataDic = {"BM25":[],"IDF_TF":[],"isrelevant":[]}

'''
this for txt data
'''
# a = -0.0022  
# b = 0.0024 
# c = 0.05
f = open("trainingdata","r")
lines = f.readlines()
f.close()

for line in lines:
	temp = line.split()
	IDF_TF = float(temp[2])
	BM25 = float(temp[3])
	dataDic["IDF_TF"].append(IDF_TF)
	dataDic["BM25"].append(BM25)
	dataDic["isrelevant"].append(float(temp[4]))
df = pd.DataFrame(dataDic)
# print('head:',df.head(),'\nShape:',df.shape)
# plt.scatter(df['isrelevant'], df['score'], color='blue')
# plt.show()



X_train,X_test,Y_train,Y_test = train_test_split(df.ix[:,:2],df.isrelevant,train_size=.95)

#线性回归
model = LinearRegression()
model.fit(X_train,Y_train)
a  = model.intercept_#截距
b = model.coef_#回归系数
print("最佳拟合线:截距",a,",回归系数：",b)
score = model.score(X_test,Y_test)
print("线性回归：%lf"%score)

#逻辑回归
LR = LogisticRegression()
LR.fit(X_train,Y_train)
score = LR.score(X_test,Y_test)
print("逻辑回归：%lf"%score)

#决策树
TR = tree.DecisionTreeClassifier(criterion="entropy")
TR.fit(X_train,Y_train)
score = TR.score(X_test,Y_test)
print("决策树：%lf"%score)

#支持向量机
SV = svm.SVC()
SV.fit(X_train,Y_train)
score = SV.score(X_test,Y_test)
print("向量机：%lf"%score)

#朴素贝叶斯
NB = naive_bayes.GaussianNB()
NB.fit(X_train,Y_train)
score = NB.score(X_test,Y_test)
print("朴素贝叶斯：%lf"%score)


'''
test for store score
'''
# print (type(X_test))
# y = TR.predict(X_test)
# # print(np.shape(y))
# X_test["score"] = y
# X_test.to_csv("result.csv")



'''
get rank of test
'''

for file in os.listdir("data"):
	f = open("data/" + file,"rb")
	li = pickle.load(f)
	f.close()
	dic_data_test = {"BM25":[],"IDF_TF":[],"docid":[]}
	for d in li:
		IDF_TF = float(d[0])
		BM25 = float(d[1])
		dic_data_test["IDF_TF"].append(IDF_TF)
		dic_data_test["BM25"].append(BM25)
		dic_data_test["docid"].append(d[2])
	dftest = pd.DataFrame(dic_data_test)
	X = dftest.ix[:,:2]
	#决策树的预测
	y = TR.predict(X)
	print(np.shape(y))
	dftest["score"] = y
	print (dftest)
	dftest.to_csv(file+"result.csv")





