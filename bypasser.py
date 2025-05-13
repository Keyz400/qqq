import re
from re import match as rematch, findall, sub as resub, compile as recompile
from re import findall, match, search
import requests
from requests import get as rget
import base64
from urllib.parse import unquote, urlparse, parse_qs, quote
import time
import cloudscraper
#from cloudscraper import create_scraper
from bs4 import BeautifulSoup, NavigableString, Tag
from lxml import etree
from curl_cffi import requests as Nreq
from curl_cffi.requests import Session as cSession
import hashlib
import json
from dotenv import load_dotenv
load_dotenv()
from asyncio import sleep as asleep, create_task,gather
import os
import ddl
from cfscrape import create_scraper
from uuid import uuid4
from requests import Session
from ddl import humanbytes
from animepahe.anime import set_direct_link
from lk21 import Bypass
from base64 import standard_b64encode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
import chromedriver_autoinstaller
##########################################################
# ENVs

GDTOT_CRYPT = "b0lDek5LSCt6ZjVRR2EwZnY4T1EvVndqeDRtbCtTWmMwcGNuKy8wYWpDaz0%3D"
Laravel_Session = os.environ.get("Laravel_Session","")
XSRF_TOKEN = os.environ.get("XSRF_TOKEN","")
DCRYPT = os.environ.get("DRIVEFIRE_CRYPT","cnhXOGVQNVlpeFZlM2lvTmN6Z2FPVWJiSjVBbWdVN0dWOEpvR3hHbHFLVT0%3D")
KCRYPT = os.environ.get("KOLOP_CRYPT","a1V1ZWllTnNNNEZtbkU4Y0RVd3pkRG5UREFJZFlUaC9GRko5NUNpTHNFcz0%3D")
HCRYPT = os.environ.get("HUBDRIVE_CRYPT","UDJvaFFVQjhlUThTN1I4elNSdkJGem1WUVZYUXFvS3FNRWlCeEM1clhnVT0%3D")
KATCRYPT = os.environ.get("KATDRIVE_CRYPT","bzQySHVKSkY0bEczZHlqOWRsSHZCazBkOGFDak9HWXc1emRTL1F6Rm9ubz0%3D")
uid=os.environ.get('PEUID')
print(uid)
class DDLException(Exception):
    """Not method found for extracting direct download link from the http link"""
    pass

############################################################
# Lists

otherslist = ["exe.io","exey.io","sub2unlock.net","sub2unlock.com","rekonise.com","letsboost.net","ph.apps2app.com","mboost.me",
"sub4unlock.com","ytsubme.com","social-unlock.com","boost.ink","goo.gl","shrto.ml"]

gdlist = ["appdrive","driveapp","drivehub","gdflix","drivesharer","drivebit","drivelinks","driveace",
"drivepro","driveseed"]

DDL_REGEX = recompile(r"DDL\(([^),]+)\, (([^),]+)), (([^),]+)), (([^),]+))\)")

POST_ID_REGEX =  recompile(r'"postId":"(\d+)"')

###############################################################

###############################################################
# index scrapper

def scrapeIndex(url, username="none", password="none"):

    def authorization_token(username, password):
        user_pass = f"{username}:{password}"
        return f"Basic {base64.b64encode(user_pass.encode()).decode()}"

          
    def decrypt(string): 
        return base64.b64decode(string[::-1][24:-20]).decode('utf-8')  

    
    def func(payload_input, url, username, password): 
        next_page = False
        next_page_token = "" 

        url = f"{url}/" if url[-1] != '/' else url

        try: headers = {"authorization":authorization_token(username,password)}
        except: return "username/password combination is wrong", None, None

        encrypted_response = requests.post(url, data=payload_input, headers=headers)
        if encrypted_response.status_code == 401: return "username/password combination is wrong", None, None

        try: decrypted_response = json.loads(decrypt(encrypted_response.text))
        except: return "something went wrong. check index link/username/password field again", None, None

        page_token = decrypted_response["nextPageToken"]
        if page_token is None: 
            next_page = False
        else: 
            next_page = True 
            next_page_token = page_token 


        if list(decrypted_response.get("data").keys())[0] != "error":
            file_length = len(decrypted_response["data"]["files"])
            result = ""

            for i, _ in enumerate(range(file_length)):
                files_type   = decrypted_response["data"]["files"][i]["mimeType"]
                if files_type != "application/vnd.google-apps.folder":
                        files_name   = decrypted_response["data"]["files"][i]["name"] 

                        direct_download_link = url + quote(files_name)
                        result += f"• {files_name} :\n{direct_download_link}\n\n"
            return result, next_page, next_page_token

    def format(result):
        long_string = ''.join(result)
        new_list = []

        while len(long_string) > 0:
            if len(long_string) > 4000:
                split_index = long_string.rfind("\n\n", 0, 4000)
                if split_index == -1:
                    split_index = 4000
            else:
                split_index = len(long_string)
                
            new_list.append(long_string[:split_index])
            long_string = long_string[split_index:].lstrip("\n\n")
        
        return new_list

    # main
    x = 0
    next_page = False
    next_page_token = "" 
    result = []

    payload = {"page_token":next_page_token, "page_index": x}   
    print(f"Index Link: {url}\n")
    temp, next_page, next_page_token = func(payload, url, username, password)
    if temp is not None: result.append(temp)
    
    while next_page == True:
        payload = {"page_token":next_page_token, "page_index": x}
        temp, next_page, next_page_token = func(payload, url, username, password)
        if temp is not None: result.append(temp)
        x += 1
        
    if len(result)==0: return None
    return format(result)


##############################################################
# shortners

def gofile_dl(url: str):
    rget = requests.Session()
    resp = rget.get('https://api.gofile.io/createAccount')
    if resp.status_code == 200:
        data = resp.json()
        if data['status'] == 'ok' and data.get('data', {}).get('token', None):
            token = data['data']['token']
        else:
            return(f'ERROR: Failed to Create GoFile Account')
    else:
       return(f'ERROR: GoFile Server Response Failed')
    headers = f'Cookie: accountToken={token}'
    def getNextedFolder(contentId, path):
        params = {'contentId': contentId, 'token': token, 'websiteToken': '7fd94ds12fds4'}
        res = rget.get('https://api.gofile.io/getContent', params=params)
        if res.status_code == 200:
            json_data = res.json()
            if json_data['status'] == 'ok':
                links = {}
                for content in json_data['data']['contents'].values():
                    if content["type"] == "folder":
                        path = path+"/"+content['name']
                        links.update(getNextedFolder(content['id'], path))
                    elif content["type"] == "file":
                        links[content['link']] = path
                return links
            else:
                return(f'ERROR: Failed to Receive All Files List')
        else:
            return(f'ERROR: GoFile Server Response Failed')
    return list([getNextedFolder(url[url.rfind('/')+1:], ""), headers][0].keys())[0]


#################################################
# drivefire

def parse_info_drivefire(res):
    info_parsed = {}
    title = re.findall('>(.*?)<\/h4>', res.text)[0]
    info_chunks = re.findall('>(.*?)<\/td>', res.text)
    info_parsed['title'] = title
    for i in range(0, len(info_chunks), 2):
        info_parsed[info_chunks[i]] = info_chunks[i+1]
    return info_parsed

def drivefire_dl(url,dcrypt):
    client = requests.Session()
    client.cookies.update({'crypt': dcrypt})
    
    res = client.get(url)
    info_parsed = parse_info_drivefire(res)
    info_parsed['error'] = False
    
    up = urlparse(url)
    req_url = f"{up.scheme}://{up.netloc}/ajax.php?ajax=download"
    
    file_id = url.split('/')[-1]
    data = { 'id': file_id }
    headers = {'x-requested-with': 'XMLHttpRequest'}
    
    try:
        res = client.post(req_url, headers=headers, data=data).json()['file']
    except:
        return "Error"#{'error': True, 'src_url': url}
    
    decoded_id = res.rsplit('/', 1)[-1]
    info_parsed = f"https://drive.google.com/file/d/{decoded_id}"
    return info_parsed


##################################################
# kolop

def parse_info_kolop(res):
    info_parsed = {}
    title = re.findall('>(.*?)<\/h4>', res.text)[0]
    info_chunks = re.findall('>(.*?)<\/td>', res.text)
    info_parsed['title'] = title
    for i in range(0, len(info_chunks), 2):
        info_parsed[info_chunks[i]] = info_chunks[i+1]
    return info_parsed

def kolop_dl(url,kcrypt):
    client = requests.Session()
    client.cookies.update({'crypt': kcrypt})
    
    res = client.get(url)
    info_parsed = parse_info_kolop(res)
    info_parsed['error'] = False
    
    up = urlparse(url)
    req_url = f"{up.scheme}://{up.netloc}/ajax.php?ajax=download"
    
    file_id = url.split('/')[-1]
    data = { 'id': file_id }
    headers = { 'x-requested-with': 'XMLHttpRequest'}
    
    try:
        res = client.post(req_url, headers=headers, data=data).json()['file']
    except:
        return "Error"#{'error': True, 'src_url': url}
    
    gd_id = re.findall('gd=(.*)', res, re.DOTALL)[0]
    info_parsed['gdrive_url'] = f"https://drive.google.com/open?id={gd_id}"
    info_parsed['src_url'] = url

    return info_parsed['gdrive_url']


##################################################
# mediafire

def mediafire(url):

    res = requests.get(url, stream=True)
    contents = res.text

    for line in contents.splitlines():
        m = re.search(r'href="((http|https)://download[^"]+)', line)
        if m:
            return m.groups()[0]


####################################################
# zippyshare

