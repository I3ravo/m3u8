import requests, json, re, os
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote
#############################################################
#web_movie = "https://www.fw4free.com/category.php?cat=movie-thai"
web_movie = "https://www.fw4free.com/category.php?cat=movie-asia"



#################################################
f_path = r"E:\fw4free\\"
# f_path = "C://000.Update_series/"
# os.makedirs(f_path, exist_ok=True)
####################################################
wname = unquote(urlparse(web_movie).netloc.strip('.').split('.')[-2])
fname = unquote(urlparse(web_movie).path.strip('/').split('/')[-1])
f_w3u = f_w3u1 = wname + "_" +fname+".w3u"
f_m3u = f_m3u1 = wname + "_" +fname+".m3u"

W_W3U = 1       
W_M3U = 1       
M_f = 1         
##########################################
aseries = """{
    "name": "",
    "author": "",
    "info": "",
    "image": "",
    "key": []}"""
##########################################
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
logo = "https://fw4free.com/images/logo7.png"
logo = "https://www.icegif.com/wp-content/uploads/2023/10/icegif-969.gif"
jmovie['name'] = wname
jmovie['image'] = logo
jmovie['author'] = jmovie['author']
page = soup.find('li', class_='page-item active')
if page is not None:
    pcurrent = int(page.text.strip())
    pmax = int(soup.find_all('li', class_='page-item')[-2].text.strip())

##########################################
pcurrent = 1
pmax = 1
##########################################
pbak = web_movie
for num in range(pcurrent-1, pmax):
    plink = web_movie if num == 1 else f"{web_movie}&page={num}"
    referer = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(plink))
    sess.headers.update({'User-Agent': str(headers), 'referer': referer})
    eprint = f"\n  หน้าที่ {num+1} จาก {pmax} หน้า"
    soup.clear()
    print(eprint)
    total_series = 0
    home_page = sess.get(plink)
    referer = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(plink))
    sess.headers.update({'User-Agent': str(headers), 'referer': referer})
    soupo = BeautifulSoup(home_page.content, "html.parser")
    container_fluid = soupo.find('div', class_='container-fluid')
    movie_divs = container_fluid.find_all('div', class_='col-4 col-lg-2')
    emax = len(movie_divs)
    for i,movie_div in enumerate(movie_divs,start=1):
        title = movie_div.find('div', class_='p-2 text-truncate').text.strip()
        image_link = movie_div.find('img', class_='img-fluid rounded')['src']
        link = movie_div.find('a')['href']
        total_movies = len(movie_divs)
        total_series += 1
        home_page = sess.get("https://fw4free.com/" + link)
        soupi = BeautifulSoup(home_page.content, "html.parser")
        div_element = soupi.find('div', class_='col-md-4 py-2 col-6 col-sm-5 col-xl-4 text-center')
        sprint = "Page%s>>[%s/%s] %s" % (num+1,i,emax,title)
        print(sprint)
        
        if div_element:
            a_element = div_element.find('a', href=True)
            if a_element:
                video_url = a_element['href']
                matches = re.findall(r"\('([^']+)',\s*'([^']+)'\)", video_url)
                
                if matches:
                    channel_code, video_id = matches[0]
                    url = get_video = f"https://fw4free.com/player2.php?channel={channel_code}&id={video_id}"
                    print(url)

        jmovie['stations'].append({"name":title,"image":image_link,"url":get_video,"referer":referer.replace("www.","")})
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
    