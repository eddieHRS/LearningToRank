'''
单个主题的平均准确率是每篇相关文档检索出后的准确率的平均值。
主集合的平均准确率(MAP)是每个主题的平均准确率的平均值。
MAP 是反映系统在全部相关文档上性能的单值指标。
系统检索出来的相关文档越靠前(rank 越高)，MAP就可能越高。如果系统没有返回相关文档，则准确率默认为0。
例如：假设有两个主题，主题1有4个相关网页，主题2有5个相关网页。某系统对于主题1检索出4个相关网页，
其rank分别为1, 2, 4, 7；对于主题2检索出3个相关网页，其rank分别为1,3,5。
对于主题1，平均准确率为(1/1+2/2+3/4+4/7)/4=0.83。
对于主题2，平均准确率为(1/1+2/3+3/5+0+0)/5=0.45。
则MAP= (0.83+0.45)/2=0.64。”



def MAP(dic)

参数dic中的格式是{
				theme1:{rele_page1:rank1,rele_page2:rank2……}
				theme2:{……}
				}
且每一个theme的rank是排好序的
'''
def MAP(result_info):
	themes = result_info.keys()
	sum_of_all_themes = 0.0
	for theme in themes:
		values = result_info[theme].values()
		temp = 0.0
		i = 1
		for v in values:
			temp += v / i
			i += 1
		sum_of_all_themes += temp
	return sum_of_all_themes/len(themes)


'''
对一个query计算其NDGG
参数：result_list
每篇文档相关度取5个等级

perfect 31
excellent 15
good 7
fair 3
bad 0

result_list = [
				[url1:gain1]
				[url2:gain2]
				……
				]

ideal_result_list = 
				[


				]

'''
def NDGG(result_list,ideal_result_list):
	#cal DCG of result_list
	temp = 0
	length = len(result_list)
	for i in range(0,length):
		result_list[i][1] = result_list[i][1] * math.log(2)/math.log(2+i) + temp
		temp = result_list[i][1]
	#cal ideal_DCG of ideal_result_list
	temp = 0
	for i in range(0,length):
		ideal_result_list[i][1] *= ideal_result_list[i][1] * math.log(2)/math.log(2+i) + temp
		temp = ideal_result_list[i][1]
	#cal NDCG
	for i in range(0,length):
		result_list[i][1] /= ideal_result_list[i][1]
	return result_list



