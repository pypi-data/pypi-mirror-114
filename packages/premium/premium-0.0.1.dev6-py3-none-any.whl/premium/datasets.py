#!/usr/bin/env python

import os

import codefast as cf


class Urls:
    prefix = 'https://filedn.com/lCdtpv3siVybVynPcgXgnPm/corpus'


def _load(fpath: str) -> None:
    cf.info(f'Downloading {fpath}')
    online_url = os.path.join(Urls.prefix, fpath)
    cf.net.download(online_url, f'/tmp/{fpath}')


class Download:
    def douban_movie_review(self):
        '''Kaggle dataset https://www.kaggle.com/liujt14/dou-ban-movie-short-comments-10377movies'''
        cf.info(
            'Downloading douban movie review data: https://www.kaggle.com/liujt14/dou-ban-movie-short-comments-10377movies',
        )
        _load('douban_movie_review.zip')

    def douban_movie_review_2(self):
        _load('douban_movie_review2.csv.zip')

    def chinese_mnist(self):
        '''https://www.kaggle.com/fedesoriano/chinese-mnist-digit-recognizer'''
        _load('Chinese_MNIST.csv.zip')

    def toxic_comments(self):
        _load('toxic_comments.csv')


downloader = Download()


def load_icwb():
    '''Data source: http://sighan.cs.uchicago.edu/bakeoff2005/
    '''
    _load('icwb2-data.zip')


def load_news2016():
    ''' 中文新闻 3.6 GB 2016年语料 
    '''
    _load('news2016.zip')


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
