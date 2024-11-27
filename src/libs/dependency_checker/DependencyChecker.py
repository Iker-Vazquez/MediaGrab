#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DependencyChecker.py
"""
Description: Class to check if necessary dependencies are installed on the system.
Author: Iker Vazquez
Email: iker-vazquez@users.noreply.github.com
Date: 2024-11-06
"""

import subprocess
import sys
import shutil
import platform
import os
from src.libs.common.Logger.Logger import Logger


class DependencyChecker:
    """
    Class to check if necessary dependencies (yt-dlp, ffmpeg) are installed on the system.

    *Attributes*:
    - logger --> Logger : Instance of the Logger class to log messages.
    - requirements_path --> str : Path to the requirements.txt file (optional).

    *Methods*:
    - check_dependencies() --> Verifies if the necessary dependencies (yt-dlp and ffmpeg) are installed.
    - install_dependency(dependency_name: str) --> Installs a dependency if it is not installed.
    - _install_requirements() --> Installs Python packages listed in the provided requirements file.
    - _check_dependency(dependency_name: str) --> Verifies if a specific dependency is installed.
    - _check_yt_dlp() --> Checks if yt-dlp is installed by attempting to import it.
    - _check_ffmpeg() --> Checks if ffmpeg is installed by running `ffmpeg --version`.
    - _install_ffmpeg() --> Installs ffmpeg using system package managers (apt, yum, pacman, brew, choco).
    """

    def __init__(self, logger: Logger,  requirements_path: str = None):
        """
        Initializes the DependencyChecker instance.

        *Arguments*:
        - logger --> Logger : Instance of the Logger class for logging messages.
        - requirements_path --> str : Path to the requirements.txt file (optional).

        *Returns*:
        - None

        *Examples*:
        - checker = DependencyChecker(logger)
        """
        self.logger = logger
        self.requirements_path = requirements_path
        self.logger.write_info("DependencyChecker initialized.")

    def check_dependencies(self) -> None:
        """
        Verifies if the necessary dependencies (yt-dlp, ffmpeg) are installed.

        If a requirements file path is provided, attempts to install Python packages listed in the file.

        *Arguments*:
        - None

        *Returns*:
        - None

        *Examples*:
        - checker.check_dependencies()
        """
        self._check_dependency('yt-dlp')
        self._check_dependency('ffmpeg')

        if self.requirements_path:
            self._install_requirements()

    def _check_dependency(self, dependency_name: str) -> None:
        """
        Verifies if a specific dependency is installed by calling the appropriate check function.

        *Arguments*:
        - dependency_name --> str : Name of the dependency to check (yt-dlp or ffmpeg).

        *Returns*:
        - None

        *Examples*:
        - checker._check_dependency('yt-dlp')
        """
        if dependency_name == 'yt-dlp':
            self._check_yt_dlp()
        elif dependency_name == 'ffmpeg':
            self._check_ffmpeg()

    def _check_yt_dlp(self) -> None:
        """
        Checks if yt-dlp is installed by attempting to import it.

        If not installed, attempts to install yt-dlp.

        *Arguments*:
        - None

        *Returns*:
        - None

        *Examples*:
        - checker._check_yt_dlp()
        """
        try:
            import yt_dlp
            self.logger.write_info("yt-dlp is already installed.")
        except ImportError:
            self.logger.write_warning("yt-dlp is not installed.")
            self.install_dependency('yt-dlp')

    def _check_ffmpeg(self) -> None:
        """
        Checks if ffmpeg is installed by running `ffmpeg --version`.

        If not installed, attempts to install ffmpeg.

        *Arguments*:
        - None

        *Returns*:
        - None

        *Examples*:
        - checker._check_ffmpeg()
        """
        try:
            subprocess.run(['ffmpeg', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.logger.write_info("ffmpeg is already installed.")
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.logger.write_warning("ffmpeg is not installed.")
            self.install_dependency('ffmpeg')

    def install_dependency(self, dependency_name: str) -> None:
        """
        Installs a specific dependency (yt-dlp or ffmpeg) if it is not installed.

        *Arguments*:
        - dependency_name --> str : Name of the dependency to install (yt-dlp or ffmpeg).

        *Returns*:
        - None

        *Examples*:
        - checker.install_dependency('yt-dlp')
        """
        self.logger.write_info(f"Attempting to install {dependency_name}...")

        try:
            if dependency_name == 'yt-dlp':
                subprocess.run([sys.executable, '-m', 'pip', 'install', 'yt-dlp'], check=True)
                self.logger.write_info("yt-dlp has been installed successfully.")
            elif dependency_name == 'ffmpeg':
                self._install_ffmpeg()
        except subprocess.CalledProcessError as e:
            self.logger.write_error(f"Failed to install {dependency_name}: {e}")

    def _install_ffmpeg(self) -> None:
        """
        Attempts to install ffmpeg using system package managers (apt, yum, pacman, brew, choco).

        Compatible with Linux, macOS, and Windows.

        *Arguments*:
        - None

        *Returns*:
        - None

        *Examples*:
        - checker._install_ffmpeg()
        """
        self.logger.write_info("Attempting to install ffmpeg...")
        os_system = platform.system()

        if os_system == "Linux":
            if shutil.which('apt'):  # Debian/Ubuntu
                subprocess.run(['sudo', 'apt', 'install', '-y', 'ffmpeg'], check=True)
                self.logger.write_info("ffmpeg has been installed successfully via apt.")
            elif shutil.which('yum'):  # Fedora/RHEL
                subprocess.run(['sudo', 'yum', 'install', '-y', 'ffmpeg'], check=True)
                self.logger.write_info("ffmpeg has been installed successfully via yum.")
            elif shutil.which('pacman'):  # Arch Linux
                subprocess.run(['sudo', 'pacman', '-S', '--noconfirm', 'ffmpeg'], check=True)
                self.logger.write_info("ffmpeg has been installed successfully via pacman.")
            else:
                self.logger.write_warning("No compatible package manager found. Please install ffmpeg manually.")

        elif os_system == "Darwin":  # macOS
            if shutil.which('brew'):
                subprocess.run(['brew', 'install', 'ffmpeg'], check=True)
                self.logger.write_info("ffmpeg has been installed successfully via Homebrew.")
            else:
                self.logger.write_warning(
                    "Homebrew not found. Please install Homebrew or install ffmpeg manually on macOS."
                )

        elif os_system == "Windows":
            if shutil.which('choco'):
                subprocess.run(['choco', 'install', '-y', 'ffmpeg'], check=True)
                self.logger.write_info("ffmpeg has been installed successfully via Chocolatey.")
            else:
                windows_error_string = (
                    "Chocolatey not found. Please install Chocolatey or manually install ffmpeg "
                    "on Windows from https://ffmpeg.org/download.html"
                )
                self.logger.write_warning(windows_error_string)
                print(windows_error_string)

    def _install_requirements(self) -> None:
        """
        Installs Python packages listed in a requirements file.

        Verifies that the file exists before attempting installation.

        *Arguments*:
        - None

        *Returns*:
        - None

        *Examples*:
        - checker._install_requirements()
        """
        if not os.path.exists(self.requirements_path):
            self.logger.write_error(f"Requirements file {self.requirements_path} not found.")
            return

        self.logger.write_info(f"Attempting to install packages from {self.requirements_path}...")

        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', self.requirements_path], check=True)
            self.logger.write_info(f"Packages from {self.requirements_path} have been installed successfully.")
        except subprocess.CalledProcessError as e:
            self.logger.write_error(f"Failed to install packages from {self.requirements_path}: {e}")
