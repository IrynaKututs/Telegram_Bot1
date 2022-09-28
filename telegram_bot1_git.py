
import telebot
from telebot import types

token = 'ХХХХХХХХХ'
bot = telebot.TeleBot(token)

name = ''
surname = ''
tel = ''
book = ''


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Здравствуйте! Здесь можно оставить заявку на желаемую книгу. Чтобы зарегистрировать Ваши данные, введите имя.")
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши Привет.")

def get_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Укажите фамилию.')
    bot.register_next_step_handler(message, get_surname)

def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, "Укажите телефон в формате +375 (XX) XXX-XX-XX.")
    bot.register_next_step_handler(message, get_tel)

def get_tel(message):
    global tel
    tel = message.text
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Верно', callback_data='yes')
    key_no = types.InlineKeyboardButton(text='Не верно', callback_data='no')
    keyboard.add(key_yes,key_no)
    bot.send_message(message.from_user.id,
                     text = 'Вас зовут: ' + ' ' + name + ' ' + surname + '\nВаш телефон: ' + ' ' + tel + ' ' +'?',
                     reply_markup=keyboard)

def get_book(message):
    global book
    book = message.text
    f = open('1.txt', 'a')
    a = name + ' ' + surname + ' ' + tel + ' ' + book
    f.write(f'\n {a}')
    f.close()
    bot.send_message(message.from_user.id, 'Вы заказали книгу: ' + book +'\nС Вами свяжется наш менеджер.'+ '\nСпасибо за заказ!')


@bot.callback_query_handler(func=lambda call:True)
def callback_worker(call):
    if call.data == 'yes':
        bot.send_message(call.message.chat.id, "Укажите название и автора книги.")
        bot.register_next_step_handler(call.message, get_book)
    elif call.data == 'no':
        bot.send_message(call.message.chat.id, 'Пройдите регистрацию повторно. Укажите Ваше имя.')
        bot.register_next_step_handler(call.message, get_name)

bot.polling(none_stop=True)