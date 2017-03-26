#!/usr/bin/env python
# -*- coding: utf-8 -*-


#Telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction
from time import sleep
from itertools import islice
import logging


#Digital Ocean
import digitalocean

manager = digitalocean.Manager(token="7630e27e3bec4147242f0707a86061e8e22e780cfd7ac69e5f1ec256e340fe90")


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    sleep(0.2)
    bot.sendMessage(chat_id=update.message.chat_id,text='''Hi! I am DigitalOcean bot. Use /help to get /help''')


def create(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    sleep(0.2)
    bot.sendMessage(chat_id=update.message.chat_id, text=''' ''')



def stats(bot, update):
    update.message.reply_text('Help!')

def images(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    sleep(0.2)
    bot.sendMessage(chat_id=update.message.chat_id, text = show_images(manager))

def echo(bot, update):
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def help(bot, update):
    update.message.reply_text("Stoics : List of commands\n 1. /create : Create a Digital Ocean droplet instance. \n 2. /stats : Check the stats of Your Droplet. ")


def create_instance(manager, name, size, stack, region):
    

    

def show_images(manager):
    images_str = ''
    counter = 0
    images = manager.get_all_images()
    for x in islice(images, 10):
        images_str += str(counter) +". " + str(x) + '\n'
        counter = counter + 1
    return images_str    

        

def main():
    print("Stoics Bot running...")
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("357335508:AAHGHM6jVx35nm92h4r0LTxoDaB1c8Q8KMM")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("stats", stats))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("images", images))
    dp.add_handler(CommandHandler("start", start))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()