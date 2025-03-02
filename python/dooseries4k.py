import requests,re,json
from bs4 import BeautifulSoup
from urllib.parse import urlparse,unquote,parse_qs
#################################################
web_movie = "https://www.dooseries4k.com/category/%e0%b8%8b%e0%b8%b5%e0%b8%a3%e0%b8%b5%e0%b8%a2%e0%b9%8c%e0%b9%80%e0%b8%81%e0%b8%b2%e0%b8%ab%e0%b8%a5%e0%b8%b5/"

#################################################
f_path = "D:/dooseries4k/"
#################################################
fname = unquote(urlparse(web_movie).path.strip('/').split('/')[-1])
wname = unquote(urlparse(web_movie).netloc.strip('.').split('.')[-2])
f_w3u = f_w3u1 = wname + "_" +fname+ ".w3u"
f_m3u = f_m3u1 = wname + "_" +fname+ ".m3u"
f_preM = "Movie_"
f_preS = "Series_"
#################################################
W_W3U = 0       # 1 = เขียน ไฟล์ w3u 
W_M3U = 1       # 1 = เขียน ไฟล์ m3u 
M_S = 0         # 1 = แยก ไฟล์ Movie กับ Series
#################################################
aseries = """{
    "name": "",
    "author": " PLAYIDTV",
    "info": "DOOSERIES4k",
    "image": "",
    "groups": []}
    """
#################################################
if W_M3U:
    #เขียนหัว M3U
    if M_S:
        f_m3u = f_preM+f_m3u1
        with open(f_path+f_m3u, 'w',encoding='utf-8') as f:
            f.write("#EXTM3U\n")
            f.close()
        f_m3u = f_preS+f_m3u1
        with open(f_path+f_m3u, 'w',encoding='utf-8') as f:
            f.write("#EXTM3U\n")
            f.close()
    else:
        with open(f_path+f_m3u, 'w',encoding='utf-8') as f:
            f.write("#EXTM3U\n")
            f.close()
#######################################################################################   
headers = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
jseries = json.loads(aseries)
referer = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(web_movie))
sess = requests.Session()
sess.headers.update({'User-Agent': headers,'referer': referer})
home_page = sess.get(web_movie)
home_page.encoding = home_page.apparent_encoding
soup = BeautifulSoup(home_page.content, "lxml")

if soup.find_all("div", {"class": "pagination-x"})[-1].find("a"):
    onepage = 0
else:
    onepage = 1
print(soup.title.string)
jseries['name'] = soup.title.string
jseries['image'] = soup.find("img")['src']
jseries['author'] = jseries['author'] + wname
###### แก้สำหรับทดสอบ##
pcurrent = 1

