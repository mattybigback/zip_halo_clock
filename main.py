from microbit import pin8, pin14, sleep, button_a, button_b, display
from neopixel import NeoPixel
from math import floor
import kitronic_min as kt


TICK_SND = True

NUM_PIXELS = 60
mark_col = [0x0F, 0, 0]
sec_col = [0x0F, 0x0F, 0x0F]
hr_am_col = [0, 0x07, 0x0f]
hr_pm_col = [0, 0, 0x17]
min_col = [0, 0x0F, 0]

ring = NeoPixel(pin8, NUM_PIXELS)
rtc = kt.KitronikRTC()

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
    hours_led, pm = calc_hour_led(time[0], time[1])
    ring.clear()
    markers()
    if pm == 1:
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
    if hour > 13:
        return ((hour-12)*5+floor(minute/12),1)
    return (hour*5+floor(minute/12),0)

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
    if state is True:
        display.scroll("N")
        state = False
    else:
        display.scroll("Y")
        state = True
    TICK_SND = state

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
        if b_cnt == 2:
            if scrolled is False:
                display.scroll("M")
                scrolled = True
            if button_b.is_pressed():
                if min < 59:
                    min +=1
                    sleep(250)
                else:
                    min = 0
            show_just_mins(min)
    
        if b_cnt == 3:
            if scrolled is False:
                display.scroll("S")
                scrolled = True
            if button_b.is_pressed():
                if sec < 59:
                    sec +=1
                    sleep(100)
                else:
                    sec = 0
            show_just_seconds(sec)
                    
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