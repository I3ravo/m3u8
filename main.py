import requests,re,json,os
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote
from clint.textui import colored
from datetime import datetime
#################################################

web_movie = "https://movie24.tv/category/true-id/"
#web_movie = ""
#web_movie = "https://www.fw4free.com/live.php"
#web_movie = input("\n  กรุณาใส่ URL : ")

f_path = r"/D/w3w"
#f_path = /storage/03FB-19EC/"

#web_movie = input("\n กรุณาใส่ URL :")

#f_path = r"e:\24movietv\\"
#f_path = r"\\"
#################################################
date = datetime.now().strftime("%d")
mo = datetime.now().strftime("%m")
month = [
    '', 'มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน',
    'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม'
]
timeday = f'วันที่ {date} {month[int(mo)]} {int(datetime.now().strftime("%Y"))+543}'
#################################################
fname = unquote(urlparse(web_movie).path.strip('/').split('/')[-1])
wname = unquote(urlparse(web_movie).netloc.strip('.').split('.')[-2])
f_w3u = wname + "_" + fname + ".w3u"
f_m3u = wname + "_" + fname + ".m3u"
#################################################
W_W3U = 0  # 1 = เขียน ไฟล์ w3u
W_M3U = 0  # 1 = เขียน ไฟล์ m3u
#################################################
M_f = 1  # ห้ามแก้
#################################################
aseries = """{
    "name": "",
    "author": "",
    "info": "",
    "image": "",
    "key": []}"""
#################################################
headers = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
jmovie = json.loads(aseries)
jmovie['stations'] = jmovie.pop('key')
jseries = json.loads(aseries)
jseries['groups'] = jseries.pop('key')
parsed_uri = urlparse(web_movie)
referer = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
sess = requests.Session()
sess.headers.update({'User-Agent': headers, 'referer': referer})
home_page = sess.get(web_movie)
home_page.encoding = home_page.apparent_encoding
soup = BeautifulSoup(home_page.content, "html.parser")
page = soup.find(role="navigation")
if page is not None:
    if page.find_all("a"):
        pmax = page.find_all("a")[-2]['href']
        pmax = unquote(urlparse(pmax).path.strip('/').split('/')[-1])
    else:
        pmax = 1
else:
    pmax = 1
jmovie['name'] = jseries['name'] = soup.h2.text.strip()
jmovie['image'] = jseries[
    'image'] = 'https://movie24.tv/wp-content/themes/servermovie/theme/images/Movie24.webp'
