""" basic command and error handlers """
import html
import json
import os
import sys
import traceback
from datetime import datetime
from typing import Dict

from loguru import logger
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import Update
from telegram.chat import Chat
from telegram.ext import CallbackContext
from telegram.ext import ConversationHandler
from telegram.utils import helpers

from bot.notion import list_tasks
from bot.utils import log_message

OWNER_ID = int(os.getenv("OWNER_ID", "0"))

text: Dict[str, str] = dict()


def tasks_msg() -> str:
    tasks = "На сегодня:\n\n‣ " + "\n‣ ".join(list_tasks())
    return tasks


refresh_markup = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Обновить 🔄", callback_data="refresh")]]
)


def start(update: Update, context: CallbackContext):
    """start command an msg"""

    log_message(update)

    if update.message.chat.id == OWNER_ID:
        update.message.reply_text(text=tasks_msg(), reply_markup=refresh_markup)
    else:
        update.message.reply_text("FUCK YOU")


def refresh(update: Update, context: CallbackContext):
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise.
    # See https://core.telegram.org/bots/api#callbackquery
    query = update.callback_query
    query.answer()

    new_tasks = tasks_msg()

    if new_tasks != query.message.text:
        query.edit_message_text(text=new_tasks, reply_markup=refresh_markup)


def info(update: Update, context: CallbackContext):
    """general info massage"""

    log_message(update)
    url = helpers.create_deep_linked_url(
        context.bot.get_me().username, "startgroup", group=True
    )
    info_text = text["info"].format(url=url)
    update.message.reply_text(info_text, disable_web_page_preview=True)


def check_id(update: Update, context: CallbackContext):
    """return user id"""

    log_message(update)
    chat_id = update.message.chat.id
    update.message.reply_text(text=f"chat_id: {chat_id}")


def check_time(update: Update, context: CallbackContext):
    """return current server time"""

    log_message(update)
    kiev_now = datetime.now()
    update.message.reply_text(
        f"Current server time by Europe/Kiev\n{str(kiev_now)}",
    )


def stop(update: Update, context: CallbackContext):
    """stops conversation handler"""

    log_message(update)
    stop_text = text["reload"]
    if update.message.chat.type != Chat.PRIVATE:
        stop_text += "@" + context.bot.username
    update.message.reply_text(
        text=stop_text,
        disable_web_page_preview=True,
    )
    return ConversationHandler.END


def echo(update: Update, context: CallbackContext):
    """echo all msgs"""

    log_message(update)
    update.message.reply_text(text["service_msg"])


def outside_the_flow(update: Update, context: CallbackContext):
    """outside_the_flow handler in case storage file was dropped or error concluded"""

    message = update.message
    if message and message.chat.type == Chat.PRIVATE:  # don't spam in chats
        log_message(update)
        logger.bind(chat_id=update.message.chat.id).warning(
            "outside the flow in <private> chat"
        )
        update.message.reply_text(text["outside_the_flow"])


def error_handler(update: Update, context: CallbackContext):
    """Log the error and send a telegram message to notify the developer"""
    # we want to notify the user of this problem.
    # This will always work, but not notify users if the update is an
    # callback or inline query, or a poll update.
    # In case you want this, keep in mind that sending the message could fail

    if update:
        local_upd = (
            update.effective_message if update.effective_message else update.message
        )
    else:
        local_upd = None

    chat_id = None
    if local_upd:
        chat_id = local_upd.chat.id
        context.bot.send_message(
            chat_id=chat_id,
            text=text["server_error"],
        )

    # Log the error before we do anything else, so we can see it even if something breaks.

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    error_tb = "".join(tb_list)
    logger.bind(chat_id=chat_id).error(f"Exception while handling an update:{error_tb}")
    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    bot_username = "@" + context.bot.username + "\n\n"
    if update:
        update_json = json.dumps(update.to_dict(), indent=2, ensure_ascii=False)
    else:
        update_json = ""
    error_message = (
        "{}"
        "An exception was raised while handling an update\n"
        "<pre>update = {}</pre>\n\n"
        "<pre>context.chat_data = {}</pre>\n\n"
        "<pre>context.user_data = {}</pre>\n\n"
        "<pre>{}</pre>"
    ).format(
        bot_username,
        html.escape(update_json),
        html.escape(str(context.chat_data)),
        html.escape(str(context.user_data)),
        html.escape(error_tb),
    )

    # Finally, send the message
    log_channel = "@" + os.environ["LOG_CHANNEL"]

    # dont print to debug channel in case that's not a production server
    if ("--debug" not in sys.argv) and ("-d" not in sys.argv):
        if len(error_message) < 4096:
            context.bot.send_message(chat_id=log_channel, text=error_message)
        else:
            msg_parts = len(error_message) // 4080
            for i in range(msg_parts):
                err_msg_truncated = error_message[i : i + 4080]
                if i == 0:
                    error_message_text = err_msg_truncated + "</pre>"
                elif i < msg_parts:
                    error_message_text = "<pre>" + err_msg_truncated + "</pre>"
                else:
                    error_message_text = "<pre>" + err_msg_truncated
                context.bot.send_message(chat_id=log_channel, text=error_message_text)
