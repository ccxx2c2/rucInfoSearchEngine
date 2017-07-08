# -*- coding: UTF-8 -*-
import codecs,re,thulac,json,sys,io,threading,math
dict={}
nthread = 11
pagelen = int(5896/nthread)#5896
thu1 = thulac.thulac(seg_only = True)
flag = '<div class="content">'
with codecs.open('docref.log','r','utf-8') as f :
    docref = json.loads(f.read())
    
wlock = threading.Lock()
tlock = threading.Lock()
dlock = threading.Lock()
def parse(num):
    global flag,thu1,tlock,docref,dlock
    print(num)
    with codecs.open('bak/'+str(num)+'.bak','r','utf-8') as f:
        html = f.read()
    
    if dlock.acquire(): 
        title = re.findall(r'<title>(.*?)</title>',html)
        if len(title)== 0:
            title.append('');
        date = re.findall(r'<span class="date">发布时间：(.*?)</span>',html)
        if len(date)== 0:
            date.append('');
        click = re.findall(r'<span class="clicks">浏览量：(.*?)</span>',html)
        if len(click)== 0:
            click.append('');
        #print(docref[str(num)])
        docref[str(num)] = [docref[str(num)],title[0],click[0],date[0]]
        #print(docref[str(num)])
        dlock.release()
    
    for i in range(len(html)):
        if html[i:i+len(flag)] == flag :
            html=html[i:]
            break
            
    div = 0
    for i in range(len(html)):
        if html[i:i+4]=='<div':
            div += 1
        if html[i:i+6]=='</div>':
            div -= 1
        if div == 0:
            html=html[len(flag):i]
            break
        
    content = re.sub(r'<.*?>','',html)
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
        writein(text,nthread*num+id)
        
tds=[]
for id in range(nthread):
    tds.append(threading.Thread(target=todo, args=(id,)))
    tds[id].start()
    
for id in range(nthread):
    tds[id].join()

for word in dict:
    for doc in dict[word]:
        dict[word][doc][0]=(1+math.log(dict[word][doc][1],10)*(pagelen/len(word)))

with codecs.open('data.json','w','utf-8') as f:
    json.dump(dict,f,ensure_ascii=False)
    
with codecs.open('docref.log','w','utf-8') as f:
    json.dump(docref,f,ensure_ascii=False)
    