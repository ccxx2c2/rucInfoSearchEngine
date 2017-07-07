# -*-coding: utf-8 -*-
import codecs,re,thulac,json,sys,io,threading,math
with codecs.open('data.json','r','utf-8') as f :
    hjson = json.loads(f.read())
with codecs.open('docref.log','r','utf-8') as f :
    djson = json.loads(f.read())
thu1 = thulac.thulac(seg_only = True)
    
query = sys.stdin.readline()
query = query.encode('gbk','surrogateescape')
query = query.decode('utf-8')
text = thu1.cut(query,text = False)
vector={}
for i in text :
    if not i[0] in vector:
        vector[i[0]]=1
    else:
        vector[i[0]]+=1
res={}
vmod = 0.0
for word in vector :
    vector[word]=(1+math.log(vector[word],10))
    vmod += vector[word]*vector[word]
    if not word in hjson:
        continue
    for docid in hjson[word]:
        if not docid in res:
            res[docid]=[0.0,0.0]
        res[docid]=[res[docid][0]+vector[word]*hjson[word][docid][0],res[docid][1]+hjson[word][docid][0]*hjson[word][docid][0]]
        
for docid in res:
    res[docid][0]/= (math.sqrt(res[docid][1])*math.sqrt(vmod))

res=sorted(res.items(),key=lambda d:-d[1][0])


print('[',end='')
for i in range(10):
    print('["%s","%s","%s"],' % (djson[res[i][0]],res[i][0],res[i][1][0]),end='')
print(']',end='')
        
