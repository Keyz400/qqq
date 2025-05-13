#7Z@QVcA^X*jV
#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
import pyrogram
from pyrogram import Client
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
from pymongo import MongoClient
import bypasser
import os
import ddl
from pyrogram.enums.parse_mode import ParseMode
import requests
import threading
from texts import HELP_TEXT,RESTART_TXT,START_TEXT,SHORT_TEXT,ABOUT_TEXT
from ddl import ddllist
import re
from broadcast_helper import broadcast_messages
import pytz
from datetime import date, timedelta
import time
import asyncio
from database import Database
from scraper import scrape
import io 
import sys
import traceback
import subprocess
from asyncio import create_subprocess_exec, create_subprocess_shell, run_coroutine_threadsafe, sleep
from asyncio.subprocess import PIPE
from io import BytesIO
from time import time
from re import match
from sys import executable, argv
from os import execl,path as ospath
from asyncio import create_task, gather




# bot
bot_token = os.environ.get("TOKEN", "6394626120:AAHVtg8PoSU_SKY6NY8C2HYXYdH0xm_wOks")
#bot_token = os.environ.get("TOKEN", "5981576988:AAEicuu56o0wk3sVTtSauMN4wX6QYd2HMig")
api_hash = os.environ.get("HASH", "8b446e569ff634428df4ad723d01b7fd") 
api_id = os.environ.get("ID", "25094651")
OWNER_ID = os.environ.get("OWNER_ID", "6131675384")
ADMIN_LIST = [int(ch) for ch in (os.environ.get("ADMIN_LIST", f"{OWNER_ID} 661054276")).split()]
OWNER_USERNAME = os.environ.get("OWNER_USERNAME", "MrPrinceSanji04")
PERMANENT_GROUP = os.environ.get("PERMANENT_GROUP", "-999549719")
GROUP_ID = [int(ch) for ch in (os.environ.get("GROUP_ID", f"{PERMANENT_GROUP}")).split()]
UPDATES_CHANNEL = str(os.environ.get("UPDATES_CHANNEL", None))
LOG_CHANNEL = int(os.environ.get('LOG_CHANNEL', -1001975074655))
name = str(os.environ.get('name', 'Bypass'))
JACK_ID='661054276'
db_url = os.environ.get("DATABASE_URL", "mongodb+srv://herukotest:herukotest@test.trmvd8p.mongodb.net/?retryWrites=true&w=majority")
#db_url = os.environ.get("DATABASE_URL", "mongodb+srv://testfiletolink:testfiletolink@file.k0gf5py.mongodb.net/?retryWrites=true&w=majority")

app = Client("my_bot",api_id=api_id, api_hash=api_hash,bot_token=bot_token)  

# db setup
m_client = MongoClient(db_url)
db = m_client['bypass12']
collection = db['users421']

if collection.find_one({"role":"admin"}):
    pass
else:
    document = {"role":"admin","value":ADMIN_LIST}
    collection.insert_one(document)

if collection.find_one({"role":"auth_chat"}):
    pass
else:
    document = {"role":"auth_chat","value":GROUP_ID}
    collection.insert_one(document)
##############################################################################################################################
START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('× ✨Jᴏɪɴ Oᴜʀ Mᴀɪɴ Cʜᴀɴɴᴇʟ✨ ×', url=f'https://t.me/MrPrinceBotz'),
        InlineKeyboardButton('× ✨sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ✨ ×', url=f'https://t.me/MrPrinceSupport'),
        ],
        [
        InlineKeyboardButton('ғᴇᴀᴛᴜʀᴇs', callback_data='shr'),
        ],
        [
        InlineKeyboardButton('Aʙᴏᴜᴛ', callback_data='about'),
        InlineKeyboardButton('Cʟᴏsᴇ', callback_data='close')
        ]]
    )
# HELP_BUTTONS = InlineKeyboardMarkup(
#         [[
#         InlineKeyboardButton('Hᴏᴍᴇ', callback_data='home'),
#         InlineKeyboardButton('Aʙᴏᴜᴛ', callback_data='about'),
#         InlineKeyboardButton('Cʟᴏsᴇ', callback_data='close')
#         ]]
#     )
ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Hᴏᴍᴇ', callback_data='home'),
        InlineKeyboardButton('Cʟᴏsᴇ', callback_data='close')
        ]]
    )

