import configparser
import discord
import re
import gspread
import json

from datetime import datetime
from discord.ext import commands, tasks
from oauth2client.service_account import ServiceAccountCredentials

SECTION = 'dev'
#SECTION = 'prod'

class ConnectSpreadSheets:
    def __init__(self, key, keyfile):
        self.key = key
        self.keyfile = keyfile

    def connect_workbook(self):
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.keyfile, scope)
        gc = gspread.authorize(credentials)
        return gc.open_by_key(self.key)

class SummarizeDamageCog(commands.Cog):
    target_date = '2020-01-25'

    def __init__(self, bot):
        self.bot = bot
        self.config_path = 'config.ini'
        self.config = configparser.ConfigParser()
        self.config.read(self.config_path, encoding='UTF-8')
        self.config_section = self.config[SECTION]
        self.spread_api_file = self.config_section.get('GSpreadApiKeyFile')
        self.sheet_key = self.config_section.get('GSpreadSheetKey')

    @commands.group(aliases=['d'])
    async def damage(self, ctx):
        if ctx.invoked_subcommand is None:
            return

    @damage.command(aliases=['set', 's'])
    async def setdate(self, ctx, date: str):
        pattern = '^\d{4}-\d{2}-\d{2}$'
        repatter = re.compile(pattern)
        result = repatter.match(date)
        if result:
            self.target_date = date
            await ctx.send(f'対象日付をセットしました。: {self.target_date}')
        else:
            await ctx.send('対象日付のフォーマットは、”yyyy-MM-dd" です。')

    @damage.command(aliases=['a'])
    async def add(self, ctx, user: str, target: str, damage: int, la = 'False'):
        values = [self.target_date, user, target, damage, bool(la)]

        workbook = ConnectSpreadSheets(self.sheet_key, self.spread_api_file).connect_workbook()
        worksheet = workbook.sheet1
        row_count = len(worksheet.get_all_values())
        cell_list = worksheet.range(row_count + 1, 1, row_count + 1, 5)
        for cell in cell_list:
            cell.value = values[cell_list.index(cell)]
        worksheet.update_cells(cell_list)
        await ctx.send('データを追加しました。')

def setup(bot):
    bot.add_cog(SummarizeDamageCog(bot))
