# 斗鱼/虎牙高能弹幕人声模仿工具

## 准备工作(开发者可以忽略)

[下载并且安装git(期间选项都不用管一路next到完成)](https://github.com/git-for-windows/git/releases/download/v2.52.0.windows.1/Git-2.52.0-64-bit.exe)

[下载并且安装python3.11(如果电脑没有装过的时候需要钩上"Add python.exe to PATH")](https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe)

[下载并安装visualstudio, 安装时选择大模块选第一项C++后安装](https://visualstudio.microsoft.com/zh-hans/thank-you-downloading-visual-studio/?sku=Community&channel=Stable&version=VS18&source=VSLandingPage&cid=2500&passive=false)

## 拉取 CosyVoice 模型

以下操作需要开启梯子

powershell cd ./voice

```
git clone --recursive https://github.com/FunAudioLLM/CosyVoice.git

mkdir -p pretrained_models

git lfs install

git clone https://www.modelscope.cn/iic/CosyVoice2-0.5B.git pretrained_models/CosyVoice2-0.5B
```

#### 如果你是 RTX50系以上的显卡 voice/CosyVoice/requirements.txt

```
--extra-index-url https://download.pytorch.org/whl/cu121 #需要将cu121改成cu128
...
torch==2.3.1 #需要将 2.3.1 改成 2.7.1
torchaudio==2.3.1#需要将 2.3.1 改成 2.7.1
```

## 直播相关的配置

danmu/config.txt

```
PLATFORM = huya #平台 douyu/huya
ROOM_ID = 142816 #房间号
OBS_WS_HOST = 127.0.0.1
OBS_WS_PORT = 8765
USE_SOCKS_PROXY = False
TTS_API_URL = http://127.0.0.1:9522/tts
MIN_PRICE=0 #高能弹幕/上电视 播报最小播放金额
MAX_PRICE=10 #高能弹幕/上电视 播报最大播放金额(如果没有限制写0)
SPEAK_TXT=normal,highenergy #播报类型 normal:普通弹幕, gift:谢礼物,  highenergy:上电视/高能弹幕
GIFT_MIN_PRICE=100 #谢礼物的最小金额 仅虎牙平台生效
GIFT_MAX_PRICE=500 #谢礼物的最大金额(如果没有限制写0) 仅虎牙平台生效
```

## 人声模型的相关配置

voice/config.txt

```
# 如果有自己想用的原声需要提供一段30秒以内的 .wav文件音频和音频完整文案（断句用空格）的 .txt文件，放入source文件夹下，命名格式必须和 SOURCE_ID 一致例如:dy.txt ,dy.wav
SOURCE_ID=fy #声源id
```

## 如何启动

运行 danmu/run_danmu.py

运行 voice/run_voice.py
