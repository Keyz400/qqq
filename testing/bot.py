#7Z@QVcA^X*jV
#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
import pyrogram
from pyrogram import Client
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
import os
import requests
from scraper import scrape
import re
from datetime import date, datetime 
import time
from pyrogram.types import Message
import asyncio
#from test import animepahe
#from testing.utils.eval import aexec
import io 
import sys 
import traceback
import subprocess



# bot
bot_token = os.environ.get("TOKEN", "6226448350:AAE439-aTXuN8BbR1VO-ifkCYSsJ0cseadE")
api_hash = os.environ.get("HASH", "8b446e569ff634428df4ad723d01b7fd") 
api_id = os.environ.get("ID", "25094651")

app = Client("my_bot",api_id=api_id, api_hash=api_hash,bot_token=bot_token)  

@app.on_message(filters.command('q', prefixes='!'))
def send_start(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    app.send_message(message.chat.id,'hello')
async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


@app.on_message(filters.command('qwe', prefixes='!'))
async def eval1(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    status_message = await message.reply_text("Processing ...")
    cmd = message.text.split(" ", maxsplit=1)[1]
    reply_to_ = message
    if message.reply_to_message:
        reply_to_ = message.reply_to_message
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    final_output = "<b>EVAL</b>: "
    final_output += f"<code>{cmd}</code>\n\n"
    final_output += "<b>OUTPUT</b>:\n"
    final_output += f"<code>{evaluation.strip()}</code> \n"
    if len(final_output) > 4096:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.txt"
            await reply_to_.reply_document(
                document=out_file, caption=cmd, disable_notification=True
            )
    else:
        await reply_to_.reply_text(final_output)
    await status_message.delete()

        

# server loop
print("Bot Starting")
print('1')
app.run()
