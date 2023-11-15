# Press Button
# Copyright (C) 2023 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/Press_Button/ >
# PLease read the GNU v3.0 License Agreement in
# <https://www.github.com/KuuhakuTeam/Press_Button/blob/master/LICENSE/>.

import os
import html

from .bot import press_button, GP_LOGS, DB_URI
from pymongo import MongoClient


db_core = MongoClient(DB_URI)
db = db_core["Press_Button"]

GROUPS = db.get_collection("GROUPS")


class Groups:
    def __init__():
        pass

    async def find_gp(gid: int):
        if GROUPS.find_one({"_id": gid}):
            return True

    async def add_gp(m):
        user = mention_html(m.from_user.id, m.from_user.first_name)
        user_start = f"#Press_Button #New_Group\n\n<b>Group</b>: {m.chat.title}\n<b>ID:</b> {m.chat.id}\n<b>User:</b> {user}"
        await press_button.send_message(GP_LOGS,
            user_start, disable_notification=False, disable_web_page_preview=True
        )
        return GROUPS.insert_one({"_id": m.chat.id})

    async def rm_gp(gid: int):
        return GROUPS.delete_one({"_id": gid})

    async def find_lang(gid: int):
        find = GROUPS.find_one({"_id": gid})
        try:
            return find["lang"]
        except (KeyError, TypeError):
            return "en"

    async def add_lang(gid: int, lang: str):
        return GROUPS.update_one(
            {"_id": gid},
            {"$set": {"lang": lang}},
            upsert=True
        )

    async def count():
        return await GROUPS.estimated_document_count()


def mention_html(user_id, name):
    return u'<a href="tg://user?id={}">{}</a>'.format(
        user_id, html.escape(name))
