import requests,re,json,os,time
from bs4 import BeautifulSoup
from urllib.parse import urlparse,unquote, parse_qs
from clint.textui import colored
from datetime import datetime
###################################################################################################


web_movie = "https://tongha-movie.com/category/18-amazon%20prime"

###################################################################################################

f_path = r"e:\tongha\\"

os.makedirs(f_path, exist_ok=True)

###################################################################################################
date = datetime.now().strftime("%d")
mo = datetime.now().strftime("%m")
month = ['','มกราคม','กุมภาพันธ์','มีนาคม','เมษายน','พฤษภาคม','มิถุนายน','กรกฎาคม','สิงหาคม','กันยายน','ตุลาคม','พฤศจิกายน','ธันวาคม']
timeday = f'วันที่ {date} {month[int(mo)]} {int(datetime.now().strftime("%Y"))+543}'
timenow =datetime.now().strftime("%H:%M:%S")    
start_time = time.time()
###################################################################################################
fname = unquote(urlparse(web_movie).path.strip('/').split('/')[-1])
wname = unquote(urlparse(web_movie).netloc.strip('.').split('.')[-2])
fname = re.sub(r' ','_',fname)
f_w3u = wname + "_" +fname+ ".w3u"
f_m3u = wname + "_" +fname+ ".m3u"
###################################################################################################
W_W3U = 1       # 1 = เขียน ไฟล์ w3u
W_M3U = 0       # 1 = เขียน ไฟล์ m3u
###################################################################################################
M_f = 1         #ห้ามแก้
S_f = 1         #ห้ามแก้
###################################################################################################
aseries = """{
    "name": "",
    "author": "",
    "info": "",
    "image": "",
    "key": []}"""
headers = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
options.headless = True  
options.add_argument('--ignore-certificate-errors') 
options.add_argument('--incognito') 
#options.add_argument('--headless')  
options.add_argument("--disable-software-rasterizer")   
options.add_argument("--disable-gpu")   
options.add_argument('--no-sandbox')    
options.add_argument('--disable-dev-shm-usage')  
options.add_argument("--window-size=10,10")  
options.add_argument("User-Agent=" + headers)   
prefs = {"profile.managed_default_content_settings.images": 2}  
options.add_experimental_option("prefs", prefs) 
options.add_experimental_option('excludeSwitches', ['enable-automation'])   
options.add_experimental_option('excludeSwitches', ['enable-logging'])  
driver = webdriver.Chrome(options=options)
jmovie = json.loads(aseries)
jmovie['stations'] = jmovie.pop('key')
jseries = json.loads(aseries)
jseries['groups'] = jseries.pop('key')
parsed_uri = urlparse(web_movie)
referer = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(web_movie))
refer = re.sub("\/$","",referer)
sess = requests.Session()
sess.headers.update({'User-Agent': headers,'referer': referer})

driver.get(web_movie)
scroll_pause_time = 2
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # เลื่อนลงสุด
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)

    # คำนวณความสูงใหม่
    new_height = driver.execute_script("return document.body.scrollHeight")

    # ตรวจสอบว่ามีการเลื่อนลงอีกหรือไม่
    if new_height == last_height:
        break  # ถ้าไม่มีการเปลี่ยนแปลงให้หยุด loop
    last_height = new_height

soup = BeautifulSoup(driver.page_source, 'lxml')

div = soup.find_all("div", {"class": "movie-container_tile__370yi"})
pmax = len(div)
fname = soup.h1.text.strip()
fname = re.sub(r'หนังหมวดหมู่ ','',fname)
jseries['name'] = jseries['name'] = fname
jseries['image'] = jseries['image'] = "https://master.server-cdn-streaming.com/uploads/web/1/20210725200620483V.png"
jseries['author'] = jmovie['author'] = jseries['author'] + timeday + " เริ่ม " +timenow


