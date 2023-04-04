#!/usr/bin/env python3

from setuptools import setup

import sys
import os
import platform

from distutils.util import execute
from distutils.dir_util import copy_tree
from distutils.file_util import copy_file
from distutils.cmd import Command
from subprocess import call
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools import setup, find_packages

readme = open("README.rst").read()
history = open("HISTORY.rst").read()

sys.executable = "/usr/bin/python3"


def udev_reload_rules():
    call(["udevadm", "control", "--reload-rules"])


def udev_trigger():
    call(
        [
            "udevadm",
            "trigger",
        ]
    )

def install_udev_rules(raise_exception):
    if check_root():
        copy_tree("udev/", "/etc/udev/rules.d/")
        copy_file("ds4drv.conf", "/etc/")
        execute(udev_reload_rules, (), "Reloading udev rules")
        execute(udev_trigger, (), "Triggering udev rules")
    else:
        msg = 'You must have root privileges to install udev rules. Run "sudo python setup.py udev_rules"'
        if raise_exception:
            raise OSError(msg)
        else:
            print(msg)



def system_daemon_reload():
    call(["systemctl", "daemon-reload"])

def system_daemon_enable_ds4drv_service():
    call(["systemctl", "enable", "ds4drv.service"])

def install_systemd_service_unit(raise_exception):
    if check_root():
        copy_file("systemd/ds4drv.service", "/lib/systemd/system/")
        execute(system_daemon_reload, (), "Reloading system daemon")
        execute(system_daemon_enable_ds4drv_service, (), "Enabling ds4drv.service")
    else:
        msg = 'You must have root privileges to install ds4drv.service. Run "sudo python setup.py systemd"'
        if raise_exception:
            raise OSError(msg)
        else:
            print(msg)


def check_root():
    return os.geteuid() == 0


def is_linux():
    return platform.system() == "Linux"


class InstallUdevRules(Command):
    description = "install udev rules (requires root privileges)"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        install_udev_rules(True)

class InstallSystemdService(Command):
    description = "install systemd service (requires root privileges)"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        install_systemd_service_unit(True)

class CustomInstall(install):
    def run(self):
        install.run(self)
        install_udev_rules(True)
        install_systemd_service_unit(True)


class CustomDevelop(develop):
    def run(self):
        develop.run(self)


setup(name="ds4drv",
      version="0.5.5",
      description="A Sony DualShock 4 userspace driver for Linux",
      url="https://github.com/chrippa/ds4drv",
      author="Christopher Rosell",
      author_email="chrippa@tanuki.se",
      license="MIT",
      long_description=readme + "\n\n" + history,
      entry_points={
        "console_scripts": [
          "ds4drv=ds4drv.__main__:main"
        ]
      },
      scripts=['scripts/ds4drv-pair'],
      packages=["ds4drv",
                "ds4drv.actions",
                "ds4drv.backends",
                "ds4drv.packages"],
      install_requires=["evdev>=0.3.0", "pyudev>=0.16"],
      classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Topic :: Games/Entertainment"
      ],
      cmdclass={
        "udev_rules": InstallUdevRules,
        "systemd": InstallSystemdService,
        "install": CustomInstall,
        "develop": CustomDevelop,
      },
)
