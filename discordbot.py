import os
import discord
import asyncio
from datetime import datetime
from discord.ext import tasks

GUILD_ID = 542316532655456276
CHANNEL_ID = 644131810829139978
MEMBER_ROLE_ID = 631489002704207872
token = ''
#emoji_one = '\U00000031\U0000FE0F\U000020E3'
#emoji_two = '\U00000032\U0000FE0F\U000020E3'
#emoji_three = '\U00000033\U0000FE0F\U000020E3'
emoji_one = '\U0001F95A'
emoji_two = '\U0001F423'
emoji_three = '\U0001F425'
embed_color = 0xff69b4

client = discord.Client()

datetime_list = [
    '2019-11-20 05:00',
    '2019-11-21 05:00',
    '2019-11-22 05:00',
    '2019-11-23 05:00'
]

@client.event
async def on_ready():
    print('ログインしました')

async def print_daily_attacking_count(idxnum, now, utcnow):
    guild = client.get_guild(GUILD_ID)
    channel = client.get_channel(CHANNEL_ID)
    all_members = client.get_all_members()
    member_role = guild.get_role(MEMBER_ROLE_ID)
    target_members = [member for member in all_members if member_role in member.roles]
    today = now.strftime('%m/%d')
    title = today
    if idxnum == len(datetime_list) - 1:
        title += " (最終日)"
    else:
        title += f" ({idxnum + 1}日目)"
    embed = discord.Embed(
        title = title,
        description = '\n'.join([member.name for member in target_members]),
        color = embed_color,
        timestamp = utcnow
    )
    embed.set_footer(text = f"Latest Edit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, User: Bot")
    msg_obj = await channel.send(embed = embed)
    await msg_obj.add_reaction(emoji_one)
    await msg_obj.add_reaction(emoji_two)
    await msg_obj.add_reaction(emoji_three)

@client.event
async def on_reaction_add(reaction, user):
    if reaction.message.channel.id != CHANNEL_ID:
        return
    if reaction.emoji not in [emoji_one, emoji_two, emoji_three]:
        return
    msg_embed = reaction.message.embeds[0]
    new_embed = discord.Embed(
        title = msg_embed.title,
        description = '\n'.join([f'{m} {reaction.emoji}' if user.name in m else m for m in msg_embed.description.split('\n')]),
        color = embed_color,
        timestamp = msg_embed.timestamp
    )
    new_embed.set_footer(text = f"Latest Edit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, User: {user.name}")
    print(f'{new_embed.title} {user.name}: {reaction.emoji} - add')
    await reaction.message.edit(embed = new_embed)

@client.event
async def on_reaction_remove(reaction, user):
    if reaction.message.channel.id != CHANNEL_ID:
        return
    if reaction.emoji not in [emoji_one, emoji_two, emoji_three]:
        return
    msg_embed = reaction.message.embeds[0]
    new_embed = discord.Embed(
        title = msg_embed.title,
        description = '\n'.join([f'{m.replace(f" {reaction.emoji}", "")}' if user.name in m else m for m in msg_embed.description.split('\n')]),
        color = embed_color,
        timestamp = msg_embed.timestamp
    )
    new_embed.set_footer(text = f"Latest Edit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, User: {user.name}")
    print(f'{new_embed.title} {user.name}: {reaction.emoji} - remove')
    await reaction.message.edit(embed = new_embed)

@tasks.loop(minutes = 1)
async def check_dateline():
    now = datetime.now()
    utc_now = datetime.utcnow()
    now_strf = now.strftime('%Y-%m-%d %H:%M')
    if now_strf in datetime_list:
        i = datetime_list.index(now_strf)
        print(now_strf)
        await print_daily_attacking_count(i, now, utc_now)
        await asyncio.sleep(30)

check_dateline.start()

client.run(token)
