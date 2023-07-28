from pydantic import BaseModel


class Preset(BaseModel):
    name: str


class TTS(BaseModel):
    text: str
    voice: str | None = "geralt"
    preset: str = "ultra_fast"
