from pystyle import System
from colorama import Fore
from concurrent.futures import ThreadPoolExecutor
import websocket
import uuid
import keyboard
from user_agent import generate_user_agent
import sys
import threading
import time
import json
from time import sleep
from tls_client import Session
import logging
import random
import datetime
import string
import requests
from typing import List, Union, Dict, Callable, Tuple, Optional, Set, TypedDict, Any

try:
    import pystyle
    import colorama
    import sys
    import os
    import concurrent.futures
    import threading
    import datetime
    import discum
    import typing
    import tls_client
except ImportError:
    os.system('pip install pystyle')
    os.system('pip install colorama')
    os.system('pip install threading')
    os.system('pip install concurrent.futures')
    os.system('pip install typing')
    os.system('pip install datetime')
    os.system('pip install tls_client')
    os.system('pip install discum')

class Core:
    EMOJIS: List[str] = [
        '🙂', '😂', '😊', '🔥', '💀', '❤️', '💯', '✨', '😁', '😎', '😃', '😜', '🙃',
        '😏', '😅', '😆', '😇', '🥳', '😋', '😱', '😜', '🤩', '😬', '😢', '😭', '😤',
        '😐', '😓', '😌', '😶', '🥺', '🤪', '🤔', '😳', '🤯', '😷', '😴', '😵', '🥴',
        '🙄', '😑', '🤭', '🤐', '😅', '🧐', '😝', '🥰'
    ]
    Session = tls_client.Session(client_identifier='safari_16_0', random_tls_extension_order=True)
    Tokens: List[str] = []

    def load(filename: str) -> List[str]:
        try:
            with open(filename, 'r') as file:
                tokens: List[str] = file.readlines()
                return [token.strip() for token in tokens if token.strip()] 
        except FileNotFoundError:
            return [] 

    timestamp = datetime.datetime.now().strftime(f'(%H:%M:%S)')

Tokens = Core.load('core/input/tokens.txt')

class Colors:
    colors: Dict[str, Tuple[Tuple[int, int, int], Tuple[int, int, int]]] = {
        'purple_to_white': ((127, 0, 255), (255, 255, 255)),
        'red_to_blue': ((255, 0, 0), (0, 0, 255)),
        'red_to_white': ((255, 0, 0), (255, 255, 255)),
        'green_to_yellow': ((0, 255, 0), (255, 255, 0)),
        'black_to_white': ((0, 0, 0), (255, 255, 255)),
        'blue_to_cyan': ((0, 0, 255), (0, 255, 255)),
        'orange_to_pink': ((255, 165, 0), (255, 192, 203)),
        'silver_blue': ((173, 216, 230), (169, 169, 169)),
        'mint': ((194, 255, 182), (255, 255, 255)),
        'red_to_yellow': ((255, 0, 0), (255, 255, 0)),
        'blue_to_green': ((0, 0, 255), (0, 255, 0)),
        'purple_to_blue': ((128, 0, 128), (0, 0, 255)),
        'pink_to_white': ((255, 20, 147), (255, 228, 225)),
        'pink_to_black': ((255, 182, 193), (105, 0, 52)),
        'brown_to_black': ((210, 180, 140), (101, 67, 33)),
        'cyan_to_magenta': ((0, 255, 255), (255, 0, 255)),
        'gray_to_black': ((169, 169, 169), (0, 0, 0)),
        'blue_to_white': ((0, 0, 255), (255, 255, 255)),
        'red_to_green': ((255, 0, 0), (0, 255, 0)),
        'green_to_blue': ((0, 255, 0), (0, 0, 255)),
        'blue_to_yellow': ((0, 0, 255), (255, 255, 0)),
        'yellow_to_cyan': ((255, 255, 0), (0, 255, 255)),
        'magenta_to_red': ((255, 0, 255), (255, 0, 0)),
        'white_to_black': ((255, 255, 255), (0, 0, 0)),
        'mystic': ((207, 188, 254), (182, 48, 220)),
        'ash': ((255, 0, 0), (128, 128, 128)),
        'blue_to_white': ((0, 0, 255), (255, 255, 255)),
        'green_to_cyan': ((0, 255, 0), (0, 255, 255)),
        'green_to_white': ((0, 255, 0), (255, 255, 255)),
        'blue_to_black': ((173, 216, 230), (0, 0, 139)),
        'red_to_black': ((255, 99, 71), (139, 0, 0)),
        'yellow_to_cyan': ((255, 255, 0), (0, 255, 255)),
        'rainbow': (
            (255, 0, 0),
            (255, 165, 0),
            (255, 255, 0),
            (0, 255, 0),
            (0, 255, 255),
            (0, 0, 255),
            (128, 0, 128)
        )
    }

    @classmethod
    def load_color_name(cls, config_path: str) -> str:
        with open(config_path, 'r') as file:
            config = json.load(file)
        return config.get('color_name', 'blue_to_cyan')

    @classmethod
    def get_color(cls, name: str, text: str) -> str:
        if name not in cls.colors:
            raise ValueError(f"Color {name} Not Found In Configuration.")
        
        color_data = cls.colors[name]
        if isinstance(color_data, list):
            return cls.apply_rainbow_gradient(text, color_data)
        else:
            return cls.apply_gradient(text, color_data[0], color_data[1])

    @classmethod
    def apply_gradient(cls, text: str, start: Tuple[int, int, int], end: Tuple[int, int, int]) -> str:
        gradient = []
        length = len(text)
        for i in range(length):
            t = i / (length - 1)
            color = tuple(int(start[j] + t * (end[j] - start[j])) for j in range(3))
            gradient.append(color)

        return ''.join(
            f'\033[38;2;{color[0]};{color[1]};{color[2]}m{char}\033[0m'
            for char, color in zip(text, gradient)
        )

    @classmethod
    def apply_rainbow_gradient(cls, text: str, rainbow_colors: List[Tuple[int, int, int]]) -> str:
        gradient = []
        length = len(text)
        num_colors = len(rainbow_colors)
        for i in range(length):
            t = i / (length - 1)
            segment = t * (num_colors - 1)
            start_idx = int(segment)
            end_idx = min(start_idx + 1, num_colors - 1)
            ratio = segment - start_idx

            start_color = rainbow_colors[start_idx]
            end_color = rainbow_colors[end_idx]
            color = tuple(int(start_color[j] + ratio * (end_color[j] - start_color[j])) for j in range(3))
            gradient.append(color)

        return ''.join(
            f'\033[38;2;{color[0]};{color[1]};{color[2]}m{char}\033[0m'
            for char, color in zip(text, gradient)
        )

