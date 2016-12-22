# DictVoice

从 [youdao.com](http://youdao.com) 获取单词或词组的音频并自动播放，可以用于简单的听写

# 安装

clone 到本地

```
git clone https://github.com/lazzzis/Youdao-DictVoice.git
```

安装依赖

```
pip3 install < requirements.txt
```

安装 ffmeg

mac :

```
brew install ffmpeg
```

其他系统: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

# 使用方法

在当前目录建立一个文件，名为 words.txt. 文件中每个单词一行。

执行文件

```
python3 dictVoice.py
```

# 可選參數

```bash
usage: dictVoice.py [-h] [-v INTERVAL_TIME] [-f FILE] [-o OUTPUT] [-rd] [-s]
                    [-rs] [-no] [-ro]

optional arguments:
  -h, --help            show this help message and exit
  -v INTERVAL_TIME, --interval-time INTERVAL_TIME
                        the interval time (seconds) between two words
                        (default: 1)
  -f FILE, --file FILE  specify the origin of words (default: words.txt)
  -o OUTPUT, --output OUTPUT
                        specify a file storing words with actual order
                        (default ans.txt)
  -rd, --random         play words according to the random order
  -s, --sort            sort all the words in alphabetical order
  -rs, --reverse-sort   sort reversely all the words in alphabetical order
  -no, --normal-order   play words according to order of the appearance in
                        file (default)
  -ro, --reverse-order  play words according to reverse order of the
                        appearance in file
```

```bash
usage: dictVoice.py [-h] [-v INTERVAL_TIME] [-f FILE] [-o OUTPUT] [-rd] [-s]
                    [-rs] [-no] [-ro]

optional arguments:
  -h, --help            显示帮助
  -v INTERVAL_TIME, --interval-time INTERVAL_TIME
                        播放两个单词之间的时长，默认为 1 秒
  -f FILE, --file FILE  指定单词的输入文本源，默认为"words.txt"
  -o OUTPUT, --output OUTPUT
                        指定文件用于存储单词（以实际播放的顺序为准），默认为"ans.txt"
  -rd, --random         随机顺序播放单词
  -s, --sort            以字典序排列所有单词
  -rs, --reverse-sort   以字典序逆序排列所有单词
  -no, --normal-order   根据文件中实际顺序播放单词（默认）
  -ro, --reverse-order  根据文件中实际顺序的逆序播放单词
```

# 删除下载的文件

因为是将音频文件获取到本地后再播放，因此在执行文件后会在本地留下音频文件。这些文件属于 **缓存文件** ，每次下载音频前，程序都会检查一遍所需单词的音频文件是否已经在当前文件夹了，如果已经在了，则不会重复下载，否则会下载音频文件。如果要删除，可以用一条命令全部删除：

```
rm *.wav
```

## TODO

- [ ] add test
