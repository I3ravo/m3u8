import requests,re,json
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import unquote,parse_qs,quote_plus
from datetime import datetime
#################################################

web_movie = "https://series-indy.com/category/%e0%b8%8b%e0%b8%b5%e0%b8%a3%e0%b8%b5%e0%b8%a2%e0%b9%8c%e0%b8%9d%e0%b8%a3%e0%b8%b1%e0%b9%88%e0%b8%87/"
#web_movie = "https://series-indy.com/genre/acton/"
#################################################
#f_path = r"D:\playlist\อินดี้\\"
f_path = r"e:\series-indy\\"
#################################################
timeday = datetime.now().strftime("%d/%m/%Y")
fname = unquote(urlparse(web_movie).path.strip('/').split('/')[-1])
wname = unquote(urlparse(web_movie).netloc.strip('.').split('.')[-2])
f_w3u = wname + "_" +fname+ "_.w3u"
f_m3u = wname + "_" +fname+ "_.m3u"
#################################################
W_W3U = 0       # 1 = เขียน ไฟล์ w3u 
W_M3U = 1       # 1 = เขียน ไฟล์ m3u 
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

headers = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"

#################################################

jmovie = json.loads(aseries)
jmovie['stations'] = jmovie.pop('key')
jseries = json.loads(aseries)
jseries['groups'] = jseries.pop('key')
parsed_uri = urlparse(web_movie)
referer = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(web_movie))
refer = re.sub("\/$","series-indy.com",referer)
sess = requests.Session()
sess.headers.update({'User-Agent': headers,'referer': referer})
home_page = sess.get(web_movie)
home_page.encoding = home_page.apparent_encoding
soup = BeautifulSoup(home_page.content, "lxml")

page = soup.find("div", {"class": "pagination"})

if page is not None:
    if page.find_all("a"):
        pmax = page.find_all("a")[-2]['href']
        pmax = unquote(urlparse(pmax).path.strip('/').split('/')[-1])
    else:
        pmax = 1
else:
    pmax = 1

