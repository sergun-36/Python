import requests
from urls_teleg import root_url
from data_test_bot import token

#url='https://api.telegram.org/bot{}/{}'

def get_updates(token=token):
	response=requests.get(f"{root_url}{token}/getUpdates")
	status=response.status_code
	if status in (200, 201, 202):
		updates=response.json()
		return updates
	else:
		raise Exseption(f"request failed. Status is {status}")


def wait_answer():
	result=[]
	while len(result)==0:
		updates=get_updates()
		result= result["result"]


def get_first_update_id():
	updates=get_updates()
	first_update_id= updates["result"][0]["update_id"]
	return first_update_id


def get_first_chat_id():
	updates=get_updates()
	first_chat_ID=updates["result"][0]["message"]["chat"]["id"]
	return first_chat_ID


def get_first_message():
	updates=get_updates()
	first_message=updates["result"][0]["message"]["text"]
	return first_message


def get_user():
	updates=get_updates()
	name=updates["result"][0]["message"]["from"]["first_name"]

	if not name:
		name="Stranger"

	return {"name": name}


def send_message_from_bot(chat_id="",text="", token=token):
	data={'chat_id': chat_id,
			'text': text}
	requests.post(f"{root_url}{token}/sendMessage", data)


def give_answer(answer_message="I don't have answer"):
	chat_id=get_first_chat_id()
	first_update_id=get_first_update_id()
	if not chat_id:
		return
		
	send_message_from_bot(chat_id=chat_id, text=answer_message)
	requests.get(f"{root_url}{token}/getUpdates?offset={first_update_id+1}")
	print("all OK")