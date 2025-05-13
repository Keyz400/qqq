import re
from re import match as rematch, findall, sub as resub, compile as recompile
import requests
from requests import get as rget,session
import time
import cloudscraper
from bs4 import BeautifulSoup, NavigableString, Tag
from requests import session
#from anime import set_direct_link
from base64 import standard_b64encode
from json import loads
from math import floor, pow
from os import environ
from re import findall, match, search, sub
from time import sleep
from urllib.parse import quote, unquote, urlparse, parse_qs
from uuid import uuid4

from bs4 import BeautifulSoup
from cfscrape import create_scraper
# fi=open('1231.html','w')
# fi.write(res.text)
# fi.close()
from lxml import etree
from requests import get,session
import requests
from asyncio import sleep as asleep, create_task,gather
import asyncio
import requests
from bs4 import BeautifulSoup

# def tenbit():
#     soup=BeautifulSoup(requests.get('https://10bitclub.me/movies/broker/').content,'html.parser')
#     l=''
#     p=0
#     # for i,j in zip(soup.find_all('span',{'style':"color: #ffffff;"}),soup.find_all('a',{'class':'mb-button'})):
#     #     l+=f'{i.text}\n'
#     #     print(i)
#     #     l+=f'<a href="{j.get("href")}">➥{str(j.text).lstrip()}</a> |\n'
#     #     print(j)
#     #     break
#     for k in soup.find_all('p'):
#         try:
#             # print(k.span.text)
#             l+=f'<a href="{k.span.a("href")}">➥{str(k.span.text).lstrip()}</a> |\n'
#         except:pass
#     return l

# print(tenbit())
#https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://www.infokeeda.xyz/2023/07/myforexfunds-review-2023.html%3Fm%3D1&ved=2ahUKEwiju4TG06CBAxUrSWwGHUamDEIQFnoECBEQAQ&usg=AOvVaw3Op1sNfIWr1dn5oy2ez3U7

#https://ontechhindi.com/token.php?post=stEwF3z

# url='https://techable.site/?id=OHI3eVduQzZ6bHBuYUo5dm9mRTJQT2hZODVGbHJDZHV4Q0NyWEswMlJWc2piMWRvNDhFbENxVEEyTjNCN3F1REpndzBodERlVEgvcXNTMGNubHJtNWk2eGdXem5MekVRNForN3M0T0VuTjVnanlZWkxxREwzaFMwek1aMVVqcXpBL012ckhFNWU5VEF0Q2pzbWEzN0pxQjFRRjVqZGF3OWxRVzFpUnFqL2RRPQ=='
# client = cloudscraper.create_scraper(allow_brotli=False)
# res=client.get(url,allow_redirects=False)
# r=open('12.html','w')
# r.write(res.text)

# def transcript(url: str, DOMAIN: str, ref: str, sltime) -> str:
#     code = url.rstrip("/").split("/")[-1]
#     cget = cloudscraper.create_scraper(allow_brotli=False).request
#     resp = cget("GET", f"{DOMAIN}/{code}", headers={"referer": ref},allow_redirects=False)
#     soup = BeautifulSoup(resp.content, "html.parser")
#     data = { inp.get('name'): inp.get('value') for inp in soup.find_all("input") }
#     print(data)
#     sleep(sltime)
#     resp = cget("POST", f"{DOMAIN}/links/go", data=data, headers={ "x-requested-with": "XMLHttpRequest" })
#     try: 
#         return resp.json()['url']
#     except: 
#         return "Something went wrong :("
# #print(transcript(url,'https://link1s.net','https://nguyenvanbao.com/',0))


# url='https://themoviesboss.online/secret?data=Ym1MRm1xV1JUc2VsM0xyZHVGNFVITitsK1ZzQStCVGFwS2Uvc3dYRkcrV0lwY1NLRVA0YmhNZzFsQ3BQUUI5cXg4azAwSWNXVU15alk1b3RIMXFRK2c9PTo6H8gNM_s_733h1dtQ3d_p_ukr6Q_e__e_'
# cget = cloudscraper.create_scraper(allow_brotli=False).request
# resp = cget("GET", url).url
# print(resp)

import requests

# cookies = {
#     'AppSession': '76e00694ea4fbe8fa997895d51ec6308',
# }

# headers = {
#     'authority': 'go.publicearn.com',
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
#     'accept-language': 'en-GB,en;q=0.5',
#     # 'cookie': 'AppSession=76e00694ea4fbe8fa997895d51ec6308',
#     'referer': 'https://starxinvestor.com/',
#     'sec-ch-ua': '"Brave";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Linux"',
#     'sec-fetch-dest': 'document',
#     'sec-fetch-mode': 'navigate',
#     'sec-fetch-site': 'cross-site',
#     'sec-fetch-user': '?1',
#     'sec-gpc': '1',
#     'upgrade-insecure-requests': '1',
#     'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
# }

# params = {
#     'uid': '350533',
# }
# #, cookies=cookies
# #https://go.publicearn.com/Oe6oRrr/?uid=350533
# response = requests.get('https://go.publicearn.com/Oe6oRrr/', params=params, headers=headers,allow_redirects=False)
# print(response.text)
# # f=open('rr1.html','w')
# # f.write(response.text)

# import requests

# cookies = {
#     'tp': 's0i2WwX',
# }

# headers = {
#     'authority': 'starxinvestor.com',
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
#     'accept-language': 'en-GB,en;q=0.7',
#     'cache-control': 'max-age=0',
#     # 'cookie': 'tp=s0i2WwX',
#     'referer': 'https://www.google.com/',
#     'sec-ch-ua': '"Brave";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Linux"',
#     'sec-fetch-dest': 'document',
#     'sec-fetch-mode': 'navigate',
#     'sec-fetch-site': 'cross-site',
#     'sec-fetch-user': '?1',
#     'sec-gpc': '1',
#     'upgrade-insecure-requests': '1',
#     'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
# }

# response = requests.get(
#     'https://starxinvestor.com/index.php/2023/05/11/best-education-college-in-world-list-top-10-college-in-world-with-their-ranking/',
#     cookies=cookies,
#     headers=headers,
# )
# f=open('rr1.html','w')
# f.write(response.text)

def is_share_link(url):
    return bool(re.search(r'gofile.io|toonshub\.xyz|toonshub\.link|www\.toonshub\.link|www\.toonshub\.xyz|toonworld4all\.me|www\.instagram|youtu|www\.youtu|www\.youtube|indexlink|d\.terabox|mega\.nz|t\.me|telegram|workers\.dev', url))

if is_share_link('https://www.toonshub.link/episode/zom-100-bucket-list-of-the-dead/1x1'):
    print('l')

    