jmovie['name'] = jseries['name'] = soup.h1.text.strip()
jmovie['image'] = jseries['image'] = "https://i0.wp.com/series-indy.com/wp-content/uploads/2023/01/series1111.png"
jmovie['author'] = jseries['author'] = jseries['author'] + timeday
###### แก้สำหรับทดสอบ##
pcurrent = 1
#pmax = 1
###############
pbak = web_movie
for num in range(int(pcurrent), int(pmax)+1):
    if num == 1:
        plink = pbak = web_movie
        sess.headers.update({'User-Agent': headers,'referer': referer})
    else:
        plink = "/page/%s" % (num)
        sess.headers.update({'User-Agent': headers,'referer': pbak})
        plink = pbak = web_movie + plink
    eprint = "Pages [%s/%s] %s" % (num,pmax,plink)
    print(eprint)
    home_page = sess.get(plink)
    soup = BeautifulSoup(home_page.content, "lxml")
    div = soup.find("div", {"class": "latest"})
    dbox = div.find_all("article")
    smax = len(div.find_all('a'))
    # print(smax)
    for i, link in enumerate(div.find_all('article'), start=1):
        purl = link.find("a")['href']
        pname = link.find("div",{"class": "addinfox"}).find("h2").text
        pname_en = link.a.find("div",{"class": "addinfox"}).get_text().strip()
        ppic = link.find("img")['data-src']
        ppic = ppic.split('?fit')[0]
        eprint = "[Pages: %s/%s No.: %s/%s] %s" % (num,pmax,i,smax,pname)
        print(eprint)
        view_page = sess.get(purl)
        if view_page.status_code == 404:
            continue
        soup = BeautifulSoup(view_page.content, "html.parser")
        div = soup.find("div", {"class": "epsdlist"})
        if div is None:
            print("no ep for video")
            continue
        emax = len(div.find_all("a"))
        jseries['groups'].append({"name":pname,"info":pname_en,"image":ppic,"stations":[]})
        for j, link in enumerate(div.find_all("a"), start=1):
            ename = link.find("div",{"class":"epl-num"}).get_text().strip()
            #print(ename,end=" >> ")
            ename_s = "ตอน"+ename.rsplit("ตอน")[-1]
            ename_s = "ตอนที่"+ename.rsplit("EP")[-1]
            ename_s = ename.rsplit("-")[-1]
            ename_s = ename_s.replace("EP", "ตอนที่")
            ename_s = ename_s.replace(" ตอนที่", "ตอนที่")
            purl = link['href']
            if purl=="":
                if emax==1:
                    jseries['groups'].pop(-1)
                continue
            if "ok.ru" in purl:   
                if emax==1:
                    jseries['groups'].pop(-1)
                continue
            if "fembed" in purl:   
                if emax==1:
                    jseries['groups'].pop(-1)
                continue
            if purl=="https://series-indy.com/watch/yes-her-majesty-subth-ep-12/":
                if emax==1:
                    jseries['groups'].pop(-1)
                continue
            if purl=="https://series-indy.com/watch/yes-her-majesty-subth-ep-13/":
                if emax==1:
                    jseries['groups'].pop(-1)
                continue
            if purl=="https://series-indy.com/watch/the-red-sleeve-subth-ep-8-v3/":
                if emax==1:
                    jseries['groups'].pop(-1)
                continue
            view_page = sess.get(purl)
            soup = BeautifulSoup(view_page.content, "html.parser")
            eprint2 = "  [%s/%s] %s >> %s" % (j,emax,ename,ename_s)
            print(eprint2)
            # continue
            try:
                if soup.find("iframe").get('src'):
                    purl = soup.find("iframe")['src']
                else:
                    purl = soup.find("iframe")['data-src']
            except Exception as e:
                print(eprint," >>> ค้นหา link ตอนนี้ ไม่เจอ")
                if emax==1:
                    jseries['groups'].pop(-1)
                continue  
            purl = re.sub(r'https://proxy.team-indy.net/', 'https://play.anime-kame.xyz/', purl)
            pbak = purl
            parsed_uri = urlparse(purl)
            referer = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
            sess.headers.update({'User-Agent': headers,'referer': referer})
            if purl=="":
                if emax==1:
                    jseries['groups'].pop(-1)
                continue
            if "ok.ru" in purl:   
                if emax==1:
                    jseries['groups'].pop(-1)
                continue
            if "fembed" in purl:   
                if emax==1:
                    jseries['groups'].pop(-1)
                continue
            if purl=="https://series-indy.com/watch/yes-her-majesty-subth-ep-12/":
                if emax==1:
                    jseries['groups'].pop(-1)
                continue
            if purl=="https://series-indy.com/watch/yes-her-majesty-subth-ep-13/":
                if emax==1:
                    jseries['groups'].pop(-1)
                continue
            if purl=="https://series-indy.com/watch/the-red-sleeve-subth-ep-8-v3/":
                if emax==1:
                    jseries['groups'].pop(-1)
                continue
            
            view_page = sess.get(purl)
            soup = BeautifulSoup(view_page.content, "html.parser")
            purl = str(soup)
            purl = purl.strip()
            purl = re.sub(r'\n', '', purl)
            purl = re.sub(r'\r', '', purl)
            # print(purl)
            # exit()
            if re.search('"GET","(.+?)"',purl):    #re.search("'GET', '(.+?)'",purl):
                elink = re.search('"GET","(.+?)"',purl).group(1)
                if re.search("ajxurl = '(.+?)'",purl):
                    elink = re.search("ajxurl = '(.+?)'",purl).group(1)
                    slug = re.search('slug = "(.+?)"',purl).group(1)
                    purl = elink + slug
                else:
                    continue
                view_page = sess.get(purl)
                data = json.loads(view_page.text)
                elink = data['url']
                # print(elink)
                # exit()
            elif re.search(r"var fulllink = '(.+?)'",purl):
                elink = re.search(r"var fulllink = '(.+?)'",purl).group(1)
            elif re.search('"file":"(.+?)"',purl):
                elink = re.search('"file":"(.+?)"',purl).group(1)
                elink = re.sub(r'\\', '', elink)
                elink = re.sub(r'^//', 'https://', elink)
            elif re.search('null,0,null,"(.+?)"',purl):
                elink = re.search('null,0,null,"(.+?)"',purl).group(1)
            elif re.search("src: '(.+?)'",purl):
                elink = re.search("src: '(.+?)'",purl).group(1)
            else:
                elink = pbak
            if re.search(r"no-video",elink):
                elink = "No Video Link"
            elink = re.search(r'embed/(.*?)/', elink)
            if elink:
                extracted_string = elink.group(1)
                elink = 'https://series-cdn.team-indy.net:8443/vod/' + extracted_string + '/video.mp4/playlist.m3u8'
            print("   elink =",elink)
            g1 = len(jseries['groups'])-1
            jseries['groups'][g1]['stations'].append({"name":ename_s,"image":ppic,"url":elink,"referer":referer})
            if W_M3U:
                if M_f:
                    with open(f_path+f_m3u, 'w',encoding='utf-8') as f:
                        f.write("#EXTM3U\n")
                        f.close()
                        M_f = 0
                with open(f_path+f_m3u, 'a',encoding='utf-8') as f:
                    f.write(f'#EXTINF:-1 tvg-logo="{ppic}" group-title="{pname_en}" ,{ename_s}\n')
                    f.write(f'#EXTVLCOPT:http-referrer={referer}\n')
                    f.write(f'{elink}\n')
                    f.close()   
            if W_W3U:   # ทีละ season
                with open(f_path+f_w3u, 'w',encoding='utf-8') as f:
                    json.dump(jseries, f, indent=1, ensure_ascii=False)

print("-----------------THE END----------------------------------------------------------")
if W_W3U:
    out  = f_path+f_w3u
    re.sub(r' ', '', out)
    out  = "W3u Go to " + out
    print(out)
if W_M3U:
    out  = f_path+f_m3u
    re.sub(r' ', '', out)
    out  = "M3u Go to " + out
    print(out)