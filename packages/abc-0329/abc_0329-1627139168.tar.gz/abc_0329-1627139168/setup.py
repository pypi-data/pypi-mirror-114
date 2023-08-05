#!/usr/bin/env python
# coding: utf-8

from setuptools import setup
import datetime
import sys


def GetCurrentOS():
    temp = sys.platform
    if temp == 'win32':
        return 'Windows'
    if temp == 'cygwin':
        return 'Cygwin'
    if temp == 'darwin':
        return 'Mac'
    return 'Linux'


def GetVersion():
    try:
        with open('./version', 'r') as f:
            version = f.read()
    except:
        now_time = datetime.datetime.now()
        version = "%s.%s.%s" % (
            now_time.strftime('%y') + now_time.strftime('%m'),
            now_time.strftime('%d') + now_time.strftime('%H'),
            now_time.strftime('%M') + now_time.strftime('%S'))

        now_time = int(datetime.datetime.now().timestamp())
        version = str(now_time)
    return version


print(GetCurrentOS())
if GetCurrentOS() == 'Windows':
    v2ray = 'v2ray_runtime_windows'
    caddy = 'caddy_runtime_windows'
else:
    v2ray = 'v2ray_runtime_linux'
    caddy = 'caddy_runtime_linux'

setup(name='abc_0329',
      version=GetVersion(),
      author='abc',
      include_package_data=True,
      zip_safe=False,
      url="https://pypi.org/",
      author_email='',
      python_requires=">=3.3",
      packages=['uif_client'],
      license="MIT",
      install_requires=[v2ray, caddy, 'fire', 'psutil'])
