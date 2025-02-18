import requests,re,json,os
from bs4 import BeautifulSoup
from urllib.parse import urlparse,unquote
from datetime import datetime
from clint.textui import colored
#################################################
#web_movie = "https://eth4k.com/category/18+"
web_movie = "https://eth4k.com/category/18+"
#web_movie = "https://eth4k.com/category/%E0%B8%AB%E0%B8%99%E0%B8%B1%E0%B8%87%E0%B9%80%E0%B8%AD%E0%B9%80%E0%B8%8A%E0%B8%B5%E0%B8%A2"

web_movie = input("\n กรุณาใส่ URL :")
#################################################
f_path = r"e:\eth4k\eth4k\\"

#f_path = r"D:\playlist\eth4k\\"
os.makedirs(f_path, exist_ok=True)
#################################################
date = datetime.now().strftime("%d")
mo = datetime.now().strftime("%m")
month = ['','มกราคม','กุมภาพันธ์','มีนาคม','เมษายน','พฤษภาคม','มิถุนายน','กรกฎาคม','สิงหาคม','กันยายน','ตุลาคม','พฤศจิกายน','ธันวาคม']
timeday = f'วันที่ {date} {month[int(mo)]} {int(datetime.now().strftime("%Y"))+543}'
#################################################

fname = unquote(urlparse(web_movie).path.strip('/').split('/')[-1])
wname = unquote(urlparse(web_movie).netloc.strip('.').split('.')[-2])
f_w3u = f_w3u1 = wname + "_" +fname+ ".w3u"
f_m3u = f_m3u1 = wname + "_" +fname+ ".m3u"
#################################################
W_W3U = 1       # 1 = เขียน ไฟล์ w3u 
W_M3U = 0       # 1 = เขียน ไฟล์ m3u 
M_S = 1         # 1 = แยก ไฟล์ Movie กับ Series
#################################################
M_f = 1         #ห้ามแก้
S_f = 1         #ห้ามแก้
#################################################
aseries = """{
    "name": "",
    "author": "",
    "info": "",
    "image": "",
    "key": []}"""
#################################################
headers = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.105 Safari/537.36"
#################################################
jmovie = json.loads(aseries)
jmovie['stations'] = jmovie.pop('key')
jseries = json.loads(aseries)
jseries['groups'] = jseries.pop('key')
referer = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(web_movie))
refer = re.sub("\/$","",referer)
sess = requests.Session()
sess.headers.update({'User-Agent': headers,'referer': referer})

home_page = sess.get(web_movie)
soup = BeautifulSoup(home_page.content, "lxml")

page = soup.find("div", {"class": "navigation"})

if page is not None:
    if 'next">ถัดไป' in str(page):
        pmax = page.find_all("a")[-2]['href']
        pmax = pmax.split('=')[-1]
    else:
        pmax = 1
else:
    pmax = 1


def find_hd(elink):
    purl = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(elink))
    view_page = sess.get(elink)
    regex_pattern = re.compile('RESOLUTION=(.+)*\n(.+[-a-zA-Z0-9()@:%_\+.~#?&//=])')
    result = regex_pattern.findall(str(view_page.text))
    if result: 
        try:
            result1 = result[-1]
            purl2 = result1[-1]
        except:
            purl2 = result[-1][-1]  
        purl2 = re.sub(r'^/', '', purl2)
        elink = purl + purl2
    return elink
try:
    fname = soup.h1.text.strip()
except:
    fname = "Home"
fname = fname.split('-')[0]

