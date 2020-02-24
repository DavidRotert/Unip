#!/usr/bin/env python3

"""
Copyright (C) 2020  David Rotert
"""

import package
import packagemanager
import getpass
import argparse
import sys

LISTFILE = "/var/lib/unip/packages.list"


def get_list_from_file(file=LISTFILE):
    l = []
    with open(file, "r") as f:
        for line in f:
            l.append(line.strip())
    return l


def write_list_to_file(l, file=LISTFILE):
    l.sort()
    with open(file, "w") as f:
        return f.write("\n".join(l))


class Unip:
    def __init__(self):
        self._list = get_list_from_file()
        self._packages_to_install = []
        self._packages_to_purge = []
        self._packages_to_remove = []

    def update(self):
        """Updates package cache."""
        packagemanager.apt.update()

    def upgrade(self):
        """Upgrade packages."""
        packagemanager.apt.upgrade()

    def sync(self):
        """Syncs package list."""
        # transform package names to URLs
        pkglist = map(lambda x: package.get_package_from_url(x).get_url(),
                    packagemanager.apt.get_manual_installed())
                    
        # Remove non installed packages
        for url in self._list:
            if type(package.get_package_from_url(url)) == package.AptPackage:
                if not url in pkglist:
                    self._list.remove(url)

        # Add packages
        for pkg in pkglist:
            if not pkg.get_url() in self._list:
                self._list.append(pkg.get_url())
        write_list_to_file(self._list)

    def autoremove(self):
        """Autoremove packages."""
        packagemanager.apt.autoremove()

    def set_purge(self, packages):
        """Purges packages."""

        for package_url in packages:
            self._packages_to_purge.append(
                package.get_package_from_url(package_url))

    def set_remove(self, packages):
        """Removes packages."""

        for package_url in packages:
            self._packages_to_remove.append(
                package.get_package_from_url(package_url))

    def set_install(self, packages):
        """Installs packages."""

        for package_url in packages:
            self._packages_to_install.append(
                package.get_package_from_url(package_url))

    def _package_list(self, name, package_list, out=sys.stdout):
        if len(package_list) == 0:
            return
        print("Packages to {}:".format(name), file=out)
        print("    ", end="", file=out)
        print(*package_list, file=out)

    def print_actions(self, out=sys.stdout):
        self._package_list("purge", self._packages_to_purge, out)
        self._package_list("remove", self._packages_to_remove, out)
        self._package_list("install", self._packages_to_install, out)

    def commit(self, out=sys.stdout):
        for p in self._packages_to_purge:
            print("x Purge package {} ...".format(str(p)))
            if p.purge():
                try:
                    self._list.remove(p.get_url())
                except ValueError:
                    pass
                print("✓ Removed package {}".format(str(p)))

        for p in self._packages_to_remove:
            print("- Remove package {} ...".format(str(p)))
            if p.remove():
                try:
                    self._list.remove(p.get_url())
                except ValueError:
                    pass
                print("✓ Removed package {}".format(str(p)))

        for p in self._packages_to_install:
            print("+ Installing package {} ...".format(str(p)))
            if p.install():
                if not p.get_url() in self._list:
                    self._list.append(p.get_url())
                print("✓ Installed package {}".format(str(p)))

        write_list_to_file(self._list)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(add_help=True, description="Unip = UNIversal Package manager. \
                                        Built on top of different Linux package managers.")
    arg_parser.add_argument("-y", "--yes", action="store_true",
                            dest="yes", help="Yes to all actions. Use with caution!")
    arg_parser.add_argument("-s", "--sync", "--sync-package-list", action="store_true",
                            dest="sync", help="Syncs list of installed packages with list of packages \
                            installed with systems package manager.")
    arg_parser.add_argument("-u", "--update", "--update-cache", action="store_true",
                            dest="update", help="Update package cache. Is executed at first.")
    arg_parser.add_argument("-if", "--install-file", dest="install_file", help="Installs packages \
                            from a list of package URLs like ist is generated by unipack.", nargs="?")
    arg_parser.add_argument("-U", "--upgrade", "--upgrade-packages", action="store_true",
                            dest="upgrade", help="Upgrade packages. Is executed after update.")
    arg_parser.add_argument("-p", "--purge", nargs="+", default=[],
                            metavar="package", dest="purge",
                            help="Packages to purge. It removes the package and its configuration \
                            files. Is executed after update.")
    arg_parser.add_argument("-r", "--remove", nargs="+", default=[],
                            metavar="package", dest="remove",
                            help="Packages to remove. Is executed after purge")
    arg_parser.add_argument("-i", "--install", nargs="+", default=[],
                            metavar="package", dest="install", help="Packages to install. Is \
                            executed after remove.")
    arg_parser.add_argument("-a", "--autoremove", action="store_true",
                            dest="autoremove", help="Autoremove packages. Is executed at last.")

    args = arg_parser.parse_args()

    if getpass.getuser() != "root":
        print("You need to run unip as root.", file=sys.stderr)
        exit(1)

    unip = Unip()

    if args.update:
        print("🗘 Update package cache ...")
        unip.update()
        print("✓ Updated package cache")

    if args.sync:
        print("🗘 Sync package list ...")
        unip.sync()
        print("✓ Synced package list")

    prompt = False

    if args.autoremove:
        print("* Autoremove packages")
        prompt = True

    if not args.install_file is None:
        unip.set_install(get_list_from_file(args.install_file))
        prompt = True

    if args.upgrade:
        print("* Upgrade packages")
        prompt = True

    if len(args.purge) > 0:
        unip.set_purge(args.purge)
        prompt = True

    if len(args.remove) > 0:
        unip.set_remove(args.remove)
        prompt = True

    if len(args.install) > 0:
        unip.set_install(args.install)
        prompt = True

    if not prompt:
        exit()

    unip.print_actions()

    yes = False
    if not args.yes:
        if input("Do you really want to continue? [y/n]: ").lower() == "y":
            yes = True
    else:
        yes = True
    if yes:
        if args.upgrade:
            print("🗘 Upgrade packages ...")
            unip.upgrade()
            print("✓ Upgraded packages")
        unip.commit()
        if args.autoremove:
            print("x Autoremove packages ...")
            unip.autoremove()
            print("✓ Removed packages")
