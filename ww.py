from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
import chromedriver_autoinstaller
from bs4 import BeautifulSoup
import cloudscraper
import os
import time
uid=os.environ.get('PEUID')
def publicearn(url,uid):
    chromedriver_autoinstaller.install()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    for i in range(0,29):
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

url='https://publicearn.com/ZFd5'
print(publicearn(url,uid))