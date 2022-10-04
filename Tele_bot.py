import telebot
import requests
from datetime import date
import gspread

photo_url = 'https://ru.wikipedia.org/wiki/Гигачад#/media/Файл:Гигачад.jpg'
bot = telebot.TeleBot('5739245273:AAEAOnt3RcetxhWpBwXUqG9GrxYQuSAXRpE')
googlesheet_id = '1QOLyt1025gAAd7ZFsqwH6_fH41VVprVag2AuHmtaBvk'
gc = gspread.service_account()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_photo(message.chat.id, photo=photo_url, caption='<b>Включен</b>', parse_mode='html')
    bot.reply_to(message,
                 "Привет, я буду вести расходы в гугл таблицы, введите данные таким образом [КАТЕГОРИЯ-ЦЕНА]:")


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    try:
        today = date.today().strftime("%d.%m.%Y")

        category, price = message.text.split("-", 1)
        text_message = f'На {today} в таблицу расходов добавлена запись: категория {category}, сумма {price}'
        bot.send_message(message.chat.id, text_message)

        sh = gc.open_by_key(googlesheet_id)
        sh.sheet1.append_row([today, category, price])
    except:
        bot.send_message(message.chat.id, 'Неправильный формат данных!')

    bot.send_message(message.chat.id, 'Введите данные о расходах через дефис в виде [КАТЕГОРИЯ-ЦЕНА]:')

bot.polling(none_stop=True)