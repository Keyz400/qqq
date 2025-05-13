# (c) adarsh-goel

import asyncio
import traceback
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
import logging
import datetime

from database import Database
db_url = "mongodb+srv://herukotest:herukotest@test.trmvd8p.mongodb.net/?retryWrites=true&w=majority"
#db_url = "mongodb+srv://testfiletolink:testfiletolink@file.k0gf5py.mongodb.net/?retryWrites=true&w=majority"
name = 'Bypass'
db = Database(db_url, name)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

#info=main.UPDATES_CHANNEL


async def broadcast_messages(user_id, message):
    try:
        await message.copy(chat_id=user_id)
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return await broadcast_messages(user_id, message)
    except InputUserDeactivated:
        await db.delete_user(int(user_id))
        logging.info(f"{user_id}-Removed from Database, since deleted account.")
        return False, "Deleted"
    except UserIsBlocked:
        logging.info(f"{user_id} -Blocked the bot.")
        return False, "Blocked"
    except PeerIdInvalid:
        await db.delete_user(int(user_id))
        logging.info(f"{user_id} - PeerIdInvalid")
        return False, "Error"
    except Exception as e:
        return False, "Error"