#!/usr/bin/env python3
import argparse
from datetime import datetime
import logging
import os
import youtube_dl

def get_view_count(video_url):
    ydl_opts = {"quiet":True}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        json_info = ydl.extract_info(video_url, download=False)
        if 'view_count' in json_info:
            return json_info['view_count']
        else:
            return -1

def get_date_time_string():
    obj_date = datetime.now()
    o_str = obj_date.strftime("%d-%b-%Y %H:%M")
    return o_str


def get_parser():
    args_parser = argparse.ArgumentParser(description='Radio CICAP YouTube count views.')
    g = args_parser.add_mutually_exclusive_group(required=True)
    g.add_argument('--video-url', type=str, help='YouTube video URL.')
    g.add_argument('--file-url-list', type=str, help='TxT file of YouTube video URLs.')
    return args_parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    if args.video_url is not None:
        video_url = 'https://www.youtube.com/watch?v=Sn7YrWMKOM4'
        vc = get_view_count(video_url)
        if vc > -1:
            print(video_url)
            print(get_date_time_string())
            print(vc)

if __name__ == '__main__':
    main()
