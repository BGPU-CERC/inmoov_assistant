import json
import os
import struct
import time

import yaml
from fuzzywuzzy import fuzz

from rich import print

from inmoov import inmoov_commands
from inmoov import led_commands
from commands import commands

from speech import tts_eden
from recognition import stt
from playback import player
import recorder

# some consts
CDIR = os.getcwd()
VA_CMD_LIST = yaml.safe_load(
    open("commands/commands.yaml", "rt", encoding="utf8"),
)


def va_respond(voice: str):
    print(f"Распознано: {voice}")

    cmd = commands.recognize_cmd(voice)

    # for i in VA_CMD_LIST.keys():
    #     print(i)

    print(cmd)

    if len(cmd["cmd"].strip()) <= 0:
        return False
    elif cmd["percent"] < 70 or cmd["cmd"] not in VA_CMD_LIST.keys():
        if fuzz.ratio(voice.join(voice.split()[:1]).strip(), "скажи") > 75:
            # response = gpt_answer()
            response = voice[5:]  # - слово "скажи"

            recorder.rec.stop()
            tts_eden.text_to_speech(response)
            time.sleep(0.5)
            recorder.rec.start()
            return False
        else:
            player.play("not_found")
            time.sleep(1)

        return False
    else:
        commands.execute_cmd(cmd["cmd"], voice)
        return True


def init_inmoov():
    inmoov_commands.serial_open()
    time.sleep(1)
    inmoov_commands.servo_attach()
    time.sleep(1)
    inmoov_commands.servo_power(1)
    inmoov_commands.set_led_state(led_commands.COLOR_WIPE)
    print(f"Inmoov assistent run")


recorder.rec.start()
print("Using device: %s" % recorder.rec.selected_device)

init_inmoov()

ltc = time.time() - 1000

while True:
    try:
        pcm = recorder.rec.read()
        keyword_index = recorder.porcupine.process(pcm)

        if keyword_index >= 0:
            inmoov_commands.set_led_state(led_commands.RAINBOW)
            recorder.rec.stop()
            print("Keyword recognized")
            recorder.rec.start()  # prevent self recording
            ltc = time.time()

        while time.time() - ltc <= 4:
            pcm = recorder.rec.read()
            sp = struct.pack("h" * len(pcm), *pcm)

            if stt.kaldi_rec.AcceptWaveform(sp):
                if va_respond(json.loads(stt.kaldi_rec.Result())["text"]):
                    ltc = time.time()

                break
        inmoov_commands.set_led_state(led_commands.COLOR_WIPE)

    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
