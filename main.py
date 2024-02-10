import time

from rich import print

from inmoov import inmoov_commands
from inmoov import led_commands


def init_inmoov():
    inmoov_commands.servo_power(0)
    inmoov_commands.serial_open()
    time.sleep(1)
    inmoov_commands.servo_attach()
    time.sleep(1)
    inmoov_commands.servo_power(1)
    inmoov_commands.set_led_state(led_commands.COLOR_WIPE)
    inmoov_commands.run_voice_control(True)
    print(f"Inmoov assistent run")


init_inmoov()
