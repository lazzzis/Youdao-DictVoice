from pydub import AudioSegment
import os
import requests
import simpleaudio as sa
import time

words_file = 'words.md'
interval_time = 1 # the internal time between two words

def check_cache(f):
    def _wrapper(words):
        if type(words) not in (type([]), type(())):
            words = [words]
        for word in words:
            if not os.path.isfile(word + '.wav'):
                f([word])
    return _wrapper


@check_cache
def download_audio(words):
    for word in words:
        r = requests.get(url='http://dict.youdao.com/dictvoice?audio=' + word + '&type=2', stream=True)
        with open(word + '.mp3', 'wb+') as f:
            f.write(r.content)
        song = AudioSegment.from_mp3(word + ".mp3")
        song.export(word + ".wav", format="wav")
        os.remove(word + '.mp3')


def play_audio(audio, wait=True, sleep=0):
    wave_obj = sa.WaveObject.from_wave_file(audio)
    play_obj = wave_obj.play()
    if wait:
        play_obj.wait_done()
    time.sleep(sleep)


with open(words_file) as f:
    lst = f.readlines()
    lst = [item.strip() for item in lst]
    lst = [item for item in lst if item != '']
download_audio(lst)
for item in (item + '.wav' for item in lst):
    play_audio(item, sleep=interval_time)
