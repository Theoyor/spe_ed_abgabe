#!/usr/bin/env python3

import asyncio
import json
import os
import random
import requests
import websockets
from spe_ed_lib import start_rek
from datetime import *

FMT = '%Y:%m:%d:%H:%M:%S:%f'
FMK = '%Y:%m:%d:%H:%M:%S'

async def play():
    url = 'wss://msoll.de/spe_ed'
    key = 'NMZ3XQEFLKBUP2434UFJONU4QCGTACGEHOWATQWHS7L4PDL5CGXZZGYX'

    async with websockets.connect(f"{url}?key={key}") as websocket:

        print("Waiting for initial state...", flush=True)
        # Berechne Zeitdifferenz zwischen Serverseite und Programmseite um die Deadline zu modifizieren
        time = datetime.now()
        st = requests.get('https://msoll.de/spe_ed_time')
        serv_t = st.content.decode().replace('-', ':').replace('T', ':').replace('}', "\"").replace('Z', "\"").split("\"")
        serv_time = serv_t[3] + serv_t[7]
        time_diff = time - datetime.strptime(serv_time, FMT)

        rd = 0

        while True:
            print("---------round:",rd,"----------")
            print("server time: ",requests.get('https://msoll.de/spe_ed_time').content)
            state_json = await websocket.recv()
            state = json.loads(state_json)
            print("deadline: {}",state["deadline"]);
            print(">",state)
            newDeadline = datetime.strptime(state['deadline'].replace('-',':').replace('T',':').split('Z')[0], FMK) - time_diff
            deadlineTicks = (newDeadline-datetime(1970, 1, 1)).total_seconds()

            own_player = state["players"][str(state["you"])]
            if not state["running"] or not own_player["active"]:
                break
            # Starte eigenen Algorithmus
            action = start_rek(state, rd, deadlineTicks)
            print(">", action)
            action_json = json.dumps({"action": action})
            await websocket.send(action_json)
            rd += 1
            print("abgabe: ",requests.get('https://msoll.de/spe_ed_time').content)

asyncio.get_event_loop().run_until_complete(play())