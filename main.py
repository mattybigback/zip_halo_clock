from microbit import (
    pin8 as neo_pin,
    pin14 as buzz,
    sleep,
    button_a as btn_a,
    button_b as btn_b,
    display as disp)
from neopixel import NeoPixel
import MCP7940N as rtc

SND = False  # Sound on or off
BRT = 1     # Brightmness (0-4)
LEDS = 60   # Number of neopixels to control

ring = NeoPixel(neo_pin, LEDS)
rtc = rtc.MCP7940N()
buzz.set_analog_period_microseconds(10000)
    
def tick(time):
    # Set the LEDs that correspond to the correct time, and if sound is enabled play a short tick.
    set_markers()
    set_hour_led(time[0], time[1])
    set_min_sec_led(time[1],"m")
    set_min_sec_led(time[2])
    ring.show()
    if SND:
        buzz.write_analog(127)
    if SND is True:
        sleep(20)
        buzz.write_analog(0)

def calc_hour_led(hr, mn):
    # Calculate the correct LED to light up for the  current time.
    # The hour "hand" progresses by one LED every 12 minutes, mimicking a real clock.
    base_hour = (hr % 12) * 5
    return (base_hour + int(mn / 12))

def set_markers():
    # Place markers on the clock face where the numbers would be.
    MRKS = (0,5,10,15,20,25,30,35,40,45,50,55)
    clear_ring()
    for i in MRKS:
        ring[i] = set_bright_offset([15, 0, 0])

def set_min_sec_led(unit, type="s"):
    # Set the second or minute LED
    if type == "m":
        color = [0,15,0]
    else:
        color = [15,15,15]
    color = set_bright_offset(color)
    ring[unit] = color

def set_hour_led(hour, min):
    # Set the hour LED. Cyan for AM, blue for PM.
    hour_led = calc_hour_led(hour, min)
    if hour > 11:
        hour_col = [0, 0, 15]
    else    :
        hour_col = [0, 15, 15]
    ring[hour_led] = set_bright_offset(hour_col)

def clear_ring():
    # Set all of the LEDs to black without transmitting the show instruction.
    for led in range(LEDS):
        ring[led] = [0,0,0]

def check_time():
    # Get the current time from the RTC chip and return it as a tuple.
    rtc.readValue()
    return (rtc.cur_hr, rtc.cur_min, rtc.cur_sec)

def toggle_tick(state):
    # Toggle audible ticking
    global SND
    disp.scroll("Off" if state else "On")
    SND = not state

def set_bright_offset(colors_in):
    # Adjust LED brightness based on BRT constant.
    colors_out = [rgb << BRT for rgb in colors_in]
    return colors_out

def menu():
    # Menu system, accessed by holding down both buttons for 2-3 seconds
    hr = rtc.cur_hr
    mins = rtc.cur_min
    sec = rtc.cur_sec
    sleep(300)
    scrl = False
    b_cnt = 1
    set_markers()
    ring.show()

    while True:
        # Toggle audible ticking
        if b_cnt == 1:
            if scrl is False:
                disp.scroll("T")
                scrl = True
            if btn_b.is_pressed():
                toggle_tick(SND)

        # Set hour
        if b_cnt == 2:
            if scrl is False:
                disp.scroll("H")
                scrl = True
                set_markers()
                set_hour_led(hr, 0)
                ring.show()
            if btn_b.is_pressed():
                hr = (hr + 1) % 24
                set_markers()
                set_hour_led(hr, 0)
                ring.show()
                sleep(500)

        # Set minute
        if b_cnt == 3:
            if scrl is False:
                disp.scroll("M")
                scrl = True
                set_markers()
                set_min_sec_led(mins, "m")
                ring.show()
            if btn_b.is_pressed():
                mins = (mins + 1) % 60
                set_markers()
                set_min_sec_led(mins, "m")
                ring.show()
                sleep(250)
            
        # Set seconds
        if b_cnt == 4:
            if scrl is False:
                disp.scroll("S")
                scrl = True
                set_markers()
                set_min_sec_led(sec)
                ring.show()
            if btn_b.is_pressed():
                sec = (sec + 1) % 60
                set_markers()
                set_min_sec_led(sec)
                ring.show()
                sleep(100)

        # Increment counter if button a is pressed
        if btn_a.is_pressed() and b_cnt < 5:
            b_cnt += 1
            scrl  = False

        # Save new time to RTC if end of menu is reached and button a is pressed
        if b_cnt >=5:
            rtc.setTime(hr, mins, sec)
            break
    return


def main():
    disp.clear() # Clears any errors or suprious data
    tks = 0
    time_now = check_time()
    while True:
        if time_now != check_time():
            time_now = check_time()
            tick(time_now)
            if btn_a.is_pressed() and btn_b.is_pressed():
                tks += 1
            if tks >= 2:
                menu()
                tks = 0

if __name__ == "__main__":
    main()