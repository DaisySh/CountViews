#!/usr/bin/env python3
import argparse
from datetime import datetime
import os
import pandas as pd
import youtube_dl


def get_playlist_urls(playlist_path):
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
        res['timestamp'] = get_date_time_string()
    return res

def get_date_time_string():
    obj_date = datetime.now()
    o_str = obj_date.strftime("%d-%b-%Y %H:%M")
    return o_str

def write_report(vc_list):
    df = pd.DataFrame (vc_list)
    df.to_csv('yt_report.csv', sep=';', index=False)

def get_parser():
    args_parser = argparse.ArgumentParser(description='Radio CICAP YouTube count views.')
    args_parser.add_argument('--save-playlist-urls', action='store_true', help='Save playlist urls flag. Use --video-url to specify the playlist.')
    args_parser.add_argument('--save-playlist-report', action='store_true', help='Save playlist report flag. Use --file-url-list to specify the txt playlist.')
    g = args_parser.add_mutually_exclusive_group(required=True)
    g.add_argument('--video-url', type=str, help='YouTube video URL.')
    g.add_argument('--file-url-list', type=str, help='TxT file of YouTube video URLs.')
    return args_parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    if args.video_url is not None:
        if args.save_playlist_urls:
            get_playlist_urls(args.video_url)
        else:
            video_url = 'https://www.youtube.com/watch?v=Sn7YrWMKOM4'
            vc = get_view_count(video_url)
            if vc['count'] > -1:
                note_str = "{}; {}; {}; {}".format(vc['title'], vc['url'],
                                                   vc['timestamp'],
                                                   vc['count'])
                print(note_str)
    if args.file_url_list is not None:
        vc_list = []
        with open(args.file_url_list, 'r') as f:
            for item in f:
                video_url = item.strip()
                vc = get_view_count(video_url)
                vc_list.append(vc)
                if vc['count'] > -1:
                    note_str = "{}; {}; {}; {}".format(vc['title'], vc['url'],
                                                       vc['timestamp'],
                                                       vc['count'])

                    print(note_str)
        if args.save_playlist_report:
            if len(vc_list) > 0:
                write_report(vc_list)

if __name__ == '__main__':
    main()
