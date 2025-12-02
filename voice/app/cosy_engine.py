# app/cosy_engine_zero_shot.py
import sys
from pathlib import Path
import io
from typing import Optional

import torch
import torchaudio

ROOT = Path(__file__).resolve().parents[1]
COSY_ROOT = ROOT / "CosyVoice"
sys.path.append(str(COSY_ROOT / "third_party" / "Matcha-TTS"))
sys.path.append(str(COSY_ROOT))

from cosyvoice.cli.cosyvoice import CosyVoice2
from cosyvoice.utils.file_utils import load_wav


class CosyVoice2ZeroShot:
    """
    ✔ 不注册说话人
    ✔ 不写 spkinfo
    ✔ 每次请求都传 reference_wav + reference_text
    ✔ 完全等价官方 demo 的“零样本克隆”
    """

    def __init__(
        self,
        model_dir="pretrained_models/CosyVoice2-0.5B",
        device=None,
    ):
        model_path = ROOT / model_dir

        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"

        self.device = device
        self.cosy = CosyVoice2(
            str(model_path),
            load_jit=False,
            load_trt=False,
            load_vllm=False,
            fp16=(device == "cuda"),
        )
        self.sample_rate = self.cosy.sample_rate

    def tts(
        self,
        tts_text: str,
        ref_text: str,
        ref_wav_path: str,
        text_frontend=True,   # 官方推荐 False
    ) -> bytes:
        """
        完美等价官方示例：
        for i,j in enumerate(cosyvoice.inference_zero_shot(tts, ref_text, prompt_speech)):
            ...
        """

        # 加载参考音
        speech_16k = load_wav(ref_wav_path, 16000)

        # 自动截断 30 秒（内部限制）
        max_len = 16000 * 30
        if speech_16k.shape[1] > max_len:
            speech_16k = speech_16k[:, :max_len]

        # 直接 zero-shot 推理（官方模式）
        chunks = self.cosy.inference_zero_shot(
            tts_text,
            ref_text,
            speech_16k,
            stream=False,
            text_frontend=text_frontend,
        )

        # 拼接 chunks → WAV 字节
        wavs = [c["tts_speech"] for c in chunks]
        full = torch.cat(wavs, dim=-1)

        buf = io.BytesIO()
        torchaudio.save(buf, full.cpu(), self.sample_rate, format="wav")
        buf.seek(0)
        return buf.read()
    
    def register_speaker(
        self,
        spk_id: str,
        ref_wav_path: str,
        ref_text: str,
    ) -> bool:
        """
        注册 zero-shot 说话人：
        - ref_wav_path: 参考音频（16k）
        - ref_text: 参考音对应文本
        """
        speech_16k = load_wav(ref_wav_path, 16000)
        max_len = 16000 * 30
        if speech_16k.shape[1] > max_len:
            speech_16k = speech_16k[:, :max_len]

        ok = self.cosy.add_zero_shot_spk(ref_text, speech_16k, spk_id)
        print(f"[ENGINE] add_zero_shot_spk({spk_id}) -> {ok}")

        if ok:
            self.cosy.save_spkinfo()
            self.default_spk_id = spk_id

        return bool(ok)
    
    def tts_with_spk(
        self,
        tts_text: str,
        spk_id: Optional[str] = None,
        text_frontend: bool = True,
    ) -> bytes:
        """
        用已经注册好的 spk_id 合成：
        - 如果 spk_id None，使用 default_spk_id
        """
        if spk_id is None:
            if self.default_spk_id is None:
                raise RuntimeError("尚未注册默认说话人")
            spk_id = self.default_spk_id

        chunks = self.cosy.inference_zero_shot(
            tts_text,
            "",   # prompt_text 留空
            "",   # prompt_speech 留空
            zero_shot_spk_id=spk_id,
            stream=False,
            text_frontend=text_frontend,
        )

        # 拼接 chunks → WAV 字节
        wavs = [c["tts_speech"] for c in chunks]
        full = torch.cat(wavs, dim=-1)

        buf = io.BytesIO()
        torchaudio.save(buf, full.cpu(), self.sample_rate, format="wav")
        buf.seek(0)
        return buf.read()