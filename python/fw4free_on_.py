from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, unquote
import json
import re

#web_movie = "https://fw4free.com/category.php?cat=fantasy"
#web_movie = "https://www.fw4free.com/category.php?cat=movie-inter"
#web_movie = "https://www.fw4free.com/category.php?cat=movie-thai"
web_movie = "https://www.fw4free.com/category.php?cat=movie-asia"
#web_movie = ""
#web_movie = "https://www.fw4free.com/live.php"
#web_movie = input("\n  กรุณาใส่ URL : ")

#f_path ="/storage/emulated/0/python/fw4free.com/ดราม่า/"
f_path = r"E:\fw4free\\"

wname = unquote(urlparse(web_movie).netloc.strip('.').split('.')[-2])
fname = unquote(urlparse(web_movie).path.strip('/').split('/')[-1])
f_w3u = f_w3u1 = wname + "_" +fname+".w3u"
f_m3u = f_m3u1 = wname + "_" +fname+".m3u"

W_W3U = 1       
W_M3U = 0       
M_f = 1         

aseries = """{
    "name": "",
    "author": "จากเว็ป",
    "info": "",
    "image": "",
    "key": []}"""

jmovie = json.loads(aseries)
jmovie['stations'] = jmovie.pop('key')

referer = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(web_movie))
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36', 
    'Accept-Language': 'en-US,en;q=0.8',
    'referer': f'{referer}'
}
sess = requests.Session()
home_page = sess.get(web_movie)
soup = BeautifulSoup(home_page.content, "html.parser")

jmovie['name'] = wname
jmovie['image'] = "https://fw4free.com/images/logo7.png"
jmovie['author'] = jmovie['author']

pcurrent = 1
pmax = 1
page = soup.find('li', class_='page-item active')
if page is not None:
    pcurrent = int(page.text.strip())
    pmax = int(soup.find_all('li', class_='page-item')[-2].text.strip())

pbak = web_movie
for num in range(pcurrent, pmax + 1):
    plink = web_movie if num == 1 else f"{web_movie}&page={num}"
    referer = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(plink))
    sess.headers.update({'User-Agent': str(headers), 'referer': referer})
    eprint = f"\n  หน้าที่ {num} จาก {pmax} หน้า"
    soup.clear()
    print(eprint)
    total_series = 0
    home_page = sess.get(plink)
    referer = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(plink))
    sess.headers.update({'User-Agent': str(headers), 'referer': referer})
    soupo = BeautifulSoup(home_page.content, "html.parser")
    container_fluid = soupo.find('div', class_='container-fluid')
    movie_divs = container_fluid.find_all('div', class_='col-4 col-lg-2')
    for movie_div in movie_divs:
        title = movie_div.find('div', class_='p-2 text-truncate').text.strip()
        image_link = movie_div.find('img', class_='img-fluid rounded')['src']
        link = movie_div.find('a')['href']
        total_movies = len(movie_divs)
        total_series += 1
        home_page = sess.get("https://fw4free.com/" + link)
        soupi = BeautifulSoup(home_page.content, "html.parser")
        div_element = soupi.find('div', class_='col-md-4 py-2 col-6 col-sm-5 col-xl-4 text-center')
        
        if div_element:
            a_element = div_element.find('a', href=True)
            if a_element:
                video_url = a_element['href']
                matches = re.findall(r"\('([^']+)',\s*'([^']+)'\)", video_url)
                
                if matches:
                    channel_code, video_id = matches[0]
                    url = f"https://fw4free.com/player2.php?channel={channel_code}&id={video_id}"
                    print("  [{}/{}] {}".format(total_series, total_movies, title))
                    home_page = sess.get(url)
                    soupv = BeautifulSoup(home_page.content, "html.parser")
                    pattern = r"'file': '([^']+)'"
                    matches = re.search(pattern, str(soupv))
                    video_url = matches.group(1)
                    video_url = video_url.split('playlist.m3u8')[0]
                    get_video = video_url+"playlist.m3u8"

        jmovie['stations'].append({"name":title,"image":image_link,"url":get_video,"referer":referer})
        if W_W3U:
            with open(f_path+f_w3u, 'w',encoding='utf-8') as f:
                json.dump(jmovie, f, indent=2, ensure_ascii=False)
        if W_M3U:
            if M_f:
                with open(f_path+f_m3u, 'w',encoding='utf-8') as f:
                    f.write("#EXTM3U\n")
                    f.close()
                    M_f = 0
            with open(f_path+f_m3u, 'a',encoding='utf-8') as f:
                f.write(f'#EXTINF:-1 tvg-logo="{image_link}" group-title="" ,{title}\n')
                f.write(f'#EXTVLCOPT:http-referrer={referer}\n')
                f.write(f'{get_video}\n')
                f.close()
print("จบ")
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
    