from piwatch import *
import time

appsfolder = 'apps'

NORMAL = 0
HEX = 1
BIN = 2
NOW = 3
TEXT = 4
num_states = 5


def hexify(int):
    return str(hex(int))[2:].upper()


def text_time(time):
    def int_to_word(int):
        if int == 0:
            return 'zero'
        elif int == 1:
            return 'one'
        elif int == 2:
            return 'two'
        elif int == 3:
            return 'three'
        elif int == 4:
            return 'four'
        elif int == 5:
            return 'five'
        elif int == 6:
            return 'six'
        elif int == 7:
            return 'seven'
        elif int == 8:
            return 'eight'
        elif int == 9:
            return 'nine'
        elif int == 10:
            return 'ten'
        elif int == 11:
            return 'eleven'
        elif int == 12:
            return 'twelve'
        elif int == 13:
            return 'thirteen'
        elif int == 14:
            return 'fourteen'
        elif int == 15:
            return 'fifteen'
        elif int == 18:
            return 'eighteen'  # just one "t"
        # 16 - 19 except 18
        elif int < 20:
            return int_to_word(int - 10) + 'teen'
        # 20 - 29
        elif int == 20:
            return 'twenty'
        elif int < 30:
            return 'twenty-' + int_to_word(int - 20)
        # 30 - 39
        elif int == 30:
            return 'thirty'
        elif int < 40:
            return 'thirty-' + int_to_word(int - 30)
        # 40 - 49
        elif int == 40:
            return 'forty'
        elif int < 50:
            return 'forty-' + int_to_word(int - 40)
        # 50 - 59
        elif int == 40:
            return 'fifty'
        elif int < 60:
            return 'fifty-' + int_to_word(int - 50)
        # 60
        elif int == 60:
            return 'sixty'

    time = time[3:5]
    hour = time[0]
    if hour == 12:
        next_hour = 1
    elif hour > 12:
        hour %= 12
        next_hour = hour + 1
    else:
        next_hour = hour + 1
    minutes = time[1]

    if hour == 0:
        if minutes == 0:
            return 'midnight'
        else:
            hour_str = 'midnight'
    elif hour == 12:
        if minutes == 0:
            return 'noon'
        else:
            hour_str = 'noon'
    else:
        hour_str = int_to_word(hour)

    if next_hour == 0:
        next_hour_str = 'midnight'
    elif hour == 12:
        next_hour_str = 'noon'
    else:
        next_hour_str = int_to_word(hour)

    if minutes == 0:
        return hour_str + " o'clock"
    elif minutes == 30:
        return 'half past ' + hour_str
    elif minutes == 15:
        return 'quarter past ' + hour_str
    elif minutes == 45:
        return 'quarter to ' + next_hour_str
    elif minutes > 30:
        return int_to_word(60 - minutes) + ' to ' + next_hour_str
    else:
        return int_to_word(minutes) + ' past ' + hour_str


class FunClock(Text):
    DEFAULTATTRS = dict(
        Clock.DEFAULTATTRS,
        state=NORMAL,
        twentyfour=True
    )

    def __init__(self, *attrs, **kwargs):
        super().__init__(*attrs, **kwargs)
        self.time = None

    def normal_message(self):
        self.time = time.localtime()[3:5]
        hours = str(self.time[0]) if self.twentyfour else str(self.time[0] % 12)
        minutes = str(self.time[1]) if len(str(self.time[1])) > 1 else '0' + str(self.time[1])
        return hours + self.separator + minutes

    def hex_message(self):
        self.time = time.localtime()[3:5]
        hours = hexify(self.time[0]) if self.twentyfour else hexify(self.time[0] % 12)
        minutes = hexify(self.time[1]) if len(hexify(self.time[1])) > 1 else '0' + hexify(self.time[1])
        return hours + self.separator + minutes

    def bin_message(self):
        self.time = time.localtime()[3:5]
        hours = str(bin(self.time[0]))[2:] if self.twentyfour else str(bin(self.time[0] % 12))[2:]
        minutes = str(bin(self.time[1]))[2:]
        return hours + self.separator + minutes

    def update(self, **kwargs):
        if 'state' in kwargs:
            if kwargs['state'] == NORMAL:
                kwargs['message'] = self.normal_message()
                kwargs['size'] = 96
            elif kwargs['state'] == HEX:
                kwargs['message'] = self.hex_message()
                kwargs['size'] = 96
            elif kwargs['state'] == BIN:
                kwargs['message'] = self.bin_message()
                kwargs['size'] = 40
            elif kwargs['state'] == NOW:
                kwargs['message'] = 'now'
                kwargs['size'] = 120
            elif kwargs['state'] == TEXT:
                kwargs['message'] = text_time(time.localtime())
                kwargs['size'] = 27
        super().update(**kwargs)

    def draw(self, surface):
        if self.state == NORMAL:
            if self.time != time.localtime()[3:5]:
                self.update(message=self.normal_message())
        elif self.state == HEX:
            if self.time != time.localtime()[3:5]:
                self.update(message=self.hex_message())
        elif self.state == BIN:
            if self.time != time.localtime()[3:5]:
                self.update(message=self.bin_message())
        elif self.state == TEXT:
            if self.time != time.localtime()[3:5]:
                self.update(message=text_time(time.localtime()))
        super().draw(surface)


def define_app():
    # App object and settings
    app = App(
        name='Home',
        icon='home.png',
        bg_color=(0, 0, 0))

    # Components
    mainclock = FunClock(
        size=96,
        position=('midbottom', 0, -110),
        separator=':'
    )

    maindate = Date(
        position=('center', 0, 40),
        size=25,
        color=(200, 200, 200)
    )

    @app.event_listener('mouse up')
    def mouse_up(event):
        if mainclock.check_collision(event.pos):
            mainclock.update(state=(mainclock.state+1) % num_states)

    # Activities
    main = Activity(name='main')
    main.add(mainclock, maindate)

    # Add the activity to the app
    app.add(main)
    return app
