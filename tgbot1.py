import logging
import settings
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

logging.basicConfig( format='%(asctime)s - %(levelname)s - %(message)s',
					level = logging.INFO,
					filename='bot.log'
					)
logger = logging.getLogger(__name__)

def start_bot(update:Updater, context: CallbackContext):
	print(update)
	first = """Добро пожаловать, {}
Чтобы узнать существующие команды напишите /help""".format(update.message.chat.first_name)
	update.message.reply_text(first)

def xcq(update:Updater, context:CallbackContext):
	print(update)
	xcq = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
	update.message.reply_text(xcq)

def alarm(context: CallbackContext):
	job = context.job
	context.bot.send_message(job.context, text='Время вышло!')


def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def set_timer(update: Update, context: CallbackContext):
	chat_id = update.message.chat_id
	try:
		# args[0] should contain the time for the timer in seconds
		due = int(context.args[0])
		if due < 0:
			update.message.reply_text('Назад в будущее! Жаль, но не получилось')
			return

		job_removed = remove_job_if_exists(str(chat_id), context)
		context.job_queue.run_once(alarm, due, context=chat_id, name=str(chat_id))

		text = 'Таймер установлен!'
		if job_removed:
			text += ' Старый таймер был удалён.'
		update.message.reply_text(text)

	except (IndexError, ValueError):
		update.message.reply_text('Используйте команду вот так: /set время в секундах')

def unset(update: Update, context: CallbackContext):
	chat_id = update.message.chat_id
	job_removed = remove_job_if_exists(str(chat_id), context)
	text = 'Таймер удалён!' if job_removed else 'У вас нет активных таймеров.'
	update.message.reply_text(text)

def helper(update:Updater, context:CallbackContext):
	print(update)
	third = """Появилась команда /set, чтобы поставить таймер
	А если будильник вам больше не нужен будильник, то напишите /unset"""
	update.message.reply_text(third)

def main():
	updtr = Updater(settings.TOKEN_TELEGRAM)

	updtr.dispatcher.add_handler(CommandHandler('start', start_bot))
	updtr.dispatcher.add_handler(CommandHandler('help', helper))
	updtr.dispatcher.add_handler(CommandHandler("set", set_timer))
	updtr.dispatcher.add_handler(CommandHandler("unset", unset))
	updtr.dispatcher.add_handler(CommandHandler("xcq", xcq))
	updtr.start_polling()
	updtr.idle()

if __name__ == "__main__":
	logging.info("Bot Started")
	main()
