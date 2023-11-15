# Press Button
# Copyright (C) 2023 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/Press_Button/ >
# PLease read the GNU v3.0 License Agreement in
# <https://www.github.com/KuuhakuTeam/Press_Button/blob/master/LICENSE/>.

import os
import sys
import httpx

from bs4 import BeautifulSoup
from translate import Translator

from .database import Groups, GROUPS
from .bot import press_button

from pyrogram import filters
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import ChatIdInvalid, ChatWriteForbidden, ChannelInvalid, ChannelPrivate, PeerIdInvalid, ChatAdminRequired


async def starting(_, message):
    """just start"""
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Repository", url=f"https://github.com/KuuhakuTeam/Prsss_Button/",
                ),
                InlineKeyboardButton(
                    text="Add to a group", url=f"https://t.me/{press_button.me.username}?startgroup=new",
                ),
            ],
        ]
    )
    if message.chat.type == ChatType.PRIVATE:
        await message.reply("<b>Can you press a button?</b>", reply_markup=keyboard)
    else:
        await message.reply("<b>Every hour I will send a dilemma.\n\n/lang - to set the polls language</b>")


async def send_dilema(_, message: Message):
    """dev function to send manual dilemmas"""
    await message.reply("sending dilemma on chats")
    await dilema()


async def dilema():
    """function to send dilemmas on all chats"""
    glist = GROUPS.find()
    for chats in glist:
        if chats == None:
            return
        else:
            gid = chats["_id"]
            with httpx.Client() as client:
                req = client.get('https://willyoupressthebutton.com/').content
            rect = BeautifulSoup(str(req), "html.parser").find("div", attrs={'id': 'cond'}).text
            res = BeautifulSoup(str(req), "html.parser").find("div", attrs={'id': 'res'}).text
            msg = str(f"{rect} BUT {res}")
            lang = await Groups.find_lang(gid)
            options = ["press button", "don't press"]
            if lang == "pt":
                translator= Translator(to_lang="pt")
                msg = translator.translate(msg)
                options = ["pressionar botão", "não pressionar"]
            try:
                await press_button.send_poll(gid, msg, options, is_anonymous=False)
            except (ChatIdInvalid, ChannelInvalid, PeerIdInvalid):
                await Groups.rm_gp(gid)
                pass
            except (ChatWriteForbidden, ChatAdminRequired, ChannelPrivate):
                pass
            except Exception as e:
                pass


async def set_lang_(_, message):
    """set language on chat"""
    chat_id = message.chat.id
    if not message.chat.type == ChatType.SUPERGROUP:
        return
    if not await check_rights(message.chat.id, message.from_user.id):
        return await message.reply("<i>You need to be admin to do this.</i>")
    if not await Groups.find_gp(chat_id):
        await Groups.add_gp(message)
    buttons_ = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🇧🇷 Português", callback_data=f"_lang|pt"),
                    InlineKeyboardButton(
                        "🇺🇸 English", callback_data=f"_lang|en")
                ],
            ]
        )
    await message.reply("<i>Select language in which you want to receive polls</i>", reply_markup=buttons_)


@press_button.on_callback_query(filters.regex(pattern=r"^_lang\|(.*)"))
async def set_language(_, cb: CallbackQuery):
    """callback response set lang"""
    data, lang = cb.data.split("|")
    gid = cb.message.chat.id
    if cb.message.chat.type == ChatType.SUPERGROUP:
        if not await check_rights(gid, cb.from_user.id):
            return await cb.answer("You need to be admin to do this", show_alert=True)
    if lang == "pt":
        await Groups.add_lang(gid, "pt")
    else:
        await Groups.add_lang(gid, "en")
    await cb.edit_message_text(f"Polls will be sent in {lang}")


async def check_rights(chat_id: int, user_id: int) -> bool:
    """check admin"""
    user = await press_button.get_chat_member(chat_id, user_id)
    if user_id in [838926101]:
        return True
    if user.status == ChatMemberStatus.MEMBER:
        return False
    elif user.status == ChatMemberStatus.OWNER or ChatMemberStatus.ADMINISTRATOR:
        return True
    else:
        return False


async def on_msg(_, message: Message):
    """incoming msg"""
    try:
        gid = message.chat.id
        user = message.from_user
        title = message.chat.title
        if not await Groups.find_gp(gid):
            await Groups.add_gp(message)
    except AttributeError:
        return


async def restarting(_, message):
    """soft restart"""
    if not message.from_user.id == 838926101:
        return
    await message.reply("kek")
    os.execv(sys.executable, [sys.executable, "-m", "dilema"])