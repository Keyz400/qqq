# import re
# from re import match as rematch, findall, sub as resub, compile as recompile
import requests
# from requests import get as rget
# import base64
# from urllib.parse import unquote, urlparse, parse_qs, quote
# import time
import cloudscraper
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
	if '-' not in url:return 'Use with parameters -10bit -tmb -cine\n/search Moviename -10bit '
	u=url.split('-')
	if u[-1]=='10bit':
		resp=requests.get(f'https://10bitclub.me/?s={u[0]}')
		soup = BeautifulSoup(resp.content, "html.parser")
		l=f'Search Result for {u[0]}\n'
		for i in soup.find_all('div',{'class':'title'}):
			li=i.a
			l+=f'➥<a href="{li["href"]}">{str(i.get_text()).lstrip()}</a> |\n'
		return l
	if u[-1]=='tmb':
		resp=requests.get(f'https://themoviesboss.site/?s={u[0]}')
		soup = BeautifulSoup(resp.content, "html.parser")
		l=f'Search Result for {u[0]}\n'
		for i in soup.find_all('a',{'class':'p-url'}):
			l+=f'➥<a href="{i.get("href")}">{str(i.text).lstrip()}</a>\n'
		return l
	if u[-1]=='cine':
		resp=requests.get(f'https://cinevood.co.uk/?s={u[0]}')
		soup = BeautifulSoup(resp.content, "html.parser")
		l=f'Search Result for {u[0]}\n'
		for i in soup.find_all('article',{'class':"latestPost excerpt"}):
			l+=f'➥<a href="{i.a["href"]}">{str(i.a["title"]).lstrip()}</a>\n'
		for i in soup.find_all('article',{'class':"latestPost excerpt first"}):
			l+=f'➥<a href="{i.a["href"]}">{str(i.a["title"]).lstrip()}</a>\n'
		for i in soup.find_all('article',{'class':"latestPost excerpt last"}):
			l+=f'➥<a href="{i.a["href"]}">{str(i.a["title"]).lstrip()}</a>\n'
		return l
	if u[-1]=='atishmkv':
		client = cloudscraper.create_scraper(allow_brotli=False)
		res=client.get(f'https://atishmkv.wiki/?s={u[0]}')
		soup=BeautifulSoup(res.content,'html.parser')
		l=f'Search Result for {u[0]}\n'
		for i in soup.find_all('h2',{'class':"entry-title"}):
			l+=f'➥<a href="{i.a.get("href")}">{str(i.get_text()).lstrip()}</a> |\n'
		return l
		

