# B站批量格式化下载工具

------

## 简介

这是一个用于流程化下载bilibili视频的音频信息的工具，本工具的整体流程为：

1. **输入所需关键词 -> 相关up主uid** 
2. **选择一个up主uid输入 -> up主页所有视频的bv号**
3. **bv号 -> 视频链接信息** 
4. **视频链接 -> 音频信息** 

所有中间流程的信息都会保存至文件中，并且单个功能也可单独运行。

## 主要文件结构及介绍
```markdown
├── AudioDownloader
│   ├── data
│   │   ├── uids.txt
│   │   └──all_contents.csv
│   ├── __init__.py
│   ├── audio_downloader.py
│   ├── bvid_search.py
│   ├── README.MD
│   ├── setup.py
│   └── up_uid_search.py
```
src中包含主要功能

data中包含信息文件

若选择结构化，data中会以`data/up主id/各类信息`的结构保存，选择否则直接保存至data文件夹下，且所有信息将保存在data下的四个文件中。

可以选择使用工具爬取相关文件，也可以自己填入以获取信息。

## 业务流程图
![bilibilidown.png](bilibilidown.png)