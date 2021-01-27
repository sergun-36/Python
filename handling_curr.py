import requests
import datetime
from all_currensies import all_currs


def do_get_request(url):
	ok_codes=(200, 201, 202)
	try:
		response=requests.get(url)
		if response.status_code in ok_codes:
			result=response.json()
			return result
		else:
			message=f"Запрос вернул ошибку со статусом {response.status_code}"
			print(f"Запрос вернул ошибку со статусом {response.status_code}")
			result={"type" : "error",
					"text" : message}
			return result
	except Exception as ex:
		print("Thix is exception")
		return {"type":"error",
				"text":f"\nВозникло исключение: \n{ex}. \nПроверьте соединение с интернетом"}


def get_dates_from_message(message):
	message=message.upper()
	words_message=message.split(" ")
	
	if message.find("СЕГОДН")>=0 or message.find("СЕЙЧАС")>=0:
		dates=str(datetime.date.today())
		return [dates]

	if message.find("ДИНАМИК")>=0 or message.find("ИЗМЕНЕНИ")>=0:
		index_days_ago=words_message.index("ЗА")+1
		days_ago=int(words_message[index_days_ago])
		dates=[]
		for i in range(0, days_ago+1):
			dates.append(str((datetime.datetime.now()-datetime.timedelta(days=i)).date()))
		return dates

	if message.find("ДАТУ")>=0 or "НА" in words_message or "ЗА" in words_message:
		if message.find("ДАТУ")>=0:
			index_date=words_message.index("ДАТУ")+1
		else:
			if "НА" in words_message:
				index_date=words_message.index("НА")+1
			else:
				index_date=words_message.index("ЗА")+1	
		date=words_message[index_date]
		dates=date.split(".")
		dates.reverse()
		dates="-".join(dates)
		return [dates]


def get_curr_from_message(message):
	message=message.upper()
	currensies=[]

	for curr in all_currs:
		if message.find(curr)>=0:
			currensies.append(curr)
	return currensies


	"""
	if message.find("ДЛЯ")>=0:
					currs=message.split("ДЛЯ ")[1]
					currs=currs.split(",")
					currencys=[]
					for curr in currs:
						#удаляем пробельные символы в конце и начале строки
						currencys.append(curr.strip(" "))
						
					#удаляем многоточие или другие знаки перпинания с последней абрревиатуры
					# Состоит ли строка из букв		
					while not currencys[len(currencys)-1].isalpha():
						currencys[len(currencys)-1]=currencys[len(currencys)-1][:-1]
					return currencys
	"""


def get_country_from_message(message):
	message=message.upper()
	if message.find("BEL")>=0 or message.find(" BY ")>=0 or message.find("БЕЛ")>=0:
		return "BY"
	if message.find("UKR")>=0 or message.find("УКР")>=0:
		return "UKR"


def get_data_for_answer(message):
	message=message.upper()
	words_message=message.split(" ")	

	currencys=get_curr_from_message(message)
	if not currencys:
		print("Впишите интересющие вас валюты в конце запроса после слова ДЛЯ")
		return {"type": "error",
				"text": "Впишите интересующие вас валюты в конце запроса после слова ДЛЯ"}

	dates=get_dates_from_message(message)
	if not dates:
		result={"type":"error",
				"text":"не найдены даты "}
		return result

	country=get_country_from_message(message)
	if not country:
		return {"type":"error",
				"text":"\n Бот поддерживает страны только Беларусь и Украину. Укажите страну явно"}

	if message.find("ДИНАМИК")>=0 or message.find("ИЗМЕНЕНИ")>=0:
		return {"type":"dinamika",
				"text_model":"\nЗа последние дни динамика курса {} {} по отношению к  {} изменилась так:",
				"currencys":currencys,
				"dates": dates,
				"country": country}

	if message.find("СЕГОДНЯ")>=0 or message.find("СЕЙЧАС")>=0:
		return {"type":"rate_on_today",
				"text_model":"\nкурс {} {} на сегодня составляет: ",
				"currencys":currencys,
				"dates": dates,
				"country": country}			

	if message.find("ДАТУ")>=0 or "НА" in words_message or "ЗА" in words_message:
		return {"type":"rate_on_date",
				"text_model":"\nКурс {} на дату {} составляет ",
				"country": country,
				"currencys":currencys,
				"dates": dates}


def get_curr_scale(result, country):
	if country=="UKR":
		return 1
	if country=="BY":
		curr_scale=result["Cur_Scale"]
		return curr_scale


def get_local_curr(country):
	if country=="UKR":
		return "украинская гривна"
	if country=="BY":
		return "белорусский рубль"


