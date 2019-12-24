import discord
import asyncio

from datetime import datetime
from discord.ext import commands, tasks

BOT_USER_ID = 00000
GUILD_ID = 00000
CHANNEL_ID = 00000
MEMBER_ROLE_ID = 00000
EMOJI_ONE = '\U0001F95A'
EMOJI_TWO = '\U0001F423'
EMOJI_THREE = '\U0001F425'
EMBED_COLOR = 0xff69b4
DATETIME_LIST = [
    '2019-12-25 05:00',
    '2019-12-26 05:00',
    '2019-12-27 05:00',
    '2019-12-28 05:00',
    '2019-12-29 05:00',
    '2019-12-30 05:00'
]

class AttackingCountCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_dateline.start()

    def cog_unload(self):
        self.check_dateline.cancel()

    async def print_daily_attacking_count(self, idxnum, now, utcnow):
        guild = self.bot.get_guild(GUILD_ID)
        channel = self.bot.get_channel(CHANNEL_ID)
        all_members = self.bot.get_all_members()
        member_role = guild.get_role(MEMBER_ROLE_ID)
        target_members = [member.name for member in all_members if member_role in member.roles]
        today = now.strftime('%m/%d')
        title = today
        if idxnum == len(DATETIME_LIST) - 1:
            title += " (最終日)"
        else:
            title += f" ({idxnum + 1}日目)"
        embed = discord.Embed(title = title, color = EMBED_COLOR, timestamp = utcnow)
        embed.add_field(name = '3凸', value = 'Nobody', inline = False)
        embed.add_field(name = '2凸', value = 'Nobody', inline = False)
        embed.add_field(name = '1凸', value = 'Nobody', inline = False)
        embed.add_field(name = '0凸', value = '\n'.join(target_members), inline = False)
        embed.set_footer(text = f"Latest Edit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, User: Bot")
        msg_obj = await channel.send(embed = embed)
        await msg_obj.add_reaction(EMOJI_ONE)
        await msg_obj.add_reaction(EMOJI_TWO)
        await msg_obj.add_reaction(EMOJI_THREE)

    async def move_username_between_field(self, reaction, user, before_index, before_name, after_index, after_name):
        embed = reaction.message.embeds[0]

        before_value = embed.fields[before_index].value
        if '\n' in before_value:
            before_value = '\n'.join([value for value in before_value.split('\n') if value != user.name])
        elif before_value == user.name:
            before_value = 'Nobody'
        else:
            return

        after_value = embed.fields[after_index].value
        if after_value == 'Nobody':
            after_value = user.name
        elif '\n' in after_value:
            after_value = after_value.split('\n')
            after_value.append(user.name)
            after_value = '\n'.join(after_value)
        else:
            after_value = '\n'.join([after_value, user.name])

        embed.set_field_at(index = before_index, name = before_name, value = before_value, inline = False)
        embed.set_field_at(index = after_index, name = after_name, value = after_value, inline = False)
        embed.set_footer(text = f"Latest Edit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, User: {user.name}")
        return embed

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.message.channel.id != CHANNEL_ID:
            return
        if user.id == BOT_USER_ID:
            return
        embed = discord.Embed()
        if reaction.emoji == EMOJI_ONE:
            embed = await self.move_username_between_field(reaction, user, 3, '0凸', 2, '1凸')
        elif reaction.emoji == EMOJI_TWO:
            embed = await self.move_username_between_field(reaction, user, 2, '1凸', 1, '2凸')
        elif reaction.emoji == EMOJI_THREE:
            embed = await self.move_username_between_field(reaction, user, 1, '2凸', 0, '3凸')
        else:
            return
        print(f'{user.name}: {reaction.emoji} - add')
        await reaction.message.edit(embed = embed)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if reaction.message.channel.id != CHANNEL_ID:
            return
        if user.id == BOT_USER_ID:
            return
        embed = discord.Embed()
        if reaction.emoji == EMOJI_THREE:
            embed = await self.move_username_between_field(reaction, user, 0, '3凸', 1, '2凸')
        elif reaction.emoji == EMOJI_TWO:
            embed = await self.move_username_between_field(reaction, user, 1, '2凸', 2, '1凸')
        elif reaction.emoji == EMOJI_ONE:
            embed = await self.move_username_between_field(reaction, user, 2, '1凸', 3, '0凸')
        else:
            return
        print(f'{user.name}: {reaction.emoji} - remove')
        await reaction.message.edit(embed = embed)

    @tasks.loop(minutes = 1)
    async def check_dateline(self):
        now = datetime.now()
        utc_now = datetime.utcnow()
        now_strf = now.strftime('%Y-%m-%d %H:%M')
        if now_strf in DATETIME_LIST:
            i = DATETIME_LIST.index(now_strf)
            print(now_strf)
            await self.print_daily_attacking_count(i, now, utc_now)
            await asyncio.sleep(30)

    @check_dateline.before_loop
    async def before_check_dateline(self):
        print('waiting...')
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(AttackingCountCog(bot))
