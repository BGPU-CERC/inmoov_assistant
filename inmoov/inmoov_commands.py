from server.api import api
from inmoov import servo_config

from opencv.face_tracking import FaceTracker
from inmoov.idle_controller import IdleController
from voice.voice_controller import VoiceController

face_track = None
idle = None
voice_control = None


def serial_open():
    api.open_serial()


def servo_attach():
    api.attach_servo()


def set_config_pose(config, speed):
    api.set_config_pose(config, speed)


def servo_power(state):
    api.set_servo_power(state)


def set_led_state(state):
    api.set_led_state(state)


def servo_dafault():
    set_config_pose(servo_config.all_servo, 50)


def run_face_tracking(mode):
    global face_track
    if face_track is None:
        face_track = FaceTracker()

    if mode:
        face_track.start_video_tracking()
    else:
        set_config_pose(servo_config.head_servo, 20)
        face_track.stop_video_tracking()
        face_track = None


def run_idle_animation(mode):
    global idle
    if idle is None:
        idle = IdleController()

    if mode:
        idle.start_idle_animation()
    else:
        idle.stop_idle_animation()
        idle = None


def run_voice_control(mode):
    global voice_control
    if voice_control is None:
        voice_control = VoiceController()

    if mode:
        voice_control.start_voice_control()
    else:
        voice_control.stop_voice_control()
        voice_control = None
