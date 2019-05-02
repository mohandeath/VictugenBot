#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.
#
# THIS EXAMPLE HAS BEEN UPDATED TO WORK WITH THE BETA VERSION 12 OF PYTHON-TELEGRAM-BOT.
# If you're still using version 11.1.0, please see the examples at
# https://github.com/python-telegram-bot/python-telegram-bot/tree/v11.1.0/examples

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

import telegram
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, SELECT_VARIANCE, PARSE_GENE , SELECT_SNR = range(3)

reply_keyboard = [['Age', 'Favourite colour'],
                  ['Number of siblings', 'Something else...'],
                  ['Done']]
markup = telegram.ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])


def start(update, context):
    update.message.reply_text(
        'Hi! \n welcome to Victugen report Bot!  \n \n  Please enter the GENE name printed in your report. \n sample : FTO' )
#  'Hi! \n welcome to <b><a href="http://victugen.com">Victugen</a></b> <br> Please enter the GENE name printed in your report. \n sample : FTO rs1421085' )

    return PARSE_GENE


def parse_gene(update, context):
    text = update.message.text
    context.user_data['gene'] = text
    
    if '-' not in text:
        update.message.reply_text('PLEASE ENTER THE GENE JUST LIKE WHAT THE SAMPLE BELOW AND THE PRINTED VERSION ON YOUR REPORT!! \n \n here\'s some samples: FTO-rs1421085(CC) , FTO , ')
        return PARSE_GENE
    else:
        gene = text.split('-')
        update.message.reply_text('So your gene is {} and the SNR is {}'.format(gene[0],gene[1]))
        return SELECT_VARIANCE


def custom_choice(update, context):
    update.message.reply_text('Alright, please send me the category first, '
                              'for example "Most impressive skill"')

    return PARSE_GENE


def received_information(update, context):
    user_data = context.user_data
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']

    update.message.reply_text("Neat! Just so you know, this is what you already told me:"
                              "{}"
                              "You can tell me more, or change your opinion on something.".format(
                                  facts_to_str(user_data)), reply_markup=markup)

    return CHOOSING

def parse_snr(update,context):
    pass

def done(update, context):
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text("I learned these facts about you:"
                              "{}"
                              "Until next time!".format(facts_to_str(user_data)))

    user_data.clear()
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(
        "652403984:AAHLzrwHQosLh1w01cvyom2dMvwbn9Vu_eA", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            SELECT_SNR : [MessageHandler(Filters.text,
                                           parse_snr,
                                           pass_user_data=True),],
            CHOOSING: [RegexHandler('^(Age|Favourite colour|Number of siblings)$',
                                    parse_gene,
                                    pass_user_data=True),
                       RegexHandler('^Something else...$',
                                    custom_choice),
                       ],

            PARSE_GENE: [MessageHandler(Filters.text,
                                           parse_gene,
                                           pass_user_data=True),
                            ],

            SELECT_VARIANCE: [MessageHandler(Filters.text,
                                          received_information,
                                          pass_user_data=True),
                           ],
        },

        fallbacks=[RegexHandler('^Done$', done, pass_user_data=True)]
    )

    dp.add_handler(conv_handler)

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
