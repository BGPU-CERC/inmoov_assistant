from pvrecorder import PvRecorder
import config
import pvporcupine

# PORCUPINE
porcupine = pvporcupine.create(
    access_key=config.PICOVOICE_TOKEN, keywords=["computer"], sensitivities=[1]
)

try:
    rec = PvRecorder(
        device_index=config.MICROPHONE_INDEX, frame_length=porcupine.frame_length
    )
except Exception as err:
    print(f"Микрофон не найден. Unexpected {err=}")
