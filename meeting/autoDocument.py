import os
import re
from os import path
import time

dirPath = path.dirname(__file__)

def readFile(file_dir,file,model):
    f = open(file_dir, 'r',encoding='UTF-8')
    print(file_dir)
    beginWord = '/*'
    endWord = '*/'
    report_lines = f.readlines()
    signal = 0
    document = open(dirPath + '\\autoInterface\\interface_'+model+'_'+ file+ '.txt', 'w', encoding='UTF-8')
    for line in report_lines:
        if (line.find(beginWord)!= -1):
            signal = 1
        if(signal == 1):
            document.write(line)
        if (line.find(endWord) != -1):
            signal = 0
            document.write("\n")
    document.close()
    print(file)

def file_name(file_dir,model):
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.php':
                readFile(root+"\\"+file,os.path.splitext(file)[0],model)
                #time.sleep(1)





folder = os.path.exists(dirPath+'/autoInterface')
if not folder:
    os.makedirs(dirPath+'/autoInterface')

codingPath=dirPath+"/application/company"
file_name(codingPath,'company')
codingPath=dirPath+"/application/admin"
file_name(codingPath,'admin')
codingPath=dirPath+"/application/index"
file_name(codingPath,'index')
codingPath=dirPath+"/application/meeting"
file_name(codingPath,'meeting')
