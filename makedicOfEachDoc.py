# -*- coding: utf-8 -*-
import os
import re
import nltk
import pickle
import sys
# import gzip

reload(sys)
sys.setdefaultencoding('iso8859-1')

#docPrePath = "../IRFinalProject/training"
docPrePath = "../IRFinalProject/testing"


#create stop_word
stw = open("stop_word.txt","r")
stopword = stw.read().splitlines()
stw.close()


for q in os.listdir(docPrePath):


	#Dir store dics
	DirStoreDocDic = 'test_dics/'+ q
	if os.path.exists(DirStoreDocDic):
		pass
	else:
		os.makedirs(DirStoreDocDic)
	#for each query
	
	DirStoreDocs = docPrePath + '/' + q
	

	docs = os.listdir(DirStoreDocs)
	for doc in docs:
		if doc.endswith("gz"):
			continue
		result = {}
		print DirStoreDocDic + '/' + doc
		dic = open(DirStoreDocDic + '/' + doc,"w+")
		
		# f = gzip.open(DirStoreDocs + '/' + doc,"rb")
		f = open(DirStoreDocs + '/' + doc,"r")
		text = f.read()#.decode("utf-8","ignore")
		text = re.sub("<[^>]*>","",text)
		text = text.replace("\n"," ")
		f.close()

		words = nltk.word_tokenize(text)
		

		#delete stopwords
		t0 = []
		for word in words:
			if word not in stopword:
				t0.append(word)
		# #print t0
		#lemmatizer
		t1 = []
		lemmatizaer = nltk.WordNetLemmatizer()
		for word in t0:
			t1.append(lemmatizaer.lemmatize(word))
		# #print t1
		#sten=mmer
		t2 = []
		porter_stemmer = nltk.PorterStemmer()
		for word in t1:
			t2.append(porter_stemmer.stem(word))
		# #print t2
		#add word to dic
		for word in t2:
			if word in result.keys():
				result[word] += 1
			else:
				result[word] = 1
		pickle.dump(result,dic)
		##print result
		dic.close()
	

		


