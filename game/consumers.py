import contextlib
from channels.generic.websocket import AsyncJsonWebsocketConsumer
import random
from game.helpers import *

class GameConsumer(AsyncJsonWebsocketConsumer):
 
    board = {
        0: '', 1: '', 2: '',
        3: '', 4: '', 5: '',
        6: '', 7: '', 8: '',
    }
    
    async def connect(self):
        print(self.scope['url_route']['kwargs']['id'])
        self.room_id = self.scope['url_route']['kwargs']['id']
        self.group_name = f"group_{self.room_id}"

        with contextlib.suppress(KeyError):
            if(len(self.channel_layer.groups[self.group_name]) >= 2):
                await self.accept()
                await self.send_json({
                    "event": "show_error",
                    "error": "This room is fool!! Just like you"
                })
                return await self.close(1)
            
        await self.accept()
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        if(len(self.channel_layer.groups[self.group_name]) == 2):
            tmpGroup = list(self.channel_layer.groups[self.group_name])
            first_player = random.choice(tmpGroup)
            tmpGroup.remove(first_player)
            final_group = [first_player, tmpGroup[0]]
            for i, channel_name in enumerate(final_group):
                await self.channel_layer.send(channel_name, {
                    "type": "gameData.send",
                    "data": {
                        "event": "game_start",
                        "board": self.board,
                        "myTurn": True if i==0 else False
                    }
                })

    

    
    async def receive_json(self, content, **kwargs):
        print(content)
        if(content['event'] == "boardData_send"):
    
            winner = checkWin(content['board'])
            if(winner):
                return await self.channel_layer.group_send(self.group_name, {
                    "type": "gameData.send",
                    "data": {
                        "event": "won",
                        "board": content['board'],
                        "winner": winner,
                        "myTurn": False,
                    }
                })
            elif(isDraw(content['board'])):
                return await self.channel_layer.group_send(self.group_name, {
                    "type": "gameData.send",
                    "data": {
                        "event": "draw",
                        "board": content['board'],
                        "myTurn": False,
                    }
                })
            else:
            
                for channel_name in self.channel_layer.groups[self.group_name]:
                    await self.channel_layer.send(channel_name, {
                        "type": "gameData.send",
                        "data": {
                            "event": "boardData_send",
                            "board": content['board'],
                            "myTurn": False if self.channel_name==channel_name else True
                        }
                    })
             
        elif(content['event'] == "restart"):

            if(len(self.channel_layer.groups[self.group_name]) == 2):
                tmpGroup = list(self.channel_layer.groups[self.group_name])
                first_player = random.choice(tmpGroup)
                tmpGroup.remove(first_player)
                final_group = [first_player, tmpGroup[0]]
                for i, channel_name in enumerate(final_group):
                    await self.channel_layer.send(channel_name, {
                        "type": "gameData.send",
                        "data": {
                            "event": "game_start",
                            "board": self.board,
                            "myTurn": True if i==0 else False
                        }
                    })

 
    async def disconnect(self, code):
        if(code==1):
            return 
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await self.channel_layer.group_send(self.group_name, {
            "type": "gameData.send",
            "data": {
                "event": "opponent_left",
                "board": self.board,
                "myTurn": False,
            }
        })
        

     
    async def gameData_send(self, context):
        await self.send_json(context['data'])
        

     