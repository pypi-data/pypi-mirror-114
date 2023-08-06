import pigpio
import RPi.GPIO as GPIO
import time


class ReedFan:
    __slots__ = ["rpm", "pin", "pulse", "wait_time"]

    def __init__(self):
        self.rpm = 0
        self.pin = 16
        self.pulse = 2
        self.wait_time = 1

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def subscribe_turnover(self):
        t = time.time()

        def fell(n):
            nonlocal t

            dt = time.time() - t
            if dt < 0.005:
                return

            freq = 1 / dt
            self.rpm = (freq / self.pulse) * 60
            t = time.time()

        GPIO.add_event_detect(self.pin, GPIO.FALLING, fell)


class SetFan:

    __slots__ = ["pin", "pwm"]

    def __init__(self):
        self.pin = 13
        self.pwm = pigpio.pi()
        self.pwm.set_mode(self.pin, pigpio.OUTPUT)
        self.pwm.set_PWM_frequency(self.pin, 25000)
        self.pwm.set_PWM_range(self.pin, 100)

    def set_speed(self, speed):
        self.pwm.set_PWM_dutycycle(self.pin, speed)


def get_cpu_temp():
    """
    Get temperature from cpu
    """
    with open("/sys/class/thermal/thermal_zone0/temp") as file:
        temp = float(file.read()) / 1000.00
        temp = float("%.2f" % temp)
    return temp


def get_fun_speed(temp, speed_config):
    """
    Calculate fun speed by temperature
    """
    fun_speed = 0
    for item in speed_config:
        if item.get("maxt"):
            if item["mint"] < temp <= item["maxt"]:
                fun_speed = item["speed"]
        else:
            if item["mint"] < temp:
                fun_speed = item["speed"]

    return fun_speed
