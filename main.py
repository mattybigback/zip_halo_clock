from microbit import pin8, pin14, sleep, button_a, button_b, display
from neopixel import NeoPixel
import kitronic
from math import floor

AUDIBLE_TICK = False

num_pixels = 60
marker_colour = [0x0F, 0x00, 0x00]  # Hex color - red, green and blue
seconds_colour = [0x0F, 0x0F, 0x0F]
hours_am_colour = [0x00, 0x07, 0x0f]
hours_pm_colour = [0x00, 0x00, 0x17]
minutes_colour = [0x00, 0x0F, 0x00]

ring = NeoPixel(pin8, num_pixels)
rtc = kitronic.KitronikRTC()

def setup():
    rtc.setTime(17,40,15)
    pin14.set_analog_period_microseconds(10000)


def markers():
    MARKERS = (0,5,10,15,20,25,30,35,40,45,50,55)
    for i in MARKERS:
        ring[i] = marker_colour

def clear_ring():
    ring.clear()
    
def tick(time):
    if AUDIBLE_TICK is True:
        pin14.write_analog(256)
    seconds_led = time[2]
    minutes_led = time[1]
    hours_led, pm = calc_hour_led(time[0], time[1])
    clear_ring()
    markers()
    if pm == 1:
        ring[hours_led]=hours_pm_colour
    else:
        ring[hours_led]=hours_am_colour
    ring[minutes_led]=minutes_colour
    ring[seconds_led]=seconds_colour
    ring.show()
    if AUDIBLE_TICK is True:
        sleep(5)
        pin14.write_analog(0)

def calc_hour_led(hour, minute):
    if hour >= 12:
        return ((hour-12)*5+floor(minute/12),1)
    return (hour*5+floor(minute/12),0)

def check_time():
    rtc.readValue()
    return (rtc.currentHours, rtc.currentMinutes, rtc.currentSeconds)

def set_time_mode():
    sleep(300)
    SET_TIME_MODE = True
    press_count = 0
    while SET_TIME_MODE is True:
        if button_a.is_pressed():
            print(press_count)
            press_count += 1
            if press_count == 1:
                display.scroll("H")
            if press_count == 2:
                display.scroll("M")
            if press_count == 3:
                display.scroll("S")
            if press_count == 4:
                return




def main():
    display.clear()
    DISPLAY_CLOCK = True
    ticks = 0
    time_now = check_time()
    while DISPLAY_CLOCK is True:
        if time_now != check_time():
            time_now = check_time()
            tick(time_now)
            if button_a.is_pressed() and button_b.is_pressed():
                ticks += 1
            if ticks >= 2:
                set_time_mode()
                ticks = 0

setup()
main()

