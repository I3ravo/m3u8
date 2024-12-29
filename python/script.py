import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote

# Define input movie URL and file path
web_movie = "https://doomovie.win/escape/"
f_path = "D:\\playlist\\"

# Generate file names
fname = unquote(urlparse(web_movie).path.strip('/').split('/')[-1])
wname = unquote(urlparse(web_movie).netloc.strip('.').split('.')[-2])
f_w3u = f"{wname}_{fname}.w3u"
f_m3u = f"{wname}_{fname}.m3u"

# Configuration flag
W_W3U = 1  # Write W3U file if set to 1

# JSON template
aseries = {
    "name": "",
    "author": "PLAYID",
    "info": "PLAYID",
    "image": "",
    "stations": []
}

# HTTP headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
}

# Set up a session
parsed_uri = urlparse(web_movie)
referer = f'{parsed_uri.scheme}://{parsed_uri.netloc}/'
sess = requests.Session()
sess.headers.update({'User-Agent': headers["User-Agent"], 'referer': referer})

# Fetch webpage
response = sess.get(web_movie)
response.encoding = response.apparent_encoding
soup = BeautifulSoup(response.content, "html.parser")

# Extract movie details
jseries['name'] = pname = soup.h2.text.strip() if soup.h2 else "Unknown"
jseries['image'] = ppic = soup.find("meta", {"property": "og:image"})['content'] if soup.find("meta", {"property": "og:image"}) else ""
jseries['stations'].append({
    "name": pname,
    "image": ppic,
    "url": web_movie,
    "referer": referer
})

# Output details
print(jseries['name'])
print(web_movie)

# Write to W3U file if enabled
if W_W3U:
    try:
        with open(f"{f_path}{f_w3u}", 'w', encoding='utf-8') as f:
            json.dump(jseries, f, indent=1, ensure_ascii=False)
        print(f"W3U file created at: {f_path}{f_w3u}")
    except Exception as e:
        print(f"Error writing file: {e}")

print("THE END")
