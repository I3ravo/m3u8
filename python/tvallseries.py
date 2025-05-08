import requests,re,json
from bs4 import BeautifulSoup
from urllib.parse import urlparse,unquote,parse_qs
from clint.textui import colored
from datetime import datetime
#################################################
web_movie = "https://tvallserie.com/"


#################################################
f_path = r"/storage/emulated/0/"
#f_path = "D:\playlist\ไทยออ\เต็ม\\"
#f_path = "/content/drive/MyDrive/output/"
#################################################
date = datetime.now().strftime("%d")
mo = datetime.now().strftime("%m")
month = ['','มกราคม','กุมภาพันธ์','มีนาคม','เมษายน','พฤษภาคม','มิถุนายน','กรกฎาคม','สิงหาคม','กันยายน','ตุลาคม','พฤศจิกายน','ธันวาคม']
timeday = f'วันที่ {date} {month[int(mo)]} {int(datetime.now().strftime("%Y"))+543}'
#################################################

#################################################
fname = unquote(urlparse(web_movie).path.strip('/').split('/')[-1])
wname = unquote(urlparse(web_movie).netloc.strip('.').split('.')[-2])
f_w3u  = wname + "_" +fname+ ".w3u"
f_m3u = wname + "_" + fname + ".m3u"


W_W3U = 0  
W_M3U = 1 

S_f = 1   

#################################################
aseries = """{
    "name": "",
    "author": "",
    "info": "",
    "image": "",
    "groups": []}
    """


#################################################
headers = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
jseries = json.loads(aseries)
parsed_uri = urlparse(web_movie)
referer = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
sess = requests.Session()
sess.headers.update({'User-Agent': headers,'referer': referer})
home_page = sess.get(web_movie)
home_page.encoding = home_page.apparent_encoding
soup = BeautifulSoup(home_page.content, "lxml")
purl = str(home_page.text)
purl = purl.strip()
purl = re.sub(r'\n', '', purl)
purl = re.sub(r'\r', '', purl)

page = soup.find('div', class_='pagination')

if page is not None:
        pcurrent = int(page.find('span', class_='current').get_text(strip=True))
        page_text = page.find('span', text=re.compile(r'Page \d+ of \d+')).text
        pmax = int(page_text.split()[-1])


jseries['name'] = soup.h1.text
jseries['image'] = "https://tvallseries.co/wp-content/uploads/2021/01/logotvseries.png.webp"
jseries['author'] = jseries['author'] + timeday

