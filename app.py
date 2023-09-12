import telebot
import requests
import json
from config import keys, TOKEN
from exceptions import APIException, CryptoConverter
bot=telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help (message: telebot.types.Message):
    text= 'Привет! Я создан для того, чтобы быстро конвертировать одну валюту в другую. Перед началом работы ознакомься с порядком ввода параметров и введи их через пробел:'\
    ' \n- <Название валюты, которую нужно конвертировать> \n- <Название валюты, в которую нужно конвертировать>) \n- <Количество конвертируемой валюты в цифрах>\n \
    Список валют доступных для конвертации доступен по ссылке: /values'
    bot.reply_to(message, text)

@bot.message_handler (commands=['values'])
def values (message: telebot.types.Message):
    text = 'Валюты доступные для конвертации:'
    for key in keys.keys():
        text = '\n'.join ((text, key,))
    bot.reply_to (message, text)

@bot.message_handler(content_types=['text', ])
def get_price (message: telebot.types.Message):
    try:
        values = message.text.split (' ')
        if len (values) !=3:
            raise APIException ('Неверно введены параметры')
        base, quote, amount = values
        base=base.lower()
        quote=quote.lower()
        total_base = CryptoConverter.get_price(base, quote, amount)
    except Exception as e:
        bot.reply_to (message, f'Неудалось обработать команду\n {e}')
    else:
        text = f'Цена {amount} {base} в {quote}:{total_base}'
        bot.send_message (message.chat.id, text)

bot.polling (none_stop=True)