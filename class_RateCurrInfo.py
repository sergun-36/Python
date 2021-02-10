import requests
import datetime
from all_currensies import all_currs



class RateCurrInfo():
	ok_codes=(200, 201, 202)
	url_rb_today="https://www.nbrb.by/api/exrates/rates/{curr}?parammode=2"
	url_rb_on_date="https://www.nbrb.by/api/exrates/rates/{curr_id}?ondate={date}"
	url_ukr="https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode={curr}&date={date}&json"

	def do_get_request(self, url):
		try:
			response=requests.get(url)
			if response.status_code in self.ok_codes:
				result=response.json()
				return result
			else:
				raise Exception(f"request failed. status {response.status_code}")
		except Exception as ex:
			print(f"Thix is exception {ex}")
			return 


	def get_dates_from_message(self, message):
		message=message.lower()
		words_message=message.split(" ")
		
		if message.find("сегодн")>=0 or message.find("сейчас")>=0:
			dates=str(datetime.date.today())
			return [dates]

		if message.find("динамик")>=0 or message.find("изменен")>=0:
			index_days_ago=words_message.index("за")+1
			days_ago=int(words_message[index_days_ago])
			dates=[]
			for i in range(0, days_ago+1):
				dates.append(str((datetime.datetime.now()-datetime.timedelta(days=i)).date()))
			return dates

		if message.find("дату")>=0 or "на" in words_message or "за" in words_message:
			if message.find("дату")>=0:
				index_date=words_message.index("дату")+1
			else:
				if "на" in words_message:
					index_date=words_message.index("на")+1
				else:
					index_date=words_message.index("за")+1	
			date=words_message[index_date]
			dates=date.split(".")
			dates.reverse()
			dates="-".join(dates)
			return [dates]


	def get_curr_from_message(self, message):
		message=message.upper()
		currensies=[]

		for curr in all_currs:
			if message.find(curr)>=0:
				currensies.append(curr)
		return currensies


	def get_country_from_message(self, message):
		message=message.upper()
		if message.find("BEL")>=0 or message.find(" BY ")>=0 or message.find("БЕЛ")>=0 or message.find(" РБ ")>=0:
			return "BY"
		if message.find("UKR")>=0 or message.find("УКР")>=0:
			return "UKR"


	def get_data_for_answer(self, message):
		message=message.upper()
		words_message=message.split(" ")	

		currencies=self.get_curr_from_message(message)
		if not currencies:
			#print("Впишите интересющие вас валюты в конце запроса после слова ДЛЯ")
			return {"type": "error",
					"text": "Введите в сообщении аббревиатуру валюты"}

		dates=self.get_dates_from_message(message)
		if not dates:
			result={"type":"error",
					"text":"не найдены даты "}
			return result

		country=self.get_country_from_message(message)
		if not country:
			return {"type":"error",
					"text":"\n Бот поддерживает страны только Беларусь и Украину. Укажите страну явно"}

		if message.find("ДИНАМИК")>=0 or message.find("ИЗМЕНЕНИ")>=0:
			return {"type":"dinamika",
					"text_model":"\nЗа последние дни динамика курса {} {} по отношению к  {} изменилась так:",
					"currencies":currencies,
					"dates": dates,
					"country": country}

		if message.find("СЕГОДНЯ")>=0 or message.find("СЕЙЧАС")>=0:
			return {"type":"rate_on_today",
					"text_model":"\nкурс {} {} на сегодня составляет: ",
					"currencies":currencies,
					"dates": dates,
					"country": country}			

		if message.find("ДАТУ")>=0 or "НА" in words_message or "ЗА" in words_message:
			return {"type":"rate_on_date",
					"text_model":"\nКурс {} на дату {} составляет ",
					"country": country,
					"currencies":currencies,
					"dates": dates}


	def get_curr_scale(self, result, country):
		if country=="UKR":
			return 1
		if country=="BY":
			curr_scale=result["Cur_Scale"]
			return curr_scale


	def get_local_curr(self, country):
		if country=="UKR":
			return "украинская гривна"
		if country=="BY":
			return "белорусский рубль"


	def add_text(self, changes_rates, message):
		for date in changes_rates:
			delta=changes_rates[date]
			if delta >0:
				message+=f"\n{date}: +{delta}"
			else:
				message+=f"\n{date}: {delta}"
		return message


	def get_rate(self, result, country):
		if country=="BY":
			return result["Cur_OfficialRate"]
		else: 
			return result[0]["rate"]


	def format_date(self, date, country):
		if country=="BY":
			return date
		if country=="UKR":
			date="".join(date.split("-"))
			return date


	def get_url_on_date(self, country, curr, date):
		date=self.format_date(date, country)
		if country=="BY":
			result=self.do_get_request(self.url_rb_today.format(curr=curr))
			if not result:
				return

			curr_id=result["Cur_ID"]

			url = self.url_rb_on_date.format(curr_id=curr_id, date=date)
			return url

		if country=="UKR":
			url=self.url_ukr.format(curr=curr, date=date)
			return url


	def curr_data_on_date(self, country, curr, date):
		url=self.get_url_on_date(country, curr, date)
		if not url:
			print("\nневерный URL")
			return "\nневерный URL"

		result=self.do_get_request(url)

		if not result:
			print(f"Такой валюты как {curr} не существует. Нет результата")
			return f"\nТакой валюты как {curr} не существует"

		rate=self.get_rate(result, country)
		scale=self.get_curr_scale(result, country)
		return {"rate":rate,
				"scale":scale}


	def get_rates_on_date(self, datas_for_answer):
		currencies=datas_for_answer["currencies"]
		text_model=datas_for_answer["text_model"]
		dates=datas_for_answer["dates"]
		country=datas_for_answer["country"]
		text_answer=""
		local_curr=self.get_local_curr(country)
		for date in dates:
			for curr in currencies:
				curr_data=self.curr_data_on_date(country, curr, date)
				if type(curr_data)==dict:
					rate=curr_data["rate"]
					scale=curr_data["scale"]
					text_answer+=text_model.format(curr, date)
					text_answer+=f"{rate} {local_curr} за {scale} {curr}"
				else:
					text_answer+=curr_data

		return text_answer


	def get_changes_rates(self, datas_for_answer):
		currencies=datas_for_answer["currencies"]
		text_model=datas_for_answer["text_model"]
		text_answer=""
		dates=datas_for_answer["dates"]
		country=datas_for_answer["country"]
		local_curr=self.get_local_curr(country)
		text_delta=""
		
		for curr in currencies:
			scale=""
			rates=[]
			for date in dates:
				curr_data=self.curr_data_on_date(country, curr, date)
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
					
				text_delta=self.add_text(changes_rates, text_delta)
				text_answer=text_delta

		return text_answer


	def get_rates_on_today(self, datas_for_answer):
		currencies=datas_for_answer["currencies"]
		text_model=datas_for_answer["text_model"]
		country=datas_for_answer["country"]
		text_answer=""
		dates=datas_for_answer["dates"]
		local_curr=self.get_local_curr(country)
		for date in dates:
			for curr in currencies:
				curr_data=self.curr_data_on_date(country, curr, date)
				if type(curr_data)==dict:
					rate=curr_data["rate"]
					scale=curr_data["scale"]
					text_answer+=text_model.format(scale, curr)
					text_answer+=f" {rate} {local_curr}"
				else:
					text_answer+=curr_data
		return text_answer


	def get_rate_info(self, user, message):
		hello=f"Привет, {user}"

		datas=self.get_data_for_answer(message)
		if not datas:
			print("Для запроса не хватает данных")
			return f"Ваш запрос\n({message}\n не является запросом на валюту"

		type_request=datas["type"]
		

		if type_request=="dinamika":
			text_answer=self.get_changes_rates(datas)
			return hello+text_answer

		if type_request=="rate_on_today":
			text_answer=self.get_rates_on_today(datas)
			return hello+text_answer

		if type_request=="rate_on_date":
			text_answer=self.get_rates_on_date(datas)
			return hello+text_answer

		if type_request=="error":
			return datas["text"]

"""
rate_info=RateCurrInfo()
message="курс UAH в Бел сегодня"
print(rate_info.get_rate_info("Sergey", message))
"""