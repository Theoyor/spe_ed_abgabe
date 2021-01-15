#!/usr/bin/env python3

import asyncio
import json
import os
import random
import websockets


async def play():
    url = "wws://msoll.de/spe_ed"
    key = "NMZ3XQEFLKBUP2434UFJONU4QCGTACGEHOWATQWHS7L4PDL5CGXZZGYX"

    async with websockets.connect(f"{url}?key={key}") as websocket:
        f = open('data.json', 'w+')
        f.write('{"game":[{"0":"dummy"}')
        f.close()
        print("Waiting for initial state...", flush=True)
        while True:
            rd = 0
            state_json = await websocket.recv()
            state = json.loads(state_json)
            with open('data.json', 'a') as f:
                f.write(',')
                f.write(json.dumps(state))

            #print("<", state)
            own_player = state["players"][str(state["you"])]
            if not state["running"] or not own_player["active"]:
                break
            action = start_rek(state, rd)
            print(">", action)
            action_json = json.dumps({"action": action})
            await websocket.send(action_json)
            rd += 1
        f = open('data.json', 'a')
        f.write(']}')
        f.close()

asyncio.get_event_loop().run_until_complete(play())