def zippyshare(url):
    resp = requests.get(url).text
    surl = resp.split("document.getElementById('dlbutton').href = ")[1].split(";")[0]
    parts = surl.split("(")[1].split(")")[0].split(" ")
    val = str(int(parts[0]) % int(parts[2]) + int(parts[4]) % int(parts[6]))
    surl = surl.split('"')
    burl = url.split("zippyshare.com")[0]
    furl = burl + "zippyshare.com" + surl[1] + val + surl[-2]
    return furl


####################################################
# filercrypt

def getlinks(dlc,client):
    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
    'Accept': 'application/json, text/javascript, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'http://dcrypt.it',
    'Connection': 'keep-alive',
    'Referer': 'http://dcrypt.it/',
    }

    data = {
        'content': dlc,
    }

    response = client.post('http://dcrypt.it/decrypt/paste', headers=headers, data=data).json()["success"]["links"]
    links = ""
    for link in response:
        links = links + link + "\n"
    return links[:-1]


def filecrypt(url):

    client = cloudscraper.create_scraper(allow_brotli=False)
    headers = {
    "authority": "filecrypt.co",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "content-type": "application/x-www-form-urlencoded",
    "dnt": "1",
    "origin": "https://filecrypt.co",
    "referer": url,
    "sec-ch-ua": '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36" 
    }
    

    resp = client.get(url, headers=headers)
    soup = BeautifulSoup(resp.content, "html.parser")

    buttons = soup.find_all("button")
    for ele in buttons:
        line = ele.get("onclick")
        if line !=None and "DownloadDLC" in line:
            dlclink = "https://filecrypt.co/DLC/" + line.split("DownloadDLC('")[1].split("'")[0] + ".html"
            break

    resp = client.get(dlclink,headers=headers)
    return getlinks(resp.text,client)


#####################################################
# dropbox

def dropbox(url):
    return url.replace("www.","").replace("dropbox.com","dl.dropboxusercontent.com").replace("?dl=0","")


######################################################
# shareus

def shareus(url):
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',}
    DOMAIN = "https://us-central1-my-apps-server.cloudfunctions.net"
    sess = requests.session()

    code = url.split("/")[-1]
    params = {'shortid': code, 'initial': 'true', 'referrer': 'https://shareus.io/',}
    response = requests.get(f'{DOMAIN}/v', params=params, headers=headers)

    for i in range(1,4):
        json_data = {'current_page': i,}
        response = sess.post(f'{DOMAIN}/v', headers=headers, json=json_data)

    response = sess.get(f'{DOMAIN}/get_link', headers=headers).json()
    return response["link_info"]["destination"]

#######################################################
# anonfiles

def anonfile(url):

    headersList = { "Accept": "*/*"}
    payload = ""

    response = requests.request("GET", url, data=payload,  headers=headersList).text.split("\n")
    for ele in response:
        if "https://cdn" in ele and "anonfiles.com" in ele and url.split("/")[-2] in ele:
            break

    return ele.split('href="')[1].split('"')[0]


##########################################################
# pixl

def pixl(url):
    count = 1
    dl_msg = ""
    currentpage = 1
    settotalimgs = True
    totalimages = ""
    client = cloudscraper.create_scraper(allow_brotli=False)
    resp = client.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    soup = BeautifulSoup(resp.content, "html.parser")
    if "album" in url and settotalimgs:
        totalimages = soup.find("span", {"data-text": "image-count"}).text
        settotalimgs = False
    thmbnailanch = soup.findAll(attrs={"class": "--media"})
    links = soup.findAll(attrs={"data-pagination": "next"})
    try:
        url = links[0].attrs["href"]
    except BaseException:
        url = None
    for ref in thmbnailanch:
        imgdata = client.get(ref.attrs["href"])
        if not imgdata.status_code == 200:
            time.sleep(5)
            continue
        imghtml = BeautifulSoup(imgdata.text, "html.parser")
        downloadanch = imghtml.find(attrs={"class": "btn-download"})
        currentimg = downloadanch.attrs["href"]
        currentimg = currentimg.replace(" ", "%20")
        dl_msg += f"{count}. {currentimg}\n"
        count += 1
    currentpage += 1
    fld_msg = f"Your provided Pixl.is link is of Folder and I've Found {count - 1} files in the folder.\n"
    fld_link = f"\nFolder Link: {url}\n"
    final_msg = fld_link + "\n" + fld_msg + "\n" + dl_msg
    return final_msg


############################################################
# sirigan  ( unused )

def siriganbypass(url):
    client = requests.Session()
    res = client.get(url)
    url = res.url.split('=', maxsplit=1)[-1]

    while True:
        try: url = base64.b64decode(url).decode('utf-8')
        except: break

    return url.split('url=')[-1]


############################################################
# shorte

def sh_st_bypass(url):    
    client = requests.Session()
    client.headers.update({'referer': url})
    p = urlparse(url)
    
    res = client.get(url)

    sess_id = re.findall('''sessionId(?:\s+)?:(?:\s+)?['|"](.*?)['|"]''', res.text)[0]
    
    final_url = f"{p.scheme}://{p.netloc}/shortest-url/end-adsession"
    params = {
        'adSessionId': sess_id,
        'callback': '_'
    }
    time.sleep(5) # !important
    
    res = client.get(final_url, params=params)
    dest_url = re.findall('"(.*?)"', res.text)[1].replace('\/','/')
    
    return {
        'src': url,
        'dst': dest_url
    }['dst']


#############################################################


def parse_info_sharer(res):
    f = re.findall(">(.*?)<\/td>", res.text)
    info_parsed = {}
    for i in range(0, len(f), 3):
        info_parsed[f[i].lower().replace(' ', '_')] = f[i+2]
    return info_parsed

def sharer_pw(url,Laravel_Session, XSRF_TOKEN, forced_login=False):
    client = cloudscraper.create_scraper(allow_brotli=False)
    client.cookies.update({
        "XSRF-TOKEN": XSRF_TOKEN,
        "laravel_session": Laravel_Session
    })
    res = client.get(url)
    token = re.findall("_token\s=\s'(.*?)'", res.text, re.DOTALL)[0]
    ddl_btn = etree.HTML(res.content).xpath("//button[@id='btndirect']")
    info_parsed = parse_info_sharer(res)
    info_parsed['error'] = True
    info_parsed['src_url'] = url
    info_parsed['link_type'] = 'login'
    info_parsed['forced_login'] = forced_login
    headers = {
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'x-requested-with': 'XMLHttpRequest'
    }
    data = {
        '_token': token
    }
    if len(ddl_btn):
        info_parsed['link_type'] = 'direct'
    if not forced_login:
        data['nl'] = 1
    try: 
        res = client.post(url+'/dl', headers=headers, data=data).json()
    except:
        return info_parsed
    if 'url' in res and res['url']:
        info_parsed['error'] = False
        info_parsed['gdrive_link'] = res['url']
    if len(ddl_btn) and not forced_login and not 'url' in info_parsed:
        # retry download via login
        return sharer_pw(url,Laravel_Session, XSRF_TOKEN, forced_login=True)
    return info_parsed["gdrive_link"]


#################################################################
# gdtot

def gdtot(url):
    cget = cloudscraper.create_scraper(allow_brotli=False)
    try:
        url = cget.get(url).url
        p_url = urlparse(url)
        res = cget.post(f"{p_url.scheme}://{p_url.hostname}/ddl", data={'dl': str(url.split('/')[-1])})
    except Exception as e:
        return(f'{e.__class__.__name__}')
    if (drive_link := findall(r"myDl\('(.*?)'\)", res.text)) and "drive.google.com" in drive_link[0]:
        d_link = drive_link[0]  
    elif GDTOT_CRYPT:
        cget.get(url, cookies={'crypt': GDTOT_CRYPT})
        p_url = urlparse(url)
        js_script = cget.post(f"{p_url.scheme}://{p_url.hostname}/dld", data={'dwnld': url.split('/')[-1]})
        g_id = findall('gd=(.*?)&', js_script.text)
        try:
            decoded_id = b64decode(str(g_id[0])).decode('utf-8')
        except:
            return("Try in your browser, mostly file not found or user limit exceeded!")
        d_link = f'https://drive.google.com/open?id={decoded_id}'
        print(f'2. {d_link}')
    else:
        return('Drive Link not found, Try in your broswer! GDTOT_CRYPT not Provided!')
    soup = BeautifulSoup(cget.get(url).content, "html.parser")
    parse_data = (soup.select('meta[property^="og:description"]')[0]['content']).replace('Download ' , '').rsplit('-', maxsplit=1)
    parse_txt = f'''┎ <b>Name :</b> <i>{parse_data[0]}</i>
┠ <b>Size :</b> <i>{parse_data[-1]}</i>
┃ 
┠ <b>GDToT Link :</b> {url}
'''
    try:
        res=cget.get(url)
        if (tele_link := findall(r"myDl2\('(.*?)'\)", res.text)):
            print(tele_link[0])
            parse_txt += f"┖ <b>Telegram Link :</b> {tele_link[0]}\n"
    except:pass
    parse_txt += f'┠ <b>Index Link :</b> https://indexlink.mrprincebotz.workers.dev/direct.aspx?id={get_gdriveid(d_link)}\n'
    parse_txt += f"┖ <b>Drive Link :</b> {d_link}"
    return parse_txt

##################################################################
# adfly

def decrypt_url(code):
    a, b = '', ''
    for i in range(0, len(code)):
        if i % 2 == 0: a += code[i]
        else: b = code[i] + b
    key = list(a + b)
    i = 0
    while i < len(key):
        if key[i].isdigit():
            for j in range(i+1,len(key)):
                if key[j].isdigit():
                    u = int(key[i]) ^ int(key[j])
                    if u < 10: key[i] = str(u)
                    i = j                   
                    break
        i+=1
    key = ''.join(key)
    decrypted = base64.b64decode(key)[16:-16]
    return decrypted.decode('utf-8')


