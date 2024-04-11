# B站批量格式化下载工具

------

## 简介

这是一个用于从哔哩哔哩流程化下载各类信息的工具，本工具的整体流程为：

1. **关键词 -> 相关up主** 
2. **up主信息及发布视频**
3. **视频信息** 
4. **视频相关文件** 

所有中间流程的信息都会保存至文件中，并且单个功能也可单独运行。

## 主要文件结构及介绍
```markdown
├── BilibiliDownloader
│   ├── data
│   │   ├── mid
│   │   │   ├── mid_bv_info.json
│   │   │   └──mid_bv_list.csv
│   │   ├── bv_info.json
│   │   ├── bv_list.csv
│   │   ├── up_info.json
│   │   └── up_list.csv
│   ├── src
│   │   ├── AudioDownloader.py
│   │   ├── UPDownloader.py
│   │   ├── UPSearch.py
│   │   ├── __init__.py
│   │   └── proxy_check.py
│   ├── config.yaml
│   └── README.md
```
src中包含主要功能

data中包含信息文件

若选择结构化，data中会以`data/up主id/各类信息`的结构保存，选择否则直接保存至data文件夹下，且所有信息将保存在data下的四个文件中。

可以选择使用工具爬取相关文件，也可以自己填入以获取信息。

## 安装

1. 克隆或下载此存储库到本地计算机。
2. 安装先决条件中提到的所需Python包。

## 用法

1. 根据需求修改config.yaml中的配置：
   - `bv_list_file`：包含BVID列表的文件路径。
   - `bv_info_file`：存储获取到的视频信息的文件路径。
   - `up_list_file`：存储获取到的up主id
   - `up_info_file`：存储获取到的up主信息
   - `download_dir`：下载的文件将保存的目录路径。

2. 使用以下命令运行脚本

```
python UPSearch.py
python UPDownloader.py
python AudioDownloader.py
```

也可以指定下面提到的可选参数。

### 可选参数

- UPSearch.py
  ```python
  --keyword //获取
  --order
  --pages
  --up_list_file
  ```

- UPDownloader.py
  ```python
  --mid
  --pages
  --up_list_file
  --up_info_file
  --structured
  ```

- AudioDownloader.py
  ```python
  --bv_list_file //包含BVID列表的文件路径
  --bv_info_file //存储获取到的信息的文件路径
  --download_dir //下载的音频文件将保存在的目录路径
  --structured //选择是否下载结构化的
  ```

## 注意事项

- 请确保您遵守哔哩哔哩的API使用政策，以避免出现任何问题。
- 该脚本的运行时间可能会较长，具体取决于要下载的音频文件数量和哔哩哔哩的API响应时间。

## 免责声明

本脚本仅供教育和个人使用。开发人员对本脚本的任何滥用或未经授权的使用不负责任。