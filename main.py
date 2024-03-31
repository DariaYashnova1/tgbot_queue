import numpy as np
import telebot
from telebot import types
import sqlite3
import random

bot = telebot.TeleBot('6867504274:AAHsAkTM1dxz0W1WIvfL9F8yKaLEkfd_rSg')
conn = sqlite3.connect('database6.db', check_same_thread=False)
cursor = conn.cursor()
queue_map_bd = {}
queue_map_tg = {}
queue_map_mic = {}
sorted = [0,0,0]
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY,
#         first_name TEXT,
#         last_name TEXT
#     )
# ''')
# conn.commit()
#
# groupmates = [
#     (1,'арсений', 'богдан'),
# (2,'владислав', 'гаар'),
# (3,'дмитрий', 'губковский'),
# (4,'игорь', 'гладков'),
# (5,'георгий', 'золоев'),
# (6,'полина', 'луговенко'),
# (7,'мартин', 'михалец'),
# (8,'винь', 'нго данг конг'),
# (9,'юлия', 'плужникова'),
# (10,'никита', 'ромашко'),
# (11,'полина', 'рябова'),
# (12,'айзек', 'салимли'),
# (13,'всеволод', 'санько'),
# (14,'кирилл', 'смирнов'),
# (15,'артем', 'тищенко'),
# (16,'алексей', 'шихалев'),
# (17,'ксения', 'шклярова'),
# (18,'дарья', 'яшнова'),
#
#  (20,'игорь', 'астафьев'),
# (21,'елизавета', 'богданова'),
# (22,'роман', 'геллер'),
# (23,'петр', 'григорьев'),
# (24,'максим', 'емешкин'),
# (25,'яна', 'зелякова'),
# (26,'павел', 'лобанов'),
# (27,'анастасия', 'ложкина'),
# (28,'мануэль', 'лухуку'),
# (29,'кирилл', 'табунов'),
# (30,'вадим', 'тугай'),
# (31,'карим', 'фаррахов'),
# (32,'кирилл', 'фролов'),
# (33,'кирилл', 'смирнов'),
# (34,'максим', 'черепнов'),
# (35,'софья', 'чурова'),
# (36,'дмитрий', 'якунин'),
# (19,'khidir', 'karawita')
#
# ]
#
# cursor.executemany('INSERT INTO users VALUES (?,?,?)', groupmates)


# Сохраняем изменения
conn.commit()
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for row in rows:
    print(row)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    Q_tg = types.KeyboardButton('Очередь на Теорию графов')
    Q_bd = types.KeyboardButton('Очередь на Базы данных')
    Q_mic = types.KeyboardButton('Очередь на Микроконтроллеры')
    R_tg = types.KeyboardButton('Сдать отчет по теории графов')
    R_mic = types.KeyboardButton('Сдать отчет по Микроконтроллерам')
    tab_1 = types.KeyboardButton('Посмотреть ведомости группы №1')
    tab_2 = types.KeyboardButton('Посмотреть ведомости группы №2')

    markup.add(Q_tg, Q_bd, Q_mic, R_tg, R_mic, tab_1, tab_2)

    bot.send_message(message.from_user.id, 'Выбери опцию', reply_markup=markup)

    bot.register_next_step_handler(message, get_opt)


def get_opt(message):
    global opt
    opt = message.text
    global bool_bd
    global bool_tg
    global bool_mc
    if (opt == 'Очередь на Теорию графов'):
        bot.send_message(message.from_user.id, "Напиши имя")

        bool_tg = True
        bool_bd = False
        bool_mc = False
        bot.register_next_step_handler(message, get_name)
    elif (opt == 'Очередь на Базы данных'):
        bot.send_message(message.from_user.id, "Напиши имя")

        bool_bd = True
        bool_tg = False
        bool_mc = False
        bot.register_next_step_handler(message, get_name)
    elif (opt == 'Очередь на Микроконтроллеры'):
        bot.send_message(message.from_user.id, "Напиши имя")

        bool_mc = True
        bool_bd = False
        bool_tg = False
        bot.register_next_step_handler(message, get_name)
    # elif (opt == 'Сдать отчет по теории графов'):
    # elif (opt == 'Сдать отчет по Микроконтроллерам'):
    # elif (opt == 'Посмотреть ведомости группы №1'):
    # elif (opt == 'Посмотреть ведомости группы №2'):


@bot.message_handler(commands=['sort'])
def sort(message):
    bot.send_message(message.from_user.id, "Напиши имя")
    bot.register_next_step_handler(message, get_name_a, 0)


@bot.message_handler(commands=['clear'])
def clear_q(message):
    bot.send_message(message.from_user.id, "Напиши имя")
    bot.register_next_step_handler(message, get_name_a, 1)


@bot.message_handler(commands=['printq'])
def printq(message):
    st_tg = ''
    st_bd = ''
    st_mic = ''
    if sorted[0]==1:
        for i in queue_map_tg.items():
            st_tg += str(i[0]) + '  ' + str(i[1]) + '\n'
        bot.send_message(message.from_user.id, 'Очередь на теорию графов \n' + st_tg)

    if sorted[1]==1:
        for i in queue_map_bd.items():
            st_bd += str(i[0]) + '  ' + str(i[1]) + '\n'
        bot.send_message(message.from_user.id, 'Очередь на базы данных \n' + st_bd)

    if sorted[2]==1:
        for i in queue_map_mic.items():
            st_mic += str(i[0]) + '  ' + str(i[1]) + '\n'
        bot.send_message(message.from_user.id, 'Очередь на микроконтроллеры \n' + st_mic)


