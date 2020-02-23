# Unip - A universal package manager for Linux

Unip is a universal package manager for Linux oerating systems written in Python. It uses different Linux package managers, depending on the operating system used (currently, only APT in combination with DPKG is supported) and extends it with confortable features and a universal command structure.

## Current project status

Features:

- Update package cache, upgrade, install, purge and remove packages.
- All packages installed with Unip are saved in a list as a special url format ``/var/lib/unip/packages.list``. This List can be used to install packages on other machine.

Currently, only APT/DPKG is supported. Features coming in future releases:

- Support for other package managers (Pacman, RPM, Snap etc.).
- Own packaging system.
- Synchronizing list of installed packages with the list of packages installed with Unip.

## Installation

Make sure you have Python 3 installed on your system. Then just copy this repository and run the ``install.sh`` script! Type ``sudo unip -h`` to list all available commands.
