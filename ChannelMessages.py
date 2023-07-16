import configparser
import json
import asyncio
import os
from datetime import date, datetime, timezone

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (
    PeerChannel
)

# some functions to parse json date
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        if isinstance(o, bytes):
            return list(o)

        return json.JSONEncoder.default(self, o)

# Reading Configs
config = configparser.ConfigParser()
config.read("config.ini")

# Setting configuration values
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']

api_hash = str(api_hash)

phone = config['Telegram']['phone']
username = config['Telegram']['username']

# Create the client and connect
client = TelegramClient(username, api_id, api_hash)

async def main(phone):
    await client.start()
    print("Client Created")
    # Ensure you're authorized
    if await client.is_user_authorized() == False:
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))

    me = await client.get_me()

    user_input_channel_list = ['https://t.me/incident22', 'https://t.me/vkurse22', 'https://t.me/barnaul22official', 'https://t.me/pb_barnaul22', 'https://t.me/novosti_barnaul', 'https://t.me/rbk_inc', 'https://t.me/katun24new', 'https://t.me/brnl01', 'https://t.me/vestialtay', 'https://t.me/amic_ru', 'https://t.me/rubtsovskienovosti', 'https://t.me/solundar', 'https://t.me/brn_ka', 'https://t.me/aleysk_news', 'https://t.me/barnaul_press', 'https://t.me/incident_22', 'https://t.me/tolknews', 'https://t.me/barnaul_org', 'https://t.me/biworkBMG', 'https://t.me/this_is_Barnaul', 'https://t.me/gornyakonline', 'https://t.me/sgk_barnaul', 'https://t.me/barnaul', 'https://t.me/sgk_biysk', 'https://t.me/COVID2019_altairegion', 'https://t.me/krasnoschekovo', 'https://t.me/nekurasov', 'https://t.me/tomenko_news', 'https://t.me/nbsk22', 'https://t.me/altainfonews', 'https://t.me/orf_22', 'https://t.me/homoalt', 'https://t.me/molodezAltai', 'https://t.me/ap22ru', 'https://t.me/russvo2023', 'https://t.me/leftbiysk', 'https://t.me/Altai_News_channel', 'https://t.me/rubtsovsk_online', 'https://t.me/bathhouse1', 'https://t.me/rossia22', 'https://t.me/gonzobarnaul', 'https://t.me/gonzobarnaul', 'https://t.me/barnaulskie', 'https://t.me/barnaul_gid', 'https://t.me/tomenko_22', 'https://t.me/altaigovernment', 'https://t.me/altaikrai', 'https://t.me/lenina59', 'https://t.me/tsur22', 'https://t.me/nelyapunov', 'https://t.me/polit22', 'https://t.me/polit22', 'https://t.me/kprfaltay', 'https://t.me/vibaltay', 'https://t.me/er_22', 'https://t.me/altaishaman', 'https://t.me/molotov_akzs', 'https://t.me/altkrai_vesna', 'https://t.me/nazbol22', 'https://t.me/m_ponkrasheva', 'https://t.me/spravedlivo_barnaul', 'https://t.me/gai100161', 'https://t.me/mparlament22', 'https://t.me/molprav22alt', 'https://t.me/Alexshipunov', 'https://t.me/youthyabloko22']
 
    file_name = ""

    with open(file_name, "a") as file:
        file.write("[")

    for user_input_channel in user_input_channel_list:
        if user_input_channel.isdigit():
            entity = PeerChannel(int(user_input_channel))
        else:
            entity = user_input_channel

        my_channel = await client.get_entity(entity)

        async for message in client.iter_messages(my_channel, reverse = True, offset_date = date(2022, 2, 24)):
            if message.date > datetime(2023, 2, 24, tzinfo=timezone.utc):
                break
    
            if (message.message == ''):
                continue

            message_dict = message.to_dict()
            message_dict['channel_url'] = user_input_channel

            with open(file_name, "a") as file:
                print(message.date)
                json.dump(message_dict, file, ensure_ascii=False, indent=4, cls=DateTimeEncoder)
                file.write(",\n")
            
            await asyncio.sleep(0.03) 

    with open(file_name, "rb+") as file:
        file.seek(-2, os.SEEK_END)
        file.truncate()

    with open(file_name, "a") as file:
        file.write("]")

with client:
    client.loop.run_until_complete(main(phone))
