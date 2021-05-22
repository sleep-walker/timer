#!/usr/bin/env python3
import datetime
import os
import time

import click
import dateparser
import notify2


notify2.init(app_name="timer")
CLEAR_THE_LINE = "\033[1K\033[1G"


def show_alert():
    n = notify2.Notification(
        summary="Timer",
        message="Time is up!"
    )
    n.set_urgency(notify2.URGENCY_NORMAL)
    n.set_timeout(notify2.EXPIRES_NEVER)
    n.show()


def wait(delay, progress):
    zero = datetime.timedelta(seconds=0)
    sec = datetime.timedelta(seconds=1)

    while delay > zero:
        delay -= sec
        if progress:
            print(delay, end='', flush=True)
        time.sleep(1)
        if progress:
            print(CLEAR_THE_LINE, end='', flush=True)


def round_to_seconds(dt):
    return dt - datetime.timedelta(microseconds=dt.microsecond)


@click.command(
    context_settings=dict(max_content_width=os.get_terminal_size().columns))
@click.option(
    "-a/-A", "--alert/--no-alert",
    help="Show notification using libnotify",
    is_flag=True, default=True, show_default=True)
@click.option(
    "-p/-P", "--progress/--no-progress",
    help="Show timer on stdout",
    is_flag=True, default=True, show_default=True)
@click.option(
    "-i", "--ignore-past",
    help=(
        "Ignore fact that timer is in the past and end with alert "
        "instead of failure."),
    is_flag=True, default=False, show_default=True)
@click.argument("when_str", nargs=-1)
def main(when_str, ignore_past, progress, alert):
    when = round_to_seconds(dateparser.parse(" ".join(when_str)))
    if when is None:
        print("Time not recognized")
        return 1

    print(f"Waiting till: {when.strftime('%Y-%m-%d %H:%M:%S')}")

    now = round_to_seconds(datetime.datetime.now())
    if not ignore_past and when < now:
        print("Timer set to past")
        return 1

    delay = when - now
    wait(delay, progress)

    if alert:
        show_alert()


if __name__ == '__main__':
    main()
