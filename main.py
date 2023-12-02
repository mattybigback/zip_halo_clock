from microbit import pin8, pin14, sleep, button_a, button_b, display
from neopixel import NeoPixel
import MCP7940N as rtc

TICK_SND = True
BRT = 0

LEDS = 60


ring = NeoPixel(pin8, LEDS)
rtc = rtc.MCP7940N()

def setup():
    rtc.setTime(0,0,0)
    pin14.set_analog_period_microseconds(10000)


def set_markers():
    MARKS = (0,5,10,15,20,25,30,35,40,45,50,55)
    clear_ring()
    for i in MARKS:
        ring[i] = set_bright_offset([15, 0, 0])
    
def tick(time):

    set_markers()
    set_hour_led(time[0], time[1])
    set_min_sec_led(time[1],"m")
    set_min_sec_led(time[2])
    ring.show()
    if TICK_SND:
        pin14.write_analog(127)
    if TICK_SND is True:
        sleep(20)
        pin14.write_analog(0)

def calc_hour_led(hr, mn):
    base_hour = (hr % 12) * 5
    return (base_hour + int(mn / 12))

def set_min_sec_led(unit, type="s"):
    if type == "m":
        color = [0,15,0]
    else:
        color = [15,15,15]
    color = set_bright_offset(color)
    ring[unit] = color


def set_hour_led(hour, min):
    hour_led = calc_hour_led(hour, min)
    if hour > 12:
        hour_col = [0, 0, 30]
    else:
        hour_col = [0,15,15]
    ring[hour_led] = set_bright_offset(hour_col)

def clear_ring():
    for led in range(LEDS):
        ring[led] = [0,0,0]

def check_time():
    rtc.readValue()
    return (rtc.cur_hr, rtc.cur_min, rtc.cur_sec)

def toggle_tick(state):
    global TICK_SND
    display.scroll("N" if state else "Y")
    TICK_SND = not state

def set_bright_offset(colors_in):
    colors_out = [rgb << BRT for rgb in colors_in]
    return colors_out


def menu():
    hr = rtc.cur_hr
    mins = rtc.cur_min
    sec = rtc.cur_sec
    sleep(300)
    scrl = False
    b_cnt = 1
    set_markers()
    ring.show()

    while True:
        if b_cnt == 1:
            if scrl is False:
                display.scroll("T")
                scrl = True
            if button_b.is_pressed():
                toggle_tick(TICK_SND)

        if b_cnt == 2:
            if scrl is False:
                display.scroll("H")
                scrl = True
                set_markers()
                set_hour_led(hr, 0)
                ring.show()
            if button_b.is_pressed():
                hr = (hr + 1) % 24
                set_markers()
                set_hour_led(hr, 0)
                ring.show()
                sleep(500)

        if b_cnt == 3:
            if scrl is False:
                display.scroll("M")
                scrl = True
                set_markers()
                set_min_sec_led(mins, "m")
                ring.show()
            if button_b.is_pressed():
                mins = (mins + 1) % 60
                set_markers()
                set_min_sec_led(mins, "m")
                ring.show()
                sleep(250)
            
    
        if b_cnt == 4:
            if scrl is False:
                display.scroll("S")
                scrl = True
                set_markers()
                set_min_sec_led(sec)
                ring.show()
            if button_b.is_pressed():
                sec = (sec + 1) % 60
                set_markers()
                set_min_sec_led(sec)
                ring.show()
                sleep(100)

        if button_a.is_pressed() and b_cnt < 5:
            b_cnt += 1
            scrl  = False

        if b_cnt >=5:
            rtc.setTime(hr, mins, sec)
            break
    return


def main():
    display.clear()
    ticks = 0
    time_now = check_time()
    while True:
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