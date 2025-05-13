import requests

headers = {
    'authority': 'publicearn.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.5',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://starxinvestor.com',
    'referer': 'https://starxinvestor.com/',
    'sec-ch-ua': '"Brave";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}

data = {
    'step_1': 'avmQ6e',
    'data': '3SeTEJE0McEmh0o3jb2CJ6swxzCdPMnCKrhUogC/BwG65knNzfuaTjoXucRdN33Zv7aa2NGUrsE81n8HmUG34oVjl9wooYDXbXLfaIkJyXQHLm9yoOuhvAA5V4dN9xMq2MY3Z9AiYXPOIRzA7CF30Q==',
}

response = requests.post('https://publicearn.com/link/verify.php', headers=headers, data=data)
print(response.json())