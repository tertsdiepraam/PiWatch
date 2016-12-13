from piwatch import *

appsfolder = 'apps'


NORMAL = 0
HEX = 1
BIN = 2
NOW = 3
num_states = 4

class FunClock(Text):
    DEFAULTATTRS = dict(
        Clock.DEFAULTATTRS,
        state=NORMAL
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
        hours = str(bin(self.time[0])) if self.twentyfour else str(hex(self.time[0] % 12))[2:]
        minutes = str(hex(self.time[1]))[2:] if len(str(hex(self.time[1]))) > 1 else '0' + str(hex(self.time[1]))[2:]
        return hours + self.separator + minutes

    def bin_message(self):
        self.time = time.localtime()[3:5]
        hours = str(bin(self.time[0])) if self.twentyfour else str(bin(self.time[0] % 12))[2:]
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
        elif self.state == NOW:
            if not self.message == "now":
                self.update(message="now")
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
        position=('center', 0, -25),
        separator=':'
    )

    maindate = Date(
        position=('center', 0, 30),
        size=25
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
