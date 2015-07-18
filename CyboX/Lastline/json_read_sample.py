#coding:utf-8
'''
Created on 2015/03/10

@author: Makoto
'''
import json

fpath = 'cfe629ab66a4446588a03a8c5aaede7b.json'

def jwrite(filepath,dump):
    fw = open('cfe629ab66a4446588a03a8c5aaede7b.log','w')
    fw.write(dump)
    fw.close()

def jread(filepath):
    f = open('cfe629ab66a4446588a03a8c5aaede7b.json', 'r')
    return json.load(f)
    f.close()

def jsontool():
    #もし存在するなら，keylistを返す
    jsonData = jread(fpath)
    dump =  json.dumps(jsonData, indent = 4)
    keyList = jsonData.keys()

    fw = open('list.log','w')

    tmp = jsonData["report"]["analysis_subjects"]
    #tmp = tmp["analysis_subjects"]

    j=0
    for key in tmp:
        print "[", key,"]"
        #groupDict = jsonData[k]
        #for i,value in tmp[key]:
        #    print "----[", i,":",value,"]"
        #print "--------------------------"
        
        #fw.write(k)
    #取得しgroupDictが見たければ下のコメントを外す
    #print groupDict
    #nameList = groupDict.keys()
    #print nameList
    fw.close()    

if __name__ == "__main__":
    jsontool()

