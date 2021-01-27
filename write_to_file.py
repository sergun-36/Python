import requests


url="https://www.nbrb.by/api/exrates/currencies"
response=requests.get(url, verify=False)
response=response.json()


all_currensies="all_currs={\n"
for i in response:
	all_currensies+=f'		\"{i["Cur_Abbreviation"]}\":\"{i["Cur_Name"]}\",\n'

all_currensies+='}'

file=open("all_currensies.py", "w")
file.write(all_currensies)
file.close()