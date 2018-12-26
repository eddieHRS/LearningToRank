'''
now i have dic of each doc and index of each query
this py to create data like
    querynum  BM25  IDF*TF isrelevant
'''
import os
import sys
import nltk
import pickle
import math
reload(sys)
sys.setdefaultencoding('iso8859-1')

queryInfoPath = "../IRFinalProject/2017TAR/training/extracted_data"
DicInfoPath = "dics"
IndexInfoPath = "index"

QueryList = os.listdir(queryInfoPath)
# DicsList = os.listdir(DicInfoPath)
# IndexList = os.listdir(IndexInfoPath)

queryinfo = {}
querywords = {}
docrelative = {}

relDoc = open("../IRFinalProject/2017TAR/training/qrels/qrel_abs_train","r")
rlines = relDoc.readlines()
relDoc.close()
for rline in rlines:
	temp = rline.split()
	if temp[3] == '1':
		if temp[0] in docrelative.keys():
			docrelative[temp[0]].append(temp[2])
		else:
			docrelative[temp[0]] = [temp[2]]
print docrelative.keys()



def CalIDF_TF_BM25(words,q,dicpath):
	dicfile = open(DicInfoPath + "/" + q + "/" + dicpath, "r")
	dic = pickle.load(dicfile)
	dicfile.close()


	result = 0.0
	N = len(queryinfo[q])
	indexfile = open(IndexInfoPath + "/" + q,"r")
	index = pickle.load(indexfile)
	indexfile.close()
	
	
	for word in words:
		nqi = len(index[word])
		if word in dic.keys():
			tf = math.log(1 + dic[word])
		else:
			tf = 0
		idf = math.log((N - nqi + 0.5) / (nqi + 0.5))
		result += tf * idf

	len_d = 0
	for k in dic.keys():
		len_d += dic[k]

	avg_d = len_d + 100


	k1 = 1.5
	b = 0.75
	bm25 = 0.0
	for word in words:
		nqi = len(index[word])
		if word in dic.keys():
			t = dic[word]
		else:
			t = 0
		idf = math.log((N - nqi + 0.5) / (nqi + 0.5))
		bm25 += idf * (t * k1 + 1) / (t + k1 * (1-b+b*len_d/avg_d))
	return result,bm25


def ProcessQuery(text):
	stw = open("stop_word.txt","r")
	stopword = stw.read().splitlines()
	stw.close()
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
	#stemmer
	t2 = []
	porter_stemmer = nltk.PorterStemmer()
	for word in t1:
		t2.append(porter_stemmer.stem(word))
	return t2




#queryinfo is a dic store queryID like CDxxxxx and relative [docsnums]
for i in QueryList:
	if i.endswith(".pids"):
		temp = i.replace(".pids","")
		queryinfo[temp] = []
		f = open(queryInfoPath + '/'+ i,"r")
		lines = f.readlines()
		f.close()
		for line in lines:
			t = line.split()
			queryinfo[temp].append(t[1])
	if i.endswith(".title"):
		temp = i.replace(".title","")
		f = open(queryInfoPath + '/'+ i,"r")
		text = f.read()
		text = text.replace(temp,"")
		f.close()
		qwords = ProcessQuery(text)
		# print qwords
		querywords[temp] = qwords

#for each query to create initial data
for q in queryinfo.keys():
	reldocs = docrelative[q]
	docs = os.listdir(DicInfoPath + "/" + q)
	print len(docs)
	words = querywords[q]
	f = open("data","a+")
	i = 0
	for doc in queryinfo[q]:
		if doc not in docs:
			continue
		print q + "  " + doc + " *** "+ str(i) + "/" + str(len(docs))
		temp = CalIDF_TF_BM25(words,q,doc)
		if doc in reldocs:
			flag = 1
		else:
			flag = 0
		f.write("%-10s %-10s  %-10lf %-10lf  %-5d\n"%(q,doc,temp[0],temp[1],flag))
		i+=1
	f.close()
