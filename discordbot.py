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

def init_config():
    pass

def show_config():
    pass

def set_config(content):
    pass

def get_config(content):
    pass

client.run('token')
