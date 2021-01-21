import asyncio
import argparse
from datetime import timedelta
from pytz import timezone

import ical
import config

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', type=str, required=True, help="path to json config file")


def _replace_timezone(dt, zone):
    return dt.replace(tzinfo=timezone(zone))


def fix_events(cal, tz):
    for event in cal.events:
        event.begin = _replace_timezone(event.begin.datetime, tz)
        event.end = _replace_timezone(event.end.datetime, tz)

        estimate = ical.parse_estimate(event)
        event.end = event.begin + timedelta(minutes=estimate)
    return cal


def fix_tasks(cal, tz):
    for todo in cal.todos:
        if todo.due:
            todo.begin = todo.due
        else:
            todo.due = todo.begin

        todo.begin = _replace_timezone(todo.begin.datetime, tz)
        todo.due = _replace_timezone(todo.due.datetime, tz)

        estimate = ical.parse_estimate(todo)
        todo.due = todo.begin + timedelta(minutes=estimate)
    return cal


async def fix_calendar(cal, tz, fixer):
    old_calendar = await ical.get_calendar(cal.uri)
    new_calendar = fixer(old_calendar, tz)
    ical.save_calendar(new_calendar, cal.save)


async def main(args):
    calendars = config.read_config(args.config)
    for cal in calendars.events:
        await fix_calendar(cal, cal.timezone, fix_events)
    for cal in calendars.tasks:
        await fix_calendar(cal, cal.timezone, fix_tasks)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(parser.parse_args()))
