# -*- coding: UTF-8 -*-
import codecs,re,thulac,json,sys,io,threading,math
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030') 
dict={}
nthread = 5
pagelen = int(5838/nthread)#5790
thu1 = thulac.thulac(seg_only = True)
flag = '<div class="content">'
wlock = threading.Lock()
tlock = threading.Lock()
def parse(num):
    global flag,thu1,tlock
    print(num)
    with codecs.open('bak/'+str(num)+'.bak','r','utf-8') as f:
    #with codecs.open('index.htm','r','utf-8') as f:
        strs = f.read()
   # print('%s *2' % num)
    for i in range(len(strs)):
        if strs[i:i+len(flag)] == flag :
            strs=strs[i:]
            break
            
    div = 0
    #print('%s *3' % num)
    for i in range(len(strs)):
        if strs[i:i+4]=='<div':
            div += 1
        if strs[i:i+6]=='</div>':
            div -= 1
        if div == 0:
            strs=strs[len(flag):i]
            break
        
    content = re.sub(r'<.*?>','',strs)
    #print('%s *4' % num)
    if tlock.acquire():
        text = thu1.cut(content,text = False)
        tlock.release()
    return text

def writein(text,num):
    global dict,wlock
    if wlock.acquire(): 
        for i in text :
            if not i[0] in dict:
                dict[i[0]]={}
            if not num in dict[i[0]]:
                dict[i[0]][num]=[0,1]
            else:
                dict[i[0]][num][1]+=1
        wlock.release()
    
def todo(id):
    global nthread,pagelen
    for num in range(pagelen):
        text = parse(nthread*num+id)
        #print('%s *5' % str(nthread*num+id))
        writein(text,nthread*num+id)
        
tds=[]
for id in range(nthread):
    tds.append(threading.Thread(target=todo, args=(id,)))
    tds[id].start()
    
for id in range(nthread):
    tds[id].join()

#print(dict)            
for word in dict:
    for doc in dict[word]:
        dict[word][doc][0]=(1+math.log(dict[word][doc][1],10)*(pagelen/len(word)))

with codecs.open('data.json','w','utf-8') as f:
    json.dump(dict,f,ensure_ascii=False)
    