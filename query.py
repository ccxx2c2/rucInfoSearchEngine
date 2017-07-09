# -*-coding: utf-8 -*-
import codecs,re,thulac,json,sys,io,threading,math
print('getin  succeed')
with codecs.open('data.json','r','utf-8') as f :
    hjson = json.loads(f.read())
with codecs.open('docref.log','r','utf-8') as f :
    djson = json.loads(f.read())
thu1 = thulac.thulac(seg_only = True)
    
while True:
    query = sys.stdin.readline()
    print('read succeed')
    if query[:2] == 'qq':
        query = query[2:-1]
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
                
        if res == {}:
            print("no result!")
            sys.stdout.flush()
            continue
            
        for docid in res:
            res[docid][0]/= (math.sqrt(res[docid][1])*math.sqrt(vmod))

        #res=sorted(res.items(),key=lambda d:-d[1][0])
        res=sorted(res.items(),key=lambda d:(0 if djson[d[0]][0][djson[d[0]][0].rfind('.')-4:djson[d[0]][0].rfind('.')] == 'list' else -1,-d[1][0],-d[1][1]))
        
        print("~%s,["% len(res),end='')
        for i in range(10 if 10 < len(res) else len(res)):
            print('["%s","%s","%s","%s","%s","%s","%s"],' % (djson[res[i][0]][0].encode('utf-8').decode('gbk','surrogateescape'),djson[res[i][0]][1].encode('utf-8').decode('gbk','surrogateescape'),djson[res[i][0]][2],djson[res[i][0]][3],res[i][0],res[i][1][0],res[i][1][1]),end='')
        sys.stdout.flush()
        
    elif query[:2] == 'gp' :
        query = query[2:-1]
        print(query)
        if (int(query)*10-10 >= len(res)):
            print("no result!")
            sys.stdout.flush()
            continue
            
        for i in range(int(query)*10-10,int(query)*10 if int(query)*10 < len(res) else len(res)):
            print('["%s","%s","%s","%s","%s","%s","%s"],' % (djson[res[i][0]][0].encode('utf-8').decode('gbk','surrogateescape'),djson[res[i][0]][1].encode('utf-8').decode('gbk','surrogateescape'),djson[res[i][0]][2],djson[res[i][0]][3],res[i][0],res[i][1][0],res[i][1][1]),end='')
        sys.stdout.flush()
