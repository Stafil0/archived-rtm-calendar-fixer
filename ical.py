import aiohttp
import re
from ics import Calendar


minutes = 'M'
hours = 'H'
estimate_pattern = re.compile(rf'((\d+)[{hours}])?((\d+)[{minutes}])?$', re.M)


def parse_estimate(event):
    description = event.description
    search = estimate_pattern.search(description)
    if search:
        estimate_hours = search.group(2) or 0
        estimate_minutes = search.group(4) or 0
        estimate = int(estimate_minutes) + int(estimate_hours) * 60
        return estimate
    return 0


async def get_calendar(uri):
    async with aiohttp.ClientSession() as session:
        async with session.get(uri) as resp:
            resp.raise_for_status()
            body = await resp.text()
            return Calendar(body)


def save_calendar(cal, path):
    with open(path, 'w', encoding='utf8') as f:
        f.writelines(str(cal))
