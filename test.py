import os
import unittest

from dictVoice import download_audio, format_transfer


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

class FormatTransferTest(unittest.TestCase):
    def test_wrong_input_format(self):
        x = 0
        try:
            format_transfer("test", "avi", "mp3")
        except ValueError:
            x = 1
        self.assertEqual(x, 1)


if __name__ == '__main__':
    unittest.main()