def adfly(url):
    client = cloudscraper.create_scraper(allow_brotli=False)
    res = client.get(url).text
    out = {'error': False, 'src_url': url}
    try:
        ysmm = re.findall("ysmm\s+=\s+['|\"](.*?)['|\"]", res)[0]
    except:
        out['error'] = True
        return out
    url = decrypt_url(ysmm)
    if re.search(r'go\.php\?u\=', url):
        url = base64.b64decode(re.sub(r'(.*?)u=', '', url)).decode()
    elif '&dest=' in url:
        url = unquote(re.sub(r'(.*?)dest=', '', url))
    out['bypassed_url'] = url
    return out


##############################################################################################        



######################################################################################################
# droplink

def droplink(url):
    client = cloudscraper.create_scraper(allow_brotli=False)
    res = client.get(url, timeout=5)
    
    ref = re.findall("action[ ]{0,}=[ ]{0,}['|\"](.*?)['|\"]", res.text)[0]
    h = {"referer": ref}
    res = client.get(url, headers=h)

    bs4 = BeautifulSoup(res.content, "html.parser")
    inputs = bs4.find_all("input")
    data = {input.get("name"): input.get("value") for input in inputs}
    h = {
            "content-type": "application/x-www-form-urlencoded",
            "x-requested-with": "XMLHttpRequest",
        }
    
    p = urlparse(url)
    final_url = f"{p.scheme}://{p.netloc}/links/go"
    time.sleep(3.1)
    res = client.post(final_url, data=data, headers=h).json()

    if res["status"] == "success": return res["url"]
    return 'Something went wrong :('


#####################################################################################################################
# link vertise

def linkvertise(url):
    params = {'url': url,}
    response = requests.get('https://bypass.pm/bypass2', params=params).json()
    if response["success"]: return response["destination"]
    else: return response["msg"]


###################################################################################################################
# others

def others(url):
    return "API Currently not Available"


#################################################################################################################
# ouo

# RECAPTCHA v3 BYPASS
# code from https://github.com/xcscxr/Recaptcha-v3-bypass
def recaptchaV3(ANCHOR_URL = 'https://www.google.com/recaptcha/api2/anchor?ar=1&k=6Lcr1ncUAAAAAH3cghg6cOTPGARa8adOf-y9zv2x&co=aHR0cHM6Ly9vdW8ucHJlc3M6NDQz&hl=en&v=pCoGBhjs9s8EhFOHJFe8cqis&size=invisible&cb=ahgyd1gkfkhe'):
    rs = Session() 
    rs.headers.update({'content-type': 'application/x-www-form-urlencoded'}) 
    matches = findall('([api2|enterprise]+)\/anchor\?(.*)', ANCHOR_URL)[0] 
    url_base = 'https://www.google.com/recaptcha/' + matches[0] + '/'
    params = matches[1] 
    res = rs.get(url_base + 'anchor', params=params)
    token = findall(r'"recaptcha-token" value="(.*?)"', res.text)[0] 
    params = dict(pair.split('=') for pair in params.split('&')) 
    res = rs.post(url_base + 'reload', params=f'k={params["k"]}', data=f"v={params['v']}&reason=q&c={token}&k={params['k']}&co={params['co']}") 
    return findall(r'"rresp","(.*?)"', res.text)[0]