@app.on_callback_query()
async def cb_data(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS
        )
    elif update.data == "shr":
        await update.message.edit_text(
            text=SHORT_TEXT,
            disable_web_page_preview=True,
            reply_markup=ABOUT_BUTTONS
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT,
            disable_web_page_preview=True,
            reply_markup=ABOUT_BUTTONS
        )

    else:
        await update.message.delete()
        

# handle ineex
def handleIndex(ele,message,msg):
    result = bypasser.scrapeIndex(ele)
    try: app.delete_messages(message.chat.id, msg.id)
    except: pass
    for page in result: app.send_message(message.chat.id, page, reply_to_message_id=message.id, disable_web_page_preview=True)

def convert_time(seconds):
    mseconds = seconds * 1000
    periods = [('d', 86400000), ('h', 3600000), ('m', 60000), ('s', 1000), ('ms', 1)]
    result = ''
    for period_name, period_seconds in periods:
        if mseconds >= period_seconds:
            period_value, mseconds = divmod(mseconds, period_seconds)
            result += f'{int(period_value)}{period_name}'
    if result == '':
        return '0ms'
    return result

def is_share_link(url):
    return bool(re.search(r'pixeldrain\.com|gofile\.io|toonshub\.xyz|toonshub\.link|www\.toonshub\.link|www\.toonshub\.xyz|toonworld4all\.me|www\.instagram|youtu|www\.youtu|www\.youtube|indexlink|d\.terabox|mega\.nz|t\.me|telegram|workers\.dev', url))
# loop thread
def loopthread(message):


    urls = []
    for ele in message.text.split():
        if "http://" in ele or "https://" in ele:
            urls.append(ele)
    if len(urls) == 0: return
    if bypasser.ispresent(ddllist,urls[0]):
        msg = app.send_message(message.chat.id, "⚡ __generating...__", reply_to_message_id=message.id)
    else:
        if urls[0] in "https://olamovies" or urls[0] in "https://psa.wf/":
            msg = app.send_message(message.chat.id, "🔎 __this might take some time...__", reply_to_message_id=message.id)
        else:
            msg = app.send_message(message.chat.id, f"🔎 __bypassing...__ {urls[0]}", reply_to_message_id=message.id)
    
    link = ""
    fails=''
    print(f'urls :{urls}')
    start=time()
    for ele in urls:
        while True:
            temp=f'┏ <b>sᴏᴜʀᴄᴇ ʟɪɴᴋ  :</b> {ele} \n┗ <b>ʙʏᴘᴀss ʟɪɴᴋ  :</b> '
            if re.search(r"https?:\/\/(?:[\w.-]+)?\.\w+\/\d+:", ele):
                handleIndex(ele,message,msg)
                return
            elif bypasser.ispresent(ddllist,ele):
                print('endered dll')
                try: tem = asyncio.run(ddl.direct_link_generator(ele))
                except Exception as e: tem = "**Error**: " + str(e)
            else:
                print('entered bypass')
                try: tem = asyncio.run(bypasser.shortners(ele))
                except Exception as e: tem = "**Error**: " + str(e)
            print("bypassed:",tem)
            temp+=tem
            link = link + temp + "\n\n"
            if is_share_link(tem) or 'Not in Supported Sites' in tem or 'https://' not in tem:
                break
            ele=tem
        link = link +"━━━━━━━━━━━❅━━━━━━━━━━━\n\n"
    end=time()
    timetaken=convert_time(end-start)
    print(timetaken)
    reqstr = app.get_users(message.from_user.id)
    v=f'Rᴇᴏ̨ᴜᴇsᴛᴇᴅ Bʏ: {reqstr.mention}\nᴛᴏᴛᴀʟ ʟɪɴᴋs: {len(urls)}\nᴛɪᴍᴇ ᴛᴀᴋᴇɴ: <code>{timetaken}</code>'
    try:
        app.edit_message_text(message.chat.id, msg.id,f'<b>❅━━━「 <a href="https://t.me/+hkU5gzW29BMzNmZl">MʀPʀɪɴᴄᴇ Bᴏᴛᴢ</a> 」━━━❅</b>\n\n{link}\n<b>{v}\n🤩 Pᴏᴡᴇʀᴇᴅ ʙʏ @MrPrinceBotz</b>', disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton(" Uᴘᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ ✴", url=f"https://t.me/+hkU5gzW29BMzNmZl")]]
                    )
            )
        app.send_message(chat_id=LOG_CHANNEL, text=f"Log of {message.chat.title}:\n\nName : {reqstr.mention}\n\nID : {message.from_user.id}\n\nBypassed Links: {link}\n\n{fails}", disable_web_page_preview=True)
    except:
        app.send_message(message.chat.id, "Failed to Bypass")