jmovie['name'] = jseries['name'] = fname
jmovie['image'] = jseries['image'] = "https://www.eth4k.com/images/logo/4ZIGX7Y8BzSjUVJsBwiY9RivoOIsVe6logo_eth4k.png"
jmovie['author'] = jseries['author'] = jseries['author'] + timeday
print(jseries['name'])
#print(pmax)
#exit()
###### แก้สำหรับทดสอบ##
pcurrent = 1
#pmax = 3
###############
pbak = web_movie
for num in range(int(pcurrent), int(pmax)+1):
    if num == 1:
        plink = pbak = web_movie
        sess.headers.update({'User-Agent': headers,'referer': referer})
    else:
        plink = "?page=%s" % (num)
        #sess.headers.update(headers)
        sess.headers.update({'User-Agent': headers,'referer': pbak})
        plink = pbak = web_movie + plink
    eprint = "หน้าที่ [%s/%s] %s" % (num,pmax,plink)
    print(eprint)
    home_page = sess.get(plink)
    if home_page.status_code!=200:
        print(f'{home_page.status_code=}')
        referer = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(plink))    ## 
        sess.headers.update({'User-Agent': headers,'referer': referer})         ## 
        home_page = sess.get(plink)
    soup = BeautifulSoup(home_page.content, "lxml")
    div = soup.find("div", {"class": "box"})
    smax = len(div.find_all("div",{"class": "movie"}))
    if smax==0: break
    for i,link in enumerate(div.find_all("div",{"class": "movie"}), start=1):
        purl = link.a['href']
        pname = link.a.text.strip()
        ppic = link.img['src']
        pinfo1 = link.find(class_="movie-footer").get_text().strip()
        if re.search('Soundtrack(T)',pinfo1):
            pinfo = "ซับไทย"
        if re.search('Soundtrack(E)',pinfo1):
            pinfo = "ซับอังกฤษ"
        else:
            pinfo = "พากย์ไทย"
        eprint = "%s\nหน้าที่ : %s/%s เรื่องที่ : [%s/%s] %s" % (fname,num,pmax,i,smax,pname)
        print(colored.yellow(eprint))
        pbak = purl
        home_page = sess.get(purl)
        soup = BeautifulSoup(home_page.content, "lxml")
        if re.search('class="episode"',str(soup)):
            ptype = 0
        else:
            ptype = 1
        if ptype ==0:
            jseries['groups'].append({"name":pname,"image":ppic,"stations":[]})
            divs = soup.find_all(class_="episode")
            epmax = len(divs)
            for l,links in enumerate(divs, start=1):
                ename = links.div['data-ep-name']
                purl = links.div['data-href']
                if "EP." in ename:
                    ename = "ตอนที่ "+ename.rsplit("EP.")[-1]
                elif "EP " in ename:
                    ename = "ตอนที่ "+ename.rsplit("EP ")[-1]
                else:
                    print(ename)
                    print('ชื่อ พึ่งเจอ')
                    exit()
                eprint = f"     [{l}/{epmax}] : {ename}"
                print(eprint)
                if purl =='':continue
                view_page = sess.get(purl)
                if re.search('lnwplayer',purl): 
                    elink = re.search(r'file: "(.+?)",',view_page.text).group(1)
                    if not 'https' in elink:
                        elink = re.sub("^/","https:/",elink)
                    referer = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(web_movie))
                elif re.search('ok.ru',purl): 
                    elink = purl
                    if not 'https' in elink:
                        elink = re.sub("^/","https:/",elink)
                    referer = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(elink))
                elif re.search('javplayer',purl): 
                    elink = re.search(r'{&quot;stream&quot;:&quot;(.+?)&quot;',view_page.text).group(1)
                    elink = re.sub(r'\\','',elink)
                    referer = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(purl))
                elif re.search('player.nung.tv',purl): 
                    elink = re.search(r"let videoUrl = '(.+?)';",view_page.text).group(1)
                    referer = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(web_movie))
                elif re.search('fpic.cc',purl):
                    elink = purl
                    referer = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(web_movie))
                elif re.search('streaming.tonytonychopper',purl):
                    elink = purl
                    referer = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(elink))
                elif re.search('online225',purl): 
                    try:
                        base = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(purl)).strip('/')
                        sess.headers.update({'User-Agent': headers,'referer': base})
                        ref = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(purl))
                        r = sess.get(purl)
                        ddd = re.search(r'vhash\, (.+?)\, false',r.text).group(1)
                        jddd = json.loads(ddd)
                        dlink = jddd['videoUrl']
                        slink = jddd['videoServer']
                        elink = f'{ref}{dlink}?s={slink}&d='
                        hh = sess.get(elink)
                        elink = hh.text.splitlines()[-1]+'.m3u'
                        referer = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(web_movie))
                    except:
                        print(colored.red('ไม่พบลิ้งค์ (⁠╥⁠﹏⁠╥⁠)'))
                        elink = ''
                elif re.search('playermhd.p2phls',purl):
                    elink = re.search(r'"file":"(.+?)",',view_page.text).group(1)
                    if not 'https' in elink:
                        elink = re.sub("^/","https:/",elink)
                    view_page = sess.get(elink)
                    regex_pattern = re.compile('RESOLUTION=(.+)*\n(.+[-a-zA-Z0-9()@:%_\+.~#?&//=])')
                    result = regex_pattern.findall(str(view_page.text))
                    elink = result[-1][-1]    
                    if not 'https' in elink:
                        elink = re.sub("^/","https:/",elink)
                    referer = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(elink))
                else:
                    print(view_page.text)
                    print(purl)
                    exit()
                    referer = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(web_movie))
                print((pinfo),"     ลิ้งค์ : ",(colored.blue(elink)))
                g1 = len(jseries['groups'])-1
                jseries['groups'][g1]['stations'].append({"name":ename,"info":pinfo,"image":ppic,"url":elink,"referer": referer})
                if W_W3U:
                    #f_w3u = "Series_"+f_w3u1
                    with open(f_path+f_w3u, 'w',encoding='utf-8') as f:
                        json.dump(jseries, f, indent=2, ensure_ascii=False)
                if W_M3U:
                    #f_m3u = "Series_"+f_m3u1
                    if S_f:
                        with open(f_path+f_m3u, 'w',encoding='utf-8') as f:
                            f.write("#EXTM3U\n")
                            f.close()
                            S_f = 0
                    with open(f_path+f_m3u, 'a',encoding='utf-8') as f:
                        f.write(f'#EXTINF:-1 tvg-logo="{ppic}" group-title=" {pname}" ,[{pinfo}] {ename}\n')
                        f.write(f'{elink}\n')
                        f.close()
        else:
            try:
                purl = soup.find("iframe",scrolling="no")['src']
            except:
                print('หาลิ้งค์ไม่เจอ')
                continue
            if purl =='':
                print('หาลิ้งค์ไม่เจอ')
                continue
            elif "ชอบหนัง" in purl:
                print('หาลิ้งค์ไม่เจอ')
                continue
            jseries['groups'].append({"name":pname,"image":ppic,"stations":[]})
            view_page = sess.get(purl)
            if re.search('lnwplayer',purl): 
                elink = re.search(r'file: "(.+?)",',view_page.text).group(1)
                if not 'https' in elink:
                    elink = re.sub("^/","https:/",elink)
                referer = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(web_movie))
            elif re.search('ok.ru',purl): 
                elink = purl
                if not 'https' in elink:
                    elink = re.sub("^/","https:/",elink)
                referer = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(elink))
            elif re.search('javplayer',purl): 
                elink = re.search(r'{&quot;stream&quot;:&quot;(.+?)&quot;',view_page.text).group(1)
                elink = re.sub(r'\\','',elink)
                referer = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(purl))
            elif re.search('player.nung.tv',purl): 
                elink = re.search(r"let videoUrl = '(.+?)';",view_page.text).group(1)
                referer = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(web_movie))
            elif re.search('fpic.cc',purl):
                elink = purl
                referer = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(web_movie))
            elif re.search('streaming.tonytonychopper',purl):
                elink = purl
                referer = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(elink))
            elif re.search('online225',purl): 
                try:
                    base = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(purl)).strip('/')
                    sess.headers.update({'User-Agent': headers,'referer': base})
                    ref = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(purl))
                    r = sess.get(purl)
                    ddd = re.search(r'vhash\, (.+?)\, false',r.text).group(1)
                    jddd = json.loads(ddd)
                    dlink = jddd['videoUrl']
                    slink = jddd['videoServer']
                    elink = f'{ref}{dlink}?s={slink}&d='
                    hh = sess.get(elink)
                    elink = hh.text.splitlines()[-1]+'.m3u'
                    referer = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(web_movie))
                except:
                    print(colored.red('ไม่พบลิ้งค์ (⁠╥⁠﹏⁠╥⁠)'))
                    elink = ''
            elif re.search('playermhd.p2phls',purl):
                elink = re.search(r'"file":"(.+?)",',view_page.text).group(1)
                if not 'https' in elink:
                    elink = re.sub("^/","https:/",elink)
                view_page = sess.get(elink)
                regex_pattern = re.compile('RESOLUTION=(.+)*\n(.+[-a-zA-Z0-9()@:%_\+.~#?&//=])')
                result = regex_pattern.findall(str(view_page.text))
                elink = result[-1][-1]    
                if not 'https' in elink:
                    elink = re.sub("^/","https:/",elink)
                referer = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(elink))
            else:
                print(view_page.text)
                print(purl)
                exit()
            print((pinfo),"   ลิ้งค์ : ",(colored.blue(elink)))
            g1 = len(jseries['groups'])-1
            jseries['groups'][g1]['stations'].append({"name":pname,"info":pinfo,"image":ppic,"url":elink,"referer": referer})
            if W_W3U:
                #f_w3u = "Series_"+f_w3u1
                with open(f_path+f_w3u, 'w',encoding='utf-8') as f:
                    json.dump(jseries, f, indent=2, ensure_ascii=False)
            if W_M3U:
                #f_m3u = "Series_"+f_m3u1
                if S_f:
                    with open(f_path+f_m3u, 'w',encoding='utf-8') as f:
                        f.write("#EXTM3U\n")
                        f.close()
                        S_f = 0
                with open(f_path+f_m3u, 'a',encoding='utf-8') as f:
                    f.write(f'#EXTINF:-1 tvg-logo="{ppic}" group-title=" {wname}" ,[{pinfo}] {pname}\n')
                    f.write(f'#EXTVLCOPT:{referer}\n')
                    f.write(f'{elink}\n')
                    f.close()
        

print("------ดึงเสร็จสิ้น------")
if W_W3U:
    out  = f_path+f_w3u
    re.sub(r' ', '', out)
    out  = "บันทึกไฟล์ W3u ที่ " + out
    print(out)
if W_M3U:
    out  = f_path+f_m3u
    re.sub(r' ', '', out)
    out  = "บันทึกไฟล์ M3u ที่ " + out
    print(out)