def ouo(url: str): 
    tempurl = url.replace("ouo.press", "ouo.io") 
    p = urlparse(tempurl)
    id = tempurl.split('/')[-1]
    client = cSession(headers={'authority': 'ouo.io', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8', 'cache-control': 'max-age=0', 'referer': 'http://www.google.com/ig/adde?moduleurl=', 'upgrade-insecure-requests': '1'}) 
    res = client.get(tempurl, impersonate="chrome110") 
    next_url = f"{p.scheme}://{p.hostname}/go/{id}" 
  
    for _ in range(2): 
         if res.headers.get('Location'): 
            break 
         bs4 = BeautifulSoup(res.content, 'lxml') 
         inputs = bs4.form.findAll("input", {"name": compile(r"token$")}) 
         data = { inp.get('name'): inp.get('value') for inp in inputs } 
         data['x-token'] = recaptchaV3()
         res = client.post(next_url, data=data, headers= {'content-type': 'application/x-www-form-urlencoded'}, allow_redirects=False, impersonate="chrome110") 
         next_url = f"{p.scheme}://{p.hostname}/xreallcygo/{id}" 
  
    return  res.headers.get('Location')



####################################################################################################################        
# mdisk

def mdisk(url):
    header = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://mdisk.me/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
         }
    
    inp = url 
    fxl = inp.split("/")
    cid = fxl[-1]

    URL = f'https://diskuploader.entertainvideo.com/v1/file/cdnurl?param={cid}'
    res = requests.get(url=URL, headers=header).json()
    return res['download'] + '\n\n' + res['source']


##################################################################################################################        
# AppDrive or DriveApp etc. Look-Alike Link and as well as the Account Details (Required for Login Required Links only)

def unified(url):

    if ddl.is_share_link(url):
        if 'https://gdtot' in url: return ddl.gdtot(url)
        else: return ddl.sharer_scraper(url)

    try:
        Email = "chzeesha4@gmail.com"
        Password = "zeeshi#789"

        account = {"email": Email, "passwd": Password}
        client = cloudscraper.create_scraper(allow_brotli=False)
        client.headers.update(
            {
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
            }
        )
        data = {"email": account["email"], "password": account["passwd"]}
        client.post(f"https://{urlparse(url).netloc}/login", data=data)
        res = client.get(url)
        key = re.findall('"key",\s+"(.*?)"', res.text)[0]
        ddl_btn = etree.HTML(res.content).xpath("//button[@id='drc']")
        info = re.findall(">(.*?)<\/li>", res.text)
        info_parsed = {}
        for item in info:
            kv = [s.strip() for s in item.split(":", maxsplit=1)]
            info_parsed[kv[0].lower()] = kv[1]
        info_parsed = info_parsed
        info_parsed["error"] = False
        info_parsed["link_type"] = "login"
        headers = {
            "Content-Type": f"multipart/form-data; boundary={'-'*4}_",
        }
        data = {"type": 1, "key": key, "action": "original"}
        if len(ddl_btn):
            info_parsed["link_type"] = "direct"
            data["action"] = "direct"
        while data["type"] <= 3:
            boundary = f'{"-"*6}_'
            data_string = ""
            for item in data:
                data_string += f"{boundary}\r\n"
                data_string += f'Content-Disposition: form-data; name="{item}"\r\n\r\n{data[item]}\r\n'
            data_string += f"{boundary}--\r\n"
            gen_payload = data_string
            try:
                response = client.post(url, data=gen_payload, headers=headers).json()
                break
            except BaseException:
                data["type"] += 1
        if "url" in response:
            info_parsed["gdrive_link"] = response["url"]
        elif "error" in response and response["error"]:
            info_parsed["error"] = True
            info_parsed["error_message"] = response["message"]
        else:
            info_parsed["error"] = True
            info_parsed["error_message"] = "Something went wrong :("
        if info_parsed["error"]:
            return info_parsed
        if "driveapp" in urlparse(url).netloc and not info_parsed["error"]:
            res = client.get(info_parsed["gdrive_link"])
            drive_link = etree.HTML(res.content).xpath(
                "//a[contains(@class,'btn')]/@href"
            )[0]
            info_parsed["gdrive_link"] = drive_link
        info_parsed["src_url"] = url
        if "drivehub" in urlparse(url).netloc and not info_parsed["error"]:
            res = client.get(info_parsed["gdrive_link"])
            drive_link = etree.HTML(res.content).xpath(
                "//a[contains(@class,'btn')]/@href"
            )[0]
            info_parsed["gdrive_link"] = drive_link
        if "gdflix" in urlparse(url).netloc and not info_parsed["error"]:
            res = client.get(info_parsed["gdrive_link"])
            drive_link = etree.HTML(res.content).xpath(
                "//a[contains(@class,'btn')]/@href"
            )[0]
            info_parsed["gdrive_link"] = drive_link

        if "drivesharer" in urlparse(url).netloc and not info_parsed["error"]:
            res = client.get(info_parsed["gdrive_link"])
            drive_link = etree.HTML(res.content).xpath(
                "//a[contains(@class,'btn')]/@href"
            )[0]
            info_parsed["gdrive_link"] = drive_link
        if "drivebit" in urlparse(url).netloc and not info_parsed["error"]:
            res = client.get(info_parsed["gdrive_link"])
            drive_link = etree.HTML(res.content).xpath(
                "//a[contains(@class,'btn')]/@href"
            )[0]
            info_parsed["gdrive_link"] = drive_link
        if "drivelinks" in urlparse(url).netloc and not info_parsed["error"]:
            res = client.get(info_parsed["gdrive_link"])
            drive_link = etree.HTML(res.content).xpath(
                "//a[contains(@class,'btn')]/@href"
            )[0]
            info_parsed["gdrive_link"] = drive_link
        if "driveace" in urlparse(url).netloc and not info_parsed["error"]:
            res = client.get(info_parsed["gdrive_link"])
            drive_link = etree.HTML(res.content).xpath(
                "//a[contains(@class,'btn')]/@href"
            )[0]
            info_parsed["gdrive_link"] = drive_link
        if "drivepro" in urlparse(url).netloc and not info_parsed["error"]:
            res = client.get(info_parsed["gdrive_link"])
            drive_link = etree.HTML(res.content).xpath(
                "//a[contains(@class,'btn')]/@href"
            )[0]
            info_parsed["gdrive_link"] = drive_link
        if info_parsed["error"]:
            return "Faced an Unknown Error!"
        return info_parsed["gdrive_link"]
    except BaseException:
        return "Unable to Extract GDrive Link"


#####################################################################################################
# urls open

def vnshortener(url):
    sess = requests.session()
    DOMAIN = "https://vnshortener.com/"
    org = "https://nishankhatri.xyz"
    PhpAcc = DOMAIN + "link/new.php"
    ref = "https://nishankhatri.com.np/"
    go = DOMAIN + "links/go"

    code = url.split("/")[3]
    final_url = f"{DOMAIN}/{code}/"
    headers = {'authority': DOMAIN, 'origin': org}

    data = {'step_1': code,}
    response = sess.post(PhpAcc, headers=headers, data=data).json()
    id = response["inserted_data"]["id"]
    data = {'step_2': code, 'id': id,}
    response = sess.post(PhpAcc, headers=headers, data=data).json()

    headers['referer'] = ref
    params = {'sid': str(id)}
    resp = sess.get(final_url, params=params, headers=headers)
    soup = BeautifulSoup(resp.content, "html.parser")
    inputs = soup.find_all("input")
    data = { input.get('name'): input.get('value') for input in inputs }

    time.sleep(1)
    headers['x-requested-with'] = 'XMLHttpRequest'
    try:
        r = sess.post(go, data=data, headers=headers).json()
        if r["status"] == "success": return r["url"]
        else: raise
    except: return "Something went wrong :("

def rslinks(url):
      client = requests.session()
      download = rget(url, stream=True, allow_redirects=False)
      v = download.headers["location"]
      code = v.split('ms9')[-1]
      final = f"http://techyproio.blogspot.com/p/short.html?{code}=="
      try: return final
      except: return "Something went wrong :("
def du_link(url):
    client = cloudscraper.create_scraper(allow_brotli=False)
    DOMAIN = "https://du-link.in"
    url = url[:-1] if url[-1] == '/' else url
    code = url.split("/")[-1]
    final_url = f"{DOMAIN}/{code}"
    ref = "https://profitshort.com/"
    h = {"referer": ref}
    resp = client.get(final_url,headers=h,allow_redirects=False)
    soup = BeautifulSoup(resp.content, "html.parser")
    inputs = soup.find_all("input")
    data = { input.get('name'): input.get('value') for input in inputs }
    h = { "x-requested-with": "XMLHttpRequest" }
    time.sleep(0)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try: return r.json()['url']
    except: return "Something went wrong :("
def atozcartoonist(url):
    re=requests.get(url,allow_redirects=False).headers['Location']
    print(re)
    if 'moonlinks' in re:
        link=transcript(re, "https://go.moonlinks.in/", "https://www.akcartoons.in/", 7)
        link='https://drive.google.com/uc?id={link.split("=")[-1]}&export=download'
    elif 'xpshort'in re:
        link=re
    return link

##################################################################################################### 
# bitly + tinyurl

def bitly_tinyurl(url: str) -> str:
    response = requests.get(url).url
    try: return response
    except: return "Something went wrong :("

##################################################################################################### 
# thinfi

def thinfi(url: str) -> str :
    response = requests.get(url)
    soup = BeautifulSoup(response.content,  "html.parser").p.a.get("href")
    try: return soup
    except: return "Something went wrong :("

##################################################################################################### 
# helpers

# check if present in list
def ispresent(inlist,url):
    for ele in inlist:
        if ele in url:
            return True
    return False


async def transcript(url: str, DOMAIN: str, ref: str, sltime) -> str:
    code = url.rstrip("/").split("/")[-1]
    cget = cloudscraper.create_scraper(allow_brotli=False).request
    resp = cget("GET", f"{DOMAIN}/{code}", headers={"referer": ref},allow_redirects=False)
    soup = BeautifulSoup(resp.content, "html.parser")
    data = { inp.get('name'): inp.get('value') for inp in soup.find_all("input") }
    await asleep(sltime)
    resp = cget("POST", f"{DOMAIN}/links/go", data=data, headers={ "x-requested-with": "XMLHttpRequest" })
    try: 
        return resp.json()['url']
    except: 
        return "Something went wrong :("


def get_gdriveid(link):
    if "folders" in link or "file" in link:
        res = search(r"https:\/\/drive\.google\.com\/(?:drive(.*?)\/folders\/|file(.*?)?\/d\/)([-\w]+)", link)
        return res.group(3)
    parsed = urlparse(link)
    return parse_qs(parsed.query)['id'][0]
def get_dl(link):
    return f"https://indexlink.mrprincebotz.workers.dev/direct.aspx?id={get_gdriveid(link)}"


def drivescript(url, crypt, dtype):
    rs = Session()
    resp = rs.get(url)
    title = findall(r'>(.*?)<\/h4>', resp.text)[0]
    size = findall(r'>(.*?)<\/td>', resp.text)[1]
    p_url = urlparse(url)
    
    dlink = ''
    if dtype != "DriveFire":
        try:
            js_query = rs.post(f"{p_url.scheme}://{p_url.hostname}/ajax.php?ajax=direct-download", data={'id': str(url.split('/')[-1])}, headers={'x-requested-with': 'XMLHttpRequest'}).json()
            if str(js_query['code']) == '200':
                dlink = f"{p_url.scheme}://{p_url.hostname}{js_query['file']}"
        except Exception as e:
            LOGGER.error(e)
        
    if not dlink and crypt:
        rs.get(url, cookies={'crypt': crypt})
        try:
            js_query = rs.post(f"{p_url.scheme}://{p_url.hostname}/ajax.php?ajax=download", data={'id': str(url.split('/')[-1])}, headers={'x-requested-with': 'XMLHttpRequest'}).json()
        except Exception as e:
            return(f'{e.__class__.__name__}')
        if str(js_query['code']) == '200':
            dlink = f"{p_url.scheme}://{p_url.hostname}{js_query['file']}"
    
    if dlink:    
        res = rs.get(dlink)
        soup = BeautifulSoup(res.text, 'html.parser')
        gd_data = soup.select('a[class="btn btn-primary btn-user"]')
        parse_txt = f'''┎ <b>Name :</b> <code>{title}</code>
┠ <b>Size :</b> <code>{size}</code>
┃ 
┠ <b>{dtype} Link :</b> {url}'''
        if dtype == "HubDrive":
            parse_txt += f'''\n┠ <b>Instant Link :</b> <a href="{gd_data[1]['href']}">Click Here</a>'''
        if (d_link := gd_data[0]['href']):
            parse_txt += f"\n┠ <b>Index Link :</b> {get_dl(d_link)}"
        parse_txt += f"\n┖ <b>Drive Link :</b> {d_link}"
        return parse_txt
    elif not dlink and not crypt:
        return(f'{dtype} Crypt Not Provided and Direct Link Generate Failed')
    else:
        return(f'{js_query["file"]}')

###################################################################################################### 
#Scrapers
def htpmovies(link):
    client = cloudscraper.create_scraper(allow_brotli=False)
    r = client.get(link, allow_redirects=True).text
    j = r.split('("')[-1]
    url = j.split('")')[0]
    param = url.split("/")[-1]
    DOMAIN = "https://go.theforyou.in"
    final_url = f"{DOMAIN}/{param}"
    resp = client.get(final_url)
    soup = BeautifulSoup(resp.content, "html.parser")    
    try: inputs = soup.find(id="go-link").find_all(name="input")
    except: return "Incorrect Link"
    data = { input.get('name'): input.get('value') for input in inputs }
    h = { "x-requested-with": "XMLHttpRequest" }
    time.sleep(10)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try:
        return r.json()['url']
    except: return "Something went Wrong !!"


def scrappers(link):
 
    try: link = rematch(r"^(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))", link)[0]
    except TypeError: return 'Not a Valid Link.'
    links = []

    if "sharespark" in link:
        gd_txt = ""
        res = rget("?action=printpage;".join(link.split('?')))
        soup = BeautifulSoup(res.text, 'html.parser')
        for br in soup.findAll('br'):
            next_s = br.nextSibling
            if not (next_s and isinstance(next_s,NavigableString)):
                continue
            next2_s = next_s.nextSibling
            if next2_s and isinstance(next2_s,Tag) and next2_s.name == 'br':
              if str(next_s).strip():
                 List = next_s.split()
                 if rematch(r'^(480p|720p|1080p)(.+)? Links:\Z', next_s):
                    gd_txt += f'<b>{next_s.replace("Links:", "GDToT Links :")}</b>\n\n'
                 for s in List:
                      ns = resub(r'\(|\)', '', s)
                      if rematch(r'https?://.+\.gdtot\.\S+', ns):
                         r = rget(ns)
                         soup = BeautifulSoup(r.content, "html.parser")
                         title = soup.select('meta[property^="og:description"]')
                         gd_txt += f"<code>{(title[0]['content']).replace('Download ' , '')}</code>\n{ns}\n\n"
                      elif rematch(r'https?://pastetot\.\S+', ns):
                         nxt = resub(r'\(|\)|(https?://pastetot\.\S+)', '', next_s)
                         gd_txt += f"\n<code>{nxt}</code>\n{ns}\n"
        return gd_txt
  
    elif "htpmovies" in link and "/exit.php" in link:
        return htpmovies(link)
        
    elif "htpmovies" in link:
        prsd = ""
        links = []
        res = rget(link)
        soup = BeautifulSoup(res.text, 'html.parser')
        x = soup.select('a[href^="/exit.php?url="]')
        y = soup.select('h5')
        z = unquote(link.split('/')[-2]).split('-')[0] if link.endswith('/') else unquote(link.split('/')[-1]).split('-')[0]

        for a in x:
            links.append(a['href'])
            prsd = f"Total Links Found : {len(links)}\n\n"
      
        msdcnt = -1
        for b in y:
            if str(b.string).lower().startswith(z.lower()):
                msdcnt += 1
                url = f"https://htpmovies.lol"+links[msdcnt]
                prsd += f"{msdcnt+1}. <b>{b.string}</b>\n{htpmovies(url)}\n\n"
                asleep(5)
        return prsd

    elif "cinevood" in link:
        res=requests.get(link)
        soup=BeautifulSoup(res.content,'html.parser')
        l=''
        ll=[]
        for j in soup.find_all('h6'):
            ll.append(j.text)
        ld=[]
        for i in soup.find_all('div',{'class':"cat-b"}):
            ld.append(f'<a href="{i.a["href"]}">➥{i.a.button.text}</a> |')
        a=0
        for i in ll:
            l+=f'{i}\n{ld[a]}{ld[a+1]}\n'
            a+=2
        return l

    elif "atishmkv" in link:
        prsd = ""
        links = []
        res = rget(link)
        soup = BeautifulSoup(res.text, 'html.parser')
        x = soup.select('a[href^="https://gdflix"]')
        for a in x:
            links.append(a['href'])
        for o in links:
            prsd += o + '\n\n'
        return prsd

    elif "teluguflix" in link:
        gd_txt = ""
        r = rget(link)
        soup = BeautifulSoup (r.text, "html.parser")
        links = soup.select('a[href*="gdtot"]')
        gd_txt = f"Total Links Found : {len(links)}\n\n"
        for no, link in enumerate(links, start=1):
            gdlk = link['href']
            t = rget(gdlk)
            soupt = BeautifulSoup(t.text, "html.parser")
            title = soupt.select('meta[property^="og:description"]')
            gd_txt += f"{no}. <code>{(title[0]['content']).replace('Download ' , '')}</code>\n{gdlk}\n\n"
            asleep(1.5)
        return gd_txt
    
    elif "taemovies" in link:
        gd_txt, no = "", 0
        r = rget(link)
        soup = BeautifulSoup (r.text, "html.parser")
        links = soup.select('a[href*="shortingly"]')
        gd_txt = f"Total Links Found : {len(links)}\n\n"
        for a in links:
            glink = transcript(a["href"], "https://insurance.techymedies.com/", "https://highkeyfinance.com/", 5)
            t = rget(glink)
            soupt = BeautifulSoup(t.text, "html.parser")
            title = soupt.select('meta[property^="og:description"]')
            no += 1
            gd_txt += f"{no}. {(title[0]['content']).replace('Download ' , '')}\n{glink}\n\n"
        return gd_txt
    
    elif "animeremux" in link:
        gd_txt, no = "", 0
        r = rget(link)
        soup = BeautifulSoup (r.text, "html.parser")
        links = soup.select('a[href*="urlshortx.com"]')
        gd_txt = f"Total Links Found : {len(links)}\n\n"
        for a in links:
            link = a["href"]
            x = link.split("url=")[-1]
            gd_txt+=f'➥ {x}\n'
        return gd_txt
    
    elif "skymovieshd" in link:
        gd_txt = ""
        res = rget(link, allow_redirects=False)
        soup = BeautifulSoup(res.text, 'html.parser')
        a = soup.select('a[href^="https://howblogs.xyz"]')
        t = soup.select('div[class^="Robiul"]')
        gd_txt += f"<i>{t[-1].text.replace('Download ', '')}</i>\n\n"
        gd_txt += f"<b>{a[0].text} :</b> \n"
        nres = rget(a[0]['href'], allow_redirects=False)
        nsoup = BeautifulSoup(nres.text, 'html.parser')
        atag = nsoup.select('div[class="cotent-box"] > a[href]')
        for no, link in enumerate(atag, start=1):
            gd_txt += f"➥ {link['href']}\n"
        return gd_txt

    elif "animekaizoku" in link:
        global post_id
        gd_txt = ""
        try: website_html = rget(link).text
        except: return "Please provide the correct episode link of animekaizoku"
        try:
            post_id = POST_ID_REGEX.search(website_html).group(0).split(":")[1].split('"')[1]
            payload_data_matches = DDL_REGEX.finditer(website_html)
        except: return "Something Went Wrong !!"

        for match in payload_data_matches:
            payload_data = match.group(0).split("DDL(")[1].replace(")", "").split(",")
            payload = {
               "action" : "DDL",
               "post_id": post_id,
               "div_id" : payload_data[0].strip(),
               "tab_id" : payload_data[1].strip(),
               "num"    : payload_data[2].strip(),
               "folder" : payload_data[3].strip(),
            }
            del payload["num"]     
            link_types = "DDL" if payload["tab_id"] == "2" else "WORKER" if payload["tab_id"] == "4" else "GDRIVE"
            response = rpost("https://animekaizoku.com/wp-admin/admin-ajax.php",headers={"x-requested-with": "XMLHttpRequest", "referer": "https://animekaizoku.com"}, data=payload)
            soup = BeautifulSoup(response.text, "html.parser")  
            downloadbutton = soup.find_all(class_="downloadbutton")

            with concurrent.futures.ThreadPoolExecutor() as executor:
                for button in downloadbutton:
                    if button.text == "Patches": pass
                    else:
                        dict_key = button.text.strip()
                        data_dict[dict_key] = []
                        executor.submit(looper, dict_key, str(button))
            main_dict[link_types] = deepcopy(data_dict)
            data_dict.clear()

        to_edit = False
        for key in main_dict:
            gd_txt += f"----------------- <b>{key}</b> -----------------\n"
            dict_data = main_dict[key]

            if bool(dict_data) == 0:
                gd_txt += "No Links Found\n"
            else:
                for y in dict_data:
                    gd_txt += f"\n○ <b>{y}</b>\n"
                    for no, i in enumerate(dict_data[y], start=1):
                        try: gd_txt += f"➥ {no}. <i>{i[0]}</i> : {i[1]}\n"
                        except: pass
                    asleep(5)
        return gd_txt

    else:
        res = rget(link)
        soup = BeautifulSoup(res.text, 'html.parser')
        mystx = soup.select(r'a[href^="magnet:?xt=urn:btih:"]')
        for hy in mystx:
            links.append(hy['href'])
        return links


###################################################
# script links

def getfinal(domain, url, sess):

    #sess = requests.session()
    res = sess.get(url)
    soup = BeautifulSoup(res.text,"html.parser")
    soup = soup.find("form").findAll("input")
    datalist = []
    for ele in soup:
        datalist.append(ele.get("value"))

    data = {
            '_method': datalist[0],
            '_csrfToken': datalist[1],
            'ad_form_data': datalist[2],
            '_Token[fields]': datalist[3],
            '_Token[unlocked]': datalist[4],
        }

    sess.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': domain,
            'Connection': 'keep-alive',
            'Referer': url,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            }

    # print("waiting 10 secs")
    time.sleep(10) # important
    response = sess.post(domain+'/links/go', data=data).json()
    furl = response["url"]
    return furl


