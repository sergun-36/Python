from for_telegram_api import give_answer, get_first_message, wait_answer
from info_for_test import questions

def create_message_from_scroll(scroll, subject=""):
	message=f"Выберете, пожалуйста, {subject} из перечня:"
	for item in scroll:
		message+=f"\n {item}"

	return message

def check_correct_user_answer(answer, correct_answer):
	if answer==correct_answer:
		return 1
	else:
		return 0	


def check_user_answer(message, scroll):
	message=message.lower()
	if message in scroll:
		return message


def get_user_answer(interface, scroll):
	message=create_message_from_scroll(scroll)
	user_answer=None
	while not user_answer:
		if interface=="telegram":
			wait_answer()
			first_message=get_first_message()
			user_answer=check_user_answer(first_message,scroll)
		else:
			user_answer=check_user_answer(input(), scroll)
		
		if user_answer:
			break

		if interface=="telegram":
			give_answer(message)
		else:
			print(message)
	return user_answer


def asking_one_theme(interface, test_questions):
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

		if interface=="telegram":
			give_answer(question_message)
		else:
			print(question_message)

		user_answer=get_user_answer(interface, answers)
		final_message+=f"\n{question_message}\nВаш ответ - {user_answer}\nПравильный ответ - {correct_answer}"
		right_answers+=check_correct_user_answer(user_answer, correct_answer)

	result=round(right_answers/len(test_questions)*100, 2)
		
	return {"final_message":final_message,
			"result": result}


def asking_questions(interface, theme, difficulty, questions):
	if theme!="all":
		test_questions=questions[theme][difficulty]
		result=asking_one_theme(interface, test_questions)
		return result

	else:
		count_of_theme=0
		total_result=0
		final_message=""

		for theme in questions:
			if difficulty not in questions[theme]:
				continue

			test_questions=questions[theme][difficulty]
			result=asking_one_theme(interface, test_questions)

			count_of_theme+=1
			total_result+=result["result"]
			final_message+=result["final_message"]

		result=round(total_result/count_of_theme, 2)

		return{"final_message":final_message,
				"result":result}


	

	result=round(right_answers/len(questions[difficulty])*100, 2)
	return result


def testing(interface):
	choice_theme_message=create_message_from_scroll(questions.keys(), "тему")
	if interface=="telegram":
		give_answer(choice_theme_message)
	else:
		print(choice_theme_message)

	theme=get_user_answer(interface, questions.keys())

	if theme=="all":
		difficulties=("easy","medium","hard")
	else:
		difficulties=questions[theme]

	choice_difficulty_message=create_message_from_scroll(difficulties, "сложность")

	if interface=="telegram":
		give_answer(choice_difficulty_message)
	else:
		print(choice_difficulty_message)
	
	difficulty=get_user_answer(interface, difficulties)
	print(difficulty)
	result=asking_questions(interface, theme, difficulty, questions)
	result_test_message=f"\nРезультаты теста таковы\n{result['final_message']}\n\n {result['result']}% правильных ответов"

	if interface=="telegram":
		return result_test_message
	else:
		print(result_test_message)


#testing("terminal")


