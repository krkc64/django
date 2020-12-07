import json
from channels.generic.websocket import AsyncWebsocketConsumer
client_dict = {}
user_list = []
data1 = []
data2 = []
num = 100
role = 'leader'
class whiteboard(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "board"
        self.room_group_name = "drawingboard"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        if (data1 != None and data2 != None):
            x =len(data1)
            if(x != 0):
                for j in range(x):
                    await self.send(text_data=json.dumps({
                        'type': 'numbers',
                        'start': data1[j],
                        'coordinate': data2[j]
                    }))


    async def disconnect(self, close_code):
        #print(client_dict["ravi"] == self)
        #print("client has disconnected ")
        global num
        for x, y in client_dict.items():
            if y == self:
                num = user_list.index(x)
                user_list.remove(x)
                #print("updated user list", user_list)
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'numbers',
                        'user_list': user_list,
                        'disc': 'yes',

                    }
                )
                if num == 0:

                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'numbers',
                            'username':  user_list[0],
                            'user_list': user_list,
                            'role': 'leader',
                            'lead_name': user_list[0],
                            'lead_disc': 'yes'

                        }
                    )

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):

        recived_data = json.loads(text_data)
        if recived_data["conn"] == 'new':
            global role
            curr_role = role
            role = 'member'
            user = recived_data["username"]
            msg_type = recived_data["type"]
            user_list.append(user)
            client_dict[user] = self
            #print("client idct is", client_dict)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': msg_type,
                    'username': user,
                    'user_list': user_list,
                    'role': curr_role,
                    'lead_name': user_list[0]

                }
            )

        elif recived_data["erase"] == 'yes':
            user = recived_data["username"]
            msg_type = recived_data["type"]
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': msg_type,
                    'username': user,
                    'erase': recived_data["erase"]

                }
            )

        else:

            msg_type = recived_data["type"]
            user = recived_data["username"]
            data1.append(recived_data["start"])
            data2.append(recived_data["coordinate"])
            # print("data 1 is", data1)
            # print("data2 is ", data2)
            if(data1 != None and data2 != None):
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': msg_type,
                        'start': recived_data["start"],
                        'coordinate': recived_data["coordinate"],
                        'username': user

                    }
                )


    async def numbers(self, event):

        await self.send(text_data=json.dumps(event))


