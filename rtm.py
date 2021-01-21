import asyncio
import argparse
from datetime import timedelta

import ical
import config

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', type=str, required=True, help="path to json config file")


def fix_events(cal):
    for event in cal.events:
        estimate = ical.parse_estimate(event)
        event.end = event.begin + timedelta(minutes=estimate)
    return cal


def fix_tasks(cal):
    for todo in cal.todos:
        if todo.due:
            todo.begin = todo.due
        else:
            todo.due = todo.begin
        estimate = ical.parse_estimate(todo)
        todo.due = todo.begin + timedelta(minutes=estimate)
    return cal


async def fix_calendar(cal, fixer):
    old_calendar = await ical.get_calendar(cal.uri)
    new_calendar = fixer(old_calendar)
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