lastpage = 1
###############
pcurrent = int(pcurrent)
while True:
    plink = "page/%s/" % (pcurrent)
    plink = web_movie + plink
    eprint = "[Pages: %s] %s" % (pcurrent,plink)
    print(eprint)
    
    home_page = sess.get(plink)
    soup = BeautifulSoup(home_page.content, "html.parser")    
    div = soup.find("div", {"class": "grid-movie"})
    div_n = soup.find("div", {"class": "nav-links"})
    smax = len(div.find_all("div","movie_box"))
    for i,link in enumerate(div.find_all("div","movie_box"), start=1):
        purl = link.find("a")['href']
        pname = link.find("p").get_text().strip()
        ppic = link.find("img")['src']
        pinfo = link.find_all("span")[-1].get_text().strip()
        ptype = link.find("div", {"class": "ssson"}).get_text().strip()
        referer = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(purl))
        sess = requests.Session()
        sess.headers.update({'User-Agent': headers,'referer': referer})
        home_page = sess.get(purl)
        home_page.encoding = home_page.apparent_encoding
        soup = BeautifulSoup(home_page.content, "lxml")
        eprint = "[Pages: %s/No.: %s/%s] %s" % (pcurrent,i,smax,pname)
        print(eprint)
        if ptype == "Movies":
            purl = soup.find("iframe", {"id": "movie"})['src']
            view_page = sess.get(purl)
            soup = BeautifulSoup(view_page.content, "lxml")
            data = re.search(r"let movieList = (.+?)\;",str(soup)).group(1)
            data = re.sub(r'}, }', '}}', data)
            data = re.sub(r', }', '}', data)
            data = re.sub(r'//', '', data)
            data = re.sub(r'\\', '', data)
            data = re.sub(r'/\*.+?\*/', '', data)
            jcode = json.loads(data)
            if re.search(r'"MU_url": ""',str(soup)):
                continue
            if len(str(jcode['link'])) < 35:
                continue
            jseries['groups'].append({"name":pname,"info":pinfo,"image":ppic,"stations":[]})           
            for num in jcode['sound']:
                elink = jcode['link'][num][0]['MU_url']
                pinfo = jcode['link'][num][0]['MU_sound'].capitalize()#.encode("raw_unicode_escape").decode('utf-8')
                elink = elink.strip()
                elink = elink.replace('/play/','/view/')
                if 'streamhls' in elink:
                    elink = re.sub(r'\?(.+?)$', '', elink)
                else:
                    elink = re.sub(r'\?(.+?)$', '.m3u8', elink)
                if elink == "":
                    continue
                print("     Playlist["+pinfo+"] :",elink,"")
                g1 = len(jseries['groups'])-1
                pname1 = f"{pname}({pinfo})"
                jseries['groups'][g1]['stations'].append({"name":pname1,"info":pinfo,"image":ppic,"url":elink})
                if M_S:
                    f_w3u = f_preM+f_w3u1
                    f_m3u = f_preM+f_m3u1
                if W_W3U:
                    with open(f_path+f_w3u, 'w',encoding='utf-8') as f:
                        json.dump(jseries, f, indent=2, ensure_ascii=False)
                if W_M3U:
                    with open(f_path+f_m3u, 'a',encoding='utf-8') as f:
                        f.write(f'#EXTINF:-1 tvg-logo="{ppic}" group-title="" ,{pname1}\n')
                        #f.write(f'#EXTVLCOPT:http-referrer={pbak}\n')
                        f.write(f'{elink}\n')
                        f.close()
        else:
            purl = soup.find("iframe", {"id": "movie"})['src']
            try:
                sss = int(parse_qs(urlparse(purl).query)['ss'][0])
            except:
                sss = int(0)
            view_page = sess.get(purl)
            soup = BeautifulSoup(view_page.content, "lxml")
            purl = str(soup)
            purl = purl.strip()
            purl = re.sub(r'\n', '', purl)
            purl = re.sub(r'\r', '', purl)
            if re.search(r"let movieList = (.+?)\;",purl):
                data = re.search(r"let movieList = (.+?)\;",purl).group(1)
            else:
                continue
            data = re.sub(r'\s', '', data)
            data = re.sub(r',}', '}', data)
            data = re.sub(r'//', '', data)
            data = re.sub(r'\\', '', data)
            data = re.sub(r'/\*.+?\*/', '', data)
            data = re.sub(r'/\*', '', data)
            site_json = json.loads(data)
            jseries['groups'].append({"name":pname,"info":pinfo,"image":ppic,"stations":[]})
            for ID in site_json['seasonList']:
                if sss != 0 and sss != int(ID):
                    continue
                ss = site_json['seasonList'][ID]['name']
                epmax = len(site_json['seasonList'][ID]['epList'])
                print("Season:",ss)
                # print("มีทั้งหมด",epmax,"ตอน")
                for EP in site_json['seasonList'][ID]['epList']:
                    try:
                        ename = ename1 = site_json['seasonList'][ID]['epList'][EP]['name']
                        esound = len(site_json['seasonList'][ID]['epList'][EP]['sound'])
                    except:
                        continue
                    for num in range(esound):
                        nsound = site_json['seasonList'][ID]['epList'][EP]['sound'][num]
                        pinfo = site_json['seasonList'][ID]['epList'][EP]['link'][nsound][0]['MU_sound'].capitalize()
                        if len(site_json['seasonList']) >1:
                            ename = f'{ss}-{ename1}({pinfo})'
                        else:
                            ename = f'{ename1}({pinfo})'
                        MU_url = site_json['seasonList'][ID]['epList'][EP]['link'][nsound][0]['MU_url']
                        if '/https://' in MU_url:
                            MU_url = 'https://'+MU_url.split('/https://')[-1]
                        if 'https://' not in MU_url:
                            MU_url = MU_url.replace('https:','https://')
                        referer = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(MU_url))
                        sess.headers.update({'User-Agent': headers,'referer': referer})
                        home_page = sess.get(MU_url)
                        soup = BeautifulSoup(home_page.content, "html.parser")
                        purl = str(soup)
                        purl = purl.strip()
                        purl = re.sub(r'\n', '', purl)
                        purl = re.sub(r'\r', '', purl)
                        if re.search('var urlVideo = "(.+?)"',purl):
                            elink = re.search('var urlVideo = "(.+?)"',purl).group(1)
                            elink = re.sub(r'^/', referer, elink)
                        elif re.search('"file":"(.+?)"',purl):
                            elink = re.search('"file":"(.+?)"',purl).group(1)
                            elink = re.sub(r'^//', 'https://', elink)
                        elif re.search('url: "(.+?)"',purl):
                            elink = re.search('url: "(.+?)"',purl).group(1)
                            referer = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(elink))
                            sess.headers.update({'User-Agent': headers,'referer': referer})
                            home_page = sess.get(elink)
                            soup = BeautifulSoup(home_page.content, "html.parser")
                            purl = str(soup)
                            purl = purl.strip()
                            purl = re.sub(r'\n', '', purl)
                            purl = re.sub(r'\r', '', purl)
                            elink = re.search('"embed_link":"(.+?)"',purl).group(1)
                            elink = re.sub(r'\\', '', elink)
                        else:    
                            elink = MU_url
                            elink = re.sub(r'/play/', '/view/', elink)
                            if 'streamhls' in elink:
                                elink = re.sub(r'\?(.+?)$', '', elink)
                            else:
                                elink = re.sub(r'\?(.+?)$', '.m3u8', elink)
                                if '.m3u8' not in elink :
                                    elink = elink + '.m3u8'
                        print("     EP Name  :",ename)
                        print("     Playlist :",elink)
                        referer = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(elink))
                        g1 = len(jseries['groups'])-1
                        jseries['groups'][g1]['stations'].append({"name":ename,"info":pinfo,"image":ppic,"url":elink,"referer":referer})
                        if M_S:
                            f_w3u = f_preS+f_w3u1
                            f_m3u = f_preS+f_m3u1
                        if W_W3U:
                            with open(f_path+f_w3u, 'w',encoding='utf-8') as f:
                                json.dump(jseries, f, indent=2, ensure_ascii=False)
                        if W_M3U:
                            with open(f_path+f_m3u, 'a',encoding='utf-8') as f:
                                f.write(f'#EXTINF:-1 tvg-logo="{ppic}" group-title="{pname}" ,{ename}\n')
                                f.write(f'#EXTVLCOPT:http-referrer={referer}\n')
                                f.write(f'{elink}\n')
                                f.close()  
    if onepage == 0:
        pmax = div_n.find_all("a")[-1].string
    else:
        pmax = 1
    ###### แก้สำหรับทดสอบ####
    #pmax = lastpage
    ################
    #print(pmax)
    if str(pcurrent) == str(pmax):
        break
    pcurrent+=1
    #exit()
print("THE END")
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