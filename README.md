# CountViews

Youtube view count. It reports views information on a given Youtube playlist.
Copyright (C) 2020  Dasara Shullani

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

## Usage

- Collect videos from playlist

```
python3 count_yt.py create-playlist --playlist-url https://www.youtube.com/playlist?list=PL1YqYT_1QpMaICoW5DdW1MDS5exOV79rK --playlist-filename ./Data/yt_radio_cicap.txt
```

- Create report from videos (Radio Cicap Playlist)

```
python3 count_yt.py create-report --report-filename ./Data/yt_radio_cicap_report.csv --playlist-filename ./Data/yt_radio_cicap.txt
```

- Create report from videos (Radio Cicap Fest 2020)

```
python3 count_yt.py create-report --report-filename ./Data/yt_fest2020_report.csv --playlist-filename ./Data/yt_fest2020.txt
```

- Update report from playlist

```
python3 count_yt.py update-report --report-filename ./Data/yt_fest2020_report.csv --playlist-filename ./Data/yt_fest2020.txt

```

## Help

- `--help`

```
$ python3 count_yt.py --help

usage: count_yt.py [-h] {create-playlist,create-report,update-report} ...

Radio CICAP YouTube count views.

positional arguments:
  {create-playlist,create-report,update-report}
                        Count views sub-commands help
    create-playlist     Create YouTube urls file from playlist link.
    create-report       Create Views Report from playlist urls.
    update-report       Update Views Report from playlist urls and views report.

optional arguments:
  -h, --help            show this help message and exit
```

- `create-playlist`

```
$ python3 count_yt.py create-playlist --help
usage: count_yt.py create-playlist [-h] --playlist-url PLAYLIST_URL --playlist-filename
                                   PLAYLIST_FILENAME

optional arguments:
  -h, --help            show this help message and exit
  --playlist-url PLAYLIST_URL
                        Youtube playlist link.
  --playlist-filename PLAYLIST_FILENAME
                        Txt filename to save each video url in playlist.

```

- `create-report`

```
$ python3 count_yt.py create-report --help
usage: count_yt.py create-report [-h] --report-filename REPORT_FILENAME --playlist-filename
                                 PLAYLIST_FILENAME

optional arguments:
  -h, --help            show this help message and exit
  --report-filename REPORT_FILENAME
                        CSV filename to save the video views of each video in the playlist.
  --playlist-filename PLAYLIST_FILENAME
                        Txt filename of playlist video urls.
```

- `update-report`

```
$ python3 count_yt.py update-report --help
usage: count_yt.py update-report [-h] --report-filename REPORT_FILENAME --playlist-filename
                                 PLAYLIST_FILENAME

optional arguments:
  -h, --help            show this help message and exit
  --report-filename REPORT_FILENAME
                        CSV filename of view's count.
  --playlist-filename PLAYLIST_FILENAME
                        Txt filename of playlist video urls.
```
