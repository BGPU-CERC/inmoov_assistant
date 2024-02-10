import requests
import json

import sounddevice as sd
import soundfile as sf

import config

filename = "audio.wav"  # Путь и имя файла, под которым сохранить аудио


def text_to_speech(text="Привет друг!"):
    headers = {"Authorization": f"Bearer {config.EDEN_API_KEY}"}
    url = "https://api.edenai.run/v2/audio/text_to_speech"

    payload = {
        "providers": "microsoft",
        "language": "ru-RU",
        "option": "MALE",
        "google": "ru-RU-Standard-C",
        "text": f"{text}",
    }

    response = requests.post(url, json=payload, headers=headers)
    result = json.loads(response.text)

    audio_url = result.get("microsoft").get("audio_resource_url")
    r = requests.get(audio_url)

    with open(f"{config.SOUNDS_PATH}{filename}", "wb") as file:
        file.write(r.content)

    data, samplerate = sf.read(f"{config.SOUNDS_PATH}{filename}")
    sd.play(data, samplerate)
    sd.wait()
