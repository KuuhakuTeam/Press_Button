# Press Button
# Copyright (C) 2023 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/Press_Button/ >
# PLease read the GNU v3.0 License Agreement in
# <https://www.github.com/KuuhakuTeam/Press_Button/blob/master/LICENSE/>.


from .bot import press_button, OWNER
from .handlers import starting, dilema, set_lang_, on_msg, restarting, send_dilema

from pyrogram import filters
from pyrogram.handlers import MessageHandler


press_button.add_handler(MessageHandler(starting, filters.command("start")))
press_button.add_handler(MessageHandler(restarting, filters.command("restart")))
press_button.add_handler(MessageHandler(send_dilema, filters.command("dilema") & filters.user(OWNER)))
press_button.add_handler(MessageHandler(set_lang_, filters.command("lang") & filters.group))
press_button.add_handler(MessageHandler(on_msg ,filters.group & filters.incoming))