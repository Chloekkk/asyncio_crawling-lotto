import requests
from bs4 import BeautifulSoup
import asyncio
import time

s = time.time()
results = []
# async def get_request(url):
#     try:
#         return requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
#     except:
#         get_request(url)

async def get_page(url):
    req = await loop.run_in_executor(None, requests.get, url)
    html = req.text
    soup = await loop.run_in_executor(None, BeautifulSoup, html, 'html.parser')
    return soup

async def main():
    urls = ["https://www.dhlottery.co.kr/gameResult.do?method=byWin&drwNo="+i
            for i in list(list(map(str, range(1, 5))))]
    # 5 -> 811 로 변경
    fts = [asyncio.ensure_future(get_page(u)) for u in urls]
    result = await asyncio.gather(*fts)
    global results
    results = result

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
e = time.time()

print("{0:.2f}초 걸렸습니다".format(e - s))