@bot.message_handler(content_types=['text'])
def get_name(message):  # получаем фамилию
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?')
    bot.register_next_step_handler(message, get_surname)


def get_name_a(message, b):  # получаем фамилию
    global name_a
    name_a = message.text
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?')
    bot.register_next_step_handler(message, get_surname_a, b)


def get_surname(message):
    global surname
    surname = message.text

    markup = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('1')
    itembtn2 = types.KeyboardButton('2')
    itembtn3 = types.KeyboardButton('3')
    itembtn4 = types.KeyboardButton('4')
    itembtn5 = types.KeyboardButton('5')
    itembtn6 = types.KeyboardButton('6')
    itembtn7 = types.KeyboardButton('7')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7)

    bot.send_message(message.from_user.id, 'Напиши номер лабораторной', reply_markup=markup)

    bot.register_next_step_handler(message, get_num)


def get_surname_a(message, b):
    global surname_a
    surname_a = message.text
    bot.send_message(message.from_user.id, 'Вы админ?')
    bot.register_next_step_handler(message, check_adm, b)



def get_num(message):
    global age
    age = message.text

    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Да')
    itembtn2 = types.KeyboardButton('Нет')
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.from_user.id,
                     'Ты хочешь сдать ' + str(age) + ' лабораторную, тебя зовут ' + name + ' ' + surname + '?',
                     reply_markup=markup)
    bot.register_next_step_handler(message, handle_message)

def check_adm(message, b):
    global pwd
    pwd = message.text
    if pwd == '1827tT' and name_a == 'khidir' and surname_a == 'karawita':
        markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        itembtn1 = types.KeyboardButton('Дискретная математика')
        itembtn2 = types.KeyboardButton('Микроконтроллеры')
        itembtn3 = types.KeyboardButton('Базы данных')

        markup.add(itembtn1, itembtn2, itembtn3)
        bot.send_message(message.from_user.id, 'Выбери предмет', reply_markup=markup)
        if(b==0):
            bot.register_next_step_handler(message, take_object)
        else:
            bot.register_next_step_handler(message, take_object_rm)
            print(b)



    else:
        bot.send_message(message.from_user.id, 'ban')

def take_object_rm(message):
    obj = message.text
    if (obj == 'Дискретная математика'):
        queue_map_tg.clear()
        sorted[0] = 0
    elif (obj == 'Микроконтроллеры'):
        queue_map_mic.clear()
        sorted[2] = 0
    else:
        queue_map_bd.clear()
        sorted[1] = 0
    bot.send_message(message.from_user.id, 'Удаление успешно')

def take_object(message):
    obj=message.text
    if (obj == 'Дискретная математика'):
        sorted[0] = 1
        for i in range(10):
            if i in queue_map_tg.keys():
                my_list = list(queue_map_tg[i])
                random.shuffle(my_list)
                for j in my_list:
                    print(j)
    elif (obj == 'Микроконтроллеры'):
        sorted[2] = 1
        for i in range(10):
            if i in queue_map_mic.keys():
                my_list = list(queue_map_mic[i])
                random.shuffle(my_list)
                for j in my_list:
                    print(j)
    elif(obj == 'Базы данных'):
        sorted[1] = 1
        for i in range(10):
            if i in queue_map_bd.keys():
                my_list = list(queue_map_bd[i])
                random.shuffle(my_list)
                for j in my_list:
                    print(j)

    bot.send_message(message.from_user.id, 'Сортировка успешна')


def handle_message(message):
    markup = types.ReplyKeyboardRemove()
    first_name = name.lower()
    last_name = surname.lower()

    cursor.execute('SELECT * FROM users WHERE first_name=? AND last_name=?', (first_name, last_name))
    user = cursor.fetchone()
    print(first_name, last_name)
    if message.text == 'Да' and user:
        if (bool_tg):
            if age in queue_map_tg.keys():
                queue_map_tg[age].add(last_name + ' ' + first_name)
            else:
                queue_map_tg[age] = {last_name + ' ' + first_name}
            bot.send_message(message.chat.id, "Вы в очереди, ожидайте распределение", reply_markup=markup)

            print(queue_map_tg)

            return
        elif bool_bd:
            if age in queue_map_bd.keys():
                queue_map_bd[age].add(last_name + ' ' + first_name)
            else:
                queue_map_bd[age] = {last_name + ' ' + first_name}
            bot.send_message(message.chat.id, "Вы в очереди, ожидайте распределение", reply_markup=markup)

            print(queue_map_bd)
        elif bool_mc:
            if age in queue_map_mic.keys():
                queue_map_mic[age].add(last_name + ' ' + first_name)
            else:
                queue_map_mic[age] = {last_name + ' ' + first_name}
            bot.send_message(message.chat.id, "Вы в очереди, ожидайте распределение", reply_markup=markup)

            print(queue_map_mic)

    elif user:
        bot.send_message(message.chat.id, "Подайте заявку снова или не подавайте, если передумали", reply_markup=markup)
        bot.register_next_step_handler(message, start)
        return
    else:
        bot.send_message(message.chat.id, "Вас нет в списках :(( или ввод некорректен", reply_markup=markup)
        bot.register_next_step_handler(message, start)
        return


bot.polling()
