import torch
from TTS.api import TTS
import numpy as np
from pathlib import Path

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# 你的原始录音，建议 30秒~3分钟，干净、无BGM
VOICE_WAV = Path("dy_voice.wav")
OUT_EMB = Path("dy_voice_emb.npy")

def main():
    if not VOICE_WAV.exists():
        print(f"[ERROR] 找不到录音文件：{VOICE_WAV}")
        return

    print("[INFO] 加载 XTTS v2 模型（首次会比较慢）...")
    # 多语种，多数据集的 XTTS v2 模型
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

    print("[INFO] 计算说话人声纹 embedding ...")
    tts.tts_to_file(text="曾焦阳，你在干什么！", speaker_wav=f"{str(VOICE_WAV)}", language="zh", file_path="test.wav")


    print("[DONE] 声纹准备完成，可以关闭本脚本。")

if __name__ == "__main__":
    main()
