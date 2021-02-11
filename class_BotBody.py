import requests
from data_test_bot import *
from urls_teleg import root_url
 

class BotBody():

	root_url=root_url
	getUpdates="/getUpdates"
	sendMessage="/sendMessage"
	bot_token=token

	def __init__(self, bot_token=token, username=username, bot_name=name):
		self.bot_token=token
		self.username=username
		self.bot_name=name


	def get_updates(self):
		response=requests.get(f"{self.root_url}{self.bot_token}{self.getUpdates}")
		status=response.status_code
		if  status in (200, 201, 202):
			updates=response.json()
			return updates
		else:
			raise Exception(f"request failed. Status is {status}")


	def send_message(self, chat_id="", text="", update_id=0):
		data={"chat_id": chat_id,
			"text": text}
		requests.post(f"{self.root_url}{self.bot_token}{self.sendMessage}", data)
		requests.get(f"{self.root_url}{self.bot_token}{self.getUpdates}?offset={update_id+1}")

	def give_answer(self, text=None):
		updates=self.get_updates()
		chat_id=updates["result"][0]["message"]["chat"]["id"]
		update_id=updates["result"][0]["update_id"]

		self.send_message(chat_id=chat_id, text=text, update_id=update_id)

	def wait_answer(self):
		result=[]
		while len(result)==0:
			updates=self.get_updates()
			result=updates["result"]




my_bot=BotBody()
"""
print(my_bot)
my_bot.working()		
"""