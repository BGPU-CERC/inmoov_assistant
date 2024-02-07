import os
import time
import yaml
from fuzzywuzzy import fuzz
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL

from playback import player
import config
from inmoov import inmoov_commands

CDIR = os.getcwd()
VA_CMD_LIST = yaml.safe_load(
    open("commands/commands.yaml", "rt", encoding="utf8"),
)


def recognize_cmd(voice: str):
    cmd = filter_cmd(voice)
    rc = {"cmd": "", "percent": 0}
    for c, v in VA_CMD_LIST.items():
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > rc["percent"]:
                rc["cmd"] = c
                rc["percent"] = vrt

    return rc


def filter_cmd(raw_voice: str):
    cmd = raw_voice

    for x in config.VA_ALIAS:
        cmd = cmd.replace(x, "").strip()

    for x in config.VA_TBR:
        cmd = cmd.replace(x, "").strip()

    return cmd


def execute_cmd(cmd: str, voice: str):
    if cmd == "sound_off":
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMute(1, None)

    elif cmd == "sound_on":
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMute(0, None)

    elif cmd == "mk_on":
        inmoov_commands.serial_open()

    elif cmd == "servo_attach":
        inmoov_commands.servo_attach()

    elif cmd == "face_tracking_on":
        inmoov_commands.face_tracking(True)

    elif cmd == "face_tracking_off":
        inmoov_commands.face_tracking(False)

    elif cmd == "servo_power_on":
        inmoov_commands.servo_power(1)

    elif cmd == "servo_power_off":
        inmoov_commands.servo_power(0)

    elif cmd == "servo_default":
        inmoov_commands.servo_dafault()

    elif cmd == "power_off":
        player.play("off", True)
        inmoov_commands.servo_power(0)

        # recorder.porcupine.delete()
        exit(0)
