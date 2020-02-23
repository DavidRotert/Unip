import enum, urllib.parse
import packagemanager


class Package:
    def __init__(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def __str__(self):
        return self.get_url()

    def install(self):
        pass

    def purge(self):
        pass

    def remove(self):
        pass

    def get_url(self):
        pass

class AptPackage(Package):
    def __init__(self, name):
        super().__init__(name)

    def install(self):
        return packagemanager.apt.install(self)

    def remove(self):
        return packagemanager.apt.remove(self)

    def purge(self):
        return packagemanager.apt.purge(self)

    def get_url(self):
        return urllib.parse.urlunparse(("apt", self.get_name(), "", "", "", ""))


def get_package_from_url(name):
    url = urllib.parse.urlparse(name)
    if url.scheme == "apt" or url.scheme == "":
        pkg_name = url.netloc
        if url.scheme == "":
            pkg_name = url.path
        return AptPackage(pkg_name)
    else:
        raise ValueError("Invalid package format: {}".format(url.scheme))
