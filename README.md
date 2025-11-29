# 直播间互动内容

## 准备工作

### Windows
- [下载 ffmpeg](https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip)
- [下载 python 3.10.11](https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe)
- [下载 生成工具](https://visualstudio.microsoft.com/zh-hans/visual-cpp-build-tools/)
- 下载完成运行 vs_BuildTools.exe
- 安装时选择 “使用 C++ 的桌面开发（Desktop development with C++）

## 如何使用

```
python run_douyu.py

HTTP_PROXY= HTTPS_PROXY= ALL_PROXY= python douyu_obs_overlay.py
```