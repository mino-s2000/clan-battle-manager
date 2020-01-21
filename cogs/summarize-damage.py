import configparser
import discord
import re

from datetime import datetime
from discord.ext import commands, tasks

SECTION = 'dev'
#SECTION = 'prod'

class SummarizeDamageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_path = 'config.ini'
        self.config = configparser.ConfigParser()
        self.config.read(self.config_path, encoding='UTF-8')
        self.config_section = self.config[SECTION]

    def set_config(self, option, value):
        self.config_section.set(option, value)
        with open(self.config_path, 'w', encoding='UTF-8') as f:
            self.config.write(f)

    def reload_config(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.config_path, encoding='UTF-8')
        self.config_section = self.config[SECTION]

    @commands.group()
    async def damage(self, ctx):
        if ctx.invoked_subcommand is None:
            return

    @damage.command()
    async def setdate(self, ctx, date: str):
        pattern = '^\d{4}-\d{2}-\d{2}$'
        repatter = re.compile(pattern)
        result = repatter.match(date)
        if result:
            self.set_config('TargetDate', date)
            self.reload_config()

def setup(bot):
    bot.add_cog(SummarizeDamageCog(bot))