def getfirst(url):

    sess = requests.session()
    res = sess.get(url)

    soup = BeautifulSoup(res.text,"html.parser")
    soup = soup.find("form")
    action = soup.get("action")
    soup = soup.findAll("input")
    datalist = []
    for ele in soup:
        datalist.append(ele.get("value"))
    sess.headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Origin': action,
        'Connection': 'keep-alive',
        'Referer': action,
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
    }

    data = {'newwpsafelink': datalist[1], "g-recaptcha-response": RecaptchaV3()}
    response = sess.post(action, data=data)
    soup = BeautifulSoup(response.text, "html.parser")
    soup = soup.findAll("div", class_="wpsafe-bottom text-center")
    for ele in soup:
        rurl = ele.find("a").get("onclick")[13:-12]

    res = sess.get(rurl)
    furl = res.url
    # print(furl)
    return getfinal(f'https://{furl.split("/")[-2]}/',furl,sess)

def decodeKey(encoded):
        key = ''

        i = len(encoded) // 2 - 5
        while i >= 0:
            key += encoded[i]
            i = i - 2
        
        i = len(encoded) // 2 + 4
        while i < len(encoded):
            key += encoded[i]
            i = i + 2

        return key

def bypassBluemediafiles(url, torrent=False):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Alt-Used': 'bluemediafiles.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',

    }

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    script = str(soup.findAll('script')[3])
    encodedKey = script.split('Create_Button("')[1].split('");')[0]


    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': url,
        'Alt-Used': 'bluemediafiles.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
    }

    params = { 'url': decodeKey(encodedKey) }
    
    if torrent:
        res = requests.get('https://dl.pcgamestorrents.org/get-url.php', params=params, headers=headers)
        soup = BeautifulSoup(res.text,"html.parser")
        furl = soup.find("a",class_="button").get("href")

    else:
        res = requests.get('https://bluemediafiles.com/get-url.php', params=params, headers=headers)
        furl = res.url
        if "mega.nz" in furl:
            furl = furl.replace("mega.nz/%23!","mega.nz/file/").replace("!","#")

    #print(furl)
    return furl

