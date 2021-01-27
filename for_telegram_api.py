import requests
from urls_teleg import *
from handling_curr import do_get_request

#url='https://api.telegram.org/bot{}/{}'


def wait_answer():
	result=[]
	while len(result)==0:
		result=do_get_request(url_teleg_updates)
		
		if "type" in result:
			return None
		result= result["result"]
	#now_update_id=get_last_update_id()


def get_first_update_id():
	result=do_get_request(url_teleg_updates)
	
	if "type" in result:
		return None

	if len(result["result"])==0:
		return None

	first_update_id= result["result"][0]["update_id"]
	return first_update_id

"""
def is_update(now_update_id):
	last_update_id=get_last_update_id()

	if now_update_id!=last_update_id and last_update_id != None:
		#do_get_request(f"{url_teleg_updates}?offset={last_update_id}")
		return True
	else:
		return False
"""


def get_first_chat_id():
	result=do_get_request(url_teleg_updates)

	if "type" in result:
		return result

	if len(result["result"])==0:
		return {"type":"error",
				"text":"Диалоги бота не обнаружены"}

	first_chat_ID=result["result"][0]["message"]["chat"]["id"]
	return first_chat_ID


def get_first_message():
	result=do_get_request(url_teleg_updates)

	if "type" in result:
		return result["text"]

	first_message=result["result"][0]["message"]["text"]
	return first_message


def get_user():
	result=do_get_request(url_teleg_updates)

	if not result:
		return
	name=result["result"][0]["message"]["from"]["first_name"]

	if not name:
		name="Stranger"
	return {"name": name}


def send_message_from_bot(chat_ID,text):
	data={'chat_id': chat_ID,
			'text': text}
	requests.post(url_teleg_send, data)


def give_answer(answer_message):
	chat_id=get_first_chat_id()
	first_update_id=get_first_update_id()
	if not chat_id:
		return

	if type(chat_id)==dict:
		print(chat_id["text"])
		return
		
	send_message_from_bot(chat_id, answer_message)
	do_get_request(f"{url_teleg_updates}?offset={first_update_id+1}")
	print("all OK")