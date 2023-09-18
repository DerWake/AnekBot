import requests
import os
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, ConversationHandler, MessageHandler, CommandHandler, filters

CHOOSING = range(3)


def build_menu(buttons, n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu

keyboard = [
        KeyboardButton("Получить Анекдот 😂"),
        KeyboardButton("Получить Анекдот 🔞")
]
reply_markup = ReplyKeyboardMarkup(build_menu(keyboard, n_cols=1))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await context.bot.send_message(chat_id=update.effective_chat.id, text="Привет, я бот случайных анекдотов. Нажми на кнопку и получи свой анекдот", reply_markup=reply_markup)
    return CHOOSING

async def get_anekdot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "http://rzhunemogu.ru/RandJSON.aspx?CType=1"
    request = requests.get(url)
    anekdot = request.text[12:]
    anekdot = anekdot[:-2]
    await context.bot.send_message(chat_id=update.effective_chat.id, text=anekdot, reply_markup=reply_markup)
    return CHOOSING

async def get_anekdot_18(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "http://rzhunemogu.ru/RandJSON.aspx?CType=11"
    request = requests.get(url)
    anekdot = request.text[12:]
    anekdot = anekdot[:-2]
    await context.bot.send_message(chat_id=update.effective_chat.id, text=anekdot, reply_markup=reply_markup)
    return CHOOSING

if __name__ == '__main__':
    TOKEN = os.environ["TOKEN"]
    application = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex(".*"), start)],
        states={
            CHOOSING: [
                MessageHandler(
                    filters.Regex("Получить Анекдот 😂"), get_anekdot
                ),
                MessageHandler(filters.Regex("Получить Анекдот 🔞"), get_anekdot_18),
            ]
        },
        fallbacks=[],
    )
    application.add_handler(conv_handler)
    application.run_polling()