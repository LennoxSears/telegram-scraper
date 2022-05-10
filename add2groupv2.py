from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerUser
import os, sys
import configparser
import csv
import time
from telethon import TelegramClient
import pandas as pd
from telethon.tl.functions.channels import InviteToChannelRequest
import random
from tqdm import tqdm

#test

re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"


# Remember to use your own values from my.telegram.org!
api_id = 17049072
api_hash = 'b57a1df48b298d34c2010887c6e0400c'
client = TelegramClient('anon2', api_id, api_hash)


async def main():

    group_list = []
    i = 0
    async for dialog in client.iter_dialogs():
        try:
            if not dialog.entity.broadcast:
                print(gr ,'[', i,']', dialog.name, 'has ID', dialog.id, ' | Users : ', dialog.entity.participants_count)
                group_list.append(dialog.id)
                i += 1
        except:
            pass

    df = pd.read_csv('membreV2.csv', sep=',')

    group_number = input('Which group do you want to add to ? : ')
    group_number = int(group_number)
    group_id = group_list[group_number]
    target_group_entity = group_id

    for i in tqdm(df.index):
        try:
            user_to_add = InputPeerUser(df['user_id'][i], df['access_hash'][i])
            await client(InviteToChannelRequest(target_group_entity, [user_to_add]))

            random_time_sleep = random.randint(5, 10)
            # user_info = await client.get_entity(df['user_id'][i])
            # print(user_info.first_name, 'added to the group | Waiting', random_time_sleep, 'seconds to add next user')
            time.sleep(random_time_sleep)
        except Exception as e:
            print('\n',e)
            print('Error | Waiting 7 seconds')
            time.sleep(7)
            pass

    print('Members added to group')

with client:
    client.loop.run_until_complete(main())
