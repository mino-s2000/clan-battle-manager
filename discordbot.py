import discord
import json
from pytz import timezone
from datetime import datetime

client = discord.Client()

@client.event
async def on_ready():
    print('Login.')

@client.event
async def on_message(message):
    cList = message.content.split(' ')
    if cList[0].startswith != '/':
        return
    if cList[0] == '/config':
        configure_bot(cList)
        return

def configure_bot(content):
    if content[1] == 'init':
        init_config()
        return
    elif content[1] == 'show':
        show_config()
        return
    elif content[1] == 'set':
        set_config(content)
        return
    elif content[1] == 'get':
        get_config(content)
        return
    else:
        return

def init_config():
    pass

def show_config():
    pass

def set_config(content):
    if content[2] == 'spreadsheets':
        set_spreadsheets(content[3])
        return
    elif content[2] == 'monsters':
        set_monsters(content[3])
        return
    elif content[2] == 'members':
        set_members(content[3])
        return
    else:
        return

def get_config(content):
    if content[2] == 'spreadsheets':
        get_spreadsheets()
        return
    elif content[2] == 'monsters':
        get_monsters()
        return
    elif content[2] == 'members':
        get_members()
        return
    else:
        return

def set_spreadsheets(uri):
    pass

def set_monsters(monsters):
    pass

def set_members(members):
    pass

def get_spreadsheets():
    pass

def get_monsters():
    pass

def get_members():
    pass

client.run('token')
