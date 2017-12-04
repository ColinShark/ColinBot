#!/usr/bin/env python3.6
# -*- coding: UTF-8 -*-
# -------------------------------------------------------------------------------
# Name:        ColinBot.py
# Purpose:     Doing Stuff for me wtf
#
# Author:      ColinShark
# Credits:     Parts of this are examples of "python-telegram-bot" on github
#
# Created:     25.11.2017
# Copyright:   (c) ColinShark 2017
# Licence:     none
# File Format: UTF-8
# -------------------------------------------------------------------------------


"""
This Bot is for personal use. I will try to learn from it and I am using code
snippets from the github repository "python-telegram-bot"
"""

from uuid import uuid4
from telegram.utils.helpers import escape_markdown
from telegram.ext import Updater, \
                         CommandHandler, \
                         MessageHandler, \
                         Filters, \
                         CallbackQueryHandler, \
                         InlineQueryHandler, \
                         RegexHandler, \
                         ConversationHandler
from telegram import InlineKeyboardButton, \
                     InlineKeyboardMarkup, \
                     InlineQueryResultArticle, \
                     ParseMode, \
                     InputTextMessageContent, \
                     ReplyKeyboardMarkup
import logging
import re

# ##############################################################################

API_TOKEN = "TOKEN"

UserID_Colin = "289579584"
UserID_Rotfell = "198748192"
UserID_KIBA = "139450056"

# ##############################################################################

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# ##############################################################################

# Beim Start des Bots oder /start
def start(bot, update):
    """Send a message when the command /start is issued."""
    #    bot.sendMessage(update.message.chat_id, text="Hallo {}".format(update.message.from_user.first_name))
    update.message.reply_text("***Dieser Bot ist aktuell noch im Aufbau.***")
    update.message.reply_text("Die verfügbaren Befehle sind aktuell noch nicht gelistet, wie man es sonst gewohnt ist. Für eine Auflistung der verfügbaren Befehle schreib /help.")
    update.message.reply_text("Bei Problemen melde dich bitte bei @ColinShark.\nViel Vergnügen mit dem Bot :3")
    bot.send_message(text='{} (@{}) hat den Bot gestartet.\n(oder nur /start benutzt ._.)'.format(
        update.effective_user.first_name,
        update.effective_user.username),
        chat_id=UserID_Colin
    )


# Bei /help
def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        'Dies ist eine Übersicht über die aktuell verfügbaren Befehle. Ich versuche diese Liste auch aktuell zu halten :D')
    update.message.reply_text(
        '/start - Die Nachricht, die du oben schon lesen konntest.'
        '/test - Ist nur ein Test zum testen von Befehlen.'
        '/keyboard - Zeigt ein Inline-Keyboard an.'
        '/set n - Stellt einen Timer mit n Sekunden.'
        '/unset n - Entfernt den mit n Sekunden gestellten Timer.'
        'Zusätzlich zu diesen Befehlen kannst du den Bot noch per Inline-Query verwenden. Schreibe in einem Chat @ColinSharkBot und etwas, dass du in Caps, Bold oder Italic haben möchtest. Der Bot übernimmt den Rest.'
    )


# def echo(bot, update):
#   Alles, was kein Befehl ist, wird Retoure geschickt
#    update.message.reply_text(update.message.text)


def test(bot, update):
    #   Einfach zum testen
    update.message.reply_text("Ein Test-Command!")
    bot.send_message(
        chat_id=UserID_Colin,
        text="{} hat /test genutzt!".format(update.effective_user.first_name),
    )


#    bot.send_message(text='{} hat /test genutzt!'.format(
#        update.effective_user.first_name), chat_id=UserID_KIBA)
#    bot.send_message(text='{} hat /test genutzt!'.format(
#        update.effective_user.first_name), chat_id=UserID_Rotfell)


def keyboard(bot, update):
    #   Gibt eine Inline-Tastatur mit Zahlen 1 bis 9 aus
    keyboard = [[InlineKeyboardButton("1", callback_data="1"),
                 InlineKeyboardButton("2", callback_data="2"),
                 InlineKeyboardButton("3", callback_data="3")],

                [InlineKeyboardButton("4", callback_data="4"),
                 InlineKeyboardButton("5", callback_data="5"),
                 InlineKeyboardButton("6", callback_data="6")],

                [InlineKeyboardButton("7", callback_data="7"),
                 InlineKeyboardButton("8", callback_data="8"),
                 InlineKeyboardButton("9", callback_data="9")]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Bitte eine Option aussuchen:", reply_markup=reply_markup)


def button(bot, update):
    query = update.callback_query

    bot.edit_message_text(text="Deine Auswahl: {}".format(query.data),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)


#   Die Inline-Anfrage in anderen Chats
#   Formattiert in CAPS, Fett und Kursiv
def inlinequery(bot, update):
    """Inline-Query wird hiermit bearbeitet"""
    query = update.inline_query.query
    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title="Caps",
            input_message_content=InputTextMessageContent(
                query.upper())),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Bold",
            input_message_content=InputTextMessageContent(
                "*{}*".format(escape_markdown(query)),
                parse_mode=ParseMode.MARKDOWN)),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Italic",
            input_message_content=InputTextMessageContent(
                "_{}_".format(escape_markdown(query)),
                parse_mode=ParseMode.MARKDOWN))]

    update.inline_query.answer(results)


#   Sekunden-Timer stellen.
#   Ziemlich fucking nutzlos xD
# def alarm(bot, job):
#    """Sendet die Benachrichtigung, dass der Alarm fällig ist."""
#    bot.send_message(job.context, text='Zeit abgelaufen!')
#
# def set_timer(bot, update, args, job_queue, chat_data):
#    """Fügt einen Job hinzu"""
#    chat_id = update.message.chat_id
#    try:
#        # args[0] enthält die Zeit des Timers in Sekunden
#        due = int(args[0])
#        if due < 0:
#            update.message.reply_text('Tut mir leid, aber wir können nicht zurück in die Zukunft.')
#            return
#        #fügt den Job hinzu
#        job = job_queue.run_once(alarm, due, context=chat_id)
#        chat_data['job'] = job
#
#        update.message.reply_text('Timer erfolgreich gestellt!')
#
#    except (IndexError, ValueError):
#            update.message.reply_text('Nutzung: /set <sekunden>')
#
# def unset(bot, update, chat_data):
#    """Entfernt den Timer"""
#    if 'job' not in chat_data:
#        update.message.reply_text('Du hast keinen aktiven Timer')
#        return
#    job = chat_data['job']
#    job.schedule_removal()
#    del chat_data['job']
#
#    update.message.reply_text('Timer erfolgreich entfernt')


# ##############################################################################

# Error Logs und so Kram
def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(API_TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("test", test))
    dp.add_handler(CommandHandler("keyboard", keyboard))
    dp.add_handler(CommandHandler("set", set_timer,
                                  pass_args=True,
                                  pass_job_queue=True)
    dp.add_handler(InlineQueryHandler(inlinequery))  # Inline-Anfrage

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
