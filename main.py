import httpx
import sys
import re
import time
import m3u8
import asyncio
from Crypto.Cipher import AES

async def fetch(client, url):
    for i in range(10):
        response = await client.get(url)
        print(url)
        if response.status_code == 200:
            return key.decrypt(response.content)
            break
        else:
            pass

async def download(url, filename):
    res = httpx.get(url)
    parsed = m3u8.loads(res.text)
    urls = parsed.segments.uri
    global key
    key = AES.new(httpx.get(parsed.keys[0].uri).content, AES.MODE_CBC)
    start = (time.time())
    async with httpx.AsyncClient(
        limits=httpx.Limits(max_connections=len(urls), max_keepalive_connections=0),
        timeout=httpx.Timeout(120)
    ) as client:
        tasks = [fetch(client, url) for url in urls]
        result = await asyncio.gather(*tasks)
        with open(f"{filename}.mp4", "ab") as vid:
            for data in result:
                if data is not None:
                    vid.write(data)
    end = round(time.time())
    print(f"Saved to {filename}.mp4 in {end-start}s")


try:
    url = sys.argv[1]
    res = sys.argv[2]
except:
    raise exit("Invalid usage! Example: python dl.py https://hanime.tv/videos/hentai/hajimete-no-hitozuma-6 720")

if not re.compile(r"https://hanime\.tv/videos/hentai/([A-Za-z0-9]+(-[A-Za-z0-9]+)+)", re.IGNORECASE).match(url):
    raise exit("Invalid URL!")

video_id = url.split("/")[5]
request = httpx.get('https://hanime.tv/api/v8/video?id='+video_id)
streams = request.json()['videos_manifest']['servers'][0]['streams']
for x in streams:
    if x['height'] == res:
        dl_url = x['url']

asyncio.run(download(dl_url, f"{video_id}-{res}p"))