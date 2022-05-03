#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""Simple inline keyboard bot with multiple CallbackQueryHandlers.
This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined as callback query handler. Then, those functions are
passed to the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot that uses inline keyboard that has multiple CallbackQueryHandlers arranged in a
ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line to stop the bot.
"""
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, KeyboardButton, InputMediaPhoto
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext, MessageHandler, Filters,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logged_in_users = []

logger = logging.getLogger(__name__)

# Stages
FIRST, SECOND = range(2)
# Callback data
MAIN, STAT, SCAN, TEST, DOWN, ERR, INST, AUTH, SERV, SALE, TRAN, REF, MB, USE, ICST, CHNG, FIO,\
INVF, VSTRNEREZ, INVEST, SIM, KK, DK, MNP, VIEW, NDZ, SEEK, NONA, NEREZ, TM, CLS = range(31)


def start(update: Update, context: CallbackContext) -> int:
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).

    # Send message with text and appended InlineKeyboard
    update.message.reply_text("Введите пароль")
    # Tell ConversationHandler that we're in state `FIRST` now
    return FIRST


def start_over(update: Update, context: CallbackContext) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    # Instead of sending a new message, edit the message that
    # originated the CallbackQuery. This gives the feeling of an
    # interactive menu.
    query.edit_message_text(text="Введите пароль")
    return FIRST


def auth(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    message = update.message
    if (message.chat['id'] in logged_in_users):
        keyboard = [
            [
                InlineKeyboardButton("Далее", callback_data=str(MAIN)),

            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("Успешная авторизация", reply_markup=reply_markup)
        return FIRST
    elif (message.text == '1'):
        logged_in_users.append(message.chat['id'])
        keyboard = [
            [
                InlineKeyboardButton("Далее", callback_data=str(MAIN)),

            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("Успешная авторизация", reply_markup=reply_markup)
        return FIRST
    else:
        update.message.reply_text("Неверный пароль")


def main_page(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Инструкции \U0001F4DA", callback_data=str(INST)),
            ],
        [
            InlineKeyboardButton("Статистика \U0001F4C8", callback_data=str(STAT)),
            ],
        [
            InlineKeyboardButton("Нарушения \U000026D4", callback_data=str(ERR)),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Главное меню", reply_markup=reply_markup
    )
    return FIRST


def stat(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Сервис \U00002B50", callback_data=str(SERV)),
            InlineKeyboardButton("Продажи \U0001F4B0", callback_data=str(SALE)),
        ],
        [
            InlineKeyboardButton("\U00002b05 Назад", callback_data=str(MAIN)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Статистика \U0001F4C8", reply_markup=reply_markup
    )
    return FIRST


def serv(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Переносы", callback_data=str(TRAN)),
            InlineKeyboardButton("Отказы", callback_data=str(REF)),
        ],
        [
            InlineKeyboardButton("МБ", callback_data=str(MB)),
            InlineKeyboardButton("Утиль", callback_data=str(USE)),
        ],
        [
            InlineKeyboardButton("\U00002b05 Назад", callback_data=str(STAT)),
            InlineKeyboardButton("Главная \U00002139", callback_data=str(MAIN)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Сервис \U00002B50", reply_markup=reply_markup
    )
    return FIRST


def transfer(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    photo = 'https://downloader.disk.yandex.ru/preview/21ce8e72be4b3abba74d66d863121d0ae7cae9abc0a62ff5b65bbdccdf4da7c8/6266f14a/lFdwpV3iYxKSoXZ5lpGVTp0UeXrWxRTIsV1sXlr8LFozKTOuOe7Kw_KKb4AUnzj7n2ZNCp-tnEyeShE7woXOdA%3D%3D?uid=0&filename=%D0%BF%D0%B5%D1%80%D0%B5%D0%BD%D0%BE%D1%81%D1%8B.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=0&tknv=v2&size=1920x830'
    with open('transfer.txt', 'r', encoding='utf-8') as file:
        message = file.read()
    context.bot.send_photo(query.message.chat_id, photo=photo)
    context.bot.send_message(query.message.chat_id, message)
    keyboard = [
        [
            InlineKeyboardButton("\U00002b05 Назад", callback_data=str(SERV)),
            InlineKeyboardButton("Главная \U00002139", callback_data=str(MAIN)),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.bot.send_message(query.message.chat_id,
                           text="Вернуться", reply_markup=reply_markup
                           )
    return FIRST


def refusion(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    photo = 'https://downloader.disk.yandex.ru/preview/b932d0b272b910c80312a153335b2dd02fc85b8271a5cc7a0c85d4089731f108/6266f14a/bWHv0SLPlo1gcj0t-3oU550UeXrWxRTIsV1sXlr8LFouBwy3roZV102gPqWcl9-coH_SMlCdgu-8eJQgFS9bmA%3D%3D?uid=0&filename=%D0%BE%D1%82%D0%BA%D0%B0%D0%B7%D1%8B.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=0&tknv=v2&size=1920x830'
    with open('refusion.txt', 'r', encoding='utf-8') as file:
        message = file.read()
    context.bot.send_photo(query.message.chat_id, photo=photo)
    context.bot.send_message(query.message.chat_id, message)
    keyboard = [
        [
            InlineKeyboardButton("\U00002b05 Назад", callback_data=str(SERV)),
            InlineKeyboardButton("Главная \U00002139", callback_data=str(MAIN)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.bot.send_message(query.message.chat_id,
                           text="Вернуться", reply_markup=reply_markup
                           )
    return FIRST


def mb(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    photo = 'https://downloader.disk.yandex.ru/preview/a79ec2780692c23fb8ee1c176064ec037412cddd2661cd3817826824b851f8ef/6266f14a/RhraJHfOzCGTWcxaGRYsBZ0UeXrWxRTIsV1sXlr8LFpUsqDfAWf7L5YIKJmKHT6WrpUosNUg7HJcTxs8Y5brAg%3D%3D?uid=0&filename=%D0%BC%D0%BF.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=0&tknv=v2&size=1920x830'
    with open('mb.txt', 'r', encoding='utf-8') as file:
        message = file.read()
    context.bot.send_photo(query.message.chat_id, caption=message,
                           photo=photo)
    keyboard = [
        [
            InlineKeyboardButton("\U00002b05 Назад", callback_data=str(SERV)),
            InlineKeyboardButton("Главная \U00002139", callback_data=str(MAIN)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.bot.send_message(query.message.chat_id,
                           text="Вернуться", reply_markup=reply_markup
                           )
    return FIRST


def use(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    photo = 'https://downloader.disk.yandex.ru/preview/d6c564a6326fc7330f84367f27a84c20257d09953d2ad1c624345419fc1ed5ec/6266f14a/Uj0A_t6X47rqE5ags1EFMp0UeXrWxRTIsV1sXlr8LFqDrv-LF2yqQORyKRX_W8tR-QdtDnoymmATqh9If3Pe8w%3D%3D?uid=0&filename=%D1%83%D1%82%D0%B8%D0%BB%D1%8C.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=0&tknv=v2&size=1920x830'
    with open('use.txt', 'r', encoding='utf-8') as file:
        message = file.read()
    context.bot.send_photo(query.message.chat_id, caption=message,
                           photo=photo)
    keyboard = [
        [
            InlineKeyboardButton("\U00002b05 Назад", callback_data=str(SERV)),
            InlineKeyboardButton("Главная \U00002139", callback_data=str(MAIN)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.bot.send_message(query.message.chat_id,
                           text="Вернуться", reply_markup=reply_markup
                           )
    return FIRST


def sale(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Приведи Друга", callback_data=str(INVF)),
            InlineKeyboardButton("Инвестиции", callback_data=str(INVEST)),
        ],
        [
            InlineKeyboardButton("Дебетовые карты", callback_data=str(DK)),
            InlineKeyboardButton("Cим", callback_data=str(SIM)),
        ],
        [
            InlineKeyboardButton("Кредитные карты", callback_data=str(KK)),
            InlineKeyboardButton("MNP", callback_data=str(MNP)),
        ],
        [
            InlineKeyboardButton("\U00002b05 Назад", callback_data=str(STAT)),
            InlineKeyboardButton("Главная \U00002139", callback_data=str(MAIN)),
        ]

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Продажи \U0001F4B0", reply_markup=reply_markup
    )
    return FIRST


def inv_friend(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    photo = 'https://downloader.disk.yandex.ru/preview/900d7279e952428f5a11924a958fe6504665c859829244e61554ad4cee26e909/6268372e/EXRWX8OGVtsqTsFB2_6kk32pyqZlUEmCtOzQtO1am9TswpteVdQFQe_hGcS64OPU392QNokKHBCn4X8G39k36A%3D%3D?uid=0&filename=%D0%BF%D0%B4.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=0&tknv=v2&size=1898x881'
    with open('пд.txt', 'r', encoding='utf-8') as file:
        message = file.read()
    context.bot.send_photo(query.message.chat_id, photo=photo)
    context.bot.send_message(query.message.chat_id, message)
    keyboard = [
        [
            InlineKeyboardButton("\U00002b05 Назад", callback_data=str(SALE)),
            InlineKeyboardButton("Главная \U00002139", callback_data=str(MAIN)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.bot.send_message(query.message.chat_id,
                           text="Вернуться", reply_markup=reply_markup
                           )
    return FIRST


def invest(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    photo = 'https://downloader.disk.yandex.ru/preview/6ee1e1066114b4b98e6b2884cff725fc0410b080c15a2a9d804bb574836026f8/6268372e/wXg6OY1KYmltw3fcV7mfiHIAgGc5JTrT15fkBx79RYB3HS5w33d4xUtH34SL7UB_su-nLAsf0ipeteapAP_vtg%3D%3D?uid=0&filename=%D0%B8%D0%BD%D0%B2%D0%B5%D1%81%D1%82%D0%B8%D1%86.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=0&tknv=v2&size=1898x881'
    with open('инвестиции.txt', 'r', encoding='utf-8') as file:
        message = file.read()
    context.bot.send_photo(query.message.chat_id, photo=photo)
    context.bot.send_message(query.message.chat_id, message)
    keyboard = [
        [
            InlineKeyboardButton("\U00002b05 Назад", callback_data=str(SALE)),
            InlineKeyboardButton("Главная \U00002139", callback_data=str(MAIN)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.bot.send_message(query.message.chat_id,
                           text="Вернуться", reply_markup=reply_markup
                           )
    return FIRST


def sim(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    photo = 'https://i.ibb.co/sgkZSw4/image.png'
    with open('сим.txt', 'r', encoding='utf-8') as file:
        message = file.read()
    context.bot.send_photo(query.message.chat_id, photo=photo)
    context.bot.send_message(query.message.chat_id, message)
    keyboard = [
        [
            InlineKeyboardButton("\U00002b05 Назад", callback_data=str(SALE)),
            InlineKeyboardButton("Главная \U00002139", callback_data=str(MAIN)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.bot.send_message(query.message.chat_id,
                           text="Вернуться", reply_markup=reply_markup
                           )
    return FIRST


def kk(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    photo = 'https://downloader.disk.yandex.ru/preview/055665cc92349aab302ce5e771ca1d39e8e85b83dafa133309933fddc6418916/6268372e/awVdKDoLeP43GFOBBlMzhgXfxQKiJCVGDvVtb35PQK7Emh3PT3WUIynkS0y2-A15UinG9BtfBMqrsK8Ho6tFxw%3D%3D?uid=0&filename=%D0%BA%D0%BA.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=0&tknv=v2&size=1898x881'
    with open('kk.txt', 'r', encoding='utf-8') as file:
        message = file.read()
    context.bot.send_photo(query.message.chat_id, photo=photo)
    context.bot.send_message(query.message.chat_id, message)
    keyboard = [
        [
            InlineKeyboardButton("\U00002b05 Назад", callback_data=str(SALE)),
            InlineKeyboardButton("Главная \U00002139", callback_data=str(MAIN)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.bot.send_message(query.message.chat_id,
                           text="Вернуться", reply_markup=reply_markup
                           )
    return FIRST


def dk(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    photo = 'https://downloader.disk.yandex.ru/preview/25fe39db1d36d7285d16040be56859556a9d970a2da94ab47efdc27386d1f2e3/6268372e/8ix1CHHhL-zuSpTD12UbNnIAgGc5JTrT15fkBx79RYDey8I5OYQlzHeaX1rOsKzDaju13tC91k1SSE3oPV8ftA%3D%3D?uid=0&filename=%D0%B4%D0%BA.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=0&tknv=v2&size=1898x881'
    with open('дк.txt', 'r', encoding='utf-8') as file:
        message = file.read()
    context.bot.send_photo(query.message.chat_id, photo=photo)
    context.bot.send_message(query.message.chat_id, message)
    keyboard = [
        [
            InlineKeyboardButton("\U00002b05 Назад", callback_data=str(SALE)),
            InlineKeyboardButton("Главная \U00002139", callback_data=str(MAIN)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.bot.send_message(query.message.chat_id,
                           text="Вернуться", reply_markup=reply_markup
                           )
    return FIRST


def mnp(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    photo = 'https://downloader.disk.yandex.ru/preview/880ed80eb85d3ede49833552e394a7743f6d4a9899e9547f917f8d66d06ec61b/6268372e/yRxP6YCDgBIoAORO0IRhRnIAgGc5JTrT15fkBx79RYAZW-7TN17B6ydnWYa1iFkJ-S2SgfQVvWKHvarZ1c4fEQ%3D%3D?uid=0&filename=%D0%BC%D0%BD%D0%BF.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=0&tknv=v2&size=1898x881'
    with open('mnp.txt', 'r', encoding='utf-8') as file:
        message = file.read()
    context.bot.send_photo(query.message.chat_id, photo=photo)
    context.bot.send_message(query.message.chat_id, message)
    keyboard = [
        [
            InlineKeyboardButton("\U00002b05 Назад", callback_data=str(SALE)),
            InlineKeyboardButton("Главная \U00002139", callback_data=str(MAIN)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.bot.send_message(query.message.chat_id,
                           text="Вернуться", reply_markup=reply_markup
                           )
    return FIRST


def err(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Не пройден курс/тест", callback_data=str(TEST)),
        ],
        [
            InlineKeyboardButton("Не сканировал документы", callback_data=str(SCAN)),
        ],
        [
            InlineKeyboardButton("Внешний вид", callback_data=str(VIEW)),
        ],
        [
            InlineKeyboardButton("Встреча не закрыта день в день", callback_data=str(CLS)),
        ],
        [
            InlineKeyboardButton("Некорректные статусы в МП", callback_data=str(ICST)),
        ],
        [
            InlineKeyboardButton("Не исправлены данные в МП", callback_data=str(CHNG)),
        ],
        [
            InlineKeyboardButton("Отсутствует или сокращено ФИО", callback_data=str(FIO)),
        ],
        [
            InlineKeyboardButton("\U00002b05 Назад", callback_data=str(MAIN)),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Нарушения \U000026D4", reply_markup=reply_markup
    )
    # Transfer to conversation state `SECOND`
    return FIRST

def test(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    with open('test.txt', 'r', encoding='utf-8') as file:
        message = file.read()
    context.bot.send_message(query.message.chat_id, message)
    keyboard = [
        [
            InlineKeyboardButton("\U00002b05 Назад", callback_data=str(ERR)),
            InlineKeyboardButton("Главная \U00002139", callback_data=str(MAIN)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.bot.send_message(query.message.chat_id,
                           text="Вернуться", reply_markup=reply_markup
                           )
    return FIRST


def scan(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    with open('scan.txt', 'r', encoding='utf-8') as file:
        message = file.read()
    context.bot.send_message(query.message.chat_id, message)
    keyboard = [
        [
            InlineKeyboardButton("\U00002b05 Назад", callback_data=str(ERR)),
            InlineKeyboardButton("Главная \U00002139", callback_data=str(MAIN)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.bot.send_message(query.message.chat_id,
                           text="Вернуться", reply_markup=reply_markup
                           )
    return FIRST


def view(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    photo = 'https://downloader.disk.yandex.ru/preview/6237cbba0f6cc7acb69da15dc3f7b957e7c58b974c56109292ff296a31225735/625da1b1/ojbONLljw4wutqEeOZV-SWTF7ZO0OUxZ_j-HOEjJuqvyub4iQhmy5OrEdTA8pB5ixdYOmiPNZ96BTQEtS-pPag%3D%3D?uid=0&filename=photo_2021-06-15_17-39-35.jpg&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=2048x2048'
    with open('view.txt', 'r', encoding='utf-8') as file:
        message = file.read()
    context.bot.send_photo(query.message.chat_id, caption=message,
                           photo=photo)
    keyboard = [
        [
            InlineKeyboardButton("\U00002b05 Назад", callback_data=str(ERR)),
            InlineKeyboardButton("Главная \U00002139", callback_data=str(MAIN)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.bot.send_message(query.message.chat_id,
                           text="Вернуться", reply_markup=reply_markup
                           )
    return FIRST

def close(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    with open('close.txt', 'r', encoding='utf-8') as file:
        message = file.read()
    context.bot.send_message(query.message.chat_id, message)
    keyboard = [
        [
            InlineKeyboardButton("\U00002b05 Назад", callback_data=str(ERR)),
            InlineKeyboardButton("Главная \U00002139", callback_data=str(MAIN)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.bot.send_message(query.message.chat_id,
                           text="Вернуться", reply_markup=reply_markup
                           )
    return FIRST

def in_status(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    with open('status.txt', 'r', encoding='utf-8') as file:
        message = file.read()
    context.bot.send_message(query.message.chat_id, message)
    keyboard = [
        [
            InlineKeyboardButton("\U00002b05 Назад", callback_data=str(ERR)),
            InlineKeyboardButton("Главная \U00002139", callback_data=str(MAIN)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.bot.send_message(query.message.chat_id,
                           text="Вернуться", reply_markup=reply_markup
                           )
    return FIRST


def change(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    with open('change.txt', 'r', encoding='utf-8') as file:
        message = file.read()
    context.bot.send_message(query.message.chat_id, message)
    keyboard = [
        [
            InlineKeyboardButton("\U00002b05 Назад", callback_data=str(ERR)),
            InlineKeyboardButton("Главная \U00002139", callback_data=str(MAIN)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.bot.send_message(query.message.chat_id,
                           text="Вернуться", reply_markup=reply_markup
                           )
    return FIRST

def no_fio(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    with open('fio.txt', 'r', encoding='utf-8') as file:
        message = file.read()
    context.bot.send_message(query.message.chat_id, message)
    keyboard = [
        [
            InlineKeyboardButton("\U00002b05 Назад", callback_data=str(ERR)),
            InlineKeyboardButton("Главная \U00002139", callback_data=str(MAIN)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.bot.send_message(query.message.chat_id,
                           text="Вернуться", reply_markup=reply_markup
                           )
    return FIRST


def inst(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Недозвон", callback_data=str(NDZ)),
            InlineKeyboardButton("Поиск конвертов", callback_data=str(SEEK)),
            ],
        [
            InlineKeyboardButton("Замена на неименную", callback_data=str(NONA)),
        ],
        [
            InlineKeyboardButton("Нерезидент доки на РФ", callback_data=str(NEREZ)),
        ],
        [
            InlineKeyboardButton("Дозагрузка фото", callback_data=str(DOWN)),
        ],
        [
            InlineKeyboardButton("Обращение в ТМ", callback_data=str(TM)),
        ],
        [
            InlineKeyboardButton("Встреча с нерезидентом", callback_data=str(VSTRNEREZ)),
        ],
        [
            InlineKeyboardButton("\U00002b05 Назад", callback_data=str(MAIN)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Инструкции \U0001F4DA", reply_markup=reply_markup
    )
    return FIRST


def ndz(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    photo_file = []
    with open('ndz.txt', 'r', encoding='utf-8') as g:
        for line in g:
            photo_file.append(InputMediaPhoto(line))
    context.bot.send_media_group(query.message.chat_id, photo_file)
    keyboard = [
        [
            InlineKeyboardButton("\U00002b05 Назад", callback_data=str(INST)),
            InlineKeyboardButton("Главная \U00002139", callback_data=str(MAIN)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.bot.send_message(query.message.chat_id,
                           text="Вернуться", reply_markup=reply_markup
                           )
    return FIRST


def seek(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    photo_file = []
    with open('seek.txt', 'r', encoding='utf-8') as g:
        for line in g:
            photo_file.append(InputMediaPhoto(line))
    context.bot.send_media_group(query.message.chat_id, photo_file)
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("\U00002b05 Назад", callback_data=str(INST)),
            InlineKeyboardButton("Главная \U00002139", callback_data=str(MAIN)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.bot.send_message(query.message.chat_id,
        text="Вернуться", reply_markup=reply_markup
    )
    return FIRST


def noname(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    photo_file = []
    with open('noname.txt', 'r', encoding='utf-8') as g:
        for line in g:
            photo_file.append(InputMediaPhoto(line))
    context.bot.send_media_group(query.message.chat_id, photo_file)
    keyboard = [
        [
            InlineKeyboardButton("\U00002b05 Назад", callback_data=str(INST)),
            InlineKeyboardButton("Главная \U00002139", callback_data=str(MAIN)),
        ]

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.bot.send_message(query.message.chat_id,
                           text="Вернуться", reply_markup=reply_markup
                           )
    return FIRST


def nerez(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    photo_file = []
    with open('nerez.txt', 'r', encoding='utf-8') as g:
        for line in g:
            photo_file.append(InputMediaPhoto(line))
    context.bot.send_media_group(query.message.chat_id, photo_file)
    keyboard = [
        [
            InlineKeyboardButton("\U00002b05 Назад", callback_data=str(INST)),
            InlineKeyboardButton("Главная \U00002139", callback_data=str(MAIN)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.bot.send_message(query.message.chat_id,
                           text="Вернуться", reply_markup=reply_markup
                           )
    return FIRST


def download(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    photo_file = []
    with open('seek1.txt', 'r', encoding='utf-8') as g:
        for line in g:
            photo_file.append(InputMediaPhoto(line))
    context.bot.send_media_group(query.message.chat_id, photo_file)
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("\U00002b05 Назад", callback_data=str(INST)),
            InlineKeyboardButton("Главная \U00002139", callback_data=str(MAIN)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.bot.send_message(query.message.chat_id,
                           text="Вернуться", reply_markup=reply_markup
                           )
    return FIRST

def tm(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    photo = 'https://downloader.disk.yandex.ru/preview/0007d2496b065b41a9b3fab2496dbc993a83a4387345b62f94e046ad640b9185/62681b2d/KylBk36ydLByxmqty3Q9R_OfM38521EEIKq5pTSrUW0sqTKU5WaeyzRcUyDh5ZAhSBplAOHAhpa_CYGwL9Aqrw%3D%3D?uid=0&filename=TM.jpg&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=2048x2048'
    context.bot.send_photo(query.message.chat_id, photo=photo)
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("\U00002b05 Назад", callback_data=str(INST)),
            InlineKeyboardButton("Главная \U00002139", callback_data=str(MAIN)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.bot.send_message(query.message.chat_id,
                           text="Вернуться", reply_markup=reply_markup
                           )
    return FIRST
    
def vstrnerez(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    context.bot.send_document(query.message.chat_id, 'https://i.ibb.co/Phd7YYY/image.jpg')
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("\U00002b05 Назад", callback_data=str(INST)),
            InlineKeyboardButton("Главная \U00002139", callback_data=str(MAIN)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.bot.send_message(query.message.chat_id,
                           text="Вернуться", reply_markup=reply_markup
                           )
    return FIRST    



def main() -> None:
    """Run the bot."""

    updater = Updater("5184243076:AAHzL08eVzAYtoYdNTapgAdqDqjZ3qyM554")


    dispatcher = updater.dispatcher


    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST: [
                # Авторизация
                MessageHandler(Filters.text, auth),
                # Главная
                CallbackQueryHandler(main_page, pattern='^' + str(MAIN) + '$'),
                ##Статистика
                CallbackQueryHandler(stat, pattern='^' + str(STAT) + '$'),
                ###Сервисная
                CallbackQueryHandler(serv, pattern='^' + str(SERV) + '$'),
                CallbackQueryHandler(transfer, pattern='^' + str(TRAN) + '$'),
                CallbackQueryHandler(refusion, pattern='^' + str(REF) + '$'),
                CallbackQueryHandler(mb, pattern='^' + str(MB) + '$'),
                CallbackQueryHandler(use, pattern='^' + str(USE) + '$'),
                ###Продажная
                CallbackQueryHandler(sale, pattern='^' + str(SALE) + '$'),
                CallbackQueryHandler(inv_friend, pattern='^' + str(INVF) + '$'),
                CallbackQueryHandler(invest, pattern='^' + str(INVEST) + '$'),
                CallbackQueryHandler(sim, pattern='^' + str(SIM) + '$'),
                CallbackQueryHandler(kk, pattern='^' + str(KK) + '$'),
                CallbackQueryHandler(dk, pattern='^' + str(DK) + '$'),
                CallbackQueryHandler(mnp, pattern='^' + str(MNP) + '$'),
                ##Нарушения
                CallbackQueryHandler(err, pattern='^' + str(ERR) + '$'),
                CallbackQueryHandler(test, pattern='^' + str(TEST) + '$'),
                CallbackQueryHandler(scan, pattern='^' + str(SCAN) + '$'),
                CallbackQueryHandler(view, pattern='^' + str(VIEW) + '$'),
                CallbackQueryHandler(close, pattern='^' + str(CLS) + '$'),
                CallbackQueryHandler(in_status, pattern='^' + str(ICST) + '$'),
                CallbackQueryHandler(change, pattern='^' + str(CHNG) + '$'),
                CallbackQueryHandler(no_fio, pattern='^' + str(FIO) + '$'),
                ##Инструкции
                CallbackQueryHandler(inst, pattern='^' + str(INST) + '$'),
                CallbackQueryHandler(ndz, pattern='^' + str(NDZ) + '$'),
                CallbackQueryHandler(seek, pattern='^' + str(SEEK) + '$'),
                CallbackQueryHandler(noname, pattern='^' + str(NONA) + '$'),
                CallbackQueryHandler(nerez, pattern='^' + str(NEREZ) + '$'),
                CallbackQueryHandler(tm, pattern='^' + str(TM) + '$'),
                CallbackQueryHandler(vstrnerez, pattern='^' + str(VSTRNEREZ) + '$'),
                CallbackQueryHandler(download, pattern='^' + str(DOWN) + '$'),
            ],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    # Add ConversationHandler to dispatcher that will be used for handling updates
    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
