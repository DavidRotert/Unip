import os

def get_manual_installed():
    l = []
    with os.popen("apt-mark showmanual", "r") as out:
        for line in out:
            l.append(line.strip())
    return l

def installed(package):
    with os.popen("dpkg-query -f '${{Package}}\\n' -W {}".format(package.get_name()), "r") as out:
        for line in out:
            if line.strip() == package.get_name():
                return True
    return False

def update():
    code = os.system("apt-get -y update")
    if code == 0:
        return True
    else:
        return False

def upgrade():
    code = os.system("apt-get -y upgrade")
    if code == 0:
        return True
    else:
        return False

def purge(package):
    if not installed(package):
        return False
    code = os.system("apt-get -y purge {}".format(package.get_name()))
    if code == 0:
        return not installed(package)
    else:
        return False

def remove(package):
    if not installed(package):
        return False
    code = os.system("apt-get -y remove {}".format(package.get_name()))
    if code == 0:
        return not installed(package)
    else:
        return False

def install(package):
    if installed(package):
        return False
    code = os.system("apt-get -y install {}".format(package.get_name()))
    if code == 0:
        return installed(package)
    else:
        return False

def autoremove():
    code = os.system("apt-get -y autoremove")
    if code == 0:
        return True
    else:
        return False