from piwatch import *
import time


def define_app():
    app = App(
        name='Stopwatch',
        bg_color=(63, 68, 84),
        icon='icon.png'
    )

    main = Activity(
        name='main'
    )

    class Stopwatch(Text):
        DEFAULTATTRS= Text.DEFAULTATTRS

        def __init__(self, *attrs, **kwargs):
            super().__init__(*attrs, **kwargs)
            self.seconds_at_start = 0
            self.start_time = None
            self.running = False

        def draw(self, surface):
            if self.running:
                total_seconds = time.time() - self.start_time + self.seconds_at_start
            else:
                total_seconds = self.seconds_at_start
            minutes = str(int(total_seconds/60))
            if len(minutes) == 1:
                minutes = '0' + minutes
            seconds = str(int(total_seconds%60))
            if len(seconds) == 1:
                seconds = '0' + seconds
            self.update(message=minutes + ':' + seconds)
            super().draw(surface)

        def reset(self):
            if self.running:
                self.pause()
            self.seconds_at_start = 0

        def start(self):
            self.start_time = time.time()
            self.running = True

        def pause(self):
            self.seconds_at_start += time.time() - self.start_time
            self.running = False

    bttn_attrs = dict(
        Text.attributes,
        size=30,
        color=(0, 0, 0),
        fixed_size=(90, 40)
    )

    bttn_start_pause = Text(
        bttn_attrs,
        message='start',
        bg_color=(69, 99, 232)
    )

    bttn_reset = Text(
        bttn_attrs,
        message='reset',
        bg_color=(255, 255, 255)
    )

    bttns = List(
        direction='right',
        position=('midbottom', 0, -40),
        children=[bttn_start_pause, bttn_reset],
        spacing=50,
        alignment='center'
    )

    stopwatch = Stopwatch(
        size=110,
        position=('center', 0, -25)
    )

    @app.event_listener('mouse down')
    def mouse_down(event):
        if bttn_start_pause.check_collision(event.pos):
            if stopwatch.running:
                stopwatch.pause()
                bttn_start_pause.update(
                    message='start',
                    bg_color=(69, 99, 232)
                )
                bttns.update()
            else:
                stopwatch.start()
                bttn_start_pause.update(
                    message='pause',
                    bg_color=(232, 99, 69)
                )
                bttns.update()
        if bttn_reset.check_collision(event.pos):
            if stopwatch.running:
                bttn_start_pause.update(
                    message='start',
                    bg_color=(69, 99, 232)
                )
                bttns.update()
            stopwatch.reset()

    main.add(bttns, stopwatch)
    app.add(main)
    return app