jmovie['author'] = jseries['author'] = jseries['author'] + timeday
print(colored.yellow(jmovie['name']))
#print(jseries['name'])
###### แก้สำหรับทดสอบ##
pcurrent = 1
#pmax = 1
###############
pbak = web_movie
for num in range(int(pcurrent), int(pmax) + 1):
    if num == 1:
        plink = pbak = web_movie
        sess.headers.update({'User-Agent': headers, 'referer': referer})
    else:
        plink = "page/%s/" % (num)
        sess.headers.update({'User-Agent': headers, 'referer': pbak})
        plink = pbak = web_movie + plink
    eprint = "Pages [%s/%s] %s" % (num, pmax, plink)
    print(colored.yellow(eprint))
    home_page = sess.get(plink)
    #soup = BeautifulSoup(home_page.content, "lxml")
    div = soup.find(
        "div",
        {"class": "mt-4 grid grid-cols-3 gap-y-5 sm:grid-cols-6 gap-x-5"})
    smax = len(div.find_all('a'))
    for i, link in enumerate(div.find_all("a"), start=1):
        purl = link['href']
        ppic = link.img['data-src']
        ppic = "https" + ppic.split('/https')[-1]
        pname = link.find(
            style="padding-top: 15px; padding-bottom: 10px;").text.strip()
        pinfo1 = link.find(class_="mt-2 text-sm text-white").text.strip()
        if re.search("เสียงไทย", pinfo1):
            pinfo = 'พากย์ไทย'
        else:
            pinfo = 'ซับไทย'
        eprint = "%s\n[Pages: %s/%s No.: %s/%s] %s" % (fname, num, pmax, i,
                                                       smax, pname)
        print(colored.green(eprint))
        view_page = sess.get(purl)
        soup = BeautifulSoup(view_page.content, "lxml")
        if re.search("ขออภัย ไม่พบวิดีโอที่ต้องการ", str(soup)): continue
        jseries['groups'].append({
            "name": pname,
            "image": ppic,
            "info": pinfo,
            "stations": []
        })
        if 'title="ซีรี่ย์"' in str(soup):
            if not 'ตอนที่ 2' in str(soup):
                ptype = 1
            else:
                ptype = 0
            print('ซีรีย์')
        else:
            ptype = 1
            print('หนัง')
        if ptype:
            purl = soup.find("iframe")['data-src']
            view_page = sess.get(purl)
            if re.search('source src="(.+?)"', view_page.text):
                refer = '{uri.scheme}://{uri.netloc}'.format(
                    uri=urlparse(purl))
                elink = refer + re.search('source src="(.+?)"',
                                          view_page.text).group(1)
                view_page = sess.get(elink)
                if re.search('movie_3.m3u8', view_page.text):
                    elink = re.sub(r'movie.m3u8', 'movie_3.m3u8', elink)
                elif re.search('movie_2.m3u8', view_page.text):
                    elink = re.sub(r'movie.m3u8', 'movie_2.m3u8', elink)
                else:
                    elink = elink
            else:
                print('พึ่งรู้ รอแก้ก่อน')
            print((pinfo), " ลิ้งค์ : ", (colored.blue(elink)))
            g1 = len(jseries['groups']) - 1
            if pinfo == 'พากย์ไทย':
                jseries['groups'][g1]['stations'].append({
                    "name":
                    pname,
                    "info":
                    pinfo,
                    "image":
                    ppic,
                    "url":
                    elink,
                    "referer":
                    referer,
                    "subtitle":
                    "https://pastebin.com/raw/cuyErKD4"
                })
            else:
                jseries['groups'][g1]['stations'].append({
                    "name": pname,
                    "info": pinfo,
                    "image": ppic,
                    "url": elink,
                    "referer": referer
                })
            if W_M3U:
                if M_f:
                    with open(f_path + f_m3u, 'w', encoding='utf-8') as f:
                        f.write("#EXTM3U\n")
                        f.close()
                        M_f = 0
                with open(f_path + f_m3u, 'a', encoding='utf-8') as f:
                    f.write(
                        f'#EXTINF:-1 tvg-logo="{ppic}" group-title="{fname}" ,[{pinfo}] {pname}\n'
                    )
                    f.write(f'#EXTVLCOPT:http-referer={referer}\n')
                    f.write(f'{elink}\n')
                    f.close()
            if W_W3U:
                with open(f_path + f_w3u, 'w', encoding='utf-8') as f:
                    json.dump(jseries, f, indent=1, ensure_ascii=False)
        else:
            div = soup.find(class_="mt-right").find(id="single-post")
            divs = div.find_all('a')
            epmax = len(divs)
            for i, link in enumerate((divs), start=1):
                purl = link['onclick'].split("'")[1] + "?web=49"
                ppic = link.img['data-src']
                ename = link.img['alt']
                if "ตอนที่" in ename:
                    ename = "ตอนที่" + ename.split('ตอนที่')[-1]
                elif "EP." in ename:
                    ename = "ตอนที่ " + ename.split('EP.')[-1]
                elif "EP" in ename:
                    ename = "ตอนที่" + ename.split('EP')[-1]
                eprint = "  [%s/%s]  %s" % (i, epmax, ename)
                print(colored.yellow(eprint))
                view_page = sess.get(purl)
                if re.search('source src="(.+?)"', view_page.text):
                    refer = '{uri.scheme}://{uri.netloc}'.format(
                        uri=urlparse(purl))
                    elink = refer + re.search('source src="(.+?)"',
                                              view_page.text).group(1)
                    view_page = sess.get(elink)
                    if re.search('movie_3.m3u8', view_page.text):
                        elink = re.sub(r'movie.m3u8', 'movie_3.m3u8', elink)
                    elif re.search('movie_2.m3u8', view_page.text):
                        elink = re.sub(r'movie.m3u8', 'movie_2.m3u8', elink)
                    else:
                        elink = elink
                else:
                    print('พึ่งรู้ รอแก้ก่อน')
                print((pinfo), " ลิ้งค์ : ", (colored.blue(elink)))
                g1 = len(jseries['groups']) - 1
                if pinfo == 'พากย์ไทย':
                    jseries['groups'][g1]['stations'].append({
                        "name":
                        ename,
                        "info":
                        pinfo,
                        "image":
                        ppic,
                        "url":
                        elink,
                        "referer":
                        referer,
                        "subtitle":
                        "https://pastebin.com/raw/cuyErKD4"
                    })
                else:
                    jseries['groups'][g1]['stations'].append({
                        "name": ename,
                        "info": pinfo,
                        "image": ppic,
                        "url": elink,
                        "referer": referer
                    })
                if W_M3U:
                    if M_f:
                        with open(f_path + f_m3u, 'w', encoding='utf-8') as f:
                            f.write("#EXTM3U\n")
                            f.close()
                            M_f = 0
                    with open(f_path + f_m3u, 'a', encoding='utf-8') as f:
                        f.write(
                            f'#EXTINF:-1 tvg-logo="{ppic}" group-title="playidtv {pname}" ,[{pinfo}] {ename}\n'
                        )
                        f.write(f'#EXTVLCOPT:http-referer={referer}\n')
                        f.write(f'{elink}\n')
                        f.close()
                if W_W3U:
                    with open(f_path + f_w3u, 'w', encoding='utf-8') as f:
                        json.dump(jseries, f, indent=1, ensure_ascii=False)
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
