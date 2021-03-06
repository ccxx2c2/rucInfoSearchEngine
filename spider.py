import re,requests,json,codecs,os,threading

s = requests.session()
rootDomain = ['http://info.ruc.edu.cn/','https://info.ruc.edu.cn']
dp = 0
url = rootDomain[dp] + 'index.php'
hrefDone = []
hrefWait = [url]

docref = {} 
num = -1

dlock = threading.Lock()
wlock = threading.Lock()
def geturl():
    global num,hrefWait,hrefDone,dlock,wlock
    if dlock.acquire() and wlock.acquire(): 
        if hrefWait == []:
            return -1,-1
        url = hrefWait.pop(0)
        while(url=='' or url in hrefDone):
            if hrefWait == []:
                return -1,-1
            url = hrefWait.pop(0)
        wlock.release()
        
        hrefDone.append(url)
        hrefDone.sort()
        num += 1
        dlock.release()
    return url,num

def filter(tHref,domain):
    global rootDomain,hrefDone,lock
    tp = 0
    for index, turl in enumerate(tHref) :
        if turl=='':
            continue
        if not turl[:7]=='http://' and not turl[:8]=='https://':
            if ':' in turl:
                tHref[index] = ''
                continue
            if turl[0]=='/':
                tHref[index]=turl[1:]
            tHref[index] = domain + tHref[index]
        if turl[-1]=='/':
            tHref[index] += 'index.php'
        
    tHref.sort()
    
    if dlock.acquire():   
        for index,turl in enumerate(tHref) :
            if turl=='':
                continue
            
            if len(turl)>5 and turl[-5]=='.' and turl[-5:]!='.html' :
                tHref[index] = ''
                
            if len(turl)>4 and turl[-4]=='.' and turl[-4:]!='.htm' and turl[-4:]!='.php':
                tHref[index] = ''
                
            r = 0
            if turl[:7]=='http://' or turl[:8]=='https://':
                for domain in rootDomain :
                    if domain == turl[:len(domain)]:
                        r = 1
                        break
                if not r:
                    tHref[index] = ''
                    continue      
                if len(hrefDone) == 0:
                    continue
                
                while tp < len(hrefDone)-1 and hrefDone[tp] < turl:
                    tp+=1
                if turl == url or turl == hrefDone[tp]:
                    tHref[index] = ''
        dlock.release()
    return tHref

def merge(tHref):
    global hrefWait,wlock
    if wlock.acquire():
        hrefWait += tHref
        hrefWait = list(set(hrefWait))
        hrefWait.sort() 
        
        wlock.release()
    
def run():
    global docref
    while len(hrefWait) != 0:
        url,num = geturl()
        if num == -1:
            return
        
        print(url)
        try:
            html = s.get(url).text
        except Exception as e:
            print('Error:', e)
            return
            
        with codecs.open('bak/%s.bak' % num, 'w','utf-8') as f:
            f.write(html)

        docref[num] = url  
        tHref = re.findall(r'a href="(.*?)"',html) #list
        tHref = list(set(tHref))
        
        tHref = filter(tHref,url[:url.rfind('/')+1])
        merge(tHref)

run()
t=0
tds=[]
for i in range(10):
    tds.append(threading.Thread(target=run))
    tds[i].start()  
for i in range(10):
    tds[i].join()
    
with codecs.open('docref.log', 'w','utf-8') as f:
    json.dump(docref,f,ensure_ascii=False)
    

#rucfd.ruc.edu.cn