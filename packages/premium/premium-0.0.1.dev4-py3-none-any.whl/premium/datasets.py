#!/usr/bin/env python

import os

import codefast as cf


class Urls:
    prefix = 'https://filedn.com/lCdtpv3siVybVynPcgXgnPm/corpus'


def _load(fpath: str) -> None:
    cf.info(f'Downloading {fpath}')
    online_url = os.path.join(Urls.prefix, fpath)
    cf.net.download(online_url, f'/tmp/{fpath}')


def load_msr_training():
    _load('msr_training.utf8')


def load_realty():
    import getpass
    cf.info("Download real estate dataset realty.csv")
    _load('realty.zip')
    passphrase = getpass.getpass('Type in your password: ').rstrip()
    cf.utils.shell(f'unzip -o -P {passphrase} /tmp/realty.zip -d /tmp/')


def load_spam(path: str = '/tmp/'):
    cf.info(f'Downloading English spam ham dataset to {path}')
    online_url = os.path.join(Urls.prefix, 'spam-ham.txt')
    local_path = path + 'spam-ham.txt'
    cf.net.download(online_url, local_path)


def load_spam_cn(path: str = '/tmp/'):
    cf.info(f'Downloading Chinese spam ham dataset to {path}')
    zipped_data = os.path.join(Urls.prefix, 'spam_cn.zip')
    label_file = os.path.join(Urls.prefix, 'spam_cn.json')
    cf.net.download(zipped_data, '/tmp/tmp_spam.zip')
    cf.utils.shell('unzip -o /tmp/tmp_spam.zip -d /tmp/')
    cf.net.download(label_file, '/tmp/spam_cn.json')
