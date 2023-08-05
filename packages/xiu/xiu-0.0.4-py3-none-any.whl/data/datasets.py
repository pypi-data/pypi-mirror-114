#!/usr/bin/env python

import os

import codefast as cf


class Urls:
    prefix = 'https://filedn.com/lCdtpv3siVybVynPcgXgnPm/corpus'


def load_spam(path: str = '/tmp/'):
    cf.info(f'Downloading English spam ham dataset to {path}')
    online_url = os.path.join(Urls.prefix, 'spam-ham.txt')
    local_path = path + 'spam-ham.txt'
    cf.net.download(online_url, local_path)


