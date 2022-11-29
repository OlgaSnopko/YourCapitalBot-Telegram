import telebot
from config import keys, TOKEN
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Приветствую Вас в Боте для расчета накоплений в другой валюте с помощью конвертера валют! Для начала работы введите команду в следующем формате (через пробел): \n- <Валюта сбережений>  \n- <Валюта, на которую Вы хотите обменять сбережения> \n- <Количество сбережений в валюте сбережений в формате целого положительного числа, либо дробного через точку> \n Перед использованием узнай доступные для расчета сбережений валюты: /values \n Нужна помощь: /help '

    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные для расчета сбережений валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text1 = 'Порядок работы с YourCapitalBot: \n 1)Прочитать условия использования Бота расчета накоплений; \n 2)Ознакомиться с вариантами ввода доступных валют; \n 3)Четко ввести три значения через пробел: валюта старых сбережений_валюта новых сбережений_количество старых сбережений числом; \n 4) Если не получилось, проверить еще раз вводимые данные и попробовать снова; \n Надеюсь, Вам понравится наш Бот!'
    bot.reply_to(message, text1)

@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Вы можете ввести только три параметра через пробел - валюта сбережений; валюта, на которую вы хотите обменять сбережения; количество сбережений в валюте сбережений. Попробуйте снова! ')

        base, quote, amount = values
        total_base = CryptoConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'На {amount} {base} ваших сбережений можно купить такое количество {quote}: {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)