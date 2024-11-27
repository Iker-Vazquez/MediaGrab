#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# YouTubeDownloader.py
"""
Description: Class to handle downloading videos and playlists from YouTube.
Author: Iker Vazquez
Email: iker-vazquez@users.noreply.github.com
Date: 2024-11-06
"""

import yt_dlp
import os
from src.libs.common.Logger.Logger import Logger
import subprocess


class YouTubeDownloader:
    """
    Class to handle downloading videos and playlists from YouTube.

    *Methods*:
    - download_video(url: str, path: str, keep_audio_only: bool = False) -> None : Downloads a single YouTube video.
    - download_playlist(url: str, path: str, keep_audio_only: bool = False) -> None : 
      Downloads an entire YouTube playlist.

    *Attributes*:
    - logger --> Logger : An instance of the Logger class used for logging events and errors.

    *Examples*:
    - downloader = YouTubeDownloader(logger)
    - downloader.download_video("https://www.youtube.com/watch?v=example", "./downloads")
    - downloader.download_playlist("https://www.youtube.com/playlist?list=example", "./downloads")

    *Notes*:
    - Requires the yt-dlp library to be installed (pip install yt-dlp).
    - Requires FFmpeg to be installed for audio conversion (https://ffmpeg.org/download.html).
    """

    def __init__(self, logger: Logger):
        """
        Initializes the YouTubeDownloader instance with a logger.

        *Arguments*:
        - logger --> Logger : An instance of the Logger class used for logging events and errors.

        *Returns*:
        - None

        *Examples*:
        - downloader = YouTubeDownloader(logger)

        *Notes*:
        - The logger instance is used to log events and errors during the download process.
        """
        self.logger = logger
        self.logger.write_info("YouTubeDownloader initialized.")

    def download_video(self, url: str, path: str, keep_audio_only: bool = False) -> None:
        """
        Downloads a single YouTube video.

        *Arguments*:
        - url --> str : The URL of the YouTube video to be downloaded.
        - path --> str : The directory where the video will be saved.
        - keep_audio_only --> bool : Whether to download only the audio (default is False, download both audio and video).

        *Returns*:
        - None

        *Examples*:
        - downloader.download_video("https://www.youtube.com/watch?v=example", "./downloads")

        *Notes*:
        - Creates the output directory if it doesn't already exist.
        - If keep_audio_only is True, only audio is downloaded and optionally converted to MP3.
        """
        self._download_from_youtube(url, path, keep_audio_only, isPlaylist=False)

    def download_playlist(self, url: str, path: str, keep_audio_only: bool = False) -> None:
        """
        Downloads an entire YouTube playlist.

        *Arguments*:
        - url --> str : The URL of the YouTube playlist to be downloaded.
        - path --> str : The directory where the playlist files will be saved.
        - keep_audio_only --> bool : Whether to download and convert only the audio for each video (default is False).

        *Returns*:
        - None

        *Examples*:
        - downloader.download_playlist("https://www.youtube.com/playlist?list=example", "./downloads")

        *Notes*:
        - Creates the output directory if it doesn't already exist.
        - If keep_audio_only is True, each video in the playlist will be downloaded and optionally converted to MP3.
        """
        self._download_from_youtube(url, path, keep_audio_only, isPlaylist=True)

    def _download_from_youtube(self, url: str, path: str, keep_audio_only: bool = False, isPlaylist: bool = False) -> None:
        """
        Downloads a single YouTube video or playlist.

        *Arguments*:
        - url --> str : The URL of the YouTube video or playlist to be downloaded.
        - path --> str : The directory where the video or playlist files will be saved.
        - keep_audio_only --> bool : Whether to download and convert only the audio for each video (default is False).

        *Returns*:
        - None

        *Examples*:
        - self._download_from_youtube("https://www.youtube.com/watch?v=example", "./downloads")
        - self._download_from_youtube("https://www.youtube.com/playlist?list=example", "./downloads")

        *Notes*:
        - Creates the output directory if it doesn't already exist.
        - If keep_audio_only is True, each video in the playlist will be downloaded and optionally converted to MP3.
        """
        try:
            self.logger.write_debug(f"Starting download for playlist: {url}")
            os.makedirs(path, exist_ok=True)  # Ensure the directory exists

            # Define download options for yt-dlp
            ydl_opts = {
                'outtmpl': os.path.join(path, '%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s'),
                'format': 'bestaudio/best' if keep_audio_only else 'bestvideo+bestaudio/best',
                'skip_unavailable_fragments': True,  # Skip any unavailable video fragments
                'ignoreerrors': True,  # Ignore any errors that occur during the download
                'progress_hooks': [
                    lambda d: self._progress_hook(d, convert_to_mp3=keep_audio_only)
                ],  # Hook to track progress and convert to MP3 if needed
                'noplaylist': True if isPlaylist else False,  # Ensure we're downloading a single video or playlist
            }

            # Download the playlist using yt-dlp
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        except Exception as e:
            self.logger.write_error(f"Error downloading playlist: {url}, {str(e)}")

    def _progress_hook(self, d, convert_to_mp3: bool = False) -> None:
        """
        This hook is called during the download to log the name of the downloaded file and optionally
        convert the downloaded audio file to MP3.

        *Arguments*:
        - d --> dict : Dictionary containing download information such as status, filename, etc.
        - convert_to_mp3 --> bool : Whether to convert the downloaded file to MP3 after it's finished (default is False).

        *Returns*:
        - None

        *Examples*:
        - self._progress_hook(d)
        - self._progress_hook(d, convert_to_mp3=True)

        *Notes*:
        - This method is called by yt-dlp during the download process.
        """
        if d['status'] == 'finished':  # Check if the download has finished
            filename = d['filename']
            self.logger.write_info(f"Downloaded file: {filename}")

            # If we want to convert to MP3, proceed with the conversion
            if convert_to_mp3:
                self.logger.write_debug(f"Converting {filename} to MP3...")

                # Prepare the output filename for the MP3 file
                output_filename = filename.rsplit('.', 1)[0] + '.mp3'

                try:
                    # Run FFmpeg to convert the downloaded file to MP3
                    command = [
                        'ffmpeg',         # FFmpeg command
                        '-i', filename,   # Input file (the downloaded file)
                        '-vn',            # Disable video processing (audio only)
                        '-ar', '44100',   # Audio sample rate (44.1 kHz)
                        '-ac', '2',       # Stereo output (2 channels)
                        '-b:a', '320k',   # Set the bitrate to 320 kbps for high-quality audio
                        '-f', 'mp3',      # Set the format to MP3
                        output_filename   # Output file name
                    ]
                    subprocess.run(command, check=True)  # Run the FFmpeg command
                    self.logger.write_info(f"Converted {filename} to MP3: {output_filename}")

                    # Remove the original file after conversion
                    os.remove(filename)
                    self.logger.write_debug(f"Deleted original file: {filename}")

                except subprocess.CalledProcessError as e:
                    self.logger.write_error(f"Error converting {filename} to MP3: {e}")  # Log errors during conversion
