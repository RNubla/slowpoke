from typing import Union

from fastapi import FastAPI

import base64
import io
from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_voices
import torchaudio


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/tts/")
async def tts(text: str):
    tts = TextToSpeech()
    voice_samples, conditioning_latents = load_voices(["random"])
    gen, dbg_state = tts.tts_with_preset(
        text,
        speaking_rate=1.0,
        k=1,
        voice_samples=voice_samples,
        conditioning_latents=conditioning_latents,
        preset="fast",
        use_deterministic_seed=None,
        return_deterministic_state=True,
        cvvp_amount=0,
    )
    buffer = io.BytesIO()

    if isinstance(gen, list):
        for j, g in enumerate(gen):
            torchaudio.save(buffer, g.squeeze(0).cpu(), 24000, format="wav")
    else:
        torchaudio.save(buffer, gen.squeeze(0).cpu(), 24000, format="wav")

    b64bytes: bytes = base64.b64encode(buffer.getvalue())
    b64string = f'data:audio/wav;base64,{b64bytes.decode("ascii")}'
    return {"base64wav": b64string}