def igggames(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text,"html.parser")
    soup = soup.find("div",class_="uk-margin-medium-top").findAll("a")

    bluelist = []
    for ele in soup:
        bluelist.append(ele.get('href'))
    bluelist = bluelist[6:-1]

    links = ""
    for ele in bluelist:
        if "bluemediafiles" in ele:
            links = links + bypassBluemediafiles(ele) + "\n"
        elif "pcgamestorrents.com" in ele:
            res = requests.get(ele)
            soup = BeautifulSoup(res.text,"html.parser")
            turl = soup.find("p",class_="uk-card uk-card-body uk-card-default uk-card-hover").find("a").get("href")
            links = links + bypassBluemediafiles(turl,True) + "\n"
        else:
            links = links + ele + "\n"

    return links[:-1]
def try2link_bypass(url):
    client = cloudscraper.create_scraper(allow_brotli=False)
    
    url = url[:-1] if url[-1] == '/' else url
    print(f'ry2link_bp {url}')
    params = (('d', int(time.time()) + (60 * 4)),)
    r = client.get(url, params=params, headers= {'Referer': 'https://newforex.online/'})
    
    soup = BeautifulSoup(r.text, 'html.parser')
    inputs = soup.find(id="go-link").find_all(name="input")
    data = { input.get('name'): input.get('value') for input in inputs }    
    time.sleep(7)
    
    headers = {'Host': 'try2link.com', 'X-Requested-With': 'XMLHttpRequest', 'Origin': 'https://try2link.com', 'Referer': url}
    
    bypassed_url = client.post('https://try2link.com/links/go', headers=headers,data=data)
    return bypassed_url.json()["url"]

