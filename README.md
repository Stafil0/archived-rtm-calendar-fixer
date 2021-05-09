rtm-calendar-fixer
=============
###### Fix "Remember The Milk" calendars start/end/due dates.

### TL;DR

A Python3 scripts that fixes start/end/due time for events and tasks in Remember The Milk icalendars.

For Events calendar:
* Event due date => Event start date;
* Event due date + estimate => Event end date.

For Tasks calendar:
* If: Task due date presents => Task begin date;
* Else: Task creation time => Task begin date;
* Task begin date + estimate => Task due date.

### Run
To run script follow this simple steps:
* install all packages from `requirements.txt` with `python -m pip install -r requirements.txt`;
* set up your json config file;
* set up cronjob, e.g. `*/15 * * * * python3 rtm.py -c config.json` to sync your local calendar with RTM;
* point your iCal software to new ics file.

### Configuration
For easy setup you can create configuration file with this content:
```json
{
  "fix": [
    {
      "calendar": {
        "timezone": "Etc/GMT-3",
        "uri": "https://www.rememberthemilk.com/icalendar/some/calendar",
        "typo": "events"
      },
      "save": "./fixed.ics"
    }
  ],
  "merge": [
    {
      "calendars": [
        {
          "timezone": "Etc/GMT-3",
          "uri": "https://www.rememberthemilk.com/icalendar/some/calendar",
          "typo": "tasks",
          "with_estimate": false
        },
        {
          "timezone": "Etc/GMT-3",
          "uri": "https://www.rememberthemilk.com/icalendar/some/calendar",
          "typo": "events",
          "with_estimate": true
        }
      ],
      "save": "./merged.ics"
    }
  ]
}
```

In `uri` field paste URL for you calendar, and in `save` field select path, where to store new calendar in `ics` format.

You can specify your timezone in `timezone` field. All avaliable timezone formats you can find in `pytz.all_timezones`.

Use `events` typo for Events calendars and `tasks` typo for Tasks calendars.

Specify `with_estimate` as `true` if you want to remove tasks\events without estimate and vice versa for `false`.
Param is optional, so if you `not specify it`, nothing will be removed.

To just fix your calendar, setup it in `fix` section. If you also want to merge multiple calendars into one, put them in `merge` section.
