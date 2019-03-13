import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from .models import Thread, ChatMessage
from .tasks import add, mul, xsum

class ChatConsumer(AsyncConsumer):
	async def websocket_connect(self, event):
		print ("connected", event)
		
		other_user = self.scope['url_route']['kwargs']['username']
		me = self.scope['user']
		# print(other_user, me)
		thread_obj = await self.get_thread(me, other_user)

		self.thread_obj = thread_obj
		chat_room = "thread_{}".format(thread_obj.id)
		self.chat_room = chat_room

		await self.channel_layer.group_add(
			chat_room,
			self.channel_name
		)

		await self.send({
			"type": "websocket.accept"
		})

		# await asyncio.sleep(10)
		

	async def websocket_receive(self, event):
		# when a message is received from the websocket
		print ("receive", event)
		# result_cel = add.delay(4, 4)
		# 수신 받으면 다음에 해당하는 리스트를 또 보낸다.
		front_text = event.get('text', None)
		if front_text is not None:
			loaded_dict_data = json.loads(front_text)
			msg = loaded_dict_data.get('message')

			user = self.scope['user']
			username = 'default'
			if user.is_authenticated:
				username = user.username
			myResponse = {
				'message' : msg,
				'username' : username
			}
			await self.create_chat_message(user, msg)
			

			#broadcasts the  message event to be sent
			await self.channel_layer.group_send(
				self.chat_room,
				{
					"type": "chat_message",
					"text": json.dumps(myResponse)
				}
			)

	async def chat_message(self, event):
		# send the actual message
		print('message', event)
		await self.send({
				"type": "websocket.send",
				"text": event['text']
			})
		# {'type': 'websocket.receive', 'text': 'sss'}

	async def websocket_disconnect(self, event):
		# when the socket connects
		print ("disconnected", event)

	@database_sync_to_async
	def get_thread(self, user, other_username):
		return Thread.objects.get_or_new(user, other_username)[0]
	
	@database_sync_to_async
	def create_chat_message(self, me, msg):
		thread_obj = self.thread_obj
		return ChatMessage.objects.create(thread = thread_obj , user = me , message = msg)
	
