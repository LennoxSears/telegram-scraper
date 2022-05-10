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
import numpy as np
from tqdm import tqdm

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
        # print(dialog)
        try:
            if not dialog.entity.broadcast:
                print(gr ,'[', i,']', dialog.name, 'has ID', dialog.id, ' | Users : ', dialog.entity.participants_count)
                group_list.append(dialog.id)
                i += 1
        except:
            pass

    group_number = input('Choose a group number : ')
    group_number = int(group_number)
    group_id = group_list[group_number]

    all_participants = await client.get_participants(group_id)

    columns = ['username', 'user_id', 'access_hash', 'name', 'bot', 'group_id']
    df = pd.DataFrame(columns=columns)

    for participant in tqdm(range(len(all_participants))):
        df_new_row = pd.DataFrame(data=np.array([[all_participants[participant].username, all_participants[participant].id, all_participants[participant].access_hash, all_participants[participant].first_name, all_participants[participant].bot, group_id]]), columns=['username', 'user_id', 'access_hash', 'name', 'bot', 'group_id'])
        df = pd.concat([df, df_new_row], ignore_index=True)

    df.to_csv("membreV2.csv")
    print('Members added to file : membreV2.csv')


with client:
    client.loop.run_until_complete(main())