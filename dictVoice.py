import argparse
import os
import random
import time
from collections import Iterable

import requests
import simpleaudio as sa
from pydub import AudioSegment


def check_cache(f):
    def _wrapper(words):
        if not isinstance(words, Iterable):
            words = (words)
        for word in words:
            if not os.path.isfile(word + '.wav'):
                f([word])

    return _wrapper


def format_transfer(name, ori_format, target_format, remove_ori=False):
    """ori_format, target_format: only 'mp3' and 'wav' and supported"""
    try:
        song = getattr(AudioSegment, "from_" + ori_format)(name + "." + ori_format)
        song.export(name + "." + target_format, format=target_format)
        if remove_ori:
            os.remove(name + "." + ori_format)
    except AttributeError():
        raise ValueError("Only 'mp3' and 'wav' format are supported")


@check_cache
def download_audio(words, target_format='wav'):
    for word in words:
        r = requests.get(
            url='http://dict.youdao.com/dictvoice?audio=' + word + '&type=2',
            stream=True)
        with open(word + '.mp3', 'wb+') as f:
            f.write(r.content)
        format_transfer(word, 'mp3', 'target_format', remove_ori=True)


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


if __name__ == '__main__':
    parser = make_parser()
    args = parser.parse_args()

    with open(args.file) as f:
        lst = f.readlines()
        lst = (item.strip() for item in lst)
        lst = (item for item in lst if item != '')

    if args.random:
        lst = list(lst)
        random.shuffle(lst)
    elif args.reverse_order:
        lst = list(lst)[::-1]
    elif args.sort or args.reverse_sort:
        lst = sorted(lst, reverse=args.reverse_sort)

    download_audio(lst)
    for item in (item + '.wav' for item in lst):
        play_audio(item)
        time.sleep(args.interval_time)

    if args.output:
        with open(args.output, 'w+') as f:
            f.write("\n".join(lst))
