basics_easy=[{"question":"\nВыберите верное написание для обозначения значения НИЧЕГО:",
			"answers":{ "a":"None",
						"b":"Null",
						"c":"none",
						"d":"nothing"},
			"correct_answer":"a"},

			{"question":"\nPython это компилируемый язык или интерпретируемый:",
			"answers":{ "a":"Компилируемый",
						"b":"Интерпретируемый",
						"c":"Ни один из вариантов неверен",
						"d":"Нивелируемый"},
			"correct_answer":"b"},

			{"question":"\nЧто выведет код: print('2'+'2')",
			"answers":{ "a":"\'4\'",
						"b":4,
						"c":"вызовет Exception",
						"d":"\'22\'"},
			"correct_answer":"d"}
			]

basics_medium=[{"question":"\nМожно ли в Python  трансформировать значения одного типа в другой?",
				"answers":{	"a":"Можно, с некоторыми логическими ограничениями. Например, число может стать строкой, но None не станет списком",
							"b":"Можно без всяких лимитов - хоть строку превратить в целое число",
							"c":"Нет, трансформация типа невозможна",
							"d":"В Python  нет различных типов данных"},
				"correct_answer":"a"},

				{"question":"""\nЧто выведет следующий код:
for i in (0, 1, 2, 3):
	print(i)
	if i>=2:
		break""",
				"answers":{	"a":"в столбик: 0, 1",
							"b":"ничегоб скрипт отработает без вывода в командную строку",
							"c":"в столбик: 0, 1, 2, 3",
							"d":"в столбик: 0, 1, 2"},
				"correct_answer":"d"}
				]

basics_hard=[{"question":"\nВыберите, что из этого является неизменяемой структурой:",
				"answers":{	"a":"frozenset({“Some value”, None, 26})",
							"b":"{“Some value”, None, 26}",
							"c":"[“Some value”, None, 26]",
							"d":"{“Some value”: None, “size”: 26}"},
				"correct_answer":"a"},

			{"question":"\nВыберите, какой из вариантов содержит только неизменяемый структуры:",
			"answers":{	"a":"int, str, float, None, frozenset, tuple",
						"b":"int, str, float, None, frozenset, dict",
						"c":"dict, list, tuple, int",
						"d":"set, str, tuple, int"},
			"correct_answer":"a"},

			{"question":"\nГде допущена ошибка?",
			"answers":{	"a":"list(1,3,5,None, 'Egor')",
						"b":"frozenset({'name': 'My name', 'age': 45})",
						"c":"frozenset({'My name', 'age', 45})",
						"d":"8,15,6,23,42"},
			"correct_answer":"b"},

			{"question":"""\nЧто будет выведено в командной строке в результате выполнения кода:
b=5
a=(1, b, 4)
b=6
print(a)""",
			"answers":{	"a":"(1, b, 4)",
						"b":"(1, 6, 4)",
						"c":"Exception(т к tuple - неизменяемая структура)",
						"d":"(1, 5, 4)"},
			"correct_answer":"d"}
			]

func_easy=[{"question":"\nКлючевое слово при объявлении функции:",
			"answers":{	"a":"func",
						"b":"function",
						"c":"def",
						"d":"Нет никакого ключевого слова"},
			"correct_answer":"c"},

			{"question":"\nОбязательно ли ключевое слово return при объявлении функции?",
			"answers":{	"a":"Да",
						"b":"Нет",
						"c":"Зависит от условий - иногда да, иногда нет",
						"d":"Если функция утрируемая, то да, в остальных случаях - нет",
						"e":"Только для интеграциональных функций"},
			"correct_answer":"b"},

			{"question":"\nЧто возвращает функция, если не указано ключевое слово return?",
			"answers":{	"a":"Null",
						"b":"result",
						"c":"False",
						"d":"None",
						"e":"undefined"},
			"correct_answer":"d"}
			]

func_medium=[{"question":"""\nЧто мы получим в результате выполнения данного кода?
def somefunc():
    return True

if somefunc():
    print('Hello')
else:
    print('Bye!')""",

			"answers":{	"a":"Напечатается 'Bye!'",
						"b":"Получим исключение AssertError",
						"c":"Ничего",
						"d":"Напечататься 'Hello!'"},
			"correct_answer":"d"}
			]

func_hard=[{"question":"""\nКакой результат мы получим, исполнив код ниже?
def myfunc(i):
    return 10

i=42
n=myfunc()
print(n)""",

			"answers":{	"a":"Напечатается 42",
						"b":"Напечатается 10",
						"c":"Будет Exception",
						"d":"None"},
			"correct_answer":"c"}
			]

api_easy=[{"question":"\nТакое понятие как API:",
			"answers":{	"a":"Относиться только к работе с интернетом",
						"b":"Относиться только к работе с железом напрямую",
						"c":"Ни один из вариантов не верен",
						"d":"Это из области разработки видеоигр"},
			"correct_answer":"c"},

			{"question":"\nМожет ли быть API у операционной системы?",
			"answers":{	"a":"Да",
						"b":"Нет",
						"c":"Пойдем взорвем башню 'Арасаки', или хотя бы фургон поломаем!"},
			"correct_answer":"a"},
		]

