#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        admin.py what else did you expect here? :D
# Purpose:     Send user input to the admin of the bot and let the admin reply
#              to those texts through the bot
#
# Author:      ColinShark
# Contact at:  t.me/ColinShark
#
# Created:     02.12.2017
# Copyright:   (c) ColinShark 2017
# Licence:     none
# -------------------------------------------------------------------------------

API_TOKEN = "TOKEN"
UserID_Colin = "289579584"
received_message = None

# -------------------------------------------------------------------------------

from telegram import (ReplyKeyboardMarkup,
                      ReplyKeyboardRemove,
                      ForceReply
                      )
from telegram.ext import (Updater,
                          CommandHandler,
                          MessageHandler,
                          Filters,
                          RegexHandler,
                          ConversationHandler
                          )

import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------

AUSWAHL, USER_INPUT, ADMIN_RESPONSE = range(3)

reply_keyboard = [['Ja', 'Nein']]
markup = ReplyKeyboardMarkup(reply_keyboard,
                             one_time_keyboard=True,
                             resize_keyboard=True
                             )

def start(bot, update):
    # Greets the User
    update.message.reply_text(
        "Hi {} 👋\nIch bin der Bot von @ColinShark.\nSende mir /admin, um Colin eine Nachricht zu senden.".format(
            update.effective_user.first_name
        )
    )
    # Sends message to admin if the Bot is started
    bot.send_message(
        chat_id=UserID_Colin,
        text="{} (@{} hat den Bot gestartet.\nOder nur /start genutzt ._.".format(
            update.effective_user.first_name,
            update.effective_user.username
        )
    )


def admin(bot, update):
    # Asks the user if he wants to contact the admin
    update.message.reply_text(
        "Möchtest du Colin kontaktieren?\nEr wird sich zeitnah über diesen Bot zurückrückmelden.",
        reply_markup=markup # Keyboard is started
    )
    return AUSWAHL # Next state of the ConversationHandler


def choice_yes(bot, update, user_data):
    update.message.reply_text(
        text="Okay. Was möchtest du Colin schreiben?",
        reply_markup=ForceReply()
    )

    return USER_INPUT # Next state of the ConversationHandler


def input_text(bot, update):
    global received_message
    received_message = update.message

    admin_notification = '{} (@{}) hat dich mit\n\n{}\n\nangeschrieben.\n_Was möchtest du antworten?_'.format(
        update.effective_user.first_name,
        update.effective_user.username,
        update.message.text
    )

    # Message to the Admin
    bot.send_message(
        UserID_Colin,
        admin_notification,
        parse_mode='markdown',
        reply_markup=ForceReply()
    )
    # Next status of the ConversationHandler
    return ADMIN_RESPONSE


def respond_to_user(bot, update):
    # Recipient ID is being extracted from the message
    recipient = received_message.from_user.id

    bot.send_message(recipient, update.message.text)

    # Exit ConversationHandler
    return ConversationHandler.END


def choice_no(bot, update):
    update.message.reply_text("Okay, Colin wird nicht benachrichtigt.",
                              reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    # Updater gets the API Token
    updater = Updater(API_Colin)

    # Dispatcher registriert die Handler
    dp = updater.dispatcher

    # Adds a ConversationHandler with the states AUSWAHL, USER_INPUT and ADMIN_RESPONSE
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('admin', admin)],

        states={
            AUSWAHL: [RegexHandler('^(Ja)$',
                                   choice_yes,
                                   pass_user_data=True)
                      ],
            USER_INPUT: [
                MessageHandler(Filters.text, input_text)
            ],
            ADMIN_RESPONSE: [
                MessageHandler(Filters.text, respond_to_user)
            ]
        },
        fallbacks=[RegexHandler('^(Nein)$', choice_no)]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler("start", start))

    # Logs the Errors
    dp.add_error_handler(error)

    # Starts the Bot
    updater.start_polling()

    # Keeps the bot running until Ctrl+C is issued
    updater.idle()


if __name__ == '__main__':
    main()
