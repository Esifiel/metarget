"""
Package List Downloader
"""

import yaml
from bs4 import BeautifulSoup
import requests
import json
import config
import re

import utils.color_print as color_print


def filter_name_by_regex(name):
    regexs = [
        r'linux-headers-.*-generic.*amd64.deb',
        r'linux-headers-.*all.deb',
        r'linux-image-.*-generic.*amd64.deb',
        r'linux-modules-.*-generic.*amd64.deb',
        r'amd64/linux-headers-.*-generic.*amd64.deb',
        r'amd64/linux-headers-.*all.deb',
        r'amd64/linux-image-.*-generic.*amd64.deb',
        r'amd64/linux-modules-.*-generic.*amd64.deb',
    ]
    for regex in regexs:
        if re.match(regex, name):
            return True
    return False


def download_package_list():
    color_print.debug('Downloading kernel package list')
    r = requests.get(config.ubuntu_kernel_repo)
    soup = BeautifulSoup(r.text, 'html.parser')
    version_table = soup.table
    tr_all = version_table.find_all("tr")
    kernels = [tr.a.get_text()
               for tr in tr_all[4:-1] if tr.a.get_text().startswith('v')]
    packages = dict()
    for kernel in kernels:
        color_print.debug('Downloading info for kernel %s' % kernel)
        r = requests.get(config.ubuntu_kernel_repo + kernel)
        soup = BeautifulSoup(r.text, 'html.parser')
        hyperlinks = soup.find_all('a')
        package_links = set(entry.get_text() for entry in hyperlinks)
        package_links = [(config.ubuntu_kernel_repo + kernel + entry)
                         for entry in package_links if filter_name_by_regex(entry)]
        packages[kernel] = package_links
        color_print.debug('Kernel info downloaded:')
        color_print.debug(json.dumps(package_links))
    with open(config.kernel_packages_list, 'w') as f:
        yaml.dump(packages, f)


if __name__ == '__main__':
    download_package_list()
