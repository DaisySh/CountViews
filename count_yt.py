#!/usr/bin/env python3
import argparse
from datetime import datetime
import logging
import os
import youtube_dl


def get_url_playlist(playlist_path):
    ydl_opts = {"quiet":True}
    res = []
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        json_info = ydl.extract_info(playlist_path, download=False)
        if 'entries' in json_info:
            for item in json_info['entries']:
                res.append(item['webpage_url'])
    with open('yt_list.txt', 'a+') as f:
        for item in res:
            f.write(item + "\n")


def get_view_count(video_url):
    ydl_opts = {"quiet":True}
    res = {'title':'', 'count':-1, 'url':''}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        json_info = ydl.extract_info(video_url, download=False)
        res['title']= json_info['title']
        res['count'] = json_info['view_count']
        res['url'] = json_info['webpage_url']
    return res

def get_date_time_string():
    obj_date = datetime.now()
    o_str = obj_date.strftime("%d-%b-%Y %H:%M")
    return o_str


def get_parser():
    args_parser = argparse.ArgumentParser(description='Radio CICAP YouTube count views.')
    args_parser.add_argument('--store-playlist', action='store_true', help='Save playlist urls flag. Use --video-url to specify the playlist.')
    g = args_parser.add_mutually_exclusive_group(required=True)
    g.add_argument('--video-url', type=str, help='YouTube video URL.')
    g.add_argument('--file-url-list', type=str, help='TxT file of YouTube video URLs.')
    return args_parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    if args.video_url is not None:
        if args.store_playlist:
            get_url_playlist(args.video_url)
        else:
            video_url = 'https://www.youtube.com/watch?v=Sn7YrWMKOM4'
            vc = get_view_count(video_url)
            if vc['count'] > -1:
                note_str = "{}; {}; {}; {}".format(vc['title'], vc['url'],
                                                   get_date_time_string(),
                                                   vc['count'])
                print(note_str)

if __name__ == '__main__':
    main()