def try2link_scrape(url):
    client = cloudscraper.create_scraper(allow_brotli=False)    
    h = {
    'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }
    res = client.get(url, cookies={}, headers=h)
    print(res.headers)
    url = 'https://try2link.com/'+re.findall('try2link\.com\/(.*?) ', res.text)[0]
    print(url)
    return try2link_bypass(url)
    

def psa_bypasser(psa_url):
    cookies = {'cf_clearance': 'EgNaZUZVvICwi_V.34D6bTmYzyp24zoY_SFrC2vqm7U-1694540798-0-1-530db2b8.dee7f907.c12667d1-0.2.1694540798' }
    headers = {
        'authority': 'psa.wf',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://psa.wf/',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    }

    r = requests.get(psa_url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(r.text, "html.parser").find_all(class_="dropshadowboxes-drop-shadow dropshadowboxes-rounded-corners dropshadowboxes-inside-and-outside-shadow dropshadowboxes-lifted-both dropshadowboxes-effect-default")
    links = []
    for link in soup:
        try:
            exit_gate = link.a.get("href")
            if "/exit" in exit_gate:
                print("scraping :",exit_gate)
                links.append(try2link_scrape(exit_gate))
        except: pass
    return links
def themoviesboss(url):
    script=requests.get(url).text
    match = re.search('window\.location\.href="(.*?)"', script)
    if match:
        url = match.group(1)
        if url=='https://themoviesboss.site':
            return 'File not Found'
        else:
            return f'link:{url}\nBypass link: {shortners(url)}'
def moviesboss(url):
    script=requests.get(url)
    soup=BeautifulSoup(script.content,'html.parser')
    l=''
    def boss(url):
        script=requests.get(url).text
        match = re.search('window\.location\.href="(.*?)"', script)
        if match:
            url = match.group(1)
            if url=='https://themoviesboss.site':
                return 'https://themoviesboss.site'
            else:
                return f'{(url)}'
    for p,q in zip(soup.find_all('p',{'style':"text-align: center;"}),soup.find_all('a', class_='maxbutton-2 maxbutton')):
        aa=p.strong.text.strip().split('\n')[0]
        l+=f"➥<a href='{boss(q['href'])}'>{aa}</a> |\n"
        
    return l
def tenbit(url):
    res=requests.get(url)
    soup=BeautifulSoup(res.content,'html.parser')
    l=''
    # for i in soup.find_all('span',{'style':"color: #ffffff;"}):
    #     l+=f'{i.text}'
    l+='\nLinks: '
    for i in soup.find_all('a',{'class':'mb-button'}):
        l+=f'<a href="{i.get("href")}">➥{str(i.text).lstrip()}</a> |'
    return l
def animepahe(link):
    client = cloudscraper.session()
    res = client.get(link)
    soup = BeautifulSoup(res.text, "html.parser")
    l = soup.find_all("div", id="pickDownload")
    l2 = []
    l3 = []
    s = f"{soup.find('title').text}\n"
    print(s)
    for i in l:
        for j in i.find_all("a"):
            l2.append(str(j.text).replace("SubsPlease · ",""))
            res1 = client.get(j.get('href')).text
            soup1 = BeautifulSoup(res1, "html.parser")
            l3.append(set_direct_link(soup1.find("a", class_="redirect").get('href')))
    for a,b in zip(l2,l3):
        s += f'<a href="{b}">➳ {a}| </a>'
    return s
async def atishmkv(url):
    client = cloudscraper.create_scraper(allow_brotli=False)
    res=client.get(url)
    soup=BeautifulSoup(res.content,'html.parser')
    l=f'Title:{soup.find("title").text}\n'
    for i in soup.find_all('a', class_="button button-shadow"):
        l+=f'➥<a href="{i.get("href")}">{str(i.get_text()).lstrip()}</a> |\n'
    return l
async def telegraph_scaper(url):
    res=requests.get(url)
    soup=BeautifulSoup(res.content,'html.parser')
    ll='Scrape Links \n'
    for i,j in zip(soup.find_all('strong'),soup.find_all('code')):#,class_='tl_article_content'):
        ll+=f'➥<a href="{i.a.get("href")}">{str(j.get_text()).lstrip()}</a> |\n'
    return(ll)

def atoz(url):
    re=requests.get(url)
    soup=BeautifulSoup(re.content,'html.parser')
    l=f'Title: {soup.find("title")}\n'
    try:
        for i in soup.select('div[class*="mks_accordion_item"]'):
            l+=f'➥<a href="https://www.atozcartoonist.com{i.a["href"]}">{str(i.text).lstrip()}</a>\n'

    except: print('j')
    return l
async def toonworld4all(url: str):
    if "/redirect/main.php?url=" in url:
        return f'┎ <b>Source Link:</b> {url}\n┃\n┖ <b>Bypass Link:</b> {rget(url).url}'
    xml = rget(url).text
    soup = BeautifulSoup(xml, 'html.parser')
    if '/episode/' not in url:
        epl = soup.select('a[href*="/episode/"]')
        tls = soup.select('div[class*="mks_accordion_heading"]')
        stitle = search(r'\"name\":\"(.+)\"', xml).group(1).split('"')[0]
        prsd = f'<b><i>{stitle}</i></b>'
        for n, (t, l) in enumerate(zip(tls, epl), start=1):
            prsd += f'''
        
{n}. <i><b>{t.strong.string}</b></i>
┖ <b>Link :</b> {l["href"]}'''
        return prsd
    links = soup.select('a[href*="/redirect/main.php?url="]')
    titles = soup.select('h5')
    prsd = f"<b><i>{titles[0].string}</i></b>"
    titles.pop(0)
    slicer, _ = divmod(len(links), len(titles))
    atasks = []
    for sl in links:
        nsl = ""
        while all(x not in nsl for x in ['rocklinks', 'link1s']):
            nsl = rget(sl["href"], allow_redirects=False).headers['location']
            print(nsl)
        if "rocklinks" in nsl:
            atasks.append(create_task(transcript(nsl, "https://insurance.techymedies.com/", "https://highkeyfinance.com/", 5)))
        elif "link1s" in nsl:
            atasks.append(create_task(transcript(nsl, "https://link1s.com", "https://anhdep24.com/", 9)))

    com_tasks = await gather(*atasks, return_exceptions=True)
    lstd = [com_tasks[i:i+slicer] for i in range(0, len(com_tasks), slicer)]

    for no, tl in enumerate(titles):
        prsd += f"\n\n<b>{tl.string}</b>\n┃\n┖ <b>Links :</b> "
        for tl, sl in zip(links, lstd[no]):
            if isinstance(sl, Exception):
                prsd += str(sl)
            else:
                prsd += f"<a href='{sl}'>{tl.string}</a>, "
        prsd = prsd[:-2]
    return prsd
async def toonhub_scrapper(url):
    client = cloudscraper.create_scraper(allow_brotli=False)
    if 'redirect/?url' in url:
        res=client.get(url,allow_redirects=False).headers['Location']
        return await shortners(res)
    res = client.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    if '/episode/' not in url:
        l = f'{soup.find("title").text}\n'
        for i, j in zip(soup.find_all('div', {'class': "three_fourth tie-columns last"}),
                        soup.find_all('div', {'class': 'toggle'})):
            l += f'<a href="{j.a.get("href")}">{str(j.h3.text).lstrip()}\n</a>Context: {i.text}\n'
        return l

    links = soup.select('a[href*="/redirect/?url="]')
    titles = soup.select('h5')
    prsd = f"<b><i>{titles[0].string}</i></b>"
    titles.pop(0)
    slicer, _ = divmod(len(links), len(titles))
    atasks = []
    for sl in links:
        nsl = client.get(f'https://toonshub.link/{sl["href"]}', allow_redirects=False).headers['location']
        print(nsl)
        atasks.append(create_task(shortners(nsl)))
    com_tasks = await gather(*atasks, return_exceptions=True)
    lstd = [com_tasks[i:i+slicer] for i in range(0, len(com_tasks), slicer)]

    for no, tl in enumerate(titles):
        prsd += f"\n\n<b>{tl.string}</b>\n┃\n┖ <b>Links :</b> "
        for tl, sl in zip(links, lstd[no]):
            if isinstance(sl, Exception):
                prsd += str(sl)
            else:
                prsd += f"<a href='{sl}'>{tl.string}</a>, "
        prsd = prsd[:-2]
    return prsd

async def dhakrey(url):
    cget = cloudscraper.create_scraper(allow_brotli=False).request
    resp = cget("GET", url)
    soup=BeautifulSoup(resp.text,'html.parser')
    title=f'\nTitle: {soup.find("title").text}\n\n'
    for button in soup.find_all('button', onclick=True):
        onclick_value = button['onclick']
        match = re.search(r"window\.open\(['\"](https://drive.daddyop.us/dl[^'\"]+)['\"].*?\)", onclick_value)
        download=re.search(r"window\.open\(['\"](https://[^'\"]*download\.aspx[^'\"]*)['\"].*?\)", onclick_value)
        if match:
            https_link = match.group(1)
            button_text = button.get_text().strip()
            if button_text=='Direct Drive Link':
                soup1=BeautifulSoup(cget('GET',https_link).content,'html.parser')
                drive_links = soup1.select('a[href^="https://drive.google.com"]')
                filepress=soup1.select('a[href^="https://new.filepress.store"]')
                for link,flink in zip(drive_links,filepress):
                        title+=f'➥<a href="{link["href"]}">{str("Drive Link").lstrip()}</a> | '
                        title+=f'➥<a href="{flink["href"]}">{str("Filepress Link").lstrip()}</a> | '
        if download:
            https_link = download.group(1)
            button_text = button.get_text().strip()
            title+=f'➥<a href="{https_link}">{str(button_text).lstrip()}</a> |\n'     

    return title
def publicearn(url,uid):
    chromedriver_autoinstaller.install()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    for i in range(0,31):
        time.sleep(1)
        print(i)
    code=url.split('/')[-1]
    ref=(driver.current_url).split('//')[-1].split('/')[0]
    print(ref)
    cget = cloudscraper.create_scraper(allow_brotli=False).request
    resp = cget("GET", f"https://go.publicearn.com/{code}/?uid={uid}", headers={"referer": f'https://{ref}/'})
    soup = BeautifulSoup(resp.content, "html.parser")
    data = { inp.get('name'): inp.get('value') for inp in soup.find_all("input") }
    print(data)
    resp = cget("POST", f"https://go.publicearn.com/links/go", data=data, headers={ "x-requested-with": "XMLHttpRequest" })
    try: 
        return resp.json()['url']
    except Exception as e:
        print(e)


# shortners
async def shortners(url):
    if "https://igg-games.com/" in url:
        print("entered igg:",url)
        return igggames(url)
    elif "https://katdrive." in url:
        if KATCRYPT == "":
            return "🚫 __You can't use this because__ **KATDRIVE_CRYPT** __ENV is not set__"
        
        print("entered katdrive:",url)
        return drivescript(url, KATCRYPT, "KatDrive")
    elif "https://kolop." in url:
        if KCRYPT  == "":
            return "🚫 __You can't use this because__ **KOLOP_CRYPT** __ENV is not set__"
        
        print("entered kolop:",url)
        return kolop_dl(url, KCRYPT)

    # hubdrive
    elif "https://hubdrive." in url:
        if HCRYPT == "":
            return "🚫 __You can't use this because__ **HUBDRIVE_CRYPT** __ENV is not set__"
 
        print("entered hubdrive:",url)
        return drivescript(url, HCRYPT, "HubDrive")

    # drivefire
    elif "https://drivefire." in url:
        if DCRYPT == "":
            return "🚫 __You can't use this because__ **DRIVEFIRE_CRYPT** __ENV is not set__"

        print("entered drivefire:",url)
        return drivefire_dl(url, DCRYPT)
        
    # filecrypt
    elif (("https://filecrypt.co/") in url or ("https://filecrypt.cc/" in url)):
        print("entered filecrypt:",url)
        return filecrypt(url)
        
    # shareus
    elif "https://shareus." in url or "https://shrs.link/" in url:
        print("entered shareus:",url)
        return shareus(url)



    elif "https://shorte.st/" in url:
        print("entered shorte:",url)
        return sh_st_bypass(url)
        
    elif "https://psa.wf/exit" in url:
        print("enterezbd psa:",url)
        return try2link_scrape(url)    
    # psa
    elif "https://psa.wf/" in url:
        print("entered pssfdgsga:",url)
        return psa_bypasser(url)
        
    # sharer pw
    elif "https://sharer.pw/" in url:
        if XSRF_TOKEN == "" or Laravel_Session == "":
            return "🚫 __You can't use this because__ **XSRF_TOKEN** __and__ **Laravel_Session** __ENV is not set__"
       
        print("entered sharer:",url)
        return sharer_pw(url, Laravel_Session, XSRF_TOKEN)

    # gdtot url
    elif "gdtot.cfd" in url:
        print("entered gdtot:",url)
        return f"<b><i>Can't bypass Now.They add cloudflare protection.</i></b>"
    elif 'dhakrey' in url:
        return await dhakrey(url)
    # adfly
    elif "https://adf.ly/" in url:
        print("entered adfly:",url)
        out = adfly(url)
        return out['bypassed_url']    
    # droplink
    elif "https://droplink.co/" in url:
        print("entered droplink:",url)
        return droplink(url)
        
    # linkvertise
    elif "https://linkvertise.com/" in url:
        print("entered linkvertise:",url)
        return linkvertise(url)
        

    # ouo
    elif "https://ouo.press/" in url or "https://ouo.io/" in url:
        print("entered ouo:",url)
        return ouo(url)

    # try2link
    elif "https://try2link.com/" in url:
        print("entered try2links:",url)
        return try2link_bypass(url)

   

    # rslinks
    elif "rslinks.net" in url:
        print("entered rslinks:",url)
        return rslinks(url)

    # bitly + tinyurl
    elif "bit.ly" in url or "tinyurl.com" in url:
        print("entered bitly_tinyurl:",url)
        return bitly_tinyurl(url)

    # thinfi
    elif "thinfi.com" in url:
        print("entered thinfi:",url)
        return thinfi(url)
        
    # htpmovies sharespark cinevood
    elif "https://htpmovies." in url or 'sharespark' in url or "https://skymovieshd" in url \
        or "https://teluguflix" in url or 'https://taemovies' in url  or "https://animeremux" in url or 'https://cinevood.' in url or 'https://animeremux.' in url:
        print("entered htpmovies sharespark cinevood skymovieshd :",url)
        return scrappers(url)

    # gdrive look alike
    elif ispresent(gdlist,url):
        print("entered gdrive look alike:",url)
        return unified(url)

    # others
    elif ispresent(otherslist,url):
        print("entered others:",url)
        return others(url)
   
    elif "toonworld4all.me/redirect/main.php?" in url:
        nsl=''
        while not any(x in nsl for x in ['rocklinks', 'link1s']):
            nsl=rget(url,allow_redirects=False).headers['location']
        if 'go.rocklinks' in nsl:
            as1=await transcript(nsl, "https://insurance.techymedies.com/", "https://highkeyfinance.com/", 5)
        else:
            as1=await transcript(nsl,"https://link1s.com/","https://anhdep24.com/",8)
        return as1
    #Toonworld4all
    elif "toonworld4all" in url:
        print("entered toonworld4all:",url)
        return await toonworld4all(url)
    elif "toonshub" in url:
        return await toonhub_scrapper(url)
    
    # elif "drive.google.com/" in url:
    #     if 'view' in url:
    #         d=url.index('view')
    #         url=url[0:66].split('/')
    #         url=url[-2]
    #         return f'🔗Link: <a href="https://indexlink.mrprincebotz.workers.dev/direct.aspx?id={url}">ɪɴᴅᴇx ʟɪɴᴋ</a>'
    #     elif 'id' in url:
    #         try:
    #             ur=url.index('&export=download')
    #             url=url[0:64].split('=')
    #             url=url[-1]
    #             return f'🔗Link: <a href="https://indexlink.mrprincebotz.workers.dev/direct.aspx?id={url}">ɪɴᴅᴇx ʟɪɴᴋ</a>'
    #         except:
    #             url=url[0:64].split('=')
    #             url=url[-1]
    #             return f'🔗Link: <a href="https://indexlink.mrprincebotz.workers.dev/direct.aspx?id={url}">ɪɴᴅᴇx ʟɪɴᴋ</a>'
    elif "drive.google.com/" in url:
        return f'🔗ɪɴᴅᴇx ʟɪɴᴋ: {get_dl(url)}'
    #vnshortener
    elif "vnshortener.com" in url:
        print("entered vnshortener:",url)
        return vnshortener(url)
    elif "themoviesboss.site/secret?" in url:
        print("entered themoviesboss:",url)
        return themoviesboss(url)
    elif "themoviesboss.site" in url:
        print("entered moviesboss:",url)
        return moviesboss(url)
    elif 'https://files.technicalatg.com/' in url:
        code=url.split('/')[-1]
        return f'https://atglinks.com/{code}'
    elif 'https://atglinks.com/' in url:
        return f"There's NO Bypass for atglinks.com Now "
    #tenbit
    elif "https://10bitclub.me" in url:
        print("entered 10bitclub:",url)
        return tenbit(url)

    elif "https://animepahe.ru" in url:
        print("entered animepahe:",url)
        return animepahe(url)

    #du_link
    elif "https://du-link.in" in url:
        print("entered du_link:",url)
        return du_link(url)
    #atozcartoonist
    elif "https://www.atozcartoonist.com/redirect/" in url:
        print("entered atozcartoonist:",url)
        return atozcartoonist(url)
    elif "https://www.atozcartoonist.com/" in url:
        print("entered atoz:",url)
        return atoz(url)
    elif 'atishmkv.wiki' in url:
        print(f"entered atishmkv: {url}")
        return await atishmkv(url)
    #telegraph_scaper
    elif 'https://graph.org' in url:
        print(f"entered telegraph_scaper: {url}")
        return await telegraph_scaper(url)

    elif "shrinkforearn" in url:
        return await transcript(url,"https://shrinkforearn.in/","https://wp.uploadfiles.in/", 10)
    elif "link.short2url" in url:
        return await transcript(url,"https://techyuth.xyz/blog/", "https://blog.mphealth.online/", 9)
    elif "viplinks" in url:
        return await transcript(url,"https://m.vip-link.net/", "https://m.leadcricket.com/", 5)
    elif "bindaaslinks" in url:
        return await transcript(url,"https://thebindaas.com/blog/", "https://finance.appsinsta.com/", 5)
    elif "sheralinks" in url:
        return await transcript(url,"https://link.blogyindia.com/", "https://blogyindia.com/", 5)
    elif "url4earn" in url:
        return await transcript(url,"https://go.url4earn.in/", "https://techminde.com/", 8)
    elif "tglink" in url:
        url=url.lower()
        return await transcript(url, "https://tglink.in/", "https://www.proappapk.com/", 5)
    elif "link1s.com" in url:
        return await transcript(url,"https://link1s.com/","https://anhdep24.com/",8)
    elif "gofile.io" in url:
        return gofile_dl(url)
    elif "publicearn" in url:
        return publicearn(url,uid)
    elif "links4money.com" in url:
        return await transcript(url,'https://links4money.com','https://gamergiri.infokeeda.xyz',2)
    elif "happiurl.com" in url:
        return await transcript(url,'https://count.financevis.com/','https://financevis.com/',5)
    elif "linkfly" in url:
        return await transcript(url, "https://go.linkfly.in", "https://techyblogs.in/", 4)
    elif "mdiskshortner" in url:
        return await transcript(url, "https://loans.yosite.net", "https://yosite.net", 10)
    elif "narzolinks" in url:
        return await transcript(url, "https://go.narzolinks.click/", "https://hydtech.in/", 5)
    elif "earn2me" in url:
        return await transcript(url, "https://blog.filepresident.com/", "https://easyworldbusiness.com/", 5)
    elif "adsfly" in url:
        return await transcript(url, "https://go.adsfly.in/", "https://loans.quick91.com/", 5)
    elif "link4earn" in url:
        return await transcript(url, "https://link4earn.com", "https://studyis.xyz/", 5)
    elif "pdisk.site" in url:
        return await transcript(url, "https://go.moneycase.link", "https://go.moneycase.link", 2)
    elif "link.tnshort.net/" in url or "link.tnlink.net/" in url:
        return await transcript(url, "https://go.tnshort.net", "https://market.finclub.in", 10)
    elif "ziplinker.net" in url:
        return await transcript(url,'https://ziplinker.net/web','https://ontechhindi.com/',0.04)
    elif "urllinkshort.in" in url:
        return await transcript(url,'https://web.urllinkshort.in/','https://suntechu.in/',4.5)
    elif "kpslink.in" in url:
        return await transcript(url, "https://get.infotamizhan.xyz/", "https://infotamizhan.xyz/", 5)
    elif "v2.kpslink.in" in url:
        return await transcript(url, "https://v2download.kpslink.in/", "https://infotamizhan.xyz/", 5)
    elif "go.lolshort" in url:
        return await transcript('http://go.lolshort.tech/DoCpsBrG', "https://get.lolshort.tech/", "https://tech.animezia.com/", 8)
    elif "go.lolshort" in url:
        return await transcript(url, "https://blog.vllinks.in", "https://vlnewshd.in/", 8)
    elif "onepagelink" in url:
        return await transcript(url, "https://go.onepagelink.in/", "https://gorating.in/", 0.9)
    elif "pkin" in url:
        return await transcript(url, "https://go.paisakamalo.in", "https://techkeshri.com/", 9)
    elif "shrinke" in url:
        return await transcript(url, "https://en.shrinke.me/", "https://themezon.net/", 15)
    elif "mplaylink" in url:
        return await transcript(url, "https://tera-box.cloud/", "https://mvplaylink.in.net/", 0.5)
    elif "ewlink" in url:
        return await transcript(url, "https://ewlink.xyz/", "https://rxfastrx.com/", 0)
    elif "sklinks" in url:
        return await transcript(url, "https://sklinks.in", "https://sklinks.in/", 4.5)
    elif "dalink" in url:
        return await transcript(url, "https://get.tamilhit.tech/X/LOG-E/", "https://www.tamilhit.tech/", 8)
    elif "rocklinks" in url:
        return await transcript(url, "https://insurance.techymedies.com/", "https://highkeyfinance.com/", 5)
    elif "short_jambo" in url:
        return await transcript(url, "https://short-jambo.com/","https://1.newworldnew.com/",0.7)
    elif "ez4short" in url:
        return await transcript(url, "https://ez4short.com/","https://ez4mods.com/",5)
    elif "shortingly.com" in url:
        return await transcript(url,"https://go.blogytube.com/","https://blogytube.com/",1)
    elif "https://gyanilinks.com/" in url or "https://gtlinks.me/" in url:
        return await transcript(url,"https://go.hipsonyc.com","https://earn.hostadviser.net",5)
    elif "https://flashlinks.in/" in url:
        return await transcript(url,"https://flashlinks.in", "https://flashlinks.online/",13)
    elif "urlsopen" in url:
        return await transcript(url, "https://s.humanssurvival.com/", "https://1topjob.xyz/", 1)
    elif "xpshort" in url:
        return f"Can't Bypass.Invisible captcha"
        #return await transcript(url, "https://techymozo.com/", "https://portgyaan.in/", 0)
    elif "go.moonlinks.in/" in url:
        return await transcript(url, "https://go.moonlinks.in/", "https://www.akcartoons.in/", 7)
    elif "vivdisk" in url:
        return await transcript(url, "https://tinyfy.in/", "https://web.yotrickslog.tech/", 0)
    elif "https://krownlinks.me" in url:
        return await transcript(url, "https://go.hostadviser.net/", "https://blog.hostadviser.net/", 8)
    elif "adrinolink" in url:
        return f'https://bhojpuritop.in/safe.php?link={url.split("/")[-1]}'#await transcript(url, "https://adrinolinks.in/", "https://amritadrino.com", 8)
    elif "mdiskshortner" in url:
        return await transcript(url, "https://mdiskshortner.link", "https://m.proappapk.com", 2)
    elif "tiny" in url:
        return await transcript(url, "https://tinyfy.in", "https://www.yotrickslog.tech", 0)
    elif "earnl" in url:
        return await transcript(url, "https://v.earnl.xyz", "https://link.modmakers.xyz", 5)
    elif "moneykamalo" in url:
        return await transcript(url, "https://go.moneykamalo.com", "https://blog.techkeshri.com", 5)
    elif "v2links" in url:
        return await transcript(url, "https://vzu.us", "https://gadgetsreview27.com", 15)
    elif "tnvalue" in url:
        return await transcript(url, "https://get.tnvalue.in/", "https://finclub.in", 8)
    elif "omnifly" in url:
        return await transcript(url, "https://f.omnifly.in.net/", "https://f.omnifly.in.net/", 8)
    elif "indianshortner" in url:
        return await transcript(url, "https://indianshortner.com/", "https://moddingzone.in", 5)
    elif "indianshortner" in url:
        return await transcript(url, "https://techy.veganab.co", "https://veganab.co/", 8)
    elif "indi" in url:
        return await transcript(url, "https://file.earnash.com/", "https://indiurl.cordtpoint.co.in/", 10)
    elif "linkbnao" in url:
        return await transcript(url, "https://vip.linkbnao.com", "https://ffworld.xyz/", 2)
    elif "mdiskpro" in url:
        return await transcript(url, "https://mdisk.pro", "https://www.meclipstudy.in", 8)
    elif "omegalinks" in url:
        return await transcript(url, "https://tera-box.com", "https://m.meclipstudy.in", 8)
    elif "mdisklink" in url:
        return await transcript(url, "https://powerlinkz.in", "https://powerlinkz.in", 2)
    elif "indshort" in url:
        return await transcript(url, "https://indianshortner.com", "https://moddingzone.in", 5)
    elif "indyshare" in url:
        return await transcript(url, "https://download.indyshare.net", "https://bestdjsong.com/", 15)
    elif "mdisklink" in url:
        return await transcript(url, "https://gotolink.mdisklink.link/", "https://loans.yosite.net/", 2)
    elif "tamizhmasters" in url:
        return await transcript(url, "https://tamizhmasters.com/", "https://pokgames.com/", 5)
    elif "vipurl" in url:
        return await transcript(url, "https://count.vipurl.in/", "https://awuyro.com/", 8)
    elif "linksly" in url:
        return await transcript(url, "https://go.linksly.co", "https://en.themezon.net/", 10)
    elif "link1s" in url:
        return await transcript(url,'https://link1s.net','https://nguyenvanbao.com/',0)
    elif "sxslink" in url:
        return await transcript(url, "https://getlink.sxslink.com/", "https://cinemapettai.in/", 5)
    elif "urlspay.in" in url:
        return await transcript(url, "https://finance.smallinfo.in/", "https://loans.techyinfo.in/", 5)
    elif "linkpays.in" in url:
        return await transcript(url, "https://tech.smallinfo.in/Gadget/", "https://loan.insuranceinfos.in/", 5)
    elif "seturl.in" in url:
        return await transcript(url,'https://set.seturl.in/','https://earn.petrainer.in/',5)
    else: return "Not in Supported Sites"
    
################################################################################################################################