for i, link in enumerate(div, start=1):
    purl = 'https://tongha-movie.com' + link.a['href']
    view_page = sess.get(purl)
    soup = BeautifulSoup(view_page.content, "lxml")
    if 'movie_videoBlock__3BaD8' in str(soup):
        if 'ยังไม่มีวีดิโอ' in soup.find(class_='movie_videoBlock__3BaD8').text:
            print(colored.red('ไม่พบลิ้งค์ (⁠╥⁠﹏⁠╥⁠)'))
            continue
    divs = soup.find('div',class_="movie_row__3sAzM")
    if re.search(r'href="/category/13-Series"',str(divs)):
        ptype = 0
    elif re.search(r'href="/genre/17-Series"',str(divs)):
        ptype = 0
    else:
        ptype = 1
    div = soup.find('div',class_="movie_cover__2CVlN")   
    pname = div.img['alt']
    if re.search(r'\[Zoom\] พากย์ไทย',pname): 
        pinfo = 'Zoom พากย์ไทย'
        zoom = 1
    elif re.search('พากย์ไทย',pname): 
        pinfo = 'พากย์ไทย'
        zoom = 0
    else:
        pinfo = "ซับไทย"
        zoom = 0
    pname = re.sub(r'ดูหนัง','',pname)
    pname = re.sub(r' \[HD\]','',pname)
    pname = re.sub(r' พากย์ไทย/ซับไทย','',pname)
    pname = re.sub(r' พากย์ไทย','',pname)
    pname = re.sub(r' บรรยายไทย','',pname)
    pname = re.sub(r'/พากย์ไทย','',pname)
    pname = re.sub(r' ซาวด์แทร็กซ์','',pname)
    pname = re.sub(r' \[Zoom\]','',pname)
    pname = re.sub(r' ซาวด์แทร็กซ์/พากย์ไทย','',pname)
    pname = re.sub(r'  - - ','',pname)
    ppic = div.img['src']
    eprint = "%s\n เรื่องที่ : %s/%s] %s" % (fname, i, pmax, pname)
    print(colored.yellow(eprint))
    jseries['groups'].append({"name":pname,"image":ppic,"info":pinfo,"stations":[]})
    purl = ppic.split('https://movie.server-cdn-streaming.com/api/uploads/movie/')[-1]
    purls = purl.split('/')[0]
    div = soup.find(id='__NEXT_DATA__')
    if 'https://movie.server-cdn-streaming.com/api/uploads/movie/{purls}/video/' in str(div):
        key = f'"coverImagePath":"https://movie.server-cdn-streaming.com/api/uploads/movie/{purls}/video/(.+?)"'
        divs = re.findall(key,str(div))
    else:
        key = re.findall(r'https://movie.server-cdn-streaming.com/api/video/player/(.+?)"',str(div))
        divs = dict.fromkeys(key)
    emax = len(divs)

    for i, link in enumerate((divs), start=1):
        url = link.split('/')[0]
        view_page = sess.get(urls)
        regex_pattern = re.compile('RESOLUTION=(.+)*\n(.+[-a-zA-Z0-9()@:%_\+.~#?&//=])')
        result = regex_pattern.findall(str(view_page.text))
        results = result[-1][-1]    
        elink  = f'https://movie.server-cdn-streaming.com/api/uploads/movie/{purls}/video/{url}/hls/{results}'
        if emax >=3:
            try:
                pinfo1 = soup.find(class_='movie-video-block_button__1ciQ4 movie-video-block_videoButton__3SSdO button_button__2JlXM').text
            except:
                pinfo1 = soup.find(class_='movie-video-block_button__1ciQ4 movie-video-block_videoButton__3SSdO button_button__2JlXM button_active__HoV_l').text
            if zoom==1: 
                pinfo = 'Zoom พากย์ไทย'
            elif 'เสียงไทย' in pinfo1:
                pinfo = "พากย์ไทย"
            elif 'ซาวด์แทร็ก' in pinfo1:
                    pinfo = "ซับไทย"
            else:
                pinfo = "ซับไทย"
            ename = "ตอนที่ "+str(i)
        elif ptype == 1:
            if i ==1:
                try:
                    pinfo1 = soup.find(class_='movie-video-block_button__1ciQ4 movie-video-block_videoButton__3SSdO button_button__2JlXM').text
                except:
                    pinfo1 = soup.find(class_='movie-video-block_button__1ciQ4 movie-video-block_videoButton__3SSdO button_button__2JlXM button_active__HoV_l').text
                if zoom==1: 
                    pinfo = 'Zoom พากย์ไทย'
                elif 'เสียงไทย' in pinfo1:
                    pinfo = "พากย์ไทย"
                elif 'ซาวด์แทร็ก' in pinfo1:
                        pinfo = "ซับไทย"
                else:
                    pinfo = "ซับไทย"
            else:
                pinfo = "ซับไทย"
            ename = pname
        else:
            try:
                pinfo1 = soup.find(class_='movie-video-block_button__1ciQ4 movie-video-block_videoButton__3SSdO button_button__2JlXM').text
            except:
                pinfo1 = soup.find(class_='movie-video-block_button__1ciQ4 movie-video-block_videoButton__3SSdO button_button__2JlXM button_active__HoV_l').text
            if zoom==1: 
                pinfo = 'Zoom พากย์ไทย'
            elif 'เสียงไทย' in pinfo1:
                pinfo = "พากย์ไทย"
            elif 'ซาวด์แทร็ก' in pinfo1:
                    pinfo = "ซับไทย"
            else:
                pinfo = "ซับไทย"
            ename = "ตอนที่ "+str(i)
        eprint = "[%s/%s]  %s" %  (i,emax,ename)
        print(colored.yellow(eprint))
        print("  ลิ้งค์ ",(pinfo)," : ",(colored.blue(elink)))
        g1 = len(jseries['groups'])-1
        if pinfo =='พากย์ไทย':
            jseries['groups'][g1]['stations'].append({"name":ename,"info":pinfo,"image":ppic,"url":elink,"referer":referer,"subtitle":""}) 
        else:
            jseries['groups'][g1]['stations'].append({"name":ename,"info":pinfo,"image":ppic,"url":elink,"referer":referer})
        if W_M3U:
            if M_f:
                with open(f_path+f_m3u, 'w',encoding='utf-8') as f:
                    f.write("#EXTM3U\n")
                    f.close()
                    M_f = 0
            with open(f_path+f_m3u, 'a',encoding='utf-8') as f:
                f.write(f'#EXTINF:-1 tvg-logo="{ppic}" group-title=" {pname}" ,[{pinfo}] {ename}\n')
                f.write(f'#EXTVLCOPT:http-referer={referer}\n')
                f.write(f'{elink}\n')
                f.close()   
        if W_W3U:
            with open(f_path+f_w3u, 'w',encoding='utf-8') as f:
                json.dump(jseries, f, indent=1, ensure_ascii=False)

timenows =datetime.now().strftime("%H:%M:%S")    
jseries['author'] = jseries['author'] + " เสร็จ " +timenows
if W_W3U:
    with open(f_path+f_w3u, 'w',encoding='utf-8') as f:
        json.dump(jseries, f, indent=1, ensure_ascii=False)
end_time = time.time()
execution_time_seconds = end_time - start_time
hours = execution_time_seconds // 3600
minutes = (execution_time_seconds % 3600) // 60
seconds = execution_time_seconds % 60

print(f"➢ | เวลาที่ใช้ในการรัน: {hours:.0f} ชม. {minutes:.0f} นาที {seconds:.0f} วินาที")
print(f"︎➢ | เริ่มรัน เวลา: {timenow} ดึงเสร็จสิ้น เวลา: {timenows}")

print("------ดึงเสร็จสิ้น------")
if W_W3U:
    out = f_path + f_w3u
    re.sub(r' ', '', out)
    out = "บันทึกไฟล์ W3u ที่ " + out
    print(out)
if W_M3U:
    out = f_path + f_m3u
    re.sub(r' ', '', out)
    out = "บันทึกไฟล์ M3u ที่ " + out
    print(out) 