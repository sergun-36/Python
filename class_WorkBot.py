from class_RateCurrInfo import RateCurrInfo
#from class_BotBody import BotBody
from class_Test import Test


class WorkBot(RateCurrInfo, Test):

	def prepare_answer_text(self, message=None, user=None):
		message=message.lower()
		if message.find("курс")>=0:
			answer_text=self.get_rate_info(user=user, message=message)
			return answer_text
		
		if message.find("тест")>=0:
			answer_message=self.testing("telegram")
			return answer_message
		
		if message.find("exit")>=0:
			return "Bye, bye .Я отключился"
				
		return message


	def working(self):
		is_working=True
		while is_working:
			self.wait_answer()
			updates=self.get_updates()

			message=updates["result"][0]["message"]["text"]
			user=updates["result"][0]["message"]["from"]["first_name"]

			answer_text=self.prepare_answer_text(message=message, user=user)
			self.give_answer(text=answer_text)
			if message.lower()=="exit":
				break
	

work_bot=WorkBot()
work_bot.working()	
"""
def run_bot():
	is_working=True
	while is_working:
		wait_answer()
		message=get_first_message()

		if select_handling_answer(message)!=None:
			is_working=False
		
	
		
if __name__=="__main__":
	run_bot()
"""



# except ImportError as ex:
# 	print(f" Обнаружено исключение импорта\n {ex}")

