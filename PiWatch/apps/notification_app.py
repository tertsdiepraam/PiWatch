from piwatch import *


def define_app():
    app = App(
        name='Notifications'
    )

    loadscreen = Activity(
        name='main'
    )

    load_text = Text(
        message='Receiving Notifications...'
    )
    loadscreen.add(load_text)

    notification_list = List(
        position=("topleft", 20, 25),
        alignment="topleft",
        spacing=5
    )

    list_screen = Activity(
        name='list'
    )
    list_screen.add(notification_list)

    @app.event_listener('started app Notifications')
    @app.event_listener('resumed app Notifications')
    def get_notifications(event):
        load_text.update(message="Receiving Notifications...")
        app.eventqueue.add('bt send', data="list notifications")

    @app.event_listener('bt send failed')
    def not_connected(event):
        load_text.update(message="Not connected.")

    @app.event_listener('bt data received')
    def list_notifications(event):
        info = event.data.decode("utf-8").split("||")
        if info[0] != "notification list": return
        if len(info) > 5: list = info[1:6]
        else: list = info[1:]

        notification_list.clear()
        itemlist = []
        for notification in list:
            app_str, title_str, text_str = notification.split("|")

            itemlist.append(
                List(
                    alignment="topleft",
                    bg_color=(200, 200, 200),
                    fixed_size=(280, 37),
                    children=[
                        Text(
                            color=(0, 0, 0),
                            message=title_str,
                            size=16,
                            padding=(6, 5)
                        ),
                        Text(
                            color=(0, 0, 0),
                            message=text_str,
                            size=14,
                            padding=(6, 3)
                        )
                    ]
                )
            )

        notification_list.add(*itemlist)
        app.set_activity("list")

    app.add(loadscreen, list_screen)
    return app
