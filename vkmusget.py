from enum import IntEnum
import multiprocessing
from pprint import pprint

import requests
from vktoken import vktok, log, pas
import vk_api
import threading


class LongPoolType(IntEnum):
    NewMessage = 4
    EditMessage = 5
    TypeText = 61


session = vk_api.VkApi(login=log, password=pas, token=vktok,
                       app_id=6121396, config_filename='VK_cfg')
session.http.headers['User-agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:94.0) Gecko/20100101 Firefox/94.0'
session.auth(token_only=True)
api = session.get_api()


def LoongPoool():
    serverParams = api.messages.getLongPollServer()

    print("Listener Started")
    while True:
        response = requests.get(
            f"https://{serverParams['server']}?act=a_check&key={serverParams['key']}&ts={serverParams['ts']}&wait=60&mode=2&version=2").json()
        updates = response.get('updates',None)
        if updates:
            for element in updates:
                if element[0] == LongPoolType.NewMessage:
                    requests.post('http://localhost:5001/newMsgVK', json={
                                  'message_id': element[1],
                                  'flags': element[2],
                                  'minor_id': element[3],
                                  'other': element[4:]
                                  })
        # обновление номера последнего обновления
        serverParams['ts'] = response['ts']


def downloadFromVK(audioAttachment):
    fname = f'{audioAttachment["title"]} {audioAttachment["artist"]}.mp3'
    try:
        r = requests.get(audioAttachment["url"])
        if r.status_code == 200:

            with open(fname, 'wb') as output_file:
                output_file.write(r.content)
    except OSError:
        print(fname)


if __name__ == "__main__":
    thread = threading.Thread(target=LoongPoool, daemon=True)
    thread.start()
    # https://dev.vk.com/method/messages.getById