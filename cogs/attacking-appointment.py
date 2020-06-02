import configparser
import discord
import asyncio

from datetime import datetime
from discord.ext import commands, tasks

SECTION = 'dev'
#SECTION = 'prod'

EMOJI_APPO_ONE = '\U0001F95A'
EMOJI_APPO_TWO = '\U0001F423'
EMOJI_APPO_THREE = '\U0001F425'
EMOJI_APPO_RETAIN = '\U0000267B'
EMOJI_NOTIFER = '\U0001F514'

class AttackingAppointmentCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_path = 'config.ini'
        self.config = configparser.ConfigParser()
        self.config.read(self.config_path, encoding='UTF-8')
        self.config_section = self.config[SECTION]
        self.guild_id = self.config_section.getint('GuildID')
        self.channel_id = self.config_section.getint('AppointmentChannelID')
        self.embed_color = eval(self.config_section.get('AppointmentEmbedColor'))
        self.datetime_list = eval(self.config_section.get('DatetimeList'))
        self.boss_list = eval(self.config_section.get('BossList'))
        self.check_dateline.start()

    def cog_unload(self):
        self.check_dateline.cancel()

    @tasks.loop(minutes = 1, count = 10)
    async def check_dateline(self):
        now = datetime.now()
        utc_now = datetime.utcnow()
        now_strf = now.strftime('%Y-%m-%d %H:%M')
        if now_strf == self.datetime_list[0]:
            await self.print_appointment(1, utc_now)
            await asyncio.sleep(30)
            await self.print_appointment(2, utc_now)
            await asyncio.sleep(30)

    @check_dateline.before_loop
    async def before_check_dateline(self):
        print('waiting...')
        await self.bot.wait_until_ready()

    async def print_appointment(self, count, utcnow):
        guild = self.bot.get_guild(self.guild_id)
        channel = self.bot.get_channel(self.channel_id)
        level = 0
        hp = []
        if count <= 3:
            level = 1
            hp = [600, 800, 1000, 1200, 1500]
        elif count > 3 and count <= 10:
            level = 2
            hp = [600, 800, 1000, 1200, 1500]
        elif count > 10 and count <= 34:
            level = 3
            hp = [700, 900, 1300, 1500, 2000]
        else:
            level = 4
            hp = [1500, 1600, 1800, 1900, 2000]
        title = f'{count}周目 ({level}段階目)'
        description = f'{EMOJI_APPO_ONE} : 1凸目\n{EMOJI_APPO_TWO} : 2凸目\n{EMOJI_APPO_THREE} : 3凸目\n{EMOJI_APPO_RETAIN} : 持ち越し'
        embed = discord.Embed(title = title, description = description, color = self.embed_color, timestamp = utcnow)
        embed.add_field(name = f'- - - - -\n{self.boss_list[0]} {hp[0]}', value = 'Nobody', inline = False)
        embed.add_field(name = f'- - - - -\n{self.boss_list[1]} {hp[1]}', value = 'Nobody', inline = False)
        embed.add_field(name = f'- - - - -\n{self.boss_list[2]} {hp[2]}', value = 'Nobody', inline = False)
        embed.add_field(name = f'- - - - -\n{self.boss_list[3]} {hp[3]}', value = 'Nobody', inline = False)
        embed.add_field(name = f'- - - - -\n{self.boss_list[4]} {hp[4]}', value = 'Nobody', inline = False)
        embed.set_footer(text = f"Latest Edit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, User: Bot")
        msg_obj = await channel.send(embed = embed)
        for boss in self.boss_list:
            msg = await channel.send(f'- - - - - {boss} - - - - -')
            await msg.add_reaction(EMOJI_APPO_ONE)
            await msg.add_reaction(EMOJI_APPO_TWO)
            await msg.add_reaction(EMOJI_APPO_THREE)
            await msg.add_reaction(EMOJI_APPO_RETAIN)
            await msg.add_reaction(EMOJI_NOTIFER)

def setup(bot):
    bot.add_cog(AttackingAppointmentCog(bot))
