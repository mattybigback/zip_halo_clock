from microbit import pin8, pin14, sleep, button_a, button_b, display
from neopixel import NeoPixel
from math import floor
import MCP7940N as rtc


TICK_SND = True

NUM_PIXELS = 60
mark_col = [0x0F, 0, 0]
sec_col = [0x0F, 0x0F, 0x0F]
hr_am_col = [0, 0x0f, 0x0f]
hr_pm_col = [0, 0, 0x17]
min_col = [0, 0x0F, 0]

ring = NeoPixel(pin8, NUM_PIXELS)
rtc = rtc.MCP7940N()

def setup():
    rtc.setTime(0,0,0)
    pin14.set_analog_period_microseconds(10000)


def markers():
    MARKS = (0,5,10,15,20,25,30,35,40,45,50,55)
    for i in MARKS:
        ring[i] = mark_col
    
def tick(time):
    if TICK_SND is True:
        pin14.write_analog(256)
    seconds_led = time[2]
    minutes_led = time[1]
    hours_led = calc_hour_led(time[0], time[1])
    ring.clear()
    markers()
    if time[0] > 12:
        ring[hours_led]=hr_pm_col
    else:
        ring[hours_led]=hr_am_col
    ring[minutes_led]=min_col
    ring[seconds_led]=sec_col
    ring.show()
    if TICK_SND is True:
        sleep(20)
        pin14.write_analog(0)

def calc_hour_led(hour, minute):
    base_hour = (hour % 12) * 5
    return (base_hour + floor(minute / 12))

def show_just_seconds(sec):
    ring.clear()
    markers()
    ring[sec] = sec_col
    ring.show()

def show_just_mins(min):
    ring.clear()
    markers()
    ring[min] = min_col
    ring.show()

def check_time():
    rtc.readValue()#
    return (rtc.cur_hr, rtc.cur_min, rtc.cur_sec)

def toggle_tick(state):
    global TICK_SND
    display.scroll("Off" if state else "On")
    TICK_SND = not state

def menu():
    hr = rtc.cur_hr
    min = rtc.cur_min
    sec = rtc.cur_sec
    sleep(300)
    scrolled = False
    b_cnt = 1
    while True:
        if b_cnt == 1:
            if scrolled is False:
                display.scroll("H")
                scrolled = True
            if button_b.is_pressed():
                hr = (hr + 1) % 24
                sleep(500)
                ring.clear()
                markers()
                hr_led = calc_hour_led(hr, 0)
                if hr > 12:
                    ring[hr_led] = hr_pm_col
                else:
                    ring[hr_led] = hr_am_col

                ring.show()

        if b_cnt == 2:
            if scrolled is False:
                display.scroll("M")
                scrolled = True
                show_just_mins(min)
            if button_b.is_pressed():
                min = (min + 1) % 60
                show_just_mins(min)
                sleep(250)

            
    
        if b_cnt == 3:
            if scrolled is False:
                display.scroll("S")
                scrolled = True
                show_just_seconds(sec)
            if button_b.is_pressed():
                sec = (sec + 1) % 60
                show_just_seconds(sec)
                sleep(100)

   
        if b_cnt == 4:
            if scrolled is False:
                display.scroll("T")
                scrolled = True
            if button_b.is_pressed():
                toggle_tick(TICK_SND)

        if button_a.is_pressed() and b_cnt < 5:
            b_cnt += 1
            scrolled  = False

        if b_cnt >=5:
            rtc.setTime(hr, min, sec)
            break
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
                menu()
                ticks = 0

setup()
main()