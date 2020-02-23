#!/bin/bash

mkdir -p /var/lib/unip
mkdir -p /usr/local/lib/unip
cp -r -f * /usr/local/lib/unip
touch /var/lib/unip/packages.list
ln -s -f /usr/local/lib/unip/unip.py /usr/local/bin/unip
