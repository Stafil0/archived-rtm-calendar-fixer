import asyncio
import argparse
from datetime import timedelta
from pytz import timezone

import ical
import config

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', type=str, required=True, help='path to json config file')


def _replace_timezone(dt, zone):
    return dt.replace(tzinfo=timezone(zone))


def fix_events(cal, tz, with_estimate):
    events = set()
    for event in cal.events:
        estimate = ical.parse_estimate(event)
        if with_estimate is True and not estimate or with_estimate is False and estimate:
            continue

        event.begin = _replace_timezone(event.begin.datetime, tz)
        event.end = _replace_timezone(event.end.datetime, tz)
        event.end = event.begin + timedelta(minutes=estimate)
        events.add(event)
    cal.events = events
    return cal


def fix_tasks(cal, tz, with_estimate):
    todos = set()
    for todo in cal.todos:
        estimate = ical.parse_estimate(todo)
        if with_estimate is True and not estimate or with_estimate is False and estimate:
            continue

        if todo.due:
            todo.begin = todo.due
        else:
            todo.due = todo.begin

        todo.begin = _replace_timezone(todo.begin.datetime, tz)
        todo.due = _replace_timezone(todo.due.datetime, tz)

        todo.due = todo.begin + timedelta(minutes=estimate)
        todos.add(todo)
    cal.todos = todos
    return cal


async def fix_calendar(cal, fixer):
    old_calendar = await ical.get_calendar(cal.uri)
    new_calendar = fixer(old_calendar, cal.timezone, cal.with_estimate)
    ical.save_calendar(new_calendar, cal.save)


async def main(args):
    calendars = config.read_config(args.config)
    for cal in calendars.events:
        await fix_calendar(cal, fix_events)
    for cal in calendars.tasks:
        await fix_calendar(cal, fix_tasks)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(parser.parse_args()))
