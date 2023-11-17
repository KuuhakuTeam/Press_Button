# Press Button
# Copyright (C) 2023 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/Press_Button/ >
# PLease read the GNU v3.0 License Agreement in
# <https://www.github.com/KuuhakuTeam/Press_Button/blob/master/LICENSE/>.

import os
import sys
import json
import random
import requests

from bs4 import BeautifulSoup
from urllib.parse import quote

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
                    text="Repository", url=f"https://github.com/KuuhakuTeam/Press_Button/",
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
            req = requests.get('https://willyoupressthebutton.com/').content
            rect = BeautifulSoup(str(req), "html.parser").find("div", attrs={'id': 'cond'}).text
            res = BeautifulSoup(str(req), "html.parser").find("div", attrs={'id': 'res'}).text
            msg = f"{rect} BUT {res}"
            lang = await Groups.find_lang(gid)
            options = ["press button", "don't press"]
            if lang == "pt":
                msg = translate(msg, lang_tgt="pt")
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
    try:
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
        await message.reply("<i>Select language in which you want to receive polls.</i>", reply_markup=buttons_)
    except ChatAdminRequired:
        await message.reply("<b>Due to the privacy of group, I need admin to do this.</b>")


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


# - part taken from
# - https://github.com/TeamUltroid/Ultroid/blob/41fb5b5250a4e0cf296b98468e50edaed101b9f0/pyUltroid/fns/tools.py#L658

def _package_rpc(text, lang_src="auto", lang_tgt="auto"):
    GOOGLE_TTS_RPC = ["MkEWBc"]
    parameter = [[text.strip(), lang_src, lang_tgt, True], [1]]
    escaped_parameter = json.dumps(parameter, separators=(",", ":"))
    rpc = [[[random.choice(GOOGLE_TTS_RPC), escaped_parameter, None, "generic"]]]
    espaced_rpc = json.dumps(rpc, separators=(",", ":"))
    freq = "f.req={}&".format(quote(espaced_rpc))
    return freq

def translate(*args, **kwargs):
    headers = {
        "Referer": "https://translate.google.co.in",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/47.0.2526.106 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
    }
    x = requests.post(
        "https://translate.google.co.in/_/TranslateWebserverUi/data/batchexecute",
        headers=headers,
        data=_package_rpc(*args, **kwargs),
    ).text
    response = ""
    data = json.loads(json.loads(x[4:])[0][2])[1][0][0]
    subind = data[-2]
    if not subind:
        subind = data[-1]
    for i in subind:
        response += i[0]
    return response