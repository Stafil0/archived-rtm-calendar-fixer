import asyncio
import argparse
from datetime import timedelta

from base import ical
from base.calendar import Calendar
from base.tz import replace_timezone
from configs import config

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', type=str, required=True, help='path to json configs file')


def _get_fixer(cal):
    if cal.typo == Calendar.Event:
        return fix_events
    if cal.typo == Calendar.Tasks:
        return fix_tasks
    raise ValueError(f"Incorrect calendar type '{cal.typo}'")


def fix_events(cal, tz, with_estimate):
    events = set()
    for event in cal.events:
        estimate = ical.parse_estimate(event)
        if with_estimate is True and not estimate or with_estimate is False and estimate:
            continue

        event.begin = replace_timezone(event.begin.datetime, tz)
        event.end = replace_timezone(event.end.datetime, tz)
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

        todo.begin = replace_timezone(todo.begin.datetime, tz)
        todo.due = replace_timezone(todo.due.datetime, tz)

        todo.due = todo.begin + timedelta(minutes=estimate)
        todos.add(todo)
    cal.todos = todos
    return cal


async def fix_calendar(cal):
    fixer = _get_fixer(cal)
    old_calendar = await ical.get_calendar(cal.uri)
    return fixer(old_calendar, cal.timezone, cal.with_estimate)


def merge_calendars(cals):
    if not cals:
        return None

    cal = cals[0]
    todos = set(todo for c in cals for todo in c.todos)
    events = set(event for c in cals for event in c.events)

    cal.todos = todos
    cal.events = events
    return cal


async def main(args):
    calendars = config.read_config(args.config)

    for fix in calendars.fix:
        new_calendar = await fix_calendar(fix.calendar)
        ical.save_calendar(new_calendar, fix.save)

    for merge in calendars.merge:
        calendars = []
        for calendar in merge.calendars:
            new_calendar = await fix_calendar(calendar)
            calendars.append(new_calendar)
        new_calendar = merge_calendars(calendars)
        if new_calendar:
            ical.save_calendar(new_calendar, merge.save)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(parser.parse_args()))
