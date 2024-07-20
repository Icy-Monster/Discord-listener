import websocket
import json

import threading
import time



Token = "" # Set this to your Discord account token- https://www.geeksforgeeks.org/how-to-get-discord-token/

#################### LISTENER ####################
def send_json_request(ws, request):
    ws.send(json.dumps(request))

def receive_json_response(ws):
    response = ws.recv()
    if response:
        return json.loads(response)

def heartbeat(interval, ws):
    print("Heartbeat begin")

    while True:
        time.sleep(interval)
        heartbeatJSON = {
            "op": 1,
            "d": "null"
        }
        send_json_request(ws, heartbeatJSON)
        print("Heartbeat sent")

ws = websocket.WebSocket()
ws.connect('wss://gateway.discord.gg/?v=6&encording=json')
event = receive_json_response(ws)

heartbeat_interval = event['d']['heartbeat_interval'] / 1000
threading._start_new_thread(heartbeat, (heartbeat_interval, ws))

payload = {
    'op': 2,
    "d": {
        "token": Token,
        "properties": {
            "$os": "windows",
            "$browser": "chrome",
            "$device": "pc"
        }
    }
}
send_json_request(ws, payload)
#################### LISTENER ####################


while True:
    event = receive_json_response(ws)

    try:
        print(event['d'])

        op_code = event('op')
        if op_code == 11:
            print("heartbeat received")
    except:
        pass