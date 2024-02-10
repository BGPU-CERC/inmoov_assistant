import vosk
import queue
import sys

import config

# VOSK
model = vosk.Model("voice/recognition/model_small")
samplerate = 16000
device = config.MICROPHONE_INDEX
kaldi_rec = vosk.KaldiRecognizer(model, samplerate)
q = queue.Queue()
# `-1` is the default input audio device.


# Not use
def q_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))
