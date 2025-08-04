import requests
import time
import os
import random
from colorama import Fore
import json
r = Fore.RED
g = Fore.GREEN
b = Fore.BLUE
c = Fore.CYAN
re = Fore.RESET

def sj(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def lj(filename):
    if not os.path.exists(filename):
        return {}

def rdm_useragent():
    ua = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
    ]
    return random.choice(ua)

def main():
    os.system('cls')
    BADGES = {
        1 << 0: "<:Badge_Discord_Staff:1365704725646807060>",
        1 << 1: "<:DiscordPartner:1365700977570742312>",
        1 << 2: "<:HypeSquadEvents:1365704359454834770>",
        1 << 3: "<:BugHunter1:1365701008184967278>",
        1 << 9: "<:86964earlysupporter:1345831325738995848>",
        1 << 14: "<:BugHunter2:1365701027830960259>",
        1 << 17: "<:dev:1365704127103107112>",
        1 << 18: "<:ModeratorProgramsAlumni:1365701046256533525>",
    }

    print(f"""
{b} $$$$$$\                                      
$$  __$$\                                     
$$ /  $$ | $$$$$$\   $$$$$$\  $$$$$$$\        
$$ |  $$ |$$  __$$\ $$  __$$\ $$  __$$\       
$$ |  $$ |$$ /  $$ |$$$$$$$$ |$$ |  $$ |      
$$ |  $$ |$$ |  $$ |$$   ____|$$ |  $$ |      
 $$$$$$  |$$$$$$$  |\$$$$$$$\ $$ |  $$ |      
 \______/ $$  ____/  \_______|\__|  \__|      
          $$ |                                
          $$ |                                
          \__|                  
                                     {r} ______                                                                       
                                     /      \                                                                      
                                    |  $$$$$$\  _______   ______   ______    ______    ______    ______    ______  
                                    | $$___\$$ /       \ /      \ |      \  /      \  /      \  /      \  /      \ 
                                     \$$    \ |  $$$$$$$|  $$$$$$\ \$$$$$$\|  $$$$$$\|  $$$$$$\|  $$$$$$\|  $$$$$$\\
                                     _\$$$$$$\| $$      | $$   \$$/      $$| $$  | $$| $$  | $$| $$    $$| $$   \$$
                                    |  \__| $$| $$_____ | $$     |  $$$$$$$| $$__/ $$| $$__/ $$| $$$$$$$$| $$      
                                     \$$    $$ \$$     \| $$      \$$    $$| $$    $$| $$    $$ \$$     \| $$      
                                      \$$$$$$   \$$$$$$$ \$$       \$$$$$$$| $$$$$$$ | $$$$$$$   \$$$$$$$ \$$      
                                                                           | $$      | $$                          
                                                                           | $$      | $$                          
                                                                            \$$       \$$                                     
""")

    channelid = input(f"{c}Channel ID: ")
    burl = f"https://discord.com/api/v9/channels/{channelid}/messages"
    token = json.loads(open("config.json").read())["token"]
    if not token:
        print(f"{r}}Invalid token please check config.json")
        return  
    webhook = json.loads(open("config.json").read()).get("webhook")
    if not webhook:
        print(f"{r}Invalid webhook please check config.json")
        return

    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": rdm_useragent()
    }

    seen = set()
    lmid = None
    ttc = 0

    while True:
        params = {"limit": 100}
        if lmid:
            params["before"] = lmid

        resp = requests.get(burl, headers=headers, params=params)
        if resp.status_code != 200:
            print("Error:", resp.status_code)
            print(resp.text)
            break

        messages = resp.json()
        if not messages:
            break  
        for msg in messages:
            author = msg["author"]
            user_id = author["id"]

            if user_id in seen:
                continue

            seen.add(user_id)
            username = author["username"]
            flags = author.get("public_flags", 0)
            badges = "".join([icon for bit, icon in BADGES.items() if flags & bit])
            if not badges and len(username) > 3:
                continue

            if not badges:
                if len(username) == 2:
                    badges = "<:2L:1388122321033629789>"
                elif len(username) == 3:
                    badges = "<:3L:1388122363953942550>"
                else:
                    badges = "No badge"

            content = f"<@{user_id}> ({username}:{user_id}) : {badges}"
            res = requests.post(webhook, data={
                "content": content,
                'username': "open scrapper",
                'avatar_url': "https://avatars.githubusercontent.com/u/198399128?v=4"
            })
            if res.status_code == 204:
                print(f"{g}{res.status_code}{re} - {content}")
                time.sleep(5) # dont change this value
            else:
                print(f"{r}{res.status_code}{re} - {content}")
                time.sleep(30) # dont change this value 

        lmid = messages[-1]["id"]
        ttc += len(messages)

main()
