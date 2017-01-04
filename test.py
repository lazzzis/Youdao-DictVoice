import os
import unittest

from dictVoice import download_audio


def remove_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)


class DownLoadAudioTest(unittest.TestCase):
    def test_download_success(self):
        name = 'test'
        remove_file(name + ".mp3")
        remove_file(name + ".wav")
        download_audio([name])
        self.assertFalse(os.path.exists(name + ".mp3"))
        self.assertTrue(os.path.exists(name + ".wav"))


if __name__ == '__main__':
    unittest.main()
