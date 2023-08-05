#!/usr/bin/env python

import codefast as cf

shared_links = {
    'Gost-Linux-64':
    'https://filedn.com/lCdtpv3siVybVynPcgXgnPm/gost-linux-amd64',
    'Gost-Darwin-64':
    'https://filedn.com/lCdtpv3siVybVynPcgXgnPm/gost-darwin-amd64',
    'Clash-Darwin-64':
    'https://filedn.com/lCdtpv3siVybVynPcgXgnPm/clash-darwin-amd64',
    'Clash-Linux-64':
    'https://filedn.com/lCdtpv3siVybVynPcgXgnPm/clash-linux-amd64',
    'demo-supervisor':
    'https://filedn.com/lCdtpv3siVybVynPcgXgnPm/demo/supervisor.conf'
}


def display_shared_links():
    for k, v in shared_links.items():
        print('{:<20}: {:<20}'.format(k, v))


