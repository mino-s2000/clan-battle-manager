import discord
import io
import os
import requests

from datetime import datetime
from discord.ext import commands
from google.cloud import vision
from google.cloud.vision import types
from google.oauth2 import service_account

IMG_CHANNEL_ID = 669477531061190666

class SummarizeDamageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def download_img(self, uri, filename):
        r = requests.get(uri, stream=True)
        if r.status_code == 200:
            with open(f'img/{filename}', 'wb') as f:
                f.write(r.content)

    def remove_img(self, filename):
        os.remove(f'img/{filename}')

    def detect_text(self, filename):
        credentials = service_account.Credentials.from_service_account_file('discordbotprj-c32cb217f63c.json')
        client = vision.ImageAnnotatorClient(credentials=credentials)

        with io.open(f'img/{filename}', 'rb') as image_file:
            content = image_file.read()

        image = vision.types.Image(content=content)
        response = client.text_detection(image=image)
        texts = response.text_annotations
        print('Texts:')
        for text in texts:
            print('\n"{}"'.format(text.description))
        return texts[0].description

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id != IMG_CHANNEL_ID:
            return
        if message.attachments == []:
            return

        for img in message.attachments:
            self.download_img(img.url, img.filename)
            text = self.detect_text(img.filename)
            await message.channel.send(content=text)
            await message.add_reaction('\U0001F44D')
            self.remove_img(img.filename)

def setup(bot):
    bot.add_cog(SummarizeDamageCog(bot))
