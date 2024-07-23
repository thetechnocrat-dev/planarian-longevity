from gpiozero import LED
import signal

# Setup the pins
led1 = LED(17)
led2 = LED(27)

# Turn on the LEDs
led1.on()
led2.on()

# Signal pause (keeps script running indefinitely)
signal.pause()
