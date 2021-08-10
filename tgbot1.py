import logging
import settings
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

logging.basicConfig( format='%(asctime)s - %(levelname)s - %(message)s',
					level = logging.INFO,
					filename='bot.log'
					)

def start_bot(update:Updater, context: CallbackContext):
	print(update)
	first = """Добро пожаловать, {}
Узнать существующие команды напишите /help""".format(update.message.chat.first_name)
	update.message.reply_text(first)

def chat(update:Updater, context:CallbackContext):
	print(update)
	second = "Думаю лучше всего написать /help"
	update.message.reply_text(second)

def helper(update:Updater, context:CallbackContext):
	print(update)
	third = """В данный момент есть 2 команды /help и /start
В будущем должны появиться ещё несколько"""
	update.message.reply_text(third)
	
def main():
	updtr = Updater(settings.TOKEN_TELEGRAM)

	updtr.dispatcher.add_handler(CommandHandler('start', start_bot))
	updtr.dispatcher.add_handler(CommandHandler('help', helper))	
	updtr.dispatcher.add_handler(MessageHandler(Filters.text, chat))
	

	updtr.start_polling()
	updtr.idle()

if __name__ == "__main__":
	logging.info("Bot Started")
	main()
