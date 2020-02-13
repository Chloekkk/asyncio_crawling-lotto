import requests
from bs4 import BeautifulSoup
import asyncio
import time
from collections import ChainMap

urls = ["https://www.dhlottery.co.kr/gameResult.do?method=byWin&drwNo="+i
            for i in list(list(map(str, range(1, 100))))] # 5 -> 811 로 변경
s = time.time()
results = []

def get_request(url):
    try:
        return requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
    except:
        get_request(url)

async def get_page(url, index):
    season = index + 1
    req = await loop.run_in_executor(None, get_request, url)
    html = req.text
    soup = await loop.run_in_executor(None, BeautifulSoup, html, 'html.parser')

    winning_numbers = []
    numbers = soup.select("span.ball_645.lrg")
    for num in numbers:
        winning_numbers.append(num.text)
    return {season:winning_numbers}

async def main():
    fts = [asyncio.ensure_future(get_page(u, urls.index(u))) for u in urls]
    result = await asyncio.gather(*fts)
    global results
    # convert list of dict to one dict
    results = dict(ChainMap(*result))
    print(results)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
e = time.time()

print("{0:.2f}초 걸렸습니다".format(e - s))