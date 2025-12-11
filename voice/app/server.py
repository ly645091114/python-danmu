# app/server.py
from pathlib import Path
import io
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from .cosy_engine import CosyVoice2ZeroShot
from .utils import load_config_txt


# ----------------------------
# 路径与固定声纹设置
# ----------------------------
config = load_config_txt("config.txt")
SOURCE_ID = config.get("SOURCE_ID", "")
ROOT = Path(__file__).resolve().parents[1]
if SOURCE_ID == "":
    print("[WARN] 请选择声源！")
else:
    REF_WAV = ROOT / "source" / f"{SOURCE_ID}.wav"
    VOICE_TXT = ROOT / "source" / f"{SOURCE_ID}.txt"

    if VOICE_TXT.exists():
        REF_TEXT = VOICE_TXT.read_text(encoding="utf-8").strip()
    else:
        print(f"[WARN] 找不到 {SOURCE_ID}.txt，REF_TEXT 使用空字符串")
        REF_TEXT = ""


    # ----------------------------
    # 初始化 FastAPI
    # ----------------------------
    app = FastAPI()


    # ----------------------------
    # 数据结构：接收 JSON
    # ----------------------------
    class TTSRequest(BaseModel):
        text: str


    print("[INIT] 初始化 CosyVoice2Engine ...")
    ENGINE = CosyVoice2ZeroShot()

    print(f"[INIT] 注册固定说话人 {SOURCE_ID} ...")
    ok = ENGINE.register_speaker(
        spk_id=SOURCE_ID,
        ref_wav_path=str(REF_WAV),
        ref_text=REF_TEXT,
    )
    print("[INIT] register_speaker ok:", ok)
    assert ok, f"固定说话人注册失败，请检查 {SOURCE_ID}.wav 和 {SOURCE_ID}.txt"

    # ----------------------------
    # 核心接口：/tts_zero_shot
    # - 每次请求都传：
    #   - text: 要读的文本
    #   - ref_text: 参考音对应的文本
    #   - ref_wav: 参考音频（wav 文件）
    # ----------------------------
    @app.post("/tts")
    async def tts_zero_shot_json(req: TTSRequest):
        text = req.text

        if not text.strip():
            raise HTTPException(400, "text 不能为空")

        print("[TTS] text:", repr(text))
        print("[TTS] 使用固定参考音:", REF_WAV)

        # 调用 Zero-Shot 推理
        try:
            # 🔥 这里用 spk_id，不再每次传 ref_wav/ref_text
            audio_bytes = ENGINE.tts_with_spk(
                tts_text=text,
                spk_id=SOURCE_ID,
                text_frontend=False,   # 你可以按听感改 True/False
            )
        except Exception as e:
            print("[ERR] TTS failed:", repr(e))
            raise HTTPException(500, f"TTS 失败: {e!r}")

        return StreamingResponse(
            io.BytesIO(audio_bytes),
            media_type="audio/wav",
            headers={"Content-Disposition": 'inline; filename="tts.wav"' },
        )