def add_text(changes_rates, message):
	for date in changes_rates:
		delta=changes_rates[date]
		if delta >0:
			message+=f"\n{date}: +{delta}"
		else:
			message+=f"\n{date}: {delta}"
	return message


def get_rate(result, country):
	if country=="BY":
		return result["Cur_OfficialRate"]
	else: 
		return result[0]["rate"]


def format_date(date, country):
	if country=="BY":
		return date
	if country=="UKR":
		date="".join(date.split("-"))
		return date


def get_url_on_date(country, curr, date):
	date=format_date(date, country)
	if country=="BY":
		rb_currency_for_today_url= f"https://www.nbrb.by/api/exrates/rates/{curr}?parammode=2"
		result=do_get_request(rb_currency_for_today_url)
		if not result.get("type"):
			curr_id=result["Cur_ID"]
			url = f"https://www.nbrb.by/api/exrates/rates/{curr_id}?ondate={date}"
			return url
		else:
			return result
	if country=="UKR":
		url=f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode={curr}&date={date}&json"
		return url


def curr_data_on_date(country, curr, date):
	url=get_url_on_date(country, curr, date)
	if type(url)==dict:
		if  url["type"]=="error":
			return f"{url['text']}\nТакой валюты как {curr} не существует точно точно"

	result=do_get_request(url)

	if type(result)==dict and result.get("type"):
		if  result["type"]=="error":
			return f"{result['text']}\nТакой валюты как {curr} не существует. Вернул ошибку"

	if not result:
		print(f"Такой валюты как {curr} не существует. Нет результата")
		return f"\nТакой валюты как {curr} не существует"

	rate=get_rate(result, country)
	scale=get_curr_scale(result, country)
	return {"rate":rate,
			"scale":scale}


def get_rates_on_date(datas_for_answer):
	currencys=datas_for_answer["currencys"]
	text_model=datas_for_answer["text_model"]
	dates=datas_for_answer["dates"]
	country=datas_for_answer["country"]
	text_answer=""
	local_curr=get_local_curr(country)
	for date in dates:
		for curr in currencys:
			curr_data=curr_data_on_date(country, curr, date)
			if type(curr_data)==dict:
				rate=curr_data["rate"]
				scale=curr_data["scale"]
				text_answer+=text_model.format(curr, date)
				text_answer+=f"{rate} {local_curr} за {scale} {curr}"
			else:
				text_answer+=curr_data

	return text_answer


def get_changes_rates(datas_for_answer):
	currencys=datas_for_answer["currencys"]
	text_model=datas_for_answer["text_model"]
	text_answer=""
	dates=datas_for_answer["dates"]
	country=datas_for_answer["country"]
	local_curr=get_local_curr(country)
	text_delta=""
	
	for curr in currencys:
		scale=""
		rates=[]
		for date in dates:
			curr_data=curr_data_on_date(country, curr, date)
			if type(curr_data)==dict:
				scale=curr_data["scale"]
				rate=curr_data["rate"]
				rates.append(rate)
			else:
				text_answer+=curr_data
				break
		else:
			text_delta+=text_model.format(scale, curr, local_curr)
			changes_rates={}
			for i in range(0, len(dates)-1):
				changes_rates[dates[i]]=round(rates[i]-rates[i+1], 5)	
				#message=add_text(day, change_rate, message)
			text_delta=add_text(changes_rates, text_delta)
			text_answer=text_delta

	return text_answer


def get_rates_on_today(datas_for_answer):
	currencys=datas_for_answer["currencys"]
	text_model=datas_for_answer["text_model"]
	country=datas_for_answer["country"]
	text_answer=""
	dates=datas_for_answer["dates"]
	local_curr=get_local_curr(country)
	for date in dates:
		for curr in currencys:
			curr_data=curr_data_on_date(country, curr, date)
			if type(curr_data)==dict:
				rate=curr_data["rate"]
				scale=curr_data["scale"]
				text_answer+=text_model.format(scale, curr)
				text_answer+=f" {rate} {local_curr}"
			else:
				text_answer+=curr_data
	return text_answer


def handling_curr_request(user, message):
	name=user["name"]
	hello=f"Привет, {name}"

	datas=get_data_for_answer(message)
	if not datas:
		print("Для запроса не хватает данных")
		return f"Ваш запрос\n({message}\n не является запросом на валюту"

	type_request=datas["type"]
	

	if type_request=="dinamika":
		text_answer=get_changes_rates(datas)
		return hello+text_answer

	if type_request=="rate_on_today":
		text_answer=get_rates_on_today(datas)
		return hello+text_answer

	if type_request=="rate_on_date":
		text_answer=get_rates_on_date(datas)
		return hello+text_answer

	if type_request=="error":
		return datas["text"]