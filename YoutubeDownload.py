#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# YoutubeDownload.py
"""
Description: Main script to download YouTube videos or playlists using YouTubeDownloader.
Author: Iker Vazquez
Email: iker-vazquez@users.noreply.github.com
Date: 2024-11-06
"""

import argparse
from src.libs.youtube_downloader.YouTubeDownloader import YouTubeDownloader
from src.libs.common.Logger.Logger import Logger


def main():
    """
    Main function to parse arguments and initiate the download process.

    *Arguments*:
    - None

    *Returns*:
    - None

    *Notes*:
    - Initiates dependency checking and download based on input arguments.
    """
    log = Logger(log_file='./logs/LogFile.log', config_json='./config.json')
    downloader = YouTubeDownloader(logger=log)

    parser = argparse.ArgumentParser(description="Download YouTube videos or playlists.")
    parser.add_argument('-u', '--url', type=str, required=True, help="YouTube video or playlist URL.")
    parser.add_argument(
                        '-t', '--type', type=str, choices=['video', 'playlist'], default='playlist',
                        help="Specify whether it's a video or playlist."
                        )
    parser.add_argument('-p', '--path', type=str, default='./downloads', help="Destination path for downloads.")
    parser.add_argument('-a', '--audioOnly', action='store_true', help="Keep only the audio of the video")

    args = parser.parse_args()

    if args.type == 'video':
        log.write_debug(f"Downloading video from URL: {args.url}")
        downloader.download_video(args.url, args.path, args.audioOnly)
    elif args.type == 'playlist':
        log.write_debug(f"Downloading playlist from URL: {args.url}")
        downloader.download_playlist(args.url, args.path, args.audioOnly)


if __name__ == "__main__":
    main()
