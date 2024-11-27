#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# install.py
"""
Description: Script to check and install necessary dependencies for the YoutubeDownload project.

Dependencies checked:
- yt-dlp: A command-line tool to download videos from YouTube and other sites.
- ffmpeg: A multimedia framework used to decode, encode, transcode, mux, demux, stream, filter, and play audio and video files.

Usage:
- Run this script as root (Linux/macOS) or with administrative privileges (Windows) to ensure system-wide dependencies (like ffmpeg) are installed.
- The script will check for the presence of yt-dlp and ffmpeg, and install them if they are missing.

Author: Iker Vazquez
Email: iker-vazquez@users.noreply.github.com
Date: 2024-11-06
"""

import subprocess
import sys
import platform
from src.libs.dependency_checker.DependencyChecker import DependencyChecker


def install_dependencies() -> None:
    """
    Checks if the necessary dependencies (yt-dlp, ffmpeg) are installed and installs them if missing.

    *Arguments*:
    - None

    *Returns*:
    - None

    *Examples*:
    - install_dependencies()

    *Notes*:
    - Utilizes the `DependencyChecker` class to check and install dependencies.
    """
    print("Starting dependency check and installation...")
    checker = DependencyChecker(requirements_path='./requirements.txt')

    checker.check_dependencies()


def check_permissions() -> bool:
    """
    Checks if the script is being run with the necessary privileges based on the operating system.

    *Arguments*:
    - None

    *Returns*:
    - bool: True if the script has necessary privileges, False otherwise.

    *Examples*:
    - check_permissions()

    *Notes*:
    - Linux/macOS: The script needs root permissions to install system-wide dependencies like ffmpeg.
    - Windows: Administrative privileges are needed for installing global dependencies.
    """
    current_os = platform.system().lower()

    if current_os == 'linux' or current_os == 'darwin':
        if subprocess.run(['whoami'], capture_output=True, text=True).stdout.strip() != 'root':
            print("Error: This script must be run as root (use sudo) to install system dependencies (e.g., ffmpeg).")
            return False
    elif current_os == 'windows':
        try:
            is_admin = subprocess.run('net session', capture_output=True, text=True)
            if is_admin.returncode != 0:
                print("Error: This script must be run with administrative privileges.")
                return False
        except subprocess.CalledProcessError:
            print("Error: Unable to check admin privileges. Please run the script as an administrator.")
            return False
    else:
        print(f"Unsupported OS: {current_os}. Please ensure you're using Linux, macOS, or Windows.")
        return False

    return True


def main():
    """
    Main execution block to check system permissions and install dependencies.

    *Arguments*:
    - None

    *Returns*:
    - None

    *Examples*:
    - Running this file as a script will invoke `install_dependencies()` if the necessary permissions are granted.

    *Notes*:
    - Verifies that the script has sufficient privileges (root/admin) to install dependencies.
    """
    if check_permissions():
        install_dependencies()
        print("All dependencies have been successfully installed.")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