exception_easy=[{"question":"""\nЗапустив данный код:
try:
    int("Hello")
except Exception:
    print("Hello!")

Мы получим:""",
				"answers":{	"a":"В командной строке выведется 'Hello'",
							"b":"Ничего",
							"c":"Exception: Hello",
							"d":"Довольно устрашающее сообщение о том, что жизнь кортка и полна страданий"},
				"correct_answer":"a"},
				]

exception_medium=[{"question":"\nЧто произойдет если вызывать код: raise Exception('Some exception')",
					"answers":{	"a":"Интерпретатор вызовет исключение и получим в консоли Exception: Some exception",
								"b":"Мы получм сообщение о том, что код написан неверно",
								"c":"Ничего",
								"d":"Получим сценарий комедийного хоррора про маньяка с Винсом Воном"},
					"correct_answer":"a"}
				]

protocol_easy=[{"question":"\nКакой из вариантов содержит исключительно упоминания протоколов?",
				"answers":{	"a":"Python, HTTPS, TCP/IP, MMS",
							"b":"BitTorrent, HTTP, HTTPS, протокол медицинского осмотра",
							"c":"TCP/IP, Megadeth, JavaScript, SMS"},
				"correct_answer":"b"}
				]

protocol_hard=[{"question":"\nЕсли мы по протоколу HTTP посылаем на сервер запрос, что мы получим:",
				"answers":{	"a":"В любом случае получим  response",
							"b":"В зависимости от настроек - можем получить строку, джсон или еще что-то",
							"c":"Либо response либо None"},
				"correct_answer":"a"}
				]

import_easy=[{"question":"""\nУ нас есть папка folder с двумя файлами  file_one.py  и file_two.py
folder\\
    file_one.py  
    file_two.py
Если я хочу подключить из file_one.py в file_two.py все его содержимое, какой код мне использовать:""",

				"answers":{	"a":"from file_one import *",
							"b":"import all from  file_one",
							"c":"from file_one.py import *",
							"d":"import * from  file_one"},
				"correct_answer":"a"}
				]

import_medium=[{"question":"""\nУ нас есть папка со структурой:
folder\\
    main.py
    subfolder\\
        some_file.py
        sub_file.py
Если я хочу подключить файл sub_file.py в main.py, что именно мне следует прописать в файле main.py""",
				
				"answers":{	"a":"connect subfile.py to main.py",
							"b":"import subfolder.sub_file",
							"c":"import sub_file from subfolder",
							"d":"import sub_file.py from subfolder"},
				"correct_answer":"b"},

				{"question":"""\nfile_1.py и file_2.py находяться в одной папке.как следует
вызвать функцию some_func из file_1.py импортированную в file_2.py следующим образом:
import file_1 as sun""",
				
				"answers":{	"a":"some_func()",
							"b":"sun.some_func()",
							"c":"file_1.some_func",
							"d":"Выведет ошибку импорта",
							"e":"file_1.sun.some_func()"},
				"correct_answer":"b"}
				]

other_easy=[{"question":"\nКак звали прибожека в английской локализации Witcher 3 :",
				"answers":{	"a":"Так же как и в русской - Ивасик",
							"b":"Так же как и в польской - Янек",
							"c":"Джонни",
							"d":"Агент Смит"},
				"correct_answer":"c"}
			]

other_medium=[{"question":"""\nСцена, где устрашающий тайский боксер обмакивал забинтованные 
руки в клей и битое стекло из:""",
				"answers":{	"a":"Кикбоксер 2",
							"b":"Кикбоксер 1",
							"c":"Римейк Кикбоксера от 2015 года",
							"e":"Лучшие из лучших"},
				"correct_answer":"b"}
				]

other_hard=[{"question":"""\nПисатель Питер Уотс, канадец, должен был писать сценарий
к видеоигре Crysis 2, и ехал, для этого, из Канады в Штаты. Однако, на границе, 
по пьяни подрался с пограничником, после чего, соответственно, был завернут обратно.
Питер Уотс после этого:""",

				"answers":{	"a":"Поехавший алкаш",
							"b":"Кикбоксер",
							"c":"Все правильной сделал, борец с системой",
							"e":"Не было такого"},
				"correct_answer":"a"}
			]

questions={"function":{"easy":func_easy,
						"medium":func_medium,
						"hard":func_hard},
			"basics":{ "easy":basics_easy,
						"medium": basics_medium,
						"hard": basics_hard},
			"api":{"easy":api_easy},
			"protocol":{"easy":protocol_easy,
						"hard":protocol_hard},
			"other":{"easy":other_easy,
					"medium":other_medium,
					"hard":other_hard},
			"import":{"easy":import_easy,
					"medium":import_medium},
			"exception":{"easy":exception_easy,
						"medium":exception_medium},
			"all":{}
			}

