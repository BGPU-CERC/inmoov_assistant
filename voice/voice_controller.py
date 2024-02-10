import threading
import os
import time
import json

from fuzzywuzzy import fuzz
import yaml
import struct

from rich import print

from voice.commands import commands
from voice.recognition import stt
from voice.speech import tts_eden
import voice.recorder as recorder
from voice.playback import player

from inmoov import inmoov_commands
from inmoov import led_commands
import config

# some consts
CDIR = os.getcwd()
VA_CMD_LIST = yaml.safe_load(
    open(config.CMD_LIST_PATH, "rt", encoding="utf8"),
)


class VoiceController:
    def __init__(self):
        recorder.rec.start()
        print("Using device: %s" % recorder.rec.selected_device)
        self.thread = None
        self.is_voice_control_enabled = False

    @staticmethod
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

    def process_voice_control(self):
        self.is_voice_control_enabled = True
        ltc = time.time() - 1000

        while self.is_voice_control_enabled:
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
                        if self.va_respond(json.loads(stt.kaldi_rec.Result())["text"]):
                            ltc = time.time()

                        break
                inmoov_commands.set_led_state(led_commands.COLOR_WIPE)

            except Exception as err:
                print(f"Unexpected {err=}, {type(err)=}")
                raise

    def start_voice_control(self):
        self.thread = threading.Thread(target=self.process_voice_control)
        self.thread.start()

    def stop_voice_control(self):
        self.is_voice_control_enabled = False
        self.thread.join()
