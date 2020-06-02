import configparser
import discord
import asyncio

from datetime import datetime
from discord.ext import commands, tasks

SECTION = 'dev'
#SECTION = 'prod'

# ConfigParserから読み込むと絵文字にならなかったので要調査
EMOJI_ONE = '\U0001F95A'
EMOJI_TWO = '\U0001F423'
EMOJI_THREE = '\U0001F425'

class AttackingCountCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_path = 'config.ini'
        self.config = configparser.ConfigParser()
        self.config.read(self.config_path, encoding='UTF-8')
        self.config_section = self.config[SECTION]
        self.bot_user_id = self.config_section.getint('BotUserID')
        self.guild_id = self.config_section.getint('GuildID')
        self.channel_id = self.config_section.getint('CountChannelID')
        self.member_role_id = self.config_section.getint('MemberRoleID')
        self.embed_color = eval(self.config_section.get('CountEmbedColor'))
        self.datetime_list = eval(self.config_section.get('DatetimeList'))
        self.check_dateline.start()

    def cog_unload(self):
        self.check_dateline.cancel()

    async def print_daily_attacking_count(self, idxnum, now, utcnow):
        guild = self.bot.get_guild(self.guild_id)
        channel = self.bot.get_channel(self.channel_id)
        all_members = self.bot.get_all_members()
        member_role = guild.get_role(self.member_role_id)
        target_members = [member.name for member in all_members if member_role in member.roles]
        today = now.strftime('%m/%d')
        title = today
        if idxnum == len(self.datetime_list) - 1:
            title += " (最終日)"
        else:
            title += f" ({idxnum + 1}日目)"
        description = f'凸状況をリアルタイムで把握したいので、1凸するごとにリアクションをしてください。\n1凸目が終わったら{EMOJI_ONE}を、2凸目が終わったら{EMOJI_TWO}を、3凸目が終わったら{EMOJI_THREE}を押してください。'
        embed = discord.Embed(title = title, description = description, color = self.embed_color, timestamp = utcnow)
        # スマホ版Discordだと、フィールドの区切りが分かりづらいため、セパレーター文字列を入れている
        embed.add_field(name = f'-----\n3凸{EMOJI_THREE}', value = 'Nobody', inline = False)
        embed.add_field(name = f'-----\n2凸{EMOJI_TWO}', value = 'Nobody', inline = False)
        embed.add_field(name = f'-----\n1凸{EMOJI_ONE}', value = 'Nobody', inline = False)
        embed.add_field(name = '-----\n0凸', value = '\n'.join(target_members), inline = False)
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
        if reaction.message.channel.id != self.channel_id:
            return
        if user.id == self.bot_user_id:
            return
        embed = discord.Embed()
        if reaction.emoji == EMOJI_ONE:
            embed = await self.move_username_between_field(reaction, user, 3, '-----\n0凸', 2, f'-----\n1凸{EMOJI_ONE}')
        elif reaction.emoji == EMOJI_TWO:
            embed = await self.move_username_between_field(reaction, user, 2, f'-----\n1凸{EMOJI_ONE}', 1, f'-----\n2凸{EMOJI_TWO}')
        elif reaction.emoji == EMOJI_THREE:
            embed = await self.move_username_between_field(reaction, user, 1, f'-----\n2凸{EMOJI_TWO}', 0, f'-----\n3凸{EMOJI_THREE}')
        else:
            return
        print(f'{user.name}: {reaction.emoji} - add')
        await reaction.message.edit(embed = embed)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if reaction.message.channel.id != self.channel_id:
            return
        if user.id == self.bot_user_id:
            return
        embed = discord.Embed()
        if reaction.emoji == EMOJI_THREE:
            embed = await self.move_username_between_field(reaction, user, 0, f'-----\n3凸{EMOJI_THREE}', 1, f'-----\n2凸{EMOJI_TWO}')
        elif reaction.emoji == EMOJI_TWO:
            embed = await self.move_username_between_field(reaction, user, 1, f'-----\n2凸{EMOJI_TWO}', 2, f'-----\n1凸{EMOJI_ONE}')
        elif reaction.emoji == EMOJI_ONE:
            embed = await self.move_username_between_field(reaction, user, 2, f'-----\n1凸{EMOJI_ONE}', 3, '-----\n0凸')
        else:
            return
        print(f'{user.name}: {reaction.emoji} - remove')
        await reaction.message.edit(embed = embed)

    @tasks.loop(minutes = 1)
    async def check_dateline(self):
        now = datetime.now()
        utc_now = datetime.utcnow()
        now_strf = now.strftime('%Y-%m-%d %H:%M')
        if now_strf in self.datetime_list:
            i = self.datetime_list.index(now_strf)
            print(now_strf)
            await self.print_daily_attacking_count(i, now, utc_now)
            await asyncio.sleep(30)

    @check_dateline.before_loop
    async def before_check_dateline(self):
        print('waiting...')
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(AttackingCountCog(bot))
