import os
import telebot
import sqlite3
from email_sender import send_email

BASE = 'server.db'
TOKEN = '1425387454:AAEEnZBldVp2Wj3aAKlLLHk2-R5kL5aymRo'

bot = telebot.TeleBot(TOKEN)
keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11')

@bot.message_handler(commands=['start'])
def start_message(message):
    try:
        con = sqlite3.connect(BASE)
        cur = con.cursor()
        cur.execute(f"""INSERT INTO events VALUES ({message.chat.id}, {0}, NULL,  '')""")
        con.commit()
        con.close()
        keyboard1 = telebot.types.ReplyKeyboardMarkup()
        keyboard1.row('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11')
        bot.send_message(message.chat.id, 'Привет, ты написал мне /start, \nВведи свой класс.', reply_markup=keyboard1)
    except:
        bot.send_message(message.chat.id, 'Ты уже писал /start. Просто введи свой класс', reply_markup=None)


@bot.message_handler(commands=['login'])
def start_message(message):
    if len(message.text.split(" ")) == 3:
        bot.send_message(message.chat.id, "Создана учётная запись, для начала работы дождитесь одобрения администратора"
                                          ". После одобрения записы вы будите уведомленны")
        con = sqlite3.connect(BASE)
        cur = con.cursor()
        print(f"""INSERT INTO logins(login, password) 
                            VALUES ('{message.text.split(" ")[1]}', '{message.text.split(" ")[2]}')""")
        cur.execute(f"""INSERT INTO logins(id, login, password) 
                            VALUES ({message.chat.id}, '{message.text.split(" ")[1]}', '{message.text.split(" ")[2]}')""")
        con.commit()
        con.close()
    else:
        bot.send_message(message.chat.id, "Ошибка синтаксиса. Проверьте что ввели логин и пароль через пробел и "
                                          "внутри логина и пароля нет пробелов")


@bot.message_handler(content_types=['text'])
def send_text(message):
    con = sqlite3.connect(BASE)
    cur = con.cursor()
    try:
        role = cur.execute(f"""SELECT role_ FROM logins WHERE id = {message.chat.id}""").fetchall()[0][0]
    except:
        bot.send_message(message.chat.id, "Зарегистрируйся командой /login (Login) (Password)")
        return None
    if role == "student":
        try:
            possition = cur.execute(f"""SELECT position_on FROM events WHERE id = {message.chat.id}""").fetchall()[0][0]
            if 2 > 1:
                if possition == 0:
                    arr_tests = os.listdir(path="tests")
                    class_ = message.text

                    arr_correct_tests = [i for i in arr_tests if i.split("_")[-1] == str(class_)]
                    if len(arr_correct_tests) > 0:
                        for i in range(len(arr_correct_tests)):
                            bot.send_message(message.chat.id, str(i + 1) + ") " + arr_correct_tests[i])
                        keyboard2 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
                        keyboard2.row(*arr_correct_tests)
                        bot.send_message(message.chat.id, 'Выбери тест', reply_markup=keyboard2)
                        cur.execute(f"""UPDATE events SET position_on = 1 WHERE id = {message.chat.id}""")
                    else:
                        bot.send_message(message.chat.id, 'Тестов нет. Отдохни', reply_markup=None)
                elif possition == 1:
                    cur.execute(f"""UPDATE events SET file = '{message.text}' WHERE id = {message.chat.id}""")
                    cur.execute(f"""UPDATE events SET position_on = 2 WHERE id = {message.chat.id}""")
                    bot.send_message(message.chat.id, 'Введите любую кнопку для подтвержения', reply_markup=None)
                else:
                    file = cur.execute(f"""SELECT file FROM events WHERE id = {message.chat.id}""").fetchall()[0][0]
                    ffile = open(f"tests\\{file}", mode="r", encoding="utf-8")
                    ffarr = ffile.readlines()[1::]
                    ffile.close()
                    if possition > 2:
                        ans = message.text
                        answ = cur.execute(f"""SELECT answ FROM events WHERE id = {message.chat.id}""").fetchall()[0][0]
                        answ += ffarr[possition - 3].strip("(").strip(")\n").split(",")[0] + "\t" + "Ответ Ученика:" \
                                + ans + "\t"\
                                + "Правильный ответ:" + ffarr[possition - 3].strip("(").strip(")\n").split(",")[1] + "\n"
                        cur.execute(f"""UPDATE events SET answ = '{answ}' WHERE id = {message.chat.id}""")
                    if possition - 2 < len(ffarr):
                        now = ffarr[possition - 2].strip("(").strip(")\n").split(",")
                        if now[2] != "__Entry__":
                            keyboard3 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
                            keyboard3.row(*now[2].split(":"))
                            bot.send_message(message.chat.id, now[0], reply_markup=keyboard3)
                        else:
                            bot.send_message(message.chat.id, now[0], reply_markup=None)
                        cur.execute(f"""UPDATE events SET position_on = position_on + 1 WHERE id = {message.chat.id}""")
                    else:
                        bot.send_message(message.chat.id, 'Тест окончен', reply_markup=None)
                        cur.execute(f"""UPDATE events SET position_on = 0 WHERE id = {message.chat.id}""")
                        answer = cur.execute(f"""SELECT answ FROM events WHERE id = {message.chat.id}""").fetchall()[0][0]
                        file = open(f"answers\\{message.from_user.first_name}_{message.from_user.last_name}_{file}",
                                    mode="w", encoding="utf-8")
                        print(answer)
                        file.write(answer)
                        file.close()
                        file = cur.execute(f"""SELECT file FROM events WHERE id = {message.chat.id}""").fetchall()[0][0]
                        fffile = open(f"tests\\{file}", mode="r", encoding="utf-8")
                        email = fffile.readlines()
                        fffile.close()
                        send_email(f"answers\\{message.from_user.first_name}_{message.from_user.last_name}_{file}", email[0])
                        cur.execute(f"""UPDATE events SET file = '', answ = '' WHERE id = {message.chat.id}""")
            else:
                bot.send_message(message.chat.id, 'Не понял', reply_markup=None)
                if possition == 0:
                    bot.send_message(message.chat.id, 'Введи свой класс', reply_markup=None)
                elif possition == 1:
                    for i in range(len(arr_correct_tests)):
                        bot.send_message(message.chat.id, str(i + 1) + ") " + arr_correct_tests[i])
                    keyboard2 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
                    keyboard2.row(*arr_correct_tests)
                    bot.send_message(message.chat.id, 'Выбери тест', reply_markup=keyboard2)
                if possition == 2:
                    bot.send_message(message.chat.id, 'Введите любую кнопку для подтвержения', reply_markup=None)
        except:
            bot.send_message(message.chat.id, 'Для начала работы введите /start', reply_markup=None)
    con.commit()
    con.close()



@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    print(message)

bot.polling()