pcurrent = 1
#pmax = 1
pbak = web_movie
for num in range(int(pcurrent), int(pmax) + 1):
    if num == 1:
        plink = web_movie
        sess.headers.update({'User-Agent': headers, 'referer': referer})
    else:
        plink = "/page/%s" % (num)
        sess.headers.update({'User-Agent': headers, 'referer': referer})
        plink = pbak = web_movie + plink
    eprint = "\n หน้าที่ %s จาก %s หน้า" % (num,pmax)
    #print(eprint)
    
    home_page = sess.get(plink)
    soup = BeautifulSoup(home_page.content, "lxml")
    divs = soup.find(class_="animation-2 items")
    try:
        articles = divs.find_all("article")
    except:
        divs = soup.find(class_="items")
        articles = divs.find_all("article")
    count = len(articles)
    total_count = count
    fetch_count = 0
    
    for j, article in enumerate(articles, start=1):
        pname = article.find("img")['alt']
        ppic = article.find("img")['src']
        pinfo = article.find(style='background-color:#007dbc;').text
        print(pname)
        #print(ppic)
        #print(pinfo)
        jseries['groups'].append({"name":pname,"info":pinfo,"image":ppic,"stations":[]})    
        url = article.find('a')['href']
        sess = requests.Session()
        sess.headers.update({'User-Agent': headers, 'referer': referer})
        home_page = sess.get(url)
        soup = BeautifulSoup(home_page.content, "lxml")
        scrsd = soup.find("div", id='seasons')
        if scrsd is not None:
            seasons = scrsd.find_all("div", class_='se-c')
            for season in seasons:
                season_name = season.find("span", class_='se-t').text.strip()
                if "season" in season_name:
                    season_name = season_name.replace("season","ซีซั่น")
                if "Season" in season_name:
                    season_name = season_name.replace("Season","ซีซั่น")
                div = season.find("ul", {"class": "episodios"})
                pmaxa = len(div.find_all("a"))
                eprint = "\n [หน้า %s/%s] [เรื่อง %s/%s] %s ซีซั่น %s มีทั้งหมด %s ตอน" % (num,pmax,j,count,pname,season_name,pmaxa)
                print(eprint)
                for i, link in enumerate(div.find_all("a"), start=1):
                    purl = link['href']
                    try:
                        if div.find("li", {"class": "none"}):
                            namefb = div.find("li", {"class": "none"})
                    except Exception as e:
                           continue  
                    view_page = sess.get(purl)
                    soup = BeautifulSoup(view_page.content, "lxml")
                    try:
                        if soup.find("div",{"class":"sbox"}).find('h1').text.strip():
                            ename = soup.find("div",{"class":"sbox"}).find('h1').text.strip()
                    except Exception as e:
                           continue
                    if "season" in ename:
                        ename = ename.replace("season","Season")
                    if "EP." in ename:
                        ename = ename.replace("EP.","ตอนที่ ")
                    ename = "ซีซั่น"+ename.rsplit("Season")[-1]
                    if "ok.ru" in purl:   
                        if i==1:
                            jseries['groups'].pop(-1)
                        continue
                    if purl== "":   
                        if i==1:
                            jseries['groups'].pop(-1)
                        continue
                    eprint = "\n ตอนที่ %s จาก %s >> %s" % (i,pmaxa,ename)
                    print(eprint)
                    #exit()
                    #print(str(soup))
                    #exit()
                    try:
                        if soup.find("iframe").get('src'):
                            purl = soup.find("iframe")['src']
                        else:
                            purl = soup.find("iframe")['data-src']
                    except Exception:
                        #print(str(soup))
                        #exit()
                        continue
                    #purl = re.sub(r'https://proxy.team-indy.net/', 'https://play.anime-kame.xyz/', purl)
                    pbak = purl
                    parsed_uri = urlparse(purl)
                    referer = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
                    sess.headers.update({'User-Agent': headers,'referer': referer})
                    if "ok.ru" in purl:   
                        if i==1:
                            jseries['groups'].pop(-1)
                        continue
                    if purl== "":   
                        if i==1:
                            jseries['groups'].pop(-1)
                        continue
                    view_page = sess.get(purl)
                    soup = BeautifulSoup(view_page.content, "lxml")
                    purl = str(soup)
                    purl = purl.strip()
                    purl = re.sub(r'\n', '', purl)
                    purl = re.sub(r'\r', '', purl)
                    #print(pbak)
                    if re.search(r'slug : "(.+?)"',purl):
                        slug = re.search(r'slug : "(.+?)"',purl).group(1)
                        data = {'slug': slug}
                        home_page = sess.post("https://play.tvallserie.com/api/get", data=data)
                        soup = BeautifulSoup(home_page.content, "lxml")
                        purl = str(soup)
                        elink = re.search('"file":"(.+?)"',purl).group(1)
                        elink = re.sub(r'\\', '', elink)
                        elink = re.sub(r'^//', 'https://', elink)
                        #print(elink)
                        #exit()
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
                    print(colored.blue(elink))
                    #print(purl)
                    #exit()
                    g1 = len(jseries['groups'])-1
                    jseries['groups'][g1]['stations'].append({"name":ename,"info":pinfo,"image":ppic,"url":elink})
                    if W_W3U:
                        with open(f_path+f_w3u, 'w',encoding='utf-8') as f:
                            json.dump(jseries, f, indent=2, ensure_ascii=False)
                    if W_M3U:
                        if S_f:
                            with open(f_path+f_m3u, 'w',encoding='utf-8') as f:
                                f.write("#EXTM3U\n")
                                f.close()
                                S_f = 0
                        with open(f_path+f_m3u, 'a',encoding='utf-8') as f:
                            f.write(f'#EXTINF:-1 tvg-logo="{ppic}" group-title="{pname}" ,{ename} {pinfo}\n')
                            f.write(f'#EXTVLCOPT:http-referrer={referer}\n')
                            f.write(f'{elink}\n')
                            f.close()
                
print("THE END")
out  = f_path+f_w3u
re.sub(r' ', '', out)
out  = "Go to " + out
print(out)