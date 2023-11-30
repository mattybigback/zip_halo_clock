def display_letter_and_check_button(letter, value, increment_func, display_func, sleep_time):
    scrolled = False
    while True:
        if not scrolled:
            display.scroll(letter)
            scrolled = True

        if button_b.is_pressed():
            value = increment_func(value)
            sleep(sleep_time)

        if button_a.is_pressed():
            return value


def increment_hour(hr):
    return (hr + 1) % 24


def increment_minute(minutes):
    return (minutes + 1) % 60


def increment_second(seconds):
    return (seconds + 1) % 60


def menu():
    hr = rtc.cur_hr
    minutes = rtc.cur_min
    seconds = rtc.cur_sec
    button_count = 1

    button_functions = {
        1: ('H', increment_hour, 500),
        2: ('M', increment_minute, 250),
        3: ('S', increment_second, 100),
        4: ('T', lambda x: toggle_tick(TICK_SND), 0)
    }

    while button_count < 5:
        letter, increment_func, sleep_time = button_functions[button_count]
        value = display_letter_and_check_button(letter, locals()[letter.lower()], increment_func, display_func, sleep_time)
        locals()[letter.lower()] = value

        button_count += 1

    rtc.setTime(hr, minutes, seconds)
