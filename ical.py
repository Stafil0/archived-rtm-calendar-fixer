import aiohttp
import re
from ics import Calendar


minutes = 'M'
hours = 'H'
estimate_pattern = re.compile(rf'(\d+)([{hours}{minutes}])$', re.M)


def parse_estimate(event):
    description = event.description
    search = estimate_pattern.search(description)
    if search:
        estimate = int(search.group(1))
        time = search.group(2)
        return estimate * 60 if time == hours else estimate
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
