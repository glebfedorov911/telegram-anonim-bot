import telebot
from database import *
from random import randint
#yes i know a lot of problem with db, but it's first project, in future i repair it
token = 'token'

bot = telebot.TeleBot(token)

checker = False
select_id_who_get_message, select_id_who_send_message = 0, 0

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1, btn2 = telebot.types.KeyboardButton("Зарегистрироваться"), telebot.types.KeyboardButton("Поиск собеседника")
    btn3 = telebot.types.KeyboardButton('Перестать общаться')
    markup.add(btn1, btn2, btn3)

    bot.send_message(message.chat.id, 'Привет! Чтобы начать общение зарегистрируйся!', reply_markup = markup)

@bot.message_handler(content_types=['text', 'photo'])
def func(message):
    global checker, select_id_who_get_message, select_id_who_send_message

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1, btn2 = telebot.types.KeyboardButton("Зарегистрироваться"), telebot.types.KeyboardButton("Поиск собеседника")
    btn3 = telebot.types.KeyboardButton('Перестать общаться')
    markup.add(btn1, btn2, btn3)

    name = message.from_user.first_name
    user_id = message.from_user.id

    if message.text == 'Зарегистрироваться':
        select = f'''SELECT * FROM user_data WHERE id == {user_id}'''
        ins_new_user = f'''INSERT INTO user_data(id, username, id_user_who_get_message, find) VALUES 
                        ({user_id}, "{name}", 0, "False")'''

        if execute_read_query(connection, select) == []:
            execute_query(connection, ins_new_user)
            bot.send_message(user_id, 'Поздравляю! Вы успешно зарегистрировались!', reply_markup = markup)
        else:
            bot.send_message(user_id, 'Вы уже зарегистрирован!', reply_markup = markup)

    elif message.text == 'Поиск собеседника':
        checker = True
        select_tt = 0
        c = False

        replace_user_now = f'''REPLACE INTO user_data(id, username, id_user_who_get_message, find) VALUES
                                    ({user_id}, "{name}", 0, "True")'''

        execute_query(connection, replace_user_now)



        counter = 0

        while True:
            select_id_get = execute_read_query(connection,
                                               f'SELECT id FROM user_data WHERE find == "True" AND id != {user_id}')  # AND id != {user_id}
            if len(select_id_get) > 0:
                random = randint(0, len(select_id_get)-1)
                sp = execute_read_query(connection, '''SELECT id_user_who_get_message FROM user_data''')
                if select_id_get[random] not in sp:
                    select_id_who_get_message = select_id_get[random][0]
                    select_tt = select_id_get[random]
                else:
                    replace_user_now = f'''REPLACE INTO user_data(id, username, id_user_who_get_message, find) VALUES
                                                                            ({user_id}, "{name}", 0, "False")'''
                    execute_query(connection, replace_user_now)
                    bot.send_message(user_id, 'Ошибка! Чат не найден =(', reply_markup=markup)
                    break
                if select_id_get[random][0] != 0:
                    c = True
                    break
                else:
                    replace_user_now = f'''REPLACE INTO user_data(id, username, id_user_who_get_message, find) VALUES
                                                                            ({user_id}, "{name}", 0, "False")'''
                    execute_query(connection, replace_user_now)
                    bot.send_message(user_id, 'Ошибка! Чат не найден =(', reply_markup=markup)
                    break
            if counter == 200000:
                replace_user_now = f'''REPLACE INTO user_data(id, username, id_user_who_get_message, find) VALUES
                                                        ({user_id}, "{name}", 0, "False")'''
                execute_query(connection, replace_user_now)
                bot.send_message(user_id, 'Ошибка! Чат не найден =(', reply_markup = markup)
                break
            counter += 1

        s = execute_read_query(connection, '''SELECT id_user_who_get_message FROM user_data''')


        if (select_tt not in s) and c: #select_id_who_get_message != user_id and c and
            a = execute_read_query(connection, f'SELECT username FROM user_data WHERE id == {select_id_who_get_message}')
            replace_user_now = f'''REPLACE INTO user_data(id, username, id_user_who_get_message, find) VALUES
                                        ({user_id}, "{name}", {select_id_who_get_message}, "False"),
                                        ({select_id_who_get_message}, "{a[0][0]}",
                                        {user_id}, "False")'''
            execute_query(connection, replace_user_now)
            c = False
            s = execute_read_query(connection, f'''SELECT id_user_who_get_message FROM user_data WHERE username != "{name}"''')
            if select_tt in s:

                replace_user_now = f'''REPLACE INTO user_data(id, username, id_user_who_get_message, find) VALUES
                                                ({user_id}, "{name}", 0, "False")'''
                execute_query(connection, replace_user_now)
        else:
            replace_user_now = f'''REPLACE INTO user_data(id, username, id_user_who_get_message, find) VALUES
                                ({user_id}, "{name}", 0, "False")'''
            execute_query(connection, replace_user_now)

        s1 = f'''SELECT id_user_who_get_message FROM user_data WHERE id = {user_id}'''
        s2 = f'''SELECT id FROM user_data WHERE id = {execute_read_query(connection, s1)[0][0]}'''
        if execute_read_query(connection, s1) == execute_read_query(connection, s2) and execute_read_query(connection, s2)[0][0] != user_id:
            bot.send_message(user_id, 'Чат найден!')
        else:
            bot.send_message(user_id, 'Ошибка! Попробуйте снова')


    elif message.text == 'Перестать общаться':
        checker = False

        sel_sobes_id = f'''SELECT id_user_who_get_message FROM user_data WHERE id == {user_id}'''
        sobes_id = execute_read_query(connection, sel_sobes_id)

        sel_sobes_name = f'''SELECT username FROM user_data WHERE id == {sobes_id[0][0]}'''
        sobes_name = execute_read_query(connection, sel_sobes_name)

        replace_user_now = f'''REPLACE INTO user_data(id, username, id_user_who_get_message, find) VALUES
                                                ({user_id}, "{name}", 0, "False")'''

        replace_user_now_2 = f'''REPLACE INTO user_data(id, username, id_user_who_get_message, find) VALUES
                                                        ({sobes_id[0][0]}, "{sobes_name[0][0]}", 0, "False")'''

        execute_query(connection, replace_user_now)
        execute_query(connection, replace_user_now_2)

        select_id_who_get_message = 0

        bot.send_message(user_id, 'Чат завершен!')
        bot.send_message(sobes_id[0][0], 'Чат завершен!')



    elif checker:


        sel_id_sobes = F'''SELECT id FROM user_data WHERE id_user_who_get_message == {user_id}'''
        sel_id_sobes = execute_read_query(connection, sel_id_sobes)

        sel_id_sobes_from_me = f'''SELECT id_user_who_get_message FROM user_data WHERE id == {user_id}'''
        sel_id_sobes_from_me = execute_read_query(connection, sel_id_sobes_from_me)

        sel_id = F'''SELECT id_user_who_get_message FROM user_data WHERE id_user_who_get_message == {user_id}'''
        sel_id = execute_read_query(connection, sel_id)

        sel_id_from_me = f'''SELECT id FROM user_data WHERE id == {user_id}'''
        sel_id_from_me = execute_read_query(connection, sel_id_from_me)

        if sel_id[0][0] == sel_id_from_me[0][0] and sel_id_sobes[0][0] == sel_id_sobes_from_me[0][0]:
            sel = f'''SELECT id_user_who_get_message FROM user_data WHERE id == {user_id}'''

            bot.send_message(execute_read_query(connection, sel)[0][0], message.text, reply_markup = markup)


bot.infinity_polling()
