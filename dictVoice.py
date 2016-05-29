from pydub import AudioSegment
import os
import requests
import simpleaudio as sa
import time

words_file = 'words.md'
interval_time = 1 # the internal time between two words

def download_audio(words):
    name_lst = []
    if type(words) not in (type([]), type(())):
        words = [words]
    for word in words:
        r = requests.get(url='http://dict.youdao.com/dictvoice?audio=' + word + '&type=2', stream=True)
        with open(word + '.mp3', 'wb+') as f:
            f.write(r.content)
        song = AudioSegment.from_mp3(word + ".mp3")
        song.export(word + ".wav", format="wav")
        os.remove(word + '.mp3')
        name_lst.append(word + '.wav')
    return name_lst


def play_audio(audio, wait=True, sleep=0):
    wave_obj = sa.WaveObject.from_wave_file(audio)
    play_obj = wave_obj.play()
    if wait:
        play_obj.wait_done()
    time.sleep(sleep)


with open(words_file) as f:
    lst = f.readlines()
    lst = [item.strip() for item in lst]
lst = download_audio(lst)
for item in lst:
    play_audio(item, sleep=interval_time)
