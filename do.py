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

manager = digitalocean.Manager(token="")
d_token = ""

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    sleep(0.2)
    bot.sendMessage(chat_id=update.message.chat_id,text='''DigitalOcean is a simple and robust cloud computing platform, designed for developers. Use /help to get /help''')


def create(bot, update ):
    bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    sleep(0.2)
    bot.sendMessage(chat_id=update.message.chat_id, text='''Wait for a 1 minute while we create your droplet.''')
    create_instance()

def account(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    bot.sendMessage(chat_id=update.message.chat_id, text=get_account(manager))



def images(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    sleep(0.2)
    bot.sendMessage(chat_id=update.message.chat_id, text = show_images(manager))

def echo(bot, update):
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def help(bot, update):
	bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
	sleep(0.2)
	bot.sendMessage(chat_id=update.message.chat_id, text='''
Use one of the following commands
/create - to create an instance of digital ocean droplet.
/images - to get list of aviviable images.
/account - to get the current user account information.
/logs - to get the logs of the instance.
''')


def create_instance(d_name='Example', d_size='512mb', d_image='ubuntu-14-04-x64', d_region='nyc2', d_backups=True):
    droplet = digitalocean.Droplet(token=d_token,
                               name=d_name,
                               region=d_region, # New York 2
                               image=d_image, # Ubuntu 14.04 x64
                               size_slug=d_size,  # 512MB
                               backups=d_backups)
    droplet.create()
    
def  get_account(manager):
    email = manager.get_account()   
    email = "Your registerd account E-Mail:\n" + str(email)
    return email

def check_logs():
    pass    

def show_images(manager):
    images_str = ''
    counter = 0
    images = manager.get_all_images()
    for x in islice(images, 10):
        images_str += str(counter) +". " + str(x) + '\n'
        counter = counter + 1
    return images_str    

        

def main():
    print("Digital Ocean Bot running...")
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("create", create))
    dp.add_handler(CommandHandler("account", account))
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
