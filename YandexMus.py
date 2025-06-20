from multiprocessing import Pool
import os
from pathlib import Path
from pprint import pprint
import re
import requests
from yandex_music import Client, exceptions, Track
from tokens import YandexToken
import eyed3
from eyed3.id3.frames import ImageFrame
from eyed3.core import Date
from datetime import datetime, timedelta
client = Client(YandexToken).init()
cache = Path.cwd()/".cache/"
cache.mkdir(exist_ok=True)


def search_best_and_save(query: str, folder=cache):
    search_result = client.search(text=query)
    if search_result.best and search_result.best.type == 'track':
        best = search_result.best.result
        artists = ''
        if best.artists:
            artists = ' - ' + ', '.join(best.artists_name())
        best_result_text = re.sub(
            '[/:*?"<>|]', '', best.title + artists+".mp3")
        file = folder/best_result_text
        # pprint(best)
        if not file.exists():
            print(f"Downloading {file}")
            file.touch(mode=0o644)
            try:
                best.download(filename=f"{file}", bitrate_in_kbps=320)
            except exceptions.InvalidBitrateError:
                best.download(filename=f"{file}")

            eyedFile = eyed3.load(str(file))
            if (eyedFile.tag == None):
                eyedFile.initTag()
            eyedFile.tag.images.set(
                ImageFrame.FRONT_COVER, getImage(best.cover_uri), 'image/jpeg')
            eyedFile.tag.artist = artists
            eyedFile.tag.title = best.title
            eyedFile.tag.year = Date(best.albums[0].year)
            try:
                eyedFile.tag.genre = best.albums[0].genre.replace("genre", "")
            except:
                pass
            eyedFile.tag.album = best.albums[0].title
            eyedFile.tag.save()


def downloadTrack(track: Track, folder):
    artists = ''
    if track.artists:
        artists = ' - ' + ', '.join(track.artists_name())
    fname = re.sub(
        '[/:*?"<>|]', '', track.title + artists+".mp3")
    fPath = folder/fname
    if not fPath.exists():
        fPath.touch(mode=0o644)
    if fPath.stat().st_size == 0:
        st = datetime.today()
        print(f"Downloading {fPath}")
        fPath.unlink()
        try:
            track.download(filename=f"{fPath}", bitrate_in_kbps=320)
        except exceptions.InvalidBitrateError:
            track.download(filename=f"{fPath}")

        eyedFile = eyed3.load(str(fPath))
        if (eyedFile.tag == None):
            eyedFile.initTag()
        eyedFile.tag.images.set(
            ImageFrame.FRONT_COVER, getImage(track.cover_uri), 'image/jpeg')
        eyedFile.tag.artist = ', '.join(track.artists_name())
        eyedFile.tag.title = track.title
        eyedFile.tag.year = Date(track.albums[0].year)
        genre = track.albums[0].genre.replace("genre", "")
        genre = genre.replace('rus', '').replace('foreign', '')

        eyedFile.tag.genre = genre
        eyedFile.tag.album = track.albums[0].title
        eyedFile.tag.save()
        dt = datetime.today()-st
        print(f"Sucksess {fPath},downloading time {dt}")
        return dt


def getImage(url):
    r = requests.get(f'https://{url.replace("%%","200x200")}', stream=True)
    if r.status_code == 200:
        r.raw.decode_content = True
        return r.raw.read()


def copy_from_history():
    mus = []
    with open("toDownl.txt", "r", encoding="utf-8")as f:
        mus = f.readlines()
    nmus = []
    nowWrit = ''
    for i in mus:
        if not re.fullmatch(r'\d:\d\d\n', i):
            if i.strip() != '':
                nowWrit += i.strip()+" "
            else:
                if nowWrit.strip() != '':
                    nmus.append(nowWrit.strip())
                nowWrit = ''
    mus.clear()
    return nmus


def downloadPlaylist(playlist, folder=cache):
    filtredTitle = re.sub(
        '[/:*?"<>|]', '', playlist.title)
    folder = folder/filtredTitle
    folder.mkdir(exist_ok=True)
    tracks = ((i.track, folder)for i in playlist.fetch_tracks())
    downloadTime = None
    while downloadTime == None:
        downloadTime = downloadTrack(*next(tracks))
    fastInternet = timedelta(seconds=15) > downloadTime
    if fastInternet:
        pool = Pool(os.cpu_count()-1)
        pool.starmap(downloadTrack, tracks)
        pool.close()
    else:
        for t in tracks:
            downloadTrack(*t)


def downloadByURL(url: str):
    track_id = int(url.split('track/')[-1])
    track = client.tracks(track_id)[0]
    print(track.title)
    downloadTrack(track, cache)


if __name__ == '__main__':
    pass

    # que=client.queues_list()
    # que = client.queue("648825e9c0c7cb38090326ff")
    # for i in que.tracks[5:30]:
    #     track = client.tracks(i.track_id)[0]
    #     # answ=input(track.title)
    #     downloadTrack(track,cache)
        # if answ=='y':
    url = 'https://music.yandex.by/album/16002307/track/84428655'
    downloadByURL(url)
    # pl2 = client.users_playlists_list()

    # for i,e in enumerate(pl2):
    #     print(i,e.title)

    # pl = client.users_likes_playlists()
    # pl[0].playlist.tit
    # for i in pl:
    #     print(i.playlist.title)
    # downloadPlaylist(pl2[13])
    # search_best_and_save('time in a bottle ')
    # cache = Path.cwd()/".cache/"
    # cache.mkdir(exist_ok=True)
    # n = copy_from_history()
    # # search_best_and_save(n[0])
    # pprint(n)
    # pool=Pool(os.cpu_count()-1)
    # pool.map(search_best_and_save,n)
    # pool.close()
