import discord

from discord.ext import tasks, commands

DISCORD_TOKEN = ''
INITIAL_EXTENSIONS = [
    'cogs.attacking-count'
]

class MainBot(commands.Bot):
    def __init__(self, command_prefix, help_command, intents):
        super().__init__(command_prefix, intents=intents)
        for cog in INITIAL_EXTENSIONS:
            self.load_extension(cog)

    async def on_ready(self):
        print('-----')
        print(self.user.name)
        print(self.user.id)
        print('-----')

if __name__ == '__main__':
    bot = MainBot(command_prefix='/', help_command=None, intents=discord.Intents.all())
    bot.run(DISCORD_TOKEN)
