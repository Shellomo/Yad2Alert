import os
from telethon import TelegramClient
# from settings import *
from settings_temp import *  # ToDo remove this
import requests
import shutil


def get_image(url):
    file_name = url.split('/')[-1]
    response = requests.get(url, stream=True)
    with open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
    return file_name


class Publisher:
    def __init__(self, telegram_channel):
        try:
            self.bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_API)
        except Exception as e:
            print(e)

        self.telegram_channel = telegram_channel

    async def send_text_to_telegram(self, user, text):
        await self.bot.send_message(user, text)

    async def send_image_to_telegram(self, user, file, caption=None):
        await self.bot.send_file(user, file, caption=caption)

    def publish(self, ad, new_price=False):
        try:
            main_image = None
            images = []

            label = ad['category_name'] + ' ב' + ad['city']
            if not new_price:
                captions = (
                        '💥מודעה חדשה💥' + '\n' +
                        '**' + label + '**' + '\n' +
                        'תיאור: ' + ad['title'] + '\n' +
                        '** מחיר: ' + ad['price'] + '**\n' +
                        'איש קשר: ' + ad['contact_name'] + '\n' +
                        'לפרטים: ' + 'https://www.yad2.co.il/item/' + ad['id'] + '\n'
                )
            else:
                captions = (
                        '\n⬇️💰ירידת מחיר💰️️⬇️' + '\n' +
                        '**' + label + '**' + '\n' +
                        'תיאור: ' + ad['title'] + '\n' +
                        '** מחיר: ' + ad['price'] + '**\n' +
                        'איש קשר: ' + ad['contact_name'] + '\n' +
                        'לפרטים: ' + 'https://www.yad2.co.il/item/' + ad['id'] + '\n'
                )

            if ad['img_url']:
                main_image = get_image(ad['img_url'])

            if ad['all_item_images']:
                for image in ad['all_item_images']:
                    images.append(get_image(image))

            if not main_image and not images:
                self.bot.loop.run_until_complete(self.send_text_to_telegram(self.telegram_channel, captions))

            elif main_image and not images:
                self.bot.loop.run_until_complete(
                    self.send_image_to_telegram(self.telegram_channel, main_image, caption=captions))
                os.remove(main_image)

            elif main_image and images:
                images.insert(0, main_image)
                self.bot.loop.run_until_complete(
                    self.send_image_to_telegram(self.telegram_channel, images, caption=captions))
                for image in images:
                    os.remove(image)

        except Exception as e:
            print(e)
            print('An error occurred when trying to send the message.\n'
                  'make sure the bot has permission to send messages to the channel.')
            self.close()
            return False

        finally:
            for image in os.listdir():
                if image.endswith('.jpg') and image.startswith('y2'):
                    os.remove(image)

        return True

    def close(self):
        self.bot.disconnect()
