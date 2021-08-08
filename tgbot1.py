import logging
import settings
from telegram.ext import Updater, CommandHandler, callbackcontext, MessageHandler, Filters

logging.basicConfig( format='%(asctime)s - %(levelname)s - %(message)s',
					level = logging.INFO,
					filename='bot.log'
					)

def start_bot(update: Updater, context: callbackcontext):
	print(update)
	mytext = """ Приветствую, {}
	Скоро меня обучат и я буду очень умным. Be patient with me""".format(update.message.chat.first_name)
	update.message.reply_text(mytext)

def chat(update: Updater, context: callbackcontext):
	answer = "Я не настолько умён, чтобы понимать тебя"

	update.message.reply_text(answer)

def main():
	updtr = Updater (settings.TOKEN_TELEGRAM)
	updtr.dispatcher.add_handler(CommandHandler("start", start_bot))
	updtr.dispatcher.add_handler(MessageHandler(Filters.text, chat))
	updtr.start_polling()
	updtr.idle
if __name__ == "__main__":
	logging.info("Bot Started")
	main()
