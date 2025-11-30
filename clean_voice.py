#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简单的人声清理脚本：
1. 从输入 WAV 中估计并削减背景噪音
2. 使用一组效果器对人声进行增强（噪声门 + 压缩 + EQ + 限制器）

用法：
    python clean_voice.py input.wav output.wav
    # 或指定噪声采样时长（前几秒当作“纯噪声”）
    python clean_voice.py input.wav output.wav --noise-seconds 0.5
"""

import argparse
from pathlib import Path

import numpy as np
import soundfile as sf
import noisereduce as nr
from pedalboard import (
    Pedalboard,
    NoiseGate,
    Compressor,
    HighpassFilter,
    LowShelfFilter,
    Limiter,
    Gain,
)


def load_mono_audio(path: Path):
    """加载音频并转成 mono、float32."""
    data, sr = sf.read(str(path))
    # 多声道转单声道（简单平均）
    if data.ndim > 1:
        data = data.mean(axis=1)
    # 确保是 float32
    if data.dtype != np.float32:
        data = data.astype(np.float32)
    return data, sr


def reduce_noise(y: np.ndarray, sr: int, noise_seconds: float = 0.5) -> np.ndarray:
    """
    使用 noisereduce 降噪：
    - 默认用前 noise_seconds 秒作为噪声样本
    - 如果长度不足，就退化为“自动估计噪声”模式
    """
    if noise_seconds > 0 and len(y) > int(noise_seconds * sr):
        noise_clip = y[: int(noise_seconds * sr)]
        print(f"[NR] 使用前 {noise_seconds:.2f} 秒作为噪声样本")
        y_denoised = nr.reduce_noise(
            y=y,
            sr=sr,
            y_noise=noise_clip,
            stationary=False,  # 非平稳噪声（说话/环境变化）通常效果更好
        )
    else:
        print("[NR] 音频太短，使用全局自动估计噪声")
        y_denoised = nr.reduce_noise(y=y, sr=sr, stationary=False)

    return y_denoised.astype(np.float32)


def enhance_voice(y: np.ndarray, sr: int) -> np.ndarray:
    """
    柔和自然的人声增强版本：
    - 降低压缩比
    - 放宽噪声门阈值
    - EQ 更温和
    - 避免出现刺耳、电音感
    """
    board = Pedalboard(
        [
            # 高通：去除超低频，但不要切太高
            HighpassFilter(cutoff_frequency_hz=60.0),

            # 更温和的 NoiseGate：不切掉尾音
            NoiseGate(
                threshold_db=-50.0,   # 比原来低10dB，更柔和
                ratio=2.0,            # 少压点
                attack_ms=10.0,
                release_ms=200.0,     # 延长释放时间，保留尾音
            ),

            # 更自然的压缩（低 ratio）
            Compressor(
                threshold_db=-22.0,   # 不要太激进
                ratio=1.8,            # 从 3.0 改成 1.8
                attack_ms=8.0,
                release_ms=200.0,
            ),

            # 更柔和的低频厚度
            LowShelfFilter(
                cutoff_frequency_hz=180.0,
                gain_db=1.0,          # 从 2dB 降至 1dB
            ),

            # Limiter 保持不变
            Limiter(threshold_db=-1.0),

            # 轻微增益
            Gain(gain_db=1.0),       # 原来是 3.0，这个更自然
        ]
    )

    processed = board(y, sample_rate=sr)
    return processed.astype(np.float32)



def main():
    parser = argparse.ArgumentParser(description="WAV 人声降噪 & 增强脚本")
    parser.add_argument("input", type=str, help="输入 wav 文件路径")
    parser.add_argument("output", type=str, help="输出 wav 文件路径")
    parser.add_argument(
        "--noise-seconds",
        type=float,
        default=0.5,
        help="前多少秒作为噪声样本用于估计噪声（默认 0.5 秒，可按素材调整）",
    )

    args = parser.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.output)

    if not in_path.exists():
        raise FileNotFoundError(f"找不到输入文件: {in_path}")

    print(f"[IO] 读取音频: {in_path}")
    y, sr = load_mono_audio(in_path)
    print(f"[IO] 采样率: {sr} Hz, 时长: {len(y)/sr:.2f} 秒")

    # 1. 降噪
    print("[STEP] 开始降噪 ...")
    y_denoised = reduce_noise(y, sr, noise_seconds=args.noise_seconds)

    # 2. 人声增强
    print("[STEP] 开始人声增强 ...")
    y_enhanced = enhance_voice(y_denoised, sr)

    # 3. 写出结果
    out_path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(out_path), y_enhanced, sr)
    print(f"[DONE] 已输出增强后音频: {out_path}")


if __name__ == "__main__":
    main()
