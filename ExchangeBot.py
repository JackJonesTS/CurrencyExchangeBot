import telebot
from Config import keys, TOKEN
from Extensions import ConvertionException, CryptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    text = 'Hello! I will help you to convert currency.\n' \
           'To get started, enter the command in the following format:\n' \
           '<Source currency name> <What currency to transfer to> <Source currency amount>\n' \
           '/values - view the list of currencies available for conversion'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Available currencies for conversion'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Wrong number of parameters.')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'User error\n{e}')
    except Exception as e:
        bot.reply_to(message, f'failed to process command\n{e}')
    else:
        text = f'Price {amount} {quote} in {base} - {round(float(amount)*float(total_base), 2)}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)