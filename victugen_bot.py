#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import telegram
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

SELECT_VARIANCE, PARSE_GENE, SELECT_SNR = range(3)


def start(update, context):
    update.message.reply_text(
        'Hi! \n welcome to Victugen report Bot!  \n \n  Please enter the GENE name printed in your report. \n sample : FTO')

    return PARSE_GENE


def parse_gene(update, context):
    text = update.message.text
    context.user_data['gene'] = text
    if 'FTO' in text:
        update.message.reply_text(
            "so Your Gene type is FTO..! \n👉 here's a fact about FTO genes : \n  '{0}' \n \n \n ⭕️ now please enter the SNR printed in your report.AKA the seccond part of the gene information you have.👇 \n sample rs1421085: ".format(
                "FTO affects the hypothalamus in the brain, which is a regulator of hunger. People with FTO variations tend to select food with higher energy content (more calories) and which are typically high in saturated fat and sugar."))
        return SELECT_SNR
    else:
        update.message.reply_text(
            'unfortunately there is no related information for the entered gene: {}. we are working on improving our gene database please comback later. you can also hit /start to begin again! best of luck!'.format(
                text))
        context.user_data.clear()
        return ConversationHandler.END


def custom_choice(update, context):
    update.message.reply_text('Alright, please send me the category first, '
                              'for example "Most impressive skill"')

    return PARSE_GENE


variants = {
    'rs1421085': ['TT', 'CT', 'CC'],
    'rs9939609': ['TT', 'TA', 'AA']
}

variant_detail = {
    'rs1421085': {
        'TT': 'You have less tendency to be overweight.',
        'CT': 'You have a single variation (CT). \n  You have a tendency to be overweight, which is enhanced by eating saturated fat.',
        'CC': 'You have a double variation (CC). \n You have a high tendency to be overweight, which is intensified by eating saturated fat.',
    },
    'rs9939609': {
        'TT': 'In general, you have lower risk of obesity and developing obesity-related type II diabetes.',
        'TA': '''You have probably had an increased tendency to be overweight from an early age. 
In general, you have higher risk of obesity and developing obesity-related type II diabetes

 
FTO single
variations are known to be associated with excess weight, often from childhood. Because you have a single variation, you are 30% more prone to being overweight than people without variations.

 
FTO
affects the hypothalamus in the brain, which is a regulator of hunger. People with FTO variations tend to select food with higher energy content (more calories) and which are typically high in saturated fat and sugar.

Carriers of single variants are shown to have 1.3 times higher risk of type II diabetes.

 
The more
saturated fat you consume, the more the FTO gene sends messages to consume more food and the poorer your sense of satiety becomes. This leads to an even greater sense of hunger. The FTO gene is also associated with having less energy and a lower desire to 
exercise.

 

Typical effects of FTO variations:

 
- Tendency to be overweight
-More hunger, less satiety


- Less willingness to exercise
    
- Having less energy
   
- More inclined to choose saturated fat and sugar


- Very self-reinforcing – the unhealthier food you have the more you crave

 
If you wish to “turn off” the FTO variation, you should:


 
*    Consume less than 10 grams of saturated fat daily. It is beneficial to have a low-fat diet, but even better to follow a Mediterranean-style diet to lose weight most effectively.

*    
Eat dairy products (cheese, butter, cream etc.) with caution.  These are particularly high in saturated fats and should be avoided. If you use milk, use skimmed milk.
*    
Eat regularly and eat a balanced diet.

     If your body’s nutritional demands are met, you should feel less prone to urgent hunger pangs and overeating. 
*    
Exercise regularly!

     There is a correlation between muscle mass and counteracting your FTO variations. Regular exercise will help you counteract the gene variation, burn calories, assist your metabolism and help you to reduce your weight, especially when you have a variation in FTO rs9939609.

 ''',
        'AA': '''You have probably had a tendency to be overweight from an early age. 
In general, you have very higher risk of obesity and developing obesity-related type II diabetes.

 
FTO double
variations are known to be associated with excess weight, often from childhood. Because you have a double variation, you are 70% more prone to being overweight than people without 
variations.
Carriers of the double variants have shown a 1.6 times higher risk of developing type II diabetes. 


 
FTO
affects the hypothalamus in the brain, which is a regulator of hunger. People with FTO variations tend to select food with higher energy content (more calories) and which are typically high in saturated fat and sugar.

 
The more
saturated fat you consume, the more the FTO gene sends messages to consume more food and the poorer your sense of satiety becomes. This leads to an even greater sense of hunger. The FTO gene is also associated with having less energy and a lower desire to 
exercise.

 

Typical effects of FTO variations:

 
*    
Tendency to be overweight
*    
More hunger, less satiety
*    
Less willingness to exercise
*    
Having less energy
*    
More inclined to choose saturated fat and sugar
*    
Very self-reinforcing – the unhealthier food you have the more you crave 

 

If you wish to “turn off” the FTO variation, you should:

 
*    Consume less than 10 grams of saturated fat daily. It is beneficial to have a low-fat diet, but even better to follow a Mediterranean-style diet to lose weight most effectively.

*    
Eat dairy products (cheese, butter, cream etc.) with caution.  These are particularly high in saturated fats and should be avoided. If you use milk, use skimmed milk.
*    
Eat regularly and eat a balanced diet.

If your body’s nutritional demands are met, you should feel less prone to urgent hunger pangs and overeating.

*    
Exercise regularly!
*    
There is a correlation between muscle mass and counteracting your FTO variations. Regular exercise will help you counteract the gene variation, burn calories, assist your metabolism and help you to reduce your weight, especially when you have a variation in FTO rs9939609.
''',
    }
}


def parse_snr(update, context):
    text = update.message.text
    context.user_data['snr'] = text
    snrs = ['rs1421085', 'rs9939609']
    print('\n \n the full gene is : {0}-{1}(?)'.format(context.user_data['gene'], text))

    if not text in snrs:
        update.message.reply_text(
            'unfortunately there is no related information for the entered gene: {}. we are working on improving our gene database please comeback later. you can also hit /start to begin again! best of luck!'.format(
                text))
        context.user_data.clear()
        return ConversationHandler.END
    else:
        genesnr = '{0}-{1}'.format(context.user_data['gene'], text)
        update.message.reply_text(
            '🧬 There are many varioations for your gene, \n the last step is to select the variation! please enter the variation for the gene (📝 you can find it on your DNA test report as well!) \n \n here is the available variations for {0} : {1}'
                .format(text, ' , '.join(variants[text])))
        return SELECT_VARIANCE


def select_variance(update, context):
    text = update.message.text
    context.user_data['variant'] = text
    snr = context.user_data['snr']
    print('\n \n the full gene is : {0}-{1}({2})'.format(context.user_data['gene'], context.user_data['snr'], text))
    if text not in variants[snr]:
        update.message.reply_text(
            'unfortunately there is no related information for the entered variation. we are working on improving our gene database please comeback later. you can also hit /start to begin again! best of luck!'.format(
                text))
        context.user_data.clear()
        return ConversationHandler.END
    else:
        update.message.reply_text('🔰 Here is some information about your type {0}-{1}({2}) : {3} '
                                  .format(context.user_data['gene'], context.user_data['snr'], text,variant_detail[snr][text]))
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
            SELECT_SNR: [MessageHandler(Filters.text,
                                        parse_snr,
                                        pass_user_data=True), ],

            PARSE_GENE: [MessageHandler(Filters.text,
                                        parse_gene,
                                        pass_user_data=True),
                         ],

            SELECT_VARIANCE: [MessageHandler(Filters.text,
                                             select_variance,
                                             pass_user_data=True),
                              ],
        },

        fallbacks=[RegexHandler('^Done$', error, pass_user_data=True)]
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
