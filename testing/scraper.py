import re
from re import match as rematch, findall, sub as resub, compile as recompile
import requests
from requests import get as rget
# import base64
# from urllib.parse import unquote, urlparse, parse_qs, quote
import time
# import cloudscraper
from bs4 import BeautifulSoup, NavigableString, Tag
# from lxml import etree
# import hashlib
# import json
# from dotenv import load_dotenv
# load_dotenv()
# from asyncio import sleep as asleep
# import os
# import ddl
# from cfscrape import create_scraper
# from uuid import uuid4
# from requests import session
# from ddl import humanbytes


def scrape(url):
	if '-' not in url:return 'Use with -10bit -tmb -cine'
	print(url)
	u=url.split('-')
	print(u)
	if u[-1]=='10bit':
		resp=requests.get(f'https://10bitclub.me/?s={u[0]}')
		soup = BeautifulSoup(resp.content, "html.parser")
		l='Titles:\n'
		for i in soup.find_all('div',{'class':'title'}):
			li=i.a
			l+=f'➥<a href="{li["href"]}">{str(i.get_text()).lstrip()}</a> |\n'
		return l
	if u[-1]=='tmb':
		resp=requests.get(f'https://themoviesboss.site/?s={u[0]}')
		soup = BeautifulSoup(resp.content, "html.parser")
		l='Titles:\n'
		for i in soup.find_all('a',{'class':'p-url'}):
			l+=f'➥<a href="{i.get("href")}">{str(i.text).lstrip()}</a>\n'
		return l
	if u[-1]=='cine':
		resp=requests.get(f'https://cinevood.motorcycles/?s={u[0]}')
		soup = BeautifulSoup(resp.content, "html.parser")
		l='Titles:\n'
		for i in soup.find_all('article',{'class':"latestPost excerpt"}):
			l+=f'➥<a href="{i.a["href"]}">{str(i.a["title"]).lstrip()}</a>\n'
		for i in soup.find_all('article',{'class':"latestPost excerpt first"}):
			l+=f'➥<a href="{i.a["href"]}">{str(i.a["title"]).lstrip()}</a>\n'
		for i in soup.find_all('article',{'class':"latestPost excerpt last"}):
			l+=f'➥<a href="{i.a["href"]}">{str(i.a["title"]).lstrip()}</a>\n'
		return l

def atozcartoon(word):
	resp=requests.get(f'https://www.atozcartoonist.com/?s={word}')
	soup = BeautifulSoup(resp.content, "html.parser")
	l='Titles:\n'
	for i in soup.find_all('h2',{'class':"entry-title h3"}):
		l+=f'➥<a href="{i.a["href"]}">{str(i.a.text).lstrip()}</a>\n'
	# for i in soup.find_all('article',{'class':"latestPost excerpt first"}):
	# 	l+=f'➥<a href="{i.a["href"]}">{str(i.a["title"]).lstrip()}</a>\n'
	# for i in soup.find_all('article',{'class':"latestPost excerpt last"}):
	# 	l+=f'➥<a href="{i.a["href"]}">{str(i.a["title"]).lstrip()}</a>\n'
	return l

print(atozcartoon('ben 10'))
#re=requests.get('https://www.atozcartoonist.com/2023/08/chhota-bheem-maha-shaitaan-ka-mahayudh-movie-multi-audio-download-480p-sdtv-web-dl.html')
#re=requests.get('https://www.atozcartoonist.com/2022/04/ben-10-reboot-season-2-hindienglish-episodes-download-1080p-fhd.html')
re=requests.get('https://www.atozcartoonist.com/2022/03/ben-10-classic-season-2-episodes-in-hindi-english-download-576p-hevc.html')
soup=BeautifulSoup(re.content,'html.parser')
print('j')
try:
    for i in soup.select('div[class*="mks_accordion_item"]'):
        print(i.text.strip())
        print(i.a['href'])
        l=i.text.strip()
except: print('j')
for i in soup.find_all('strong'):
    try:
        print(i.a['href'])
        print(i.text.strip())
    except:pass
# if l!=None:
#     print('d')
# else:
#     print('Something went Wrong')
for i in soup.find_all('strong'):
    try:
        print(i.a['href'])
        print(i.text.strip())
    except:pass