import torchaudio
from tortoise.api import TextToSpeech

from tortoise.utils.audio import load_voice
from Models.TTSModel import TTS
import io
import base64


def init():
    print("Running init()")

    global model

    model = TextToSpeech()

    print("Finished running `init()` in `app.py`. Waiting for an `interface()` call.")


def inference(data: TTS):
    global model

    # Prep the model
    voice_samples, conditioning_latents = load_voice(data.voice)

    # if voice_samples is None:
    #     raise HTTPException(status_code=404, detail="Voice was not found")

    # Run the model

    gen = model.tts_with_preset(
        data.text,
        voice_samples=voice_samples,
        conditioning_latents=conditioning_latents,
        preset=data.preset,
    )

    # Save the audio file as base64
    buffer = io.BytesIO()

    torchaudio.save(buffer, gen.squeeze(0).cpu(), 24000, format="wav")

    b64bytes: bytes = base64.b64encode(buffer.getvalue())
    b64string = f'data:audio/wav;base64,{b64bytes.decode("ascii")}'

    # output
    return b64string
