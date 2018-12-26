import os
import pickle
import sys
reload(sys)
sys.setdefaultencoding('iso8859-1')


DicPath = "test_dics"

lis = os.listdir(DicPath)


for q in lis:
	if os.path.exists("index"):
		pass
	else:
		os.mkdir("index")
	index = {}
	dics = os.listdir(DicPath + "/" + q)
	l = len(dics)
	i = 0
	for dic in dics:
		dicfile = open(DicPath + "/" + q + "/" + dic)
		print q + "  " + DicPath + "/" + q + "/" + dic +"    " +str(i) +"/"+str(l)
		d = pickle.load(dicfile)
		dicfile.close()

		dkey = d.keys()
		ikey = index.keys()
		bothkey = set(dkey).intersection(set(ikey))

		for dk in dkey:
			if dk in bothkey:
				# print dk + "**"
				index[dk].append(dic)
			else:
				index[dk] = [dic]



		i += 1
	indexfile = open("index/" + q,"w+")
	pickle.dump(index,indexfile)
	indexfile.close()

	
