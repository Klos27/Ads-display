import RPi.GPIO as GPIO
import os
import time
import threading

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.OUT)
GPIO.output(24, 1)  # Turn off realy
os.system('killall -9 omxplayer.bin')

relay = 0  # realy turned off
timeout = 0


def movies():
    """Thread omxplayer function"""
    print('Play the movie')
    time.sleep(2)  # Wait until monitor turns on -- type there amount of seconds you need
    os.system('omxplayer --loop -o hdmi --blank --vol -200 --no-osd /home/pi/Videos/*')
    print("Kill the movie")
    return


try:
    while True:
        if (GPIO.input(23) == 0):
            if (relay == 0):
                timeout = time.perf_counter()
                print("Motion detected : ", timeout)
                relay = 1
                t = threading.Thread(target=movies)
                t.start()
                GPIO.output(24, 0)  # Turn on relay
            timeout = time.perf_counter()
        else:
            if relay == 1:
                if time.perf_counter() - timeout > 30:  # type there how many seconds screen should display ads while end of detection
                    print("End of motion detection : ", timeout)
                    print("Measured time : ", time.perf_counter())
                    relay = 0
                    GPIO.output(24, 1)  # Turn off realy
                    time.sleep(2)
                    os.system('killall -9 omxplayer.bin')

except KeyboardInterrupt:  # trap a CTRL+C keyboard interrupt
    print("Script end")
    os.system('killall -9 omxplayer.bin')
    GPIO.cleanup()  # resets all GPIO ports used by this script
