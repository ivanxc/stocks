import telebot
import sys
import getHistory
import machinelearning
sys.path.append('C:/Users/Иван/PycharmProjects/pythonProject')

bot = telebot.TeleBot('1835056120:AAF-hyyEFichtUQeai371dRw3V1f2aQWB1U')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/help":
        bot.send_message(message.from_user.id, "Отправь мне имя тикера")
    else:
        if getHistory.getHistory(message.text, 60) != None:
            isRised = machinelearning.getPrediction(message.text)
            if isRised == '0':
                bot.send_message(message.from_user.id, "📉 В следующий торговый день ожидается падение цены тикера ")
            else:
                bot.send_message(message.from_user.id, "📈 В следующий торговый день ожидается рост цены тикера ")
        else:
            bot.send_message(message.from_user.id, "Невозможно предсказать поведение данного тикера или введено некорректное название")

bot.polling(none_stop=True, interval=0)