@app.on_message(filters.command(["search"]))
def send_start(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    msg=message.text
    if '@MrPrince_Link_Bypass_bot' in msg:
        msg=msg.split('/search@MrPrince_Link_Bypass_bot ')[-1]
    else:
        msg=msg.split('/search ')[-1]
    app.send_message(message.chat.id,scrape(msg),disable_web_page_preview=True)
@app.on_message(filters.command('restart'))
async def restart(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    print('restarting')
    restart_message = await message.reply('<i>Restarting...</i>')
    await (await create_subprocess_exec('python3', 'update.py')).wait()
    await cmd_exec('rm rm -rf my_bot.session  __pycache__/',shell=True)
    execl(executable, executable,"main.py")


async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


@app.on_message(filters.command('eval', prefixes='!'))
#@app.on_message(filters.command(["eval"]))
async def send_start(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
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

async def cmd_exec(cmd, shell=False):
    if shell:
        proc = await create_subprocess_shell(cmd, stdout=PIPE, stderr=PIPE)
    else:
        proc = await create_subprocess_exec(*cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = await proc.communicate()
    stdout = stdout.decode().strip()
    stderr = stderr.decode().strip()
    return stdout, stderr, proc.returncode

@app.on_message(filters.command('sh', prefixes='!'))
async def shell(_, message):
    cmd = message.text.split(maxsplit=1)
    if len(cmd) == 1:
        await app.send_message(message.chat.id, 'No command to execute was given.')
        return
    cmd = cmd[1]
    # Check if it's an environment variable setting command
    if cmd.startswith('export '):
        parts = cmd.split(' ', 1)
        if len(parts) == 2:
            var, value = parts[1].split('=', 1)
            os.environ[var] = value
            await app.send_message(message.chat.id, f"Set environment variable {var} to {value}")
        else:
            await app.send_message(message.chat.id, 'Invalid command to set environment variable.')
    else:
        stdout, stderr, _ = await cmd_exec(cmd, shell=True)
        reply = ''
        if len(stdout) != 0:
            reply += f"*Stdout*\n{stdout}\n"
            #LOGGER.info(f"Shell - {cmd} - {stdout}")
            print(f"Shell - {cmd} - {stdout}")
        if len(stderr) != 0:
            reply += f"*Stderr*\n{stderr}"
            #LOGGER.error(f"Shell - {cmd} - {stderr}")
            print(f"Shell - {cmd} - {stderr}")
        if len(reply) > 3000:
            with BytesIO(str.encode(reply)) as out_file:
                out_file.name = "shell_output.txt"
                await app.send_document(message.chat.id, out_file)
        elif len(reply) != 0:
            await app.send_message(message.chat.id, reply)
        else:
            await app.send_message(message.chat.id, 'No Reply')


# start command
@app.on_message(filters.command(["start"]))
async def send_start(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    result = collection.find_one({"role":"auth_chat"})
    GROUP_ID = result["value"]
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        await client.send_message(
            LOG_CHANNEL,
            f"**Nᴇᴡ Usᴇʀ Jᴏɪɴᴇᴅ:** \n\n__Mʏ Nᴇᴡ Fʀɪᴇɴᴅ__ [{message.from_user.first_name}](tg://user?id={message.from_user.id}) __Sᴛᴀʀᴛᴇᴅ Yᴏᴜʀ Bᴏᴛ !!__"
        )
    if str(message.chat.id).startswith("-100") and message.chat.id not in GROUP_ID:
        return
    elif message.chat.id not in GROUP_ID:
        if UPDATES_CHANNEL != "None":
            try:
                user = await app.get_chat_member(UPDATES_CHANNEL, message.chat.id)
                if user.status == enums.ChatMemberStatus.BANNED:
                    await app.send_message(
                        chat_id=message.chat.id,
                        text=f"__Sorry, you are banned. Contact My [ Owner ](https://telegram.me/{OWNER_USERNAME})__",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                 await app.send_message(
                    chat_id=message.chat.id,
                    text="<i>🔐 Join Channel To Use Me 🔐</i>",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🔓 Join Now 🔓", url=f"https://t.me/{UPDATES_CHANNEL}")
                            ]
                        ]
                    ),

                )
                 return
            except Exception:
                await app.send_message(
                    chat_id=message.chat.id,
                    text=f"<i>Something went wrong</i> <b> <a href='https://telegram.me/{OWNER_USERNAME}'>CLICK HERE FOR SUPPORT </a></b>",

                    disable_web_page_preview=True)
                return
    await message.reply_photo(
        photo='https://telegra.ph/file/84831ad030f1f607b2232.png',
        caption=START_TEXT.format(message.from_user.mention),
        reply_markup=START_BUTTONS,
        parse_mode=enums.ParseMode.HTML
    )

# help command
@app.on_message(filters.command(["help"]))
async def send_help(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    result = collection.find_one({"role":"auth_chat"})
    GROUP_ID = result["value"]
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        await client.send_message(
            LOG_CHANNEL,
            f"**Nᴇᴡ Usᴇʀ Jᴏɪɴᴇᴅ:** \n\n__Mʏ Nᴇᴡ Fʀɪᴇɴᴅ__ [{message.from_user.first_name}](tg://user?id={message.from_user.id}) __Sᴛᴀʀᴛᴇᴅ Yᴏᴜʀ Bᴏᴛ !!__"
        )
    if str(message.chat.id).startswith("-100") and message.chat.id not in GROUP_ID:
        return
    elif message.chat.id not in GROUP_ID:
        if UPDATES_CHANNEL != "None":
            try:
                user = await app.get_chat_member(UPDATES_CHANNEL, message.chat.id)
                if user.status == enums.ChatMemberStatus.BANNED:
                    await app.send_message(
                        chat_id=message.chat.id,
                        text=f"__Sorry, you are banned. Contact My [ Owner ](https://telegram.me/{OWNER_USERNAME})__",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                 await app.send_message(
                    chat_id=message.chat.id,
                    text="<i>🔐 Join Channel To Use Me 🔐</i>",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🔓 Join Now 🔓", url=f"https://t.me/{UPDATES_CHANNEL}")
                            ]
                        ]
                    ),

                )
                 return
            except Exception:
                await app.send_message(
                    chat_id=message.chat.id,
                    text=f"<i>Something went wrong</i> <b> <a href='https://telegram.me/{OWNER_USERNAME}'>CLICK HERE FOR SUPPORT </a></b>",

                    disable_web_page_preview=True)
                return
    await app.send_message(message.chat.id, HELP_TEXT, reply_to_message_id=message.id, disable_web_page_preview=True)

@app.on_message(filters.command(["authorize"]))
async def send_help(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    
    result = collection.find_one({"role":"admin"})
    ADMIN_LIST = result["value"]
    result = collection.find_one({"role":"auth_chat"})
    GROUP_ID = result["value"]
    if message.chat.id in ADMIN_LIST or message.from_user.id in ADMIN_LIST :
        try :
            msg = int(message.text.split()[-1])
        except ValueError:
            await app.send_message(message.chat.id, f"Example\n<code>/authorize -100</code>", reply_to_message_id=message.id, disable_web_page_preview=True)
            return
        if msg in GROUP_ID:
            await app.send_message(message.chat.id, f"Already Added", reply_to_message_id=message.id, disable_web_page_preview=True)
        else :
            GROUP_ID.append(msg)
            collection.update_one({"role":"auth_chat"}, {"$set": {"value":GROUP_ID}}, upsert=True)
            await app.send_message(message.chat.id, f"Authorized Sucessfully!", reply_to_message_id=message.id, disable_web_page_preview=True)
    else:
        await app.send_message(message.chat.id, f"This Command Is Only For Admins", reply_to_message_id=message.id, disable_web_page_preview=True)

@app.on_message(filters.command("unauthorize"))
async def send_help(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    result = collection.find_one({"role":"admin"})

    ADMIN_LIST = result["value"]
    result = collection.find_one({"role":"auth_chat"})
    GROUP_ID = result["value"]
    if message.chat.id in ADMIN_LIST or message.from_user.id in ADMIN_LIST :
        try :
            msg = int(message.text.split()[-1])
        except ValueError:
            await app.send_message(message.chat.id, f"Example\n<code>/unauthorize -100</code>", reply_to_message_id=message.id, disable_web_page_preview=True)
            return
        if msg not in GROUP_ID:
            await app.send_message(message.chat.id, f"Already Removed", reply_to_message_id=message.id, disable_web_page_preview=True)
        else :
            if msg == int(PERMANENT_GROUP) :
                await app.send_message(message.chat.id, f"Even Owner Can't Remove This {msg} Chat 😂😂", reply_to_message_id=message.id, disable_web_page_preview=True)
                return
            GROUP_ID.remove(msg)
            collection.update_one({"role":"auth_chat"}, {"$set": {"value":GROUP_ID}}, upsert=True)
            await app.send_message(message.chat.id, f"Unauthorized!", reply_to_message_id=message.id, disable_web_page_preview=True)
    else:
        await app.send_message(message.chat.id, f"This Command Is Only For Admins", reply_to_message_id=message.id, disable_web_page_preview=True)

@app.on_message(filters.command(["addsudo"]))
async def send_help(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    result = collection.find_one({"role":"admin"})

    ADMIN_LIST = result["value"]
    if message.chat.id == int(OWNER_ID) or message.from_user.id == int(OWNER_ID) :
        try :
            msg = int(message.text.split()[-1])
        except ValueError:
            await app.send_message(message.chat.id, f"Example\n<code>/addsudo 123</code>", reply_to_message_id=message.id, disable_web_page_preview=True)
            return
        if msg in ADMIN_LIST:
            await app.send_message(message.chat.id, f"Already Admin", reply_to_message_id=message.id, disable_web_page_preview=True)
        else :
            ADMIN_LIST.append(msg)
            collection.update_one({"role":"admin"}, {"$set": {"value":ADMIN_LIST}}, upsert=True)
            await app.send_message(message.chat.id, f"Promoted As Admin", reply_to_message_id=message.id, disable_web_page_preview=True)
    else:
        await app.send_message(message.chat.id, f"This Command Is Only For Owner", reply_to_message_id=message.id, disable_web_page_preview=True)
        
@app.on_message(filters.command(["remsudo"]))
async def send_help(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    result = collection.find_one({"role":"admin"})

    ADMIN_LIST = result["value"]
    if message.chat.id == int(OWNER_ID) or message.from_user.id == int(OWNER_ID) :
        try :
            msg = int(message.text.split()[-1])
        except ValueError:
            await app.send_message(message.chat.id, f"Example\n<code>/remsudo 123</code>", reply_to_message_id=message.id, disable_web_page_preview=True)
            return
        if msg not in ADMIN_LIST:
            await app.send_message(message.chat.id, f"Already Demoted!", reply_to_message_id=message.id, disable_web_page_preview=True)
        else :
            if msg == int(message.from_user.id) :
                await app.send_message(message.chat.id, f"You Can't Remove Yourself 😂😂", reply_to_message_id=message.id, disable_web_page_preview=True)
                return
            elif msg == int(OWNER_ID) :
                await app.send_message(message.chat.id, f"Even Owner Can't Remove Himself 😂😂", reply_to_message_id=message.id, disable_web_page_preview=True)
                return
            ADMIN_LIST.remove(msg)
            collection.update_one({"role":"admin"}, {"$set": {"value":ADMIN_LIST}}, upsert=True)
            await app.send_message(message.chat.id, f"Demoted!", reply_to_message_id=message.id, disable_web_page_preview=True)
    else:
        await app.send_message(message.chat.id, f"This Command Is Only For Owner", reply_to_message_id=message.id, disable_web_page_preview=True)
        
@app.on_message(filters.command(["users"]))
async def send_help(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    result = collection.find_one({"role":"admin"})

    ADMIN_LIST = result["value"]
    result = collection.find_one({"role":"auth_chat"})
    GROUP_ID = result["value"]
    if message.chat.id in ADMIN_LIST or message.from_user.id in ADMIN_LIST :
        lol = "List Of Authorized Chats\n\n"
        for i in GROUP_ID:
            lol += "<code>" + str(i) + "</code>\n"
        lol += "\nList Of Admin ID's\n\n"
        for i in ADMIN_LIST:
            lol += "<code>" + str(i) + "</code>\n"
        await app.send_message(message.chat.id, lol, reply_to_message_id=message.id, disable_web_page_preview=True)
    else :
        await app.send_message(message.chat.id, f"This Command Is Only For Admins", reply_to_message_id=message.id, disable_web_page_preview=True)

###############
db = Database(db_url, name)
ADMINS='661054276'
@app.on_message(filters.command(["broadcast123"]))
async def send_help(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    print('hi')
    db = Database(db_url, name)
    users = await db.get_all_users()
    b_msg = message.reply_to_message
    sts = await message.reply_text(
        text='Broadcasting your messages...'
    )
    start_time = time()
    total_users = await db.total_users_count()
    done = 0
    blocked = 0
    deleted = 0
    failed =0

    success = 0
    async for user in users:
        pti, sh = await broadcast_messages(int(user['id']), b_msg)
        if pti:
            success += 1
        elif pti == False:
            if sh == "Blocked":
                blocked+=1
            elif sh == "Deleted":
                deleted += 1
            elif sh == "Error":
                failed += 1
        done += 1
        await asyncio.sleep(2)
        if not done % 20:
            await sts.edit(f"Broadcast in progress:\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nBlocked: {blocked}\nDeleted: {deleted}")    
    time_taken = timedelta(seconds=int(time()-start_time))
    await sts.edit(f"Broadcast Completed:\nCompleted in {time_taken} seconds.\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nBlocked: {blocked}\nDeleted: {deleted}")

############

# links
@app.on_message(filters.text)
async def receive(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    result = collection.find_one({"role":"auth_chat"})
    GROUP_ID = result["value"]
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        await client.send_message(
            LOG_CHANNEL,
            f"**Nᴇᴡ Usᴇʀ Jᴏɪɴᴇᴅ:** \n\n__Mʏ Nᴇᴡ Fʀɪᴇɴᴅ__ [{message.from_user.first_name}](tg://user?id={message.from_user.id}) __Sᴛᴀʀᴛᴇᴅ Yᴏᴜʀ Bᴏᴛ !!__"
        )
    if str(message.chat.id).startswith("-100") and message.chat.id not in GROUP_ID:
        return
    elif message.chat.id not in GROUP_ID:
        if UPDATES_CHANNEL != "None":
            try:
                user = await app.get_chat_member(UPDATES_CHANNEL, message.chat.id)
                if user.status == enums.ChatMemberStatus.BANNED:
                    await app.send_message(
                        chat_id=message.chat.id,
                        text=f"__Sorry, you are banned. Contact My [ Owner ](https://telegram.me/{OWNER_USERNAME})__",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                 await app.send_message(
                    chat_id=message.chat.id,
                    text="<i>🔐 Join Channel To Use Me 🔐</i>",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🔓 Join Now 🔓", url=f"https://t.me/{UPDATES_CHANNEL}")
                            ]
                        ]
                    ),

                )
                 return
            except Exception:
                await app.send_message(
                    chat_id=message.chat.id,
                    text=f"<i>Something went wrong</i> <b> <a href='https://telegram.me/{OWNER_USERNAME}'>CLICK HERE FOR SUPPORT </a></b>",

                    disable_web_page_preview=True)
                return
    bypass = threading.Thread(target=lambda:loopthread(message),daemon=True)
    bypass.start()



# doc thread
def docthread(message):
    if message.document.file_name.endswith("dlc"):
        msg = app.send_message(message.chat.id, "🔎 __bypassing...__", reply_to_message_id=message.id)
        print("sent DLC file")
        sess = requests.session()
        file = app.download_media(message)
        dlccont = open(file,"r").read()
        link = bypasser.getlinks(dlccont,sess)
        app.edit_message_text(message.chat.id, msg.id, f'__{link}__')
        os.remove(file)

@app.on_message(filters.document)
async def docfile(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    result = collection.find_one({"role":"auth_chat"})
    GROUP_ID = result["value"]
    if str(message.chat.id).startswith("-100") and message.chat.id not in GROUP_ID:
        return
    elif message.chat.id not in GROUP_ID:
        if UPDATES_CHANNEL != "None":
            try:
                user = await app.get_chat_member(UPDATES_CHANNEL, message.chat.id)
                if user.status == enums.ChatMemberStatus.BANNED:
                    await app.send_message(
                        chat_id=message.chat.id,
                        text=f"__Sorry, you are banned. Contact My [ Owner ](https://telegram.me/{OWNER_USERNAME})__",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                 await app.send_message(
                    chat_id=message.chat.id,
                    text="<i>🔐 Join Channel To Use Me 🔐</i>",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🔓 Join Now 🔓", url=f"https://t.me/{UPDATES_CHANNEL}")
                            ]
                        ]
                    ),

                )
                 return
            except Exception:
                await app.send_message(
                    chat_id=message.chat.id,
                    text=f"<i>Something went wrong</i> <b> <a href='https://telegram.me/{OWNER_USERNAME}'>CLICK HERE FOR SUPPORT </a></b>",

                    disable_web_page_preview=True)
                return
    if message.document.file_name.endswith(".dlc"):
        bypass = threading.Thread(target=lambda:docthread(message),daemon=True)
        bypass.start()



# server loop
print("Bot Starting")
app.run()
