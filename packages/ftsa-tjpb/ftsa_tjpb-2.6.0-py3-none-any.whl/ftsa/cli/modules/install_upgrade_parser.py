import os
import platform
from ftsa.cli.modules.properties import DEPENDENCIES


BROWSERS = [
    'firefox',
    'chrome',
    'opera'
]


def run(up):
    for dependency in DEPENDENCIES:
        os.system(f'pip install {"--upgrade " if up else ""}{dependency}')
    for browser in BROWSERS:
        os.system(f'webdrivermanager {browser}')
    if platform.system() in 'Windows':
        os.system(f'webdrivermanager edge')
        os.system(f'webdrivermanager ie')
    os.system('npm install -g allure-commandline')
    os.system('npm install -g appium')


def install(args):
    run(False)


def upgrade(args):
    run(True)


def uninstall(args):
    for dependency in DEPENDENCIES:
        os.system(f'pip uninstall -y {dependency}')
    os.system(f'pip uninstall -y ftsa-tjpb')
