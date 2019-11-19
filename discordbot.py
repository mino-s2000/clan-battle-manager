import os
import discord
import asyncio
from datetime import datetime
from discord.ext import tasks

GUILD_ID = 00000
CHANNEL_ID = 00000
MEMBER_ROLE_ID = 00000
token = ''
emoji_one = '\U00000031\U0000FE0F\U000020E3'
emoji_two = '\U00000032\U0000FE0F\U000020E3'
emoji_three = '\U00000033\U0000FE0F\U000020E3'
client = discord.Client()

datetime_list = [
    '2019-11-24 05:00',
    '2019-11-25 05:00',
    '2019-11-26 05:00',
    '2019-11-27 05:00',
    '2019-11-28 05:00',
    '2019-11-29 05:00'
]

@client.event
async def on_ready():
    print('ログインしました')

async def print_daily_attacking_count(idxnum):
    guild = client.get_guild(GUILD_ID)
    channel = client.get_channel(CHANNEL_ID)
    all_members = client.get_all_members()
    member_role = guild.get_role(MEMBER_ROLE_ID)
    target_members = list(filter(lambda member: member_role in member.roles, all_members))
    msg = f"__**{datetime.now().strftime('%m/%d')}"
    if idxnum == len(datetime_list) - 1:
        msg += " (最終日)**__\n"
    else:
        msg += f" ({idxnum + 1}日目)**__\n"
    for member in target_members:
        msg += f'> `{member.name}`\n'
    msg_obj = await channel.send(msg)
    await msg_obj.add_reaction(emoji_one)
    await msg_obj.add_reaction(emoji_two)
    await msg_obj.add_reaction(emoji_three)

@client.event
async def on_reaction_add(reaction, user):
    if reaction.message.channel.id != CHANNEL_ID:
        return
    if reaction.emoji not in [emoji_one, emoji_two, emoji_three]:
        return
    msg = reaction.message
    msg_content = msg.content
    new_msg = '\n'.join([f'{m} {reaction.emoji}' if user.name in m else m for m in msg_content.split('\n')])
    print(f'{user.name}: {reaction.emoji} - add')
    await msg.edit(content = new_msg)

@client.event
async def on_reaction_remove(reaction, user):
    if reaction.message.channel.id != CHANNEL_ID:
        return
    if reaction.emoji not in [emoji_one, emoji_two, emoji_three]:
        return
    msg = reaction.message
    msg_content = msg.content
    new_msg = '\n'.join([f'{m.replace(f" {reaction.emoji}", "")}' if user.name in m else m for m in msg_content.split('\n')])
    print(f'{user.name}: {reaction.emoji} - remove')
    await msg.edit(content = new_msg)

@tasks.loop(minutes = 1)
async def check_dateline():
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    if now in datetime_list:
        i = datetime_list.index(now)
        print(now)
        await print_daily_attacking_count(i)
        await asyncio.sleep(30)

check_dateline.start()

client.run(token)
