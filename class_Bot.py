import requests
from data_test_bot import *
from urls_teleg import root_url
from bot_logic import select_handling_answer 

class Bot():

	root_url=root_url


	def __init__(self, token=token, username=username, bot_name=name):
		self.token=token
		self.username=username
		self.bot_name=name


	def get_updates(self):
		response=requests.get(f"{self.root_url}{self.token}/getUpdates")
		status=response.status_code
		if  status in (200, 201, 202):
			updates=response.json()
			return updates
		else:
			raise Exception(f"request failed. Status is {status}")


	def send_message(self, chat_id="", text="", update_id=0):
		data={"chat_id": chat_id,
			"text": text}
		requests.post(f"{self.root_url}{self.token}/sendMessage", data)
		requests.get(f"{self.root_url}{self.token}/getUpdates?offset={update_id+1}")

	def wait_answer(self):
		result=[]
		while len(result)==0:
			updates=self.get_updates()
			result=updates["result"]


	def prepare_answer_text(self, message="nothing", user="NoName"):
		answer_text=select_handling_answer(message=message, user=user)
		return  answer_text


	def working(self):
		is_working=True
		while is_working:
			self.wait_answer()
			updates=self.get_updates()

			chat_id=updates["result"][0]["message"]["chat"]["id"]
			message=updates["result"][0]["message"]["text"]
			update_id=updates["result"][0]["update_id"]
			user=updates["result"][0]["message"]["from"]["first_name"]

			answer_text=self.prepare_answer_text(message=message, user=user)
			self.send_message(chat_id=chat_id, text=answer_text, update_id=update_id)
			if message.lower()=="exit":
				break


my_bot=Bot()
print(my_bot)
my_bot.working()		