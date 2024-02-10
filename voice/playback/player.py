import simpleaudio as sa
import os

import config
import voice.recorder as recorder


# some consts
CDIR = os.getcwd()


def play(phrase, wait_done=True):
    global recorder
    filename = f"{CDIR}{config.SOUNDS_PATH_PLAYER}"

    if phrase == "greet":  # for py 3.8
        filename += "greet.wav"
    elif phrase == "not_found":
        filename += "not_found.wav"

    if wait_done:
        recorder.rec.stop()

    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()

    if wait_done:
        play_obj.wait_done()
        recorder.rec.start()
