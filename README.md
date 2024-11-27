YouTube Download Script

Description:
---------------
This script allows you to download YouTube videos or playlists using the powerful yt-dlp tool. It checks for the necessary dependencies, logs the process, and saves the downloaded content to a specified directory.

Features:
----------
- Download individual videos or entire playlists.
- Auto-check and install dependencies (yt-dlp and ffmpeg).
- Save downloaded content in a specified directory.
- Logs detailed information, including errors and successful downloads.
- Cross-platform support (Linux, macOS, and Windows).
- Automatically handles permission requirements (root/admin privileges).

Installation:

Prerequisites:
---------------
- Python 3.x: This project is compatible with Python 3.
- yt-dlp: A command-line program to download videos from YouTube.
- ffmpeg: A tool to handle multimedia files and convert formats.

Installing Dependencies:
------------------------
1. Clone this repository or download the source files to your machine.
2. Navigate to the project folder.

   Example:
   git clone https://github.com/yourusername/YoutubeDownload.git
   cd YoutubeDownload

3. Run the `install.py` script to check and install dependencies:

   - On Linux/macOS, make sure to run the script with `sudo`:

     sudo python3 install.py

   - On Windows, run the script as Administrator.

   The script will:
   - Check for `yt-dlp` and `ffmpeg` installation.
   - Automatically install any missing dependencies.

4. Alternatively, you can manually install dependencies via `requirements.txt` if needed:

   pip install -r requirements.txt

Dependencies:
-------------
This project uses the following libraries:

- yt-dlp: Fork of youtube-dl that allows downloading YouTube videos.
- ffmpeg: A tool for handling multimedia data.
- requests: HTTP library for interacting with the web.
- argparse: For parsing command-line arguments.

All dependencies are listed in the `requirements.txt` file.

Usage:

Running the Script:
-------------------
You can run the script from the command line to download videos or playlists:

- To download a single video:
  python YoutubeDownload.py -u "https://www.youtube.com/watch?v=9FlwDGY_C3w" -t video

- To download a playlist:
  python YoutubeDownload.py -u "https://www.youtube.com/playlist?list=PL9t5mX4YxIiDxlAt6jFeX6pSBQ9IbGb-w" -t playlist

Arguments:
-----------
- -u, --url: The URL of the video or playlist you wish to download.
- -t, --type: Specify whether to download a "video" or a "playlist".
- -p, --path: The directory to save the downloaded content (default is ./downloads).

License Compliance:
-------------------
This script makes use of external tools and libraries that may have specific licensing requirements. The following are the licenses for the main tools used:

- yt-dlp: MIT License
- ffmpeg: LGPL-2.1 License
- requests: Apache 2.0 License

Ensure you comply with the licenses of these dependencies when using or distributing this project. For more details on how to comply with these licenses, please refer to the respective documentation and license files of the tools you're using.

License:
--------
This project is licensed under the **GNU General Public License (GPL) v3**, with a **Non-Commercial Use Only** restriction.

You are free to use, modify, and share the code, but **commercial use is prohibited**. The software is provided "as is" without warranty of any kind.

For more details, see the LICENSE file or visit the official GNU website:
https://www.gnu.org/licenses/gpl-3.0.html
