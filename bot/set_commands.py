""" Commands interface """
from loguru import logger
from telegram import Bot
from telegram import BotCommandScopeAllChatAdministrators
from telegram import BotCommandScopeAllGroupChats
from telegram import BotCommandScopeAllPrivateChats

# from telegram import BotCommandScopeChat


def clear_bot(bot: Bot):
    """deletes previous commands"""

    bot.delete_my_commands(BotCommandScopeAllPrivateChats())
    bot.delete_my_commands(BotCommandScopeAllGroupChats())
    bot.delete_my_commands(BotCommandScopeAllChatAdministrators())
    logger.debug("User commands were cleared.")


all_commands = [
    # ("today", "Розклад на сьогодні ⬇️"),
    # ("tomorrow", "Розклад на завтра ➡️"),
    # ("week", "Розклад на неділю ⬇️"),
    # ("nextweek", "Розклад на наступну неділю ➡️"),
    # ("who", " Підказує ім'я викладача 👨‍🏫"),
    # ("left", "Показує час до кінця пари 🕘"),
    # ("profile", "Профіль 👤"),
    # ("timer", "Створити будильник ⏰"),
    # ("drop_timer", "Видалити будильник 🗑"),
    # ("info", "Про нас 📚"),
    ("start", "Старт"),
]

admin_commands = [
    ("id", "current chat_id 💳"),
    ("time", "server time 🕡"),
    # ("stat", "bot statistics 📊"),
    # ("drop", "delete user by chat id 🔞"),
    # ("set", "set user_data in your profile by chat_id 👨‍👦"),
    # ("parse", "parse specific university by id 🏛"),
    # ("push_status", "push status % and time 📫"),
]


def set_bot_commands(bot: Bot):
    """create commands lists for different chats and users"""

    # admins
    # for chat_id in ADMINS.keys():
    #     try:
    #         bot.set_my_commands(
    #             all_commands + admin_commands, scope=BotCommandScopeChat(chat_id)
    #         )
    #     except Exception as error:
    #         logger.error(
    #             f"Setting commands for chat_id: {chat_id}, failed with error: {error}"
    #         )

    # privat chats
    bot.set_my_commands(all_commands, scope=BotCommandScopeAllPrivateChats())

    # group admins
    bot.set_my_commands(all_commands, scope=BotCommandScopeAllChatAdministrators())

    #
    bot.set_my_commands(
        [
            ("today", "Розклад на сьогодні ⬇️"),
            ("tomorrow", "Розклад на завтра ➡️"),
            ("week", "Розклад на неділю ⬇️"),
            ("nextweek", "Розклад на наступну неділю ➡️"),
        ],
        scope=BotCommandScopeAllGroupChats(),
    )

    logger.debug("Command list was updated.")