color_name = Colors.load_color_name('core/themes/config.json')

""" 
class Forecolors:
    c   :   str = Fore.RESET
    s   :   str = Fore.BLUE
    a   :   str = Fore.LIGHTBLACK_EX
    k   :   str = Fore.RED
    l   :   str = Fore.GREEN
    n   :   str = Fore.LIGHTRED_EX
    o   :   str = Fore.LIGHTGREEN_EX

These might be used in the future
"""

"""THIS IS NOT MINE"""

frames = [
    fr'''
                                                     
                                                    
                                                    
                                                  
                                                          
                                                      
                                        ########## ########   ########     ### 
    ''',
    fr'''
                                                     
                                                     
                                                      
                                               
                                                          
                                         #+#              
                                        ########## ########   ########     ### 
    ''',
    fr'''
                                                      
                                                    
                                                      
                                                  
                                          +#+               
                                         #+#              
                                        ########## ########   ########     ### 
    ''',
    fr'''
                                                     
                                                     
                                                      
                                           +#+      
                                          +#+               
                                         #+#              
                                        ########## ########   ########     ### 
    ''',
    fr'''
                                                      
                                                     
                                            +:+           
                                           +#+      
                                          +#+               
                                         #+#              
                                        ########## ########   ########     ###
    ''',
    fr'''
                                                     
                                             :+:        
                                            +:+           
                                           +#+      
                                          +#+               
                                         #+#              
                                        ########## ########   ########     ###
    ''',
    fr'''
                                              :::        
                                             :+:        
                                            +:+           
                                           +#+      
                                          +#+               
                                         #+#              
                                        ########## ########   ########     ### 
    ''',
    fr'''
                                              :::       
                                             :+:         
                                            +:+           
                                           +#+       
                                          +#+               
                                         #+#       #+#    #+# #+#    #+#    #+#          
                                        ########## ########   ########     ###                
    ''',
    fr'''
                                              :::       
                                             :+:        
                                            +:+          
                                           +#+         
                                          +#+       +#+    +#+        +#+    +#+         
                                         #+#       #+#    #+# #+#    #+#    #+#          
                                        ########## ########   ########     ###                                 
    ''',
    fr'''
                                              :::       
                                             :+:              
                                            +:+               
                                           +#+       +#+    +:+ +#++:++#++    +#+        
                                          +#+       +#+    +#+        +#+    +#+         
                                         #+#       #+#    #+# #+#    #+#    #+#          
                                        ########## ########   ########     ###                  
    ''',
    fr'''
                                              :::       
                                             :+:        
                                            +:+       +:+    +:+ +:+           +:+       
                                           +#+       +#+    +:+ +#++:++#++    +#+        
                                          +#+       +#+    +#+        +#+    +#+         
                                         #+#       #+#    #+# #+#    #+#    #+#          
                                        ########## ########   ########     ###                
    ''',
    fr'''
                                              :::       
                                             :+:       :+:    :+: :+:    :+:    :+:      
                                            +:+       +:+    +:+ +:+           +:+       
                                           +#+       +#+    +:+ +#++:++#++    +#+        
                                          +#+       +#+    +#+        +#+    +#+         
                                         #+#       #+#    #+# #+#    #+#    #+#          
                                        ########## ########   ########     ### V                  
    ''',
    fr''' 
                                              :::        ::::::::   :::::::: ::::::::::: 
                                             :+:       :+:    :+: :+:    :+:    :+:      
                                            +:+       +:+    +:+ +:+           +:+       
                                           +#+       +#+    +:+ +#++:++#++    +#+        
                                          +#+       +#+    +#+        +#+    +#+         
                                         #+#       #+#    #+# #+#    #+#    #+#          
                                        ########## ########   ########     ### V1                  
    '''
]

continue_animation = True

def check_for_enter() -> None:
    global continue_animation
    while continue_animation:
        if keyboard.is_pressed('s'):
            continue_animation = False
        if continue_animation == False:
            break

def intro() -> None:
    global continue_animation
    os.system(f"mode con: cols=126 lines=24")
    enter_thread = threading.Thread(target=check_for_enter, daemon=True)
    enter_thread.start()
    for frame in frames:
        if not continue_animation:
            break

        sys.stdout.write("\033[2J\033[H")
        sys.stdout.write(Colors.get_color(color_name, frame))
        sys.stdout.flush()
        time.sleep(0.016)
    continue_animation = False

"""THIS IS NOT MINE"""

class visual:
    @classmethod
    def upper(cls):
        print("\033[F", end="")

    @classmethod
    def size(cls, width, height):
        return(
            os.system(f"mode con: cols={width} lines={height}")
        )

    typing_speed = 1700

    @classmethod
    def slowp(cls, message):
        for char in message:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(random.random() * 10.0 / cls.typing_speed)

class Cursor:
    @classmethod
    def hide(cls):
        return(
            print("\033[?25l", end='')
        )

class UtilsFuncs:
    def token_count():
        try:
            with open('core/input/tokens.txt', 'r') as file:
                lines = file.readlines()
                return len(lines)
        except FileNotFoundError:
            return 0
        except Exception as e:
            return 0

    def proxy_count():
        try:
            with open('core/input/proxies.txt', 'r') as file:
                lines = file.readlines()
                return len(lines)
        except FileNotFoundError:
            return 0
        except Exception as e:
            return 0

    def notbuilt():
        return

class Utils:
    def center(msg):
        return(
            print(UtilsFuncs.center(msg))
        )

    def clear():
        return(
            System.Clear()
        )

    def settitle(title):
        return(
            System.Title(title)
        )

class UI:
    def prnt(msg):
        return(
            print(Colors.get_color(color_name, msg))
        )

    def ask(msg):
        return(
            input(Colors.get_color(color_name, f"{Core.timestamp} - ({Vars.tool_name}) -> " + msg + " -> "))
        )

