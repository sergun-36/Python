from class_BotBody import BotBody
from info_for_test import questions


class Test(BotBody):

	def create_message_from_scroll(self, scroll, subject=""):
		message=f"Выберете, пожалуйста, {subject} из перечня:"
		for item in scroll:
			message+=f"\n {item}"
		return message

	def check_correct_user_answer(self, answer, correct_answer):
		if answer==correct_answer:
			return 1
		else:
			return 0	


	def check_user_answer(self, message, scroll):
		message=message.lower()
		if message in scroll:
			return message


	def get_user_answer(self,  scroll):
		message=self.create_message_from_scroll(scroll)
		user_answer=None
		while not user_answer:
			if self.interface=="telegram":
				self.wait_answer()
				chat_id=self.get_updates()["result"][0]["message"]["chat"]["id"]
				
				while self.test_chat_id!=chat_id:
					self.give_answer(text="Sorry, somebody is testing, try later")
					self.wait_answer()
					chat_id=self.get_updates()["result"][0]["message"]["chat"]["id"]
					print(self.test_chat_id!=chat_id)

				first_message=self.get_updates()["result"][0]["message"]["text"]
				user_answer=self.check_user_answer(first_message,scroll)
			else:
				user_answer=self.check_user_answer(input(), scroll)
			
			if user_answer:
				break

			if self.interface=="telegram":
				self.give_answer(text=message)
			else:
				print(message)
		return user_answer


	def asking_one_theme(self, test_questions):
		right_answers=0
		final_message=""
		for question in test_questions:
			answers=question["answers"]
			correct_answer=question["correct_answer"]
			question=question["question"]
			answers_message=""
			for key, value in answers.items():
				answers_message+=f"\n{key}) {value}"
			question_message=f"{question}\n{answers_message}"

			if self.interface=="telegram":
				self.give_answer(text=question_message)
			else:
				print(question_message)

			user_answer=self.get_user_answer(answers)
			final_message+=f"\n{question_message}\nВаш ответ - {user_answer}\nПравильный ответ - {correct_answer}"
			right_answers+=self.check_correct_user_answer(user_answer, correct_answer)

		result=round(right_answers/len(test_questions)*100, 2)
			
		return {"final_message":final_message,
				"result": result}


	def asking_questions(self, theme, difficulty, questions):
		if theme!="all":
			test_questions=questions[theme][difficulty]
			result=self.asking_one_theme(test_questions)
			return result

		else:
			count_of_theme=0
			total_result=0
			final_message=""

			for theme in questions:
				if difficulty not in questions[theme]:
					continue

				test_questions=questions[theme][difficulty]
				result=self.asking_one_theme(test_questions)

				count_of_theme+=1
				total_result+=result["result"]
				final_message+=result["final_message"]

			result=round(total_result/count_of_theme, 2)

			return{"final_message":final_message,
					"result":result}


		

		result=round(right_answers/len(questions[difficulty])*100, 2)
		return result


	def testing(self, interface=None):
		self.interface=interface
		self.test_chat_id=self.get_updates()["result"][0]["message"]["chat"]["id"]
		print(self.test_chat_id)

		choice_theme_message=self.create_message_from_scroll(questions.keys(), "тему")
		
		if self.interface=="telegram":
			self.give_answer(text=choice_theme_message)
		else:
			print(choice_theme_message)

		theme=self.get_user_answer(questions.keys())

		if theme=="all":
			difficulties=("easy","medium","hard")
		else:
			difficulties=questions[theme]

		choice_difficulty_message=self.create_message_from_scroll(difficulties, "сложность")

		if self.interface=="telegram":
			self.give_answer(text=choice_difficulty_message)
		else:
			print(choice_difficulty_message)
		
		difficulty=self.get_user_answer(difficulties)
		print(difficulty)
		result=self.asking_questions(theme, difficulty, questions)
		result_test_message=f"\nРезультаты теста таковы\n{result['final_message']}\n\n {result['result']}% правильных ответов"

		if self.interface=="telegram":
			return result_test_message
		else:
			print(result_test_message)

#test=Test()
#test.testing()


