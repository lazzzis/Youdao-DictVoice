# DictVoice

从 [youdao.com]() 获取单词的音频，可以用于简单的听写

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

其他: [https://ffmpeg.org/download.html]()

# 使用方法

在当前目录建立一个文件，名为 words.md。文件中每个单词一行。

执行文件

```
python3 dictVoice.py
```

# 参数更改

打开文件，可在文件开头（前10行）中看到两个参数：

- interval_time: 两个单词声音之间的间隙，默认为 1，单位为秒，即一个单词读完后，停顿一秒后在读下一个单词
- words_file: 读取单词的文件的名字，默认为 "words.md"

# 删除下载的文件

因为是将音频文件获取到本地后再播放，因此在执行文件后会在本地留下音频文件。可以用一条命令全部删除：

```
rm *.wav
```