class Vars:
    tool_name = 'Lost-Spammer-V1'
    tool_owner = 'Bytecode'

    banner: str = f"""
                                              :::        ::::::::   :::::::: ::::::::::: 
                                             :+:       :+:    :+: :+:    :+:    :+:      
                                            +:+       +:+    +:+ +:+           +:+       
                                           +#+       +#+    +:+ +#++:++#++    +#+        
                                          +#+       +#+    +#+        +#+    +#+         
                                         #+#       #+#    #+# #+#    #+#    #+#          
                                        ########## ########   ########     ### V1                 
    """

    opts: str = f"""
                                               :::        ::::::::   :::::::: :::::::::::   +         +
    +                +           +            :+:       :+:    :+: :+:    :+:    :+:                       +              +
                                             +:+       +:+    +:+ +:+           +:+     +            +
          +                                 +#+       +#+    +:+ +#++:++#++    +#+                                  +
  +                   +             +      +#+       +#+    +#+        +#+    +#+         +                 +
                                          #+#       #+#    #+# #+#    #+#    #+#                                          +
          +               +              ########## ########   ########     ### V1                   +          +
                                                                                      +
                                        [Warning] -> Proxy support update next update
 +                  +           +       Succesfully Loaded [{UtilsFuncs.token_count()}] - Tokens -> [{UtilsFuncs.proxy_count()}] - Proxies

  +           (01) | Guild Joiner      (09) | Pronouns Changer  (17) | Ghost Pinger     (25) | Invite Spammer             +
              (02) | Guild Leaver      (10) | Bio Changer       (18) | Rules Bypass     (26) | Dyno WhoIs Exploit      +
              (03) | Token Formatter   (11) | Guild Checker     (19) | Remove Doubles   (27) | Vc Joiner
      +       (04) | Nickname Changer  (12) | Forum Spammer     (20) | Reaction Spammer (28) | Vc Spammer    +
              (05) | Ticket Spammer    (13) | Guild Booster     (21) | Token Reactor    (29) | RestoreCord Byp.              +
              (06) | Channel Spammer   (14) | Fake Typing       (22) | Vanity Sniper    (30) | Onboarding Bypass +
  +           (07) | Reply Spammer     (15) | Token Onliner     (23) | Scrape Users     (31) | Pin Spammer         +
              (08) | Token Checker     (16) | Thread Flooder    (24) | Hypesquad Joiner (32) | Button Bypass       +
    """

class Logger:
    def bad(self, msg):
        print(Colors.get_color('red_to_white', f"{Core.timestamp} - {Vars.tool_name} {msg}"))

    def good(self, msg):
        print(Colors.get_color('green_to_cyan', f"{Core.timestamp} - {Vars.tool_name} {msg}"))

    def warn(self, msg):
        print(Colors.get_color('red_to_yellow', f"{Core.timestamp} -> ({Vars.tool_name}) | {msg}"))

log = Logger()

class OnboardBypass:
    def __init__(self):
        self.session = tls_client.Session('chrome_131', random_tls_extension_order=True)

    def headers(self, token: str) -> dict:
        user_agent = generate_user_agent()
        return {
            "Authorization": token,
            "User-Agent": user_agent,
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Host": "discord.com",
            "Origin": "https://discord.com",
            "Referer": "https://discord.com/",
            "TE": "Trailers",
            "X-Discord-Locale": "en-US"
        }

    def read_tokens(self, file_path: str) -> List[str]:
        with open(file_path, 'r') as f:
            return f.read().splitlines()

    def get_onboarding_questions(self, token: str, guild_id: str) -> List[dict]:
        url = f"https://discord.com/api/v9/guilds/{guild_id}/onboarding"
        response = self.session.get(url, headers=self.headers(token))
        
        if response.status_code == 200:
            return response.json().get("prompts", [])
        else:
            log.bad("Failure | Failed to fetch onboarding questions")
            return []

    def answer_onboarding(self, token: str, guild_id: str, prompts: List[dict]) -> dict:
        onboarding_responses = []
        onboarding_prompts_seen = {}
        onboarding_responses_seen = {}

        for prompt in prompts:
            onboarding_responses.append(prompt["options"][-1]["id"])
            onboarding_prompts_seen[prompt["id"]] = int(datetime.datetime.now().timestamp())

            for option in prompt["options"]:
                onboarding_responses_seen[option["id"]] = int(datetime.datetime.now().timestamp())

        return {
            "onboarding_responses": onboarding_responses,
            "onboarding_prompts_seen": onboarding_prompts_seen,
            "onboarding_responses_seen": onboarding_responses_seen
        }

    def submit_onboarding_responses(self, token: str, guild_id: str, responses: dict) -> bool:
        url = f"https://discord.com/api/v9/guilds/{guild_id}/onboarding-responses"
        response = self.session.post(url, headers=self.headers(token), json=responses)

        if response.status_code == 200:
            log.good(f"Successfully Bypassed onboarding | {token[:25]}")
            return True
        else:
            log.bad(f"Failed onboarding | {token[:25]}")
            return False

    def onboard_bypass(self):
        Utils.clear()
        UI.prnt(Vars.banner)
        Utils.settitle('Lost Spammer V1 ┃ Location: [Onboarding ┃ (Bypass)]')

        guild_id = UI.ask("Guild")
        thread_count = int(UI.ask("Thread Ammount"))

        Utils.clear()
        UI.prnt(Vars.banner)
        Utils.settitle('Lost Spammer V1 ┃ Location: [Onboarding ┃ (Bypass)]')

        tokens = self.read_tokens("core/input/tokens.txt")
        in_guild = []

        for token in tokens:
            prompts = self.get_onboarding_questions(token, guild_id)
            if prompts:
                in_guild.append(token)

        if not in_guild:
            return

        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            futures = []
            for token in in_guild:
                prompts = self.get_onboarding_questions(token, guild_id)
                responses = self.answer_onboarding(token, guild_id, prompts)
                futures.append(executor.submit(self.submit_onboarding_responses, token, guild_id, responses))

            for future in futures:
                future.result()

