# This script works with turbowarp's custom websocket feature
# wss://amogus-scratch-server1.onrender.com

from simple_websocket_server import WebSocketServer, WebSocket
import random
import json

class Turbowap(WebSocket):        
    def handle(self):
        global client_players
        global clients
        global rooms
        print(self.data)
        if "TO_HOST" in str(self.data):
            request_id = str(self.data).split(".")[1].split("?")[0]
            
            if "playerid=null" in str(self.data):
                print(request_id)
                player_id = str(random.randint(0,1000000))
                client_players[self] = player_id
                
                self.send_message(json.dumps({"method":"set","project_id":"701819238","name":"☁ TO_HOST","value":player_id+"?id="+request_id}))
            
            if "?newroom" in str(self.data):

                if len(list(rooms.keys())) > 30:
                    self.send_message(json.dumps({"method":"set","project_id":"701819238","name":"☁ TO_HOST","value":"!full"+"?id="+request_id}))
                    return
                    
                room_id = str(random.randint(0,1000000))
                hostname = str(self.data).split("hostname=")[1].split("&")[0]
                playerid = str(self.data).split("playerid=")[1].split("&")[0]
        
                rooms[room_id] = {"hostname":hostname,"playerdata":{playerid:""},"status":1,"private":False}
                self.send_message(json.dumps({"method":"set","project_id":"701819238","name":"☁ TO_HOST","value":room_id+"?id="+request_id}))
        else:
            try:
                playerid = str(self.data).split("playerid=")[1].split("&")[0]
                roomid = str(self.data).split("roomid=")[1].split("&")[0]
                hostname = str(self.data).split("hostname=")[1].split("&")[0]

                rooms[roomid]["hostname"] = hostname
                rooms[roomid]["playerdata"][playerid] = str(self.data).split('value":"')[0].split('"')[0]
                print(rooms[roomid]["playerdata"][playerid])
            except Exception as e:
                print(e)
                
    def connected(self):
        global client_players
        global clients        
        print(self.address, 'connected')
        clients.append(self)

    def handle_close(self):
        global client_players
        global clients
        clients.remove(self)
        client_players.pop(self)
        print(self.address, 'closed')


clients = []
client_players = {}
rooms = {}

server = WebSocketServer('0.0.0.0', 8000, Turbowap)
server.serve_forever()
