# from kwik_extractor import KwikExtractor
import cloudscraper
from bs4 import BeautifulSoup
from time import sleep
import re
session = cloudscraper.create_scraper()
from animepahe.kwik_token_extractor import kwik_token_extractor

def get_cookie_and_response(episode):

        head = {
            "referer": episode,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36 Edg/80.0.361.69"
        }
        response = session.get(episode, headers=head)
        cookie = []
        try:
            cookie.append(response.headers["set-cookie"])
            cookie.append(response)
        except Exception as ex:
            return None

        return cookie

def set_token(response_text):
        data = re.search("[\S]+\",[\d]+,\"[\S]+\",[\d]+,[\d]+,[\d]+", response_text).group(0)
        parameters = data.split(",")
        para1 = parameters[0].strip("\"")
        para2 = int(parameters[1])
        para3 = parameters[2].strip("\"")
        para4 = int(parameters[3])
        para5 = int(parameters[4])
        para6 = int(parameters[5])

        page_data = kwik_token_extractor.extract_data(para1, para2, para3, para4, para5, para6)
        page_data = BeautifulSoup(page_data, "html.parser")

        input_field = page_data.find("input", attrs={"name": "_token"})

        # print(input_field)

        if input_field is not None:
            token = input_field["value"]
            print(token)
            return token

        return False


def set_direct_link(episode):
        cookie = get_cookie_and_response(episode)
        if cookie is None:
            sleep(2)
            cookie = get_cookie_and_response(episode)

        if cookie is None:
            return False
        token=set_token(cookie[1].text)
        if token is None:
            return False
        head = {
            "origin": "https://kwik.cx",
            "referer": 'https://kwik.cx/f/'+episode.split('/')[-1],
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36 Edg/80.0.361.69",
            "cookie": cookie[0]
        }

        payload = {
            "_token": token
        }

        post_url = "https://kwik.cx/d/"+episode.split('/')[-1]
        print(post_url)
        resp_headers = session.post(post_url, data=payload, headers=head, allow_redirects=False)
        return resp_headers.headers['location']

