#!/usr/bin/env python3

import asyncio
import json
import os
import random
import requests
import websockets
from spe_ed_lib import start_rek
from datetime import *

async def play():
    url = 'wss://msoll.de/spe_ed'
    key = 'NMZ3XQEFLKBUP2434UFJONU4QCGTACGEHOWATQWHS7L4PDL5CGXZZGYX'

    async with websockets.connect(f"{url}?key={key}") as websocket:
        #f = open('data.json', 'w+')
        #f.write('{"game":[{"0":"dummy"}')
       # f.close()
        print("Waiting for initial state...", flush=True)
        serv_time = requests.get('https://msoll.de/spe_ed_time')
        print(serv_time.content)
        rd = 0

        time = datetime.now()
        st = requests.get('https://msoll.de/spe_ed_time')
        serv_t = st.content.decode().replace('-', ':').replace('T', ':').replace('}', "\"").replace('Z', "\"").split("\"")
        serv_time = serv_t[3] + serv_t[7]
        FMT = '%Y:%m:%d:%H:%M:%S:%f'
        FMK = '%Y:%m:%d:%H:%M:%S'
        diff = time - datetime.strptime(serv_time, FMT)

        while True:
            print("---------round:",rd,"----------")
            print("server time: ",requests.get('https://msoll.de/spe_ed_time').content)
            state_json = await websocket.recv()
            state = json.loads(state_json)
            print("<", state)
            print(state['deadline'])
            newDeadline = datetime.strptime(state['deadline'].replace('-',':').replace('T',':').split('Z')[0], FMK) - diff
            deadlineTicks = (newDeadline-datetime(1970, 1, 1)).total_seconds()

            #with open('data.json', 'a') as f:
            #    f.write(',')
            #    f.write(json.dumps(state))

            own_player = state["players"][str(state["you"])]
            if not state["running"] or not own_player["active"]:
                break

            action = start_rek(state, rd, deadlineTicks)
            print(">", action)
            action_json = json.dumps({"action": action})
            await websocket.send(action_json)
            rd += 1
            print("abgabe: ",requests.get('https://msoll.de/spe_ed_time').content)
        #f = open('data.json', 'a')
        #f.write(']}')
        #f.close()

asyncio.get_event_loop().run_until_complete(play())