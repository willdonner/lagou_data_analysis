
# -*- coding: utf-8 -*-
import jieba
import os
import codecs
from scipy.misc import imread
import matplotlib as mpl 
import matplotlib.pyplot as plt 
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

class GetWords(object):
    def __init__(self, dict_name, file_list , dic_list):
        self.dict_name = dict_name
        self.file_list = file_list
        self.dic_list = dic_list

    #获取自定义词典的词列表
    def get_dic(self):  
        dic = open(self.dict_name, 'r')
        while 1:
            line = dic.readline().decode('utf-8').strip()
            self.dic_list.append(line)
            if not line:
                break
            pass
            
    def get_word_to_cloud(self):
        for file in self.file_list:
            with codecs.open('../spider/' + file, "r",encoding='utf-8', errors='ignore') as string:
                #把文档中所有英文单词转成大写方便统计
                string = string.read().upper()
                #分词，关闭新词发现功能
                res = jieba.cut(string, HMM=False)
                reslist = list(res)
                wordDict = {}
                #统计词频，获取词频字典
                for i in reslist:
                    if i not in self.dic_list:
                        continue
                    if i in wordDict:
                        wordDict[i]=wordDict[i]+1
                    else:
                        wordDict[i] = 1
            #设置词云形状图
            coloring = imread('test.jpeg')
            #设置词云相关配置如字体背景色等
            wc = WordCloud(font_path='msyh.ttc',mask=coloring,
                    background_color="white", max_words=50,
                    max_font_size=40, random_state=42)

            wc.generate_from_frequencies(wordDict)
            #导出图片
            wc.to_file("%s.png"%(file))
#导入自定义词典
def set_dic():
    _curpath=os.path.normpath( os.path.join( os.getcwd(), os.path.dirname(__file__) ))
    settings_path = os.environ.get('dict.txt')
    if settings_path and os.path.exists(settings_path):
        jieba.set_dictionary(settings_path)
    elif os.path.exists(os.path.join(_curpath, 'data/dict.txt.big')):
        jieba.set_dictionary('data/dict.txt.big')
    else:
        print "Using traditional dictionary!"
 
if __name__ == '__main__':
    set_dic()
    file_list = ['data_visualize.txt', 'data_dev.txt', 'data_mining.txt', 'data_arc.txt', 'data_analysis.txt']
    dic_name = 'dict.txt'
    dic_list = []
    getwords = GetWords(dic_name, file_list, dic_list)
    getwords.get_dic()
    getwords.get_word_to_cloud()

