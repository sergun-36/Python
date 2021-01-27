from test_logic import testing
from bot_logic import run_bot
from data_test_bot import username

def start_test():
	interface=input("""\nВыберете пожалуйста интерфейс с помощью которого хотите пройти тест: 
		\na)telegram
		\nb)terminal\n\n""").lower()
	while not interface in ("a", "b"):
		interface=input("Введите пожалуйста латинскую букву 'a'  или 'b'\n\n")

	if interface=="a":
		print(f"отправьте боту {username} в telegram сообщение со словом 'тест' ")
		run_bot()
	else:
		testing("terminal")

start_test()
