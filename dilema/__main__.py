# Press Button
# Copyright (C) 2023 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/Press_Button/ >
# PLease read the GNU v3.0 License Agreement in
# <https://www.github.com/KuuhakuTeam/Press_Button/blob/master/LICENSE/>.

import asyncio

from pyrogram import idle
from logger import LOGGER
from pymongo.errors import ConnectionFailure
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .database import db_core
from .handlers import dilema
from .bot import press_button


scheduler = AsyncIOScheduler(timezone="America/Sao_Paulo")


async def db_connect():
    """Check Mongo Client"""
    try:
        LOGGER.info("[★] Connecting to MongoDB")
        db_core.server_info()
        LOGGER.info("[★] Database connected")
    except (BaseException, ConnectionFailure) as e:
        LOGGER.error("[X] Failed to connect to database, exiting....")
        LOGGER.error(str(e))
        exit(1)


async def run_press():
    """Start Bot"""
    await press_button.start()
    LOGGER.info("[★] BOT Started.")


async def run_all():
    """Run all Functions"""
    await db_connect()
    await run_press()
    scheduler.add_job(dilema, "interval", hours=1, id='dilemas')
    scheduler.start()
    await idle()


if __name__ == "__main__" :
    LOGGER.info("[★] Trying to launch bot.")
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run_all())
    except KeyboardInterrupt:
        exit()
    except Exception as err:
        LOGGER.error(err.with_traceback(None))
    finally:
        loop.stop()