class RulesBypass:
    def __init__(self):
        self.session = Session('chrome_131', random_tls_extension_order=True)

    def headers(self, token: str) -> dict:
        return {
            "Authorization": token,
            "User-Agent": generate_user_agent(),
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def accept_rules(self):
        try:
            Utils.clear()
            UI.prnt(Vars.banner)
            Utils.settitle('Lost Spammer V1 ┃ Location: [Rules ┃ (Bypass)]')
            guild_id = UI.ask("Guild").strip()
            thread_amount = int(UI.ask("Thread Ammount").strip())
            Utils.clear()
            UI.prnt(Vars.banner)
            Utils.settitle('Lost Spammer V1 ┃ Location: [Rules ┃ (Bypass)]')

            valid_tokens = []
            payload = None

            with open("core/input/tokens.txt", "r") as f:
                tokens = f.read().splitlines()

            for token in tokens:
                response = self.session.get(
                    f"https://discord.com/api/v9/guilds/{guild_id}/member-verification",
                    headers=self.headers(token)
                )
                if response.status_code == 200:
                    valid_tokens.append(token)
                    payload = response.json()
                    break

            if not valid_tokens:
                main()

        except Exception as e:
            log.bad("Failure | Failed to fetch rules")
            return

        def bypasstherules(token: str):
            try:
                response = self.session.put(
                    f"https://discord.com/api/v9/guilds/{guild_id}/requests/@me",
                    headers=self.headers(token),
                    json=payload
                )
                if response.status_code == 201:
                    log.good(f"Succesfully Accepted Rules | {guild_id}")
                else:
                    log.bad(f"Failure | Failed accepting rules -> {guild_id}")
            except Exception as e:
                print(f"{e}")

        with ThreadPoolExecutor(max_workers=thread_amount) as executor:
            executor.map(bypasstherules, tokens)

bypass = RulesBypass()

class Functions:
    def returnHeaders(token: str) -> dict:
        return {
            'accept': '*/*',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'authorization': token,
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'priority': 'u=1, i',
            'referer': 'https://discord.com/channels/@me/1266414756882026590',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'x-debug-options': 'bugReporterEnabled',
            'x-discord-locale': 'en-GB',
            'x-discord-timezone': 'Europe/London',
            'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLUdCIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyNi4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTI2LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjMxMzM0NCwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0=',
        }

    def sendMessage(message: str, channel_id: int, token: str, random_string: bool, emojis: bool, mass_ping: bool, message_count: int, emoji_count: int, ping_count: int) -> None:
        for _ in range(message_count):
            original_message = message

            if random_string:
                original_message = f"{original_message} -> {Functions.random_string_func(10)}"

            if emojis:
                emojis_str = ' '.join(random.sample(Core.EMOJIS, emoji_count))
                original_message = f"{original_message} -> {emojis_str}"

            if mass_ping:
                pings = [f"<@{Functions.random_ping_func()}>" for _ in range(ping_count)]
                pings_str = ' '.join(pings)
                original_message = f"{original_message} -> {pings_str}"

            response = Core.Session.post(
                url=f'https://discord.com/api/v9/channels/{channel_id}/messages',
                headers=Functions.returnHeaders(token),
                json={'mobile_network_type': 'unknown', 'content': original_message, 'tts': False, 'flags': 0}
            )

            if response.status_code == 200:
                log.good(f"Succesfully Sent Message | 200 -> {channel_id}")
            elif response.status_code == 429:
                log.warn(f"Ratelimited while sending message | 429 -> {channel_id}")
            elif response.status_code == 400:
                log.bad(f"Failure sending message | 400 -> {channel_id}")
            else:
                log.bad(f"Failure sending message | 401 -> {channel_id}")

    def random_string_func(length: int) -> str:
        return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=length))

    def random_ping_func() -> str:
        with open('core/output/scrapped_IDs.txt', 'r') as file:
            ids = file.readlines()
        return random.choice(ids).strip()

    def scrapperiddz():
        Utils.clear()
        UI.prnt(Vars.banner)
        Utils.settitle('Lost Spammer V1 ┃ Location: [Id Scraper]')
        token = UI.ask("Token")
        serv1 = UI.ask("Guild")
        cha1 = UI.ask("Channel")

        Utils.clear()
        UI.prnt(Vars.banner)

        output_lock = threading.Lock()

        class DevNull:
            def write(self, _):
                pass
            def flush(self):
                pass

        logging.getLogger('discum').setLevel(logging.CRITICAL)
        sys.stdout = DevNull()

        try:
            bot = discum.Client(token=token)

            def closefetching(nothing, guildid):
                if bot.gateway.finishedMemberFetching(guildid):
                    bot.gateway.removeCommand({'function': closefetching, 'params': {'guildid': guildid}})
                    bot.gateway.close()

            def getmembers(guildid, channelid):
                bot.gateway.fetchMembers(guildid, channelid, keep='all', wait=1)
                bot.gateway.command({'function': closefetching, 'params': {'guildid': guildid}})
                bot.gateway.run()
                bot.gateway.resetSession()
                return bot.gateway.session.guild(guildid).members

            members = getmembers(serv1, cha1)
            memberids = []

            for memberId in members:
                memberids.append(memberId)

            with open('core/output/scrapped_IDs.txt', 'w') as ids:
                for element in memberids:
                    ids.write(element + '\n')
        except KeyError:
            pass
        except Exception as e:
            pass

        sleep(2)
        sys.stdout = sys.__stdout__

        with open('core/output/scrapped_IDs.txt', 'r') as print_id:
            for id in print_id:
                try:
                    with output_lock:
                        log.good(f"Scraped | {id}")
                except KeyError:
                    pass

    def chspammer() -> None:
        Utils.clear()
        UI.prnt(Vars.banner)
        Utils.settitle('Lost Spammer V1 ┃ Location: [Channel Spammer]')

        message = UI.ask("Message")
        channel_id = int(UI.ask("Channel (messages)"))
        thread_count = int(UI.ask("Thread Ammount"))
        delay = float(UI.ask("Delay"))
        random_string = UI.ask("Random String | (y/n)").lower() == 'y'
        emojis = UI.ask(f"Random Emojis | (y/n)").lower() == 'y'
        mass_ping = UI.ask("Mass Ping | (y/n)").lower() == 'y'
        message_count = int(UI.ask("Message Ammount"))
        emoji_count = int(UI.ask("Emoji Ammount"))
        ping_count = int(UI.ask("Ping Ammount"))
        auto_scrape = UI.ask("Auto Scrape? | (y/n)").lower() == 'y'

        Utils.clear()
        UI.prnt(Vars.banner)
        Utils.settitle('Lost Spammer V1 ┃ Location: [Channel Spammer]')

        if auto_scrape:
            Functions.scrapperiddz()

        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            futures = []
            for token in Tokens:
                future = executor.submit(Functions.sendMessage, message, channel_id, token, random_string, emojis, mass_ping, message_count, emoji_count, ping_count)
                futures.append(future)
            for future in futures:
                future.result()

    def Formatter() -> None:
        Utils.clear()
        UI.prnt(Vars.banner)
        Utils.settitle('Lost Spammer V1 ┃ Location: [Token Formatter]')

        success = 0
        failure = 0
    
        with open("core/input/tokens.txt", "r") as input_file, open("core/output/formatted_tokens.txt", "w") as output_file:
            for line in input_file:
                line = line.strip()
            
                if ":" in line:
                    token_parts = line.split(":")
                    new_token = token_parts[-1] + "\n"
                    output_file.write(new_token)
                    success += 1
                    log.good(f"Succes | Succesfully Formatted -> {line[:35]}")
                    time.sleep(0.0001)

                else:
                    output_file.write(line + "\n")
                    failure += 1
                    log.bad(f"Failure | Formatting -> {line[:35]}")
                    time.sleep(0.0001)

        Utils.clear()
        UI.prnt(Vars.banner)
        Utils.settitle('Lost Spammer V1 ┃ Location: [Formatter Results]')
        log.good(f"Succes | ({success})")
        log.bad(f"Failure | ({failure})")

    def idscraper():
        Utils.clear()
        UI.prnt(Vars.banner)
        Utils.settitle('Lost Spammer V1 ┃ Location: [Id Scraper]')
        
        token = UI.ask("Token")
        serv1 = UI.ask("Guild")
        cha1 = UI.ask("Channel")

        Utils.clear()
        UI.prnt(Vars.banner)

        output_lock = threading.Lock()

        class DevNull:
            def write(self, _):
                pass
            def flush(self):
                pass

        logging.getLogger('discum').setLevel(logging.CRITICAL)
        sys.stdout = DevNull()

        try:
            bot = discum.Client(token=token)

            def closefetching(nothing, guildid):
                if bot.gateway.finishedMemberFetching(guildid):
                    bot.gateway.removeCommand({'function': closefetching, 'params': {'guildid': guildid}})
                    bot.gateway.close()

            def getmembers(guildid, channelid):
                bot.gateway.fetchMembers(guildid, channelid, keep='all', wait=1)
                bot.gateway.command({'function': closefetching, 'params': {'guildid': guildid}})
                bot.gateway.run()
                bot.gateway.resetSession()
                return bot.gateway.session.guild(guildid).members

            members = getmembers(serv1, cha1)
            memberids = []

            for memberId in members:
                memberids.append(memberId)

            with open('core/output/scrapped_IDs.txt', 'w') as ids:
                for element in memberids:
                    ids.write(element + '\n')

        except KeyError:
            pass
        except Exception as e:
            pass

        sleep(2)
        sys.stdout = sys.__stdout__

        with open('core/output/scrapped_IDs.txt', 'r') as print_id:
            for id in print_id:
                try:
                    with output_lock:
                        log.good("Scraped | {id}")
                except KeyError:
                    pass

    def replyspam() -> None:
        Utils.clear()
        UI.prnt(Vars.banner)
        Utils.settitle(f'Lost Spammer V1 ┃ Location: [Reply Spammer]')

        session = tls_client.Session(client_identifier="chrome_116")

        channelid  : str = UI.ask("Channel ID").strip()
        msg1       : str = UI.ask("Message ID").strip()
        msg2       : str = UI.ask("Your Reply")
        hm         : int = int(UI.ask("Reply Ammount"))
        delay      : float = float(UI.ask("Delay"))

        Utils.clear()
        UI.prnt(Vars.banner)
        Utils.settitle('Lost Spammer V1 ┃ Location: [Reply Spammer]')
   
        token = Core.load('core/input/tokens.txt')

        def process(token, channelid, msg1, msg2, hm):
            for i in range(hm):
                payload = {
                    'content': msg2,
                    'tts': False
                }

                headers = {
                    "accept": "*/*",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "en-US,en;q=0.9",
                    "authorization": token,
                    "cookie": "__dcfduid=88221810e37411ecb92c839028f4e498; __sdcfduid=88221811e37411ecb92c839028f4e498dc108345b16a69b7966e1b3d33d2182268b3ffd2ef5dfb497aef45ea330267cf; locale=en-US",
                    "referer": "https://discord.com/channels/967617613960187974/981260247807168532",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "sec-gpc": "1",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36",
                    "x-discord-locale": "en-US",
                }

                payload['message_reference'] = {
                    "channel_id": channelid,
                    "message_id": msg1
                }

                r = session.post(f"https://discord.com/api/v9/channels/{channelid}/messages", headers=headers, json=payload)

                if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                    log.good(f"Succesfully Sent Reply | ({channelid}) -> ({msg1})")

                elif r.status_code == 429:
                    log.warn(f"Ratelimited | ({channelid}) -> ({msg1})")
                else:
                    log.bad(f"Failure | ({channelid}) -> ({msg1}) | Couldn't Send reply")

                time.sleep(delay)

        with ThreadPoolExecutor() as executor:
            for token in token:
                executor.submit(process, token, channelid, msg1, msg2, hm)

    def changegame(token, game, type, status):
        log.good(f"Succes | Onlined token | {token[:25]}")
        ws = websocket.WebSocket()
        if status == "random":
            stat = ['online', 'dnd', 'idle']
            status = random.choice(stat)
        ws.connect('wss://gateway.discord.gg/?v=6&encoding=json')
        hello = json.loads(ws.recv())
        heartbeat_interval = hello['d']['heartbeat_interval']
        
        if type == "Playing":
            gamejson = {
                "name": game,
                "type": 0
            }
        elif type == 'Streaming':
            gamejson = {
                "name": game,
                "type": 1,
                "url": "https://www.twitch.tv/zetrium"
            }
        elif type == "Listening to":
            gamejson = {
                "name": game,
                "type": 2
            }
        elif type == "Watching":
            gamejson = {
                "name": game,
                "type": 3
            }
    
        auth = {
            "op": 2,
            "d": {
                "token": token,
                "properties": {
                    "$os": sys.platform,
                    "$browser": "RTB",
                    "$device": f"{sys.platform} Device"
                },
                "presence": {
                    "game": gamejson,
                    "status": status,
                    "since": 0,
                    "afk": False
                }
            },
            "s": None,
            "t": None
        }
    
        ws.send(json.dumps(auth))
        ack = {
            "op": 1,
            "d": None
        }
    
        while True:
            time.sleep(heartbeat_interval / 1000)
            try:
                ws.send(json.dumps(ack))
            except Exception as e:
                break

    def activity():
        types = ['Playing', 'Streaming', 'Watching', 'Listening to']
        type = "Watching"
        Utils.clear()
        UI.prnt(Vars.banner)
        Utils.settitle('Lost Spammer V1 ┃ Location: [Token Onliner]')
        game = UI.ask("Activity")
        Utils.clear()
        UI.prnt(Vars.banner)
        Utils.settitle('Lost Spammer V1 ┃ Location: [Token Onliner]')
    
        status = ['online', 'dnd', 'idle', 'random']
        status = status[3]
    
        executor = ThreadPoolExecutor(max_workers=1000)

        futures = []
        for token in open("core/input/tokens.txt", "r+").readlines():
            token = token.strip()
            future = executor.submit(Functions.changegame, token, game, type, status)
            futures.append(future)

        for future in futures:
            future.result()

        exit = UI.ask(f"Press [ Enter ] To go Home")
        exit = MainVisuals.main()

    def send_request(token, channel_id, random_id, delay):
        url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        data = {
            "content": f"?whois {random_id}"
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            log.good(f"Successfully Sent Message | {channel_id} -> {token[:30]}")
        else:
            log.bad(f"Failure Sending Message | {channel_id} -> {token[:30]}")
        time.sleep(delay)

    def send_message(token, channel_id, delay):
        with open("core/output/scrapped_IDs.txt", "r") as file:
            scraped_ids = [line.strip() for line in file.readlines()]

        if not scraped_ids:
            log.warn("No Scraped IDs found in the file.")
            return
    
        random_id = random.choice(scraped_ids)
        send_request(token, channel_id, random_id, delay)

    def dynoexploit():
        Utils.clear()
        UI.prnt(Vars.banner)
        Utils.settitle('Lost Spammer V1 ┃ Location: [Dyno Exploit ┃ (whois)]')

        channel_id = UI.ask("Channel")
        guild_id = UI.ask("Guild")
        delay = float(UI.ask("Delay"))
        thread_count = int(UI.ask("Thread Amount"))
        message_count = int(UI.ask("Message Amount"))
        auto_scrape = UI.ask("Auto Scrape | (y/n)")

        if auto_scrape == "y":
            Functions.id_scraper()

        Utils.clear()
        UI.prnt(Vars.banner)
        Utils.settitle('Lost Spammer V1 ┃ Location: [Dyno Exploit ┃ (whois)]')

        with open("core/input/tokens.txt", "r") as file:
            tokens = [line.strip() for line in file.readlines()]

        if not tokens:
            log.warn("No tokens found in the file.")
            return

        for _ in range(message_count):
            with ThreadPoolExecutor(max_workers=thread_count) as executor:
                for token in tokens:
                    executor.submit(Functions.send_message, token, channel_id, delay)

    def send_message(token, channel_id, scrapped_ids, message_count, delay):
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        url = f'https://discord.com/api/v10/channels/{channel_id}/messages'

        for _ in range(message_count):
            message = f"?whois {random.choice(scrapped_ids)}"
            payload = {
                'content': message
            }
            response = requests.post(url, headers=headers, json=payload)

            if response.status_code == 200:
                log.good(f"Successfully Sent Message | {channel_id} -> {token[:30]}")
            else:
                log.bad(f"Failure Sending Message | {channel_id} -> {token[:30]}")

            time.sleep(delay)

    def start_dynoexploit(tokens, channel_id, scrapped_ids, thread_count, message_count, delay):
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            for token in tokens:
                executor.submit(Functions.send_message, token, channel_id, scrapped_ids, message_count, delay)

    def dynoexploit():
        Utils.clear()
        UI.prnt(Vars.banner)
        Utils.settitle('Lost Spammer V1 ┃ Location: [Dyno Exploit ┃ (whois)]')
        channel_id = UI.ask("Channel")
        guild_id = UI.ask("Guild")
        delay = float(UI.ask("Delay"))
        thread_count = int(UI.ask("Thread Amount"))
        message_count = int(UI.ask("Message Amount"))
        Utils.clear()
        UI.prnt(Vars.banner)
        Utils.settitle('Lost Spammer V1 ┃ Location: [Dyno Exploit ┃ (whois)]')

        tokens = Core.load('core/input/tokens.txt')
        scrapped_ids = Core.load('core/output/scrapped_IDs.txt')

        Functions.start_dynoexploit(tokens, channel_id, scrapped_ids, thread_count, message_count, delay)

    def vanity_sniper() -> None:
        Utils.clear()
        UI.prnt(Vars.banner)
        Utils.settitle('Lost Spammer V1 ┃ Location: [Vanity Claimer]')

        vanity_code : str = UI.ask("Vanity")
        server_id   : str = UI.ask("Guild").strip()
        token       : str = UI.ask("Token").strip()
        Utils.clear()
        UI.prnt(Vars.banner)
        Utils.settitle('Lost Spammer V1 ┃ Location: [Vanity Claimer]')
    
        invite_url   : str = f'https://discord.com/api/v9/invites/{vanity_code}'
        settings_url : str = f'https://discord.com/api/v9/guilds/{server_id}/vanity-url'
    
        headers = {
            'Authorization': f'{token}',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }

        while True:
            try:
                response = requests.get(invite_url)

                if response.status_code == 404:
                    log.bad("Failure | Vanity code is NOT available")
                    time.sleep(1)

                    patch_response = requests.patch(
                        settings_url,
                        headers=headers,
                        json={'code': vanity_code}
                    )

                    if patch_response.status_code == 200:
                        log.good(f"Succes -> {vanity_code} | Has been set for the server")
                        break
                    else:
                        log.bad("Failure | Failed to set vanity code")

                elif response.status_code == 200:
                    log.good(f"Succes | Vanity code is available -> {vanity_code}")
                    time.sleep(1)

                else:
                    log.bad("Unexpected Error")
                    time.sleep(60)

            except requests.RequestException as e:
                log.bad("Bad request")
                time.sleep(60)

    def stringen(length: int = 10) -> str:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def headers(token: str, channel_id: str) -> dict:
        user_agent = generate_user_agent()
        return {
            "Authorization": token,
            "Content-Type": "application/json",
            "User-Agent": user_agent,
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Host": "discord.com",
            "Origin": "https://discord.com",
            "Referer": f"https://discord.com/channels/{channel_id}",
            "TE": "Trailers"
        }

    def send_message(token: str, channel_id: str, message: str, session: tls_client.Session) -> str:
        url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
        random_string = Functions.stringen()
        content = f"{message} -> {random_string}"

        header = Functions.headers(token, channel_id)
        data = {"content": content}

        response = session.post(url, json=data, headers=header)
        if response.status_code == 200:
            message_id = response.json().get("id")
            return message_id
        else:
            log.bad("Failed to send message")
            return None

    def pin_message(token: str, channel_id: str, message_id: str, session: tls_client.Session):
        url = f"https://discord.com/api/v9/channels/{channel_id}/pins/{message_id}"

        header = Functions.headers(token, channel_id)

        while True:
            response = session.put(url, headers=header)
            if response.status_code == 204:
                log.good(f"Succes | Pinned {message_id} -> Succesfully")
                break
            else:
                log.bad(f"Failed | Pinning {message_id} -> [{response.status_code}]")

    def pin_spammer():
        Utils.clear()
        UI.prnt(Vars.banner)
        Utils.settitle('Lost Spammer V1 ┃ Location: [Pin Spammer ┃ One Token]')
        channel_id: str = UI.ask("Channel ID")
        threads: int = int(UI.ask("Thread Ammount"))
        message: str = UI.ask("Message")
        token: str = UI.ask("Token")
        num_messages: int = int(UI.ask("Ammount of messages (pins)"))
        delay: float = float(UI.ask("Delay"))
        Utils.clear()
        UI.prnt(Vars.banner)
        Utils.settitle('Lost Spammer V1 ┃ Location: [Pin Spammer ┃ One Token]')

        session = tls_client.Session('chrome_131', random_tls_extension_order=True)

        with ThreadPoolExecutor(max_workers=threads) as executor:
            for _ in range(num_messages):
                message_id = Functions.send_message(token, channel_id, message, session)
                if message_id:
                    executor.submit(Functions.pin_message, token, channel_id, message_id, session)
                time.sleep(delay)

    def generate_heads(token: str) -> dict:
        return {
            'Authorization': token,
            'User-Agent': generate_user_agent(),
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Dnt': '1',  # no tracking
            'Cookie': 'cf_clearance=1234567890abcdef; locale=en-US; session=abcdef123456; theme=dark; discord_locale=en-US',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-Content-Type-Options': 'nosniff',
            'X-Forwarded-For': '192.168.1.1',
            'X-Forwarded-Port': '443',
            'X-Forwarded-Proto': 'https',
        }

    def nonce() -> str:
        return str(uuid.uuid4().hex)

    def button_bypass(token: str, message_id: str, channel_id: str, guild_id: str):
        try:
            session = Session('chrome_131', random_tls_extension_order=True)
            payload = {"limit": "50", "around": message_id}
            response = session.get(
                f"https://discord.com/api/v9/channels/{channel_id}/messages",
                params=payload,
                headers=Functions.generate_heads(token)
            )

            messages = response.json()
            message_to_click = next((msg for msg in messages if msg["id"] == message_id), None)

            if message_to_click is None:
                log.bad("No buttons found")
                return
        
            buttons = [comp["components"][0] for comp in message_to_click.get("components", [])]
            if not buttons:
                log.bad("Failure | No buttons found in the message")
                return

            for button in buttons:
                data = {
                    "application_id": message_to_click["author"]["id"],
                    "channel_id": channel_id,
                    "data": {
                        "component_type": 2,
                        "custom_id": button["custom_id"],
                    },
                    "guild_id": guild_id,
                    "message_flags": 0,
                    "message_id": message_id,
                    "nonce": Functions.nonce(),
                    "session_id": uuid.uuid4().hex,
                    "type": 3,
                }

                response = session.post(
                    "https://discord.com/api/v9/interactions",
                    headers=Functions.generate_heads(token),
                    json=data
                )

                match response.status_code:
                    case 204:
                        log.good(f"Succes | Succesfully clicked button -> {button['custom_id']}")
                    case _:
                        log.bad(f"Failure | Failed to click -> {button['custom_id']}")

        except Exception as e:
            print("FAILED: Failed to click button", e)

    def buttonbypass():
        Utils.clear()
        UI.prnt(Vars.banner)
        Utils.settitle('Lost Spammer V1 ┃ Location: [Button Clicker ┃ (Button Bypass)]')
        guild_id = UI.ask("Guild")
        message_id = UI.ask("Message")
        channel_id = UI.ask("Channel")
        Utils.clear()
        UI.prnt(Vars.banner)
        Utils.settitle('Lost Spammer V1 ┃ Location: [Button Clicker ┃ (Button Bypass)]')
    
        with open('core/input/tokens.txt', 'r') as file:
            tokens = file.read().splitlines()

        for token in tokens:
            Functions.button_bypass(token, message_id, channel_id, guild_id)

    def guildcheck_headers(token: str):
        user_agent = generate_user_agent(device_type="desktop")
        return {
            "Authorization": token,
            "User-Agent": user_agent,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }

    def get_user_id(token: str) -> str:
        session = tls_client.Session('chrome_131', random_tls_extension_order=True)
        response = session.get(
            "https://discord.com/api/v9/users/@me",
            headers=Functions.guildcheck_headers(token)
        )

        if response.status_code == 200:
            return response.json().get("id")
        else:
            log.bad("Failed getting uid")
            return None

    def guild_checker(guild_id: str):
        in_guild = []

        def main_checker(token: str):
            try:
                user_id = Functions.get_user_id(token)
                if user_id is None:
                    return

                session = tls_client.Session('chrome_131', random_tls_extension_order=True)
                while True:
                    response = session.get(
                        f"https://discord.com/api/v9/guilds/{guild_id}/members/{user_id}",
                        headers=Functions.guildcheck_headers(token)
                    )

                    match response.status_code:
                        case 200:
                            log.good(f"Success | {token[:25]} -> Was found in | {guild_id}")
                            in_guild.append(token)
                            break
                        case 429:
                            retry_after = response.json().get("retry_after")
                            log.warn(f"Ratelimited -> ({token[:25]}) -> Retrying after | {retry_after}")
                            time.sleep(float(retry_after))
                        case 404:
                            log.bad(f"{token[:25]} | Was not found in -> {guild_id}")
                            break
                        case _:
                            log.bad(f"Failure | {token[:25]} | Was not found in guild -> {response.status_code}")
                            break
            except Exception as e:
                log.bad(f"Failure: {str(e)}")

        with open("core/input/tokens.txt", "r") as f:
            tokens = f.read().splitlines()

        for token in tokens:
            main_checker(token)

    def guildcheck():
        Utils.clear()
        UI.prnt(Vars.banner)
        Utils.settitle('Lost Spammer V1 ┃ Location: [Guild Checker]')
        guild_id = UI.ask("Guild")
        Utils.clear()
        UI.prnt(Vars.banner)
        Utils.settitle('Lost Spammer V1 ┃ Location: [Guild Checker]')
        Functions.guild_checker(guild_id)

    def create_invite(token: str, guild_id: str, channel_id: str, delay: float, inv_count: int) -> None:
        url : str = f'https://discord.com/api/v10/channels/{channel_id}/invites'

        headers = {
            'Authorization': f'{token}',
            'Content-Type': 'application/json'
        }
        data = {
            'max_uses': 0,
            'temporary': False,
            'unique': True
        }

        session = requests.Session()

        for _ in range(inv_count):
            response = session.post(url, headers=headers, json=data)
        
            if response.status_code in [200, 201, 204]:
                log.good(f"Succes | {token[:25]} | Created invite -> 200")

            else:
                log.bad(f"Failure | {token[:25]} | Creating invite -> 400")
            time.sleep(delay)

    def start_invites(tokens: list[str], guild_id: str, channel_id: str, inv_count: int, delay: float) -> None:
        threads: list[threading.Thread] = []
        for token in tokens:
            thread = threading.Thread(target=Functions.create_invite, args=(token, guild_id, channel_id, delay, inv_count))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def logspam() -> None:
        Utils.clear()
        UI.prnt(Vars.banner)
        Utils.settitle('Lost Spammer V1 ┃ Location: [Invite Spammer ┃ (Audit Bomber)]')

        tokens = Core.load("core/input/tokens.txt")
        guild_id       : str = UI.ask("Guild").strip()
        channel_id     : str = UI.ask("Channel").strip()
        inv_count      : int = int(UI.ask("Invite Ammount"))
        delay          : float = float(UI.ask("Delay"))
    
        Utils.clear()
        UI.prnt(Vars.banner)
        Utils.settitle('Lost Spammer V1 ┃ Location: [Invite Spammer ┃ (Audit Bomber)]')
    
        Functions.start_invites(tokens, guild_id, channel_id, inv_count, delay)

onboard_bypass = OnboardBypass()

class MainVisuals:
    def main():
        Utils.clear()
        Utils.settitle('Lost Spammer V1 ┃ Location: [Page (one)] ┃ Fuck skids')
        visual.size(126, 24)
        UI.prnt(Vars.opts)
        
        Cursor.hide()
        choice = UI.ask(f'input')

        options = {
            '1': UtilsFuncs.notbuilt, # 1
            '2': UtilsFuncs.notbuilt, # 2
            '3': Functions.Formatter, # done
            '4': UtilsFuncs.notbuilt, # 3
            '5': UtilsFuncs.notbuilt, # 4
            '6': Functions.chspammer, # done
            '7': Functions.replyspam, # done
            '8': UtilsFuncs.notbuilt, # 5
            '9': UtilsFuncs.notbuilt, # 6
            '10': UtilsFuncs.notbuilt, # 7
            '11': Functions.guildcheck, # done
            '13': UtilsFuncs.notbuilt, # 8
            '14': UtilsFuncs.notbuilt, # 9
            '15': Functions.activity, # done
            '16': UtilsFuncs.notbuilt, # 10
            '17': UtilsFuncs.notbuilt, # 11
            '18': bypass.accept_rules, # done
            '19': UtilsFuncs.notbuilt, # 12
            '20': UtilsFuncs.notbuilt, # 13
            '21': UtilsFuncs.notbuilt, # 14
            '22': Functions.vanity_sniper, # done
            '23': Functions.idscraper, # done
            '24': UtilsFuncs.notbuilt, # 15
            '25': Functions.logspam, # done
            '26': Functions.dynoexploit, # done
            '27': UtilsFuncs.notbuilt, # 17
            '28': UtilsFuncs.notbuilt, # 18
            '29': UtilsFuncs.notbuilt, # 19
            '30': onboard_bypass.onboard_bypass, # done
            '31': Functions.pin_spammer, # done
            '32': Functions.buttonbypass, # done
        }

        if choice in options:
            options[choice]()
        else:
            MainVisuals.main()

if __name__ == "__main__":
    intro()
    MainVisuals.main()