# -*- coding: UTF-8 -*-
import argparse
import random
import time
from collections.abc import Iterable

import requests
import simpleaudio as sa
from pydub import AudioSegment
from contextlib import contextmanager
from os import chdir, getcwd, listdir, remove, makedirs
from os.path import isfile, exists, join, expanduser

import chardet
import json


def check_cache(f):
    def _wrapper(words):
        if not isinstance(words, Iterable):
            words = (words)
        for word in words:
            if not isfile(word + '.wav'):
                f([word])

    return _wrapper


def format_transfer(name, ori_format, target_format, remove_ori=False):
    """ori_format, target_format: only 'mp3' and 'wav' and supported"""
    try:
        song = getattr(AudioSegment, "from_" + ori_format)(name + "." + ori_format)
    except AttributeError:
        raise ValueError("Only 'mp3' and 'wav' format are supported")
    song.export(name + "." + target_format, format=target_format)
    if remove_ori:
        remove(name + "." + ori_format)


@check_cache
def download_audio(words, target_format='wav'):
    for word in words:
        r = requests.get(
            url='http://dict.youdao.com/dictvoice?audio=' + word + '&type=1',
            stream=True)
        with open(word + '.mp3', 'wb+') as f:
            f.write(r.content)
        format_transfer(word, 'mp3', target_format, remove_ori=True)


def play_audio(audio, wait=True, sleep=0):
    wave_obj = sa.WaveObject.from_wave_file(audio)
    play_obj = wave_obj.play()
    if wait:
        play_obj.wait_done()


def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--interval-time",
        help="the interval time (seconds) between two words (default: 1)",
        type=int,
        default=1)

    parser.add_argument(
        "-f",
        "--file",
        help="specify the origin of words (default: words.txt)",
        type=str,
        default="words.txt")

    parser.add_argument(
        "-o",
        "--output",
        help="specify a file storing words with actual order (default ans.txt)",
        type=str,
        default="ans.txt")

    parser.add_argument(
        "-cd",
        "--cache-directory",
        help="specify the directory storing cache (default cache)",
        type=str,
        default="cache")

    parser.add_argument(
        "-rd",
        "--random",
        help="play words according to the random order",
        action="store_true",
        default=False)

    parser.add_argument(
        "-s",
        "--sort",
        help="sort all the words in alphabetical order",
        action="store_true",
        default=False)

    parser.add_argument(
        "-rs",
        "--reverse-sort",
        help="sort reversely all the words in alphabetical order",
        action="store_true",
        default=False)

    parser.add_argument(
        "-no",
        "--normal-order",
        help="play words according to order of the appearance in file (default)",
        action="store_true",
        default=True)

    parser.add_argument(
        "-ro",
        "--reverse-order",
        help="play words according to reverse order of the appearance in file",
        action="store_true",
        default=False)

    return parser


@contextmanager
def change_dir(target_path):
    """A function assisting change working directory temporarily

    >>> import os
    >>> os.chdir(os.path.expanduser('~'))
    >>> os.getcwd() == os.path.expanduser('~')  # You're in your home directory now
    True
    >>> with change_dir('/usr/local'): # change working directory to '/usr/local'
    ...     print(os.getcwd())
    ...     pass # Anything you want to do in this directory
    ...
    /usr/local
    >>> os.getcwd() == os.path.expanduser('~') # You're back in your previous working directory
    True

    """
    current_path = getcwd()
    chdir(target_path)
    yield
    chdir(current_path)


def translate(s: str) -> str:
    url = 'http://fanyi.youdao.com/translate?i=%s&smartresult=dict&smartresult=rule' % s

    data = {
        'from': 'AUTO',
        'to': 'AUTO',
        'doctype': 'json',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_REALTIME',
        'TypoResult': 'false'
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                      ' AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/73.0.3683.86 Safari/537.36'
    }

    response = requests.post(url, data=data, headers=headers)
    html = response.content
    json_data = json.loads(html.decode('utf-8'))
    # print(json_data['translateResult'][0][0]['tgt'])
    return json_data['translateResult'][0][0]['tgt']


if __name__ == '__main__':
    parser = make_parser()
    args = parser.parse_args()

    with open(args.file) as f:
        lst = f.readlines()
        lst = (item.strip() for item in lst)
        lst = [item for item in lst if item != '']

    if args.random:
        random.shuffle(lst)
    elif args.reverse_order:
        lst = lst[::-1]
    elif args.sort or args.reverse_sort:
        lst = sorted(lst, reverse=args.reverse_sort)

    args.cache_directory = expanduser(args.cache_directory)
    if not exists(args.cache_directory):
        makedirs(args.cache_directory)

    with change_dir(args.cache_directory):
        download_audio(lst)
        for item in [item + '.wav' for item in lst]:
            play_audio(item)
            time.sleep(args.interval_time)

    for key, word in enumerate(lst):
        lst[key] = word + ' ' + translate(word)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write("\n".join(lst))
