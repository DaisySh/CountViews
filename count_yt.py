#!/usr/bin/env python3
#
# Youtube view count. It reports views information on a given Youtube playlist.
# Copyright (C) 2020  Dasara Shullani
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import argparse
from datetime import datetime
import os
import pandas as pd
import youtube_dl


def get_playlist_urls(playlist_url, playlist_filename):
    ydl_opts = {"quiet":True}
    res = []
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        json_info = ydl.extract_info(playlist_url, download=False)
        if 'entries' in json_info:
            for item in json_info['entries']:
                res.append(item['webpage_url'])
    with open(playlist_filename, 'a+') as f:
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
        res['upload_date'] = int(json_info['upload_date'])
        res['timestamp'] = get_date_time_string()
    return res

def get_date_time_string():
    obj_date = datetime.now()
    o_str = obj_date.strftime("%d-%b-%Y %H:%M")
    return o_str

def write_report(df, report_name):
    df.to_csv(report_name, sep=';', index=False)

def create_report(file_url_list, report_name=None):
    vc_list = []
    with open(file_url_list, 'r') as f:
        for item in f:
            video_url = item.strip()
            vc = get_view_count(video_url)
            if vc['count'] > -1:
                note_str = "{}; {}; {}; {}".format(vc['title'], vc['url'],
                                                   vc['timestamp'],
                                                   vc['count'])
                tmp_count = vc['count']
                tmp_date = vc['timestamp']
                vc[tmp_date] = tmp_count
                vc.pop('timestamp')
                vc.pop('count')
                vc_list.append(vc)
                print(note_str)
    df = pd.DataFrame(vc_list)
    if report_name is not None and len(vc_list) > 0:
        write_report(df, report_name)
    return df

def update_report(file_url_list, report_name):
    df = create_report(file_url_list)
    origin = pd.read_csv(report_name, sep=';')
    a = pd.merge(origin, df, how='right', on=['title', 'url', 'upload_date'])
    # check the last 2 columns, if different update
    if any(a[df.columns[-1]] != a[origin.columns[-1]]):
        write_report(a, report_name)
        print(a)


def get_parser():
    args_parser = argparse.ArgumentParser(description='Radio CICAP YouTube count views.')
    #args_parser.add_argument('--save-playlist-urls', action='store_true', help='Save playlist urls flag. Use --video-url to specify the playlist.')
    #args_parser.add_argument('--save-playlist-report', action='store_true', help='Save playlist report flag. Use --file-url-list to specify the txt playlist.')
    #args_parser.add_argument('--update-report', type=str, help='Update report with current views. Use --file-url-list to specify the txt playlist.')

    #g = args_parser.add_mutually_exclusive_group(required=True)
    #g.add_argument('--video-url', type=str, help='YouTube video URL.')
    #g.add_argument('--file-url-list', type=str, help='TxT file of YouTube video URLs.')

    subparsers = args_parser.add_subparsers(help='Count views sub-commands help', dest='cmd')
    sp_cp = subparsers.add_parser('create-playlist', help='Create YouTube urls file from playlist link.')
    sp_cr = subparsers.add_parser('create-report', help='Create Views Report from playlist urls.')
    sp_ur = subparsers.add_parser('update-report', help='Update Views Report from playlist urls and views report.')


    # create playlist
    sp_cp.add_argument('--playlist-url', type=str, required=True, help='Youtube playlist link.')
    sp_cp.add_argument('--playlist-filename', type=str, required=True, help='Txt filename to save each video url in playlist.')

    # create report from playlist
    sp_cr.add_argument('--report-filename', type=str, required=True, help='CSV filename to save the video views of each video in the playlist.')
    sp_cr.add_argument('--playlist-filename', type=str, required=True, help='Txt filename of playlist video urls.')

    # update report
    sp_ur.add_argument('--report-filename', type=str, required=True, help="CSV filename of view's count.")
    sp_ur.add_argument('--playlist-filename', type=str, required=True, help='Txt filename of playlist video urls.')
    return args_parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    if args.cmd == 'create-playlist':
        pl_url = args.playlist_url
        pl_txt = args.playlist_filename
        get_playlist_urls(pl_url, pl_txt)
    elif args.cmd == 'create-report':
        pl_txt = args.playlist_filename
        rp_csv = args.report_filename
        create_report(pl_txt, rp_csv)
    elif args.cmd == 'update-report':
        pl_txt = args.playlist_filename
        rp_csv = args.report_filename
        update_report(pl_txt, rp_csv)
    else:
        print('Wrong usage. Please check the --help option.')


if __name__ == '__main__':
    main()
