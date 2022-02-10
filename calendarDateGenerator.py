from datetime import date, timedelta, datetime
import holidays
import uuid
import os
from pathlib import Path
import argparse
import logging

WEEKDAY_NUMBER = 5
WEEKDAYS_BETWEEN_PICKUPS = 10
TIMEZONE = "America/Vancouver"
EVENT_DESCRIPTION = "Garbage pickup"
FILE_NAME_PREFIX = "oakbay_garbage_file_schedule_"
FILE_NAME_SUFFIX = ".ics"


def add_event_to_calendar(garbage_calendar: list, event_date: date, description: str, route: str) -> list:
    garbage_calendar.append("BEGIN:VEVENT")
    garbage_calendar.append("DESCRIPTION:" + description)
    garbage_calendar.append("DTSTART;VALUE=DATE:" + event_date.strftime("%Y%m%d"))
    garbage_calendar.append("SUMMARY:" + description)
    garbage_calendar.append("UID:" + str(uuid.uuid4()))
    garbage_calendar.append("END:VEVENT")
    logging.warning(route + " " + event_date.strftime("%B-%d"))
    return garbage_calendar


def calendar_start(garbage_calendar: list, timezone: str, route: str) -> list:
    garbage_calendar.append("BEGIN:VCALENDAR")
    garbage_calendar.append("VERSION:2.0")
    garbage_calendar.append("METHOD:PUBLISH")
    garbage_calendar.append("PRODID:Data::ICal 0.24")
    garbage_calendar.append("X-PUBLISHED-TTL:1440")
    garbage_calendar.append("X-WR-CALDESC:Oak Bay Garbage Schedule")
    garbage_calendar.append("X-WR-CALNAME:Route " + route)
    garbage_calendar.append("X-WR-TIMEZONE:" + timezone)
    return garbage_calendar


def calendar_end(garbage_calendar: list) -> list:
    garbage_calendar.append("END:VCALENDAR")
    return garbage_calendar


def print_calendar(garbage_calendar: list, route: str):
    file_name = FILE_NAME_PREFIX + route + FILE_NAME_SUFFIX
    directory = str(Path(__file__).parent) + "/Schedules/"
    print("ics file will be generated at ", directory)
    f = open(os.path.join(directory, file_name), 'wb')
    f.write(bytes('\n'.join(garbage_calendar), "utf-8"))
    f.close()


def main():
    parser = argparse.ArgumentParser(description="Generates .ics file for Oak Bay garbage and recycling pickup days")
    parser.add_argument('-s', '--startdate', required=True, help='first pickup date for this route - YYYYMMDD')
    parser.add_argument('-r', '--route', required=True, help='route description ex. 1n')
    parser.add_argument('-d', '--description', required=True, help='event description')
    args = parser.parse_args()

    calendar = []
    calendar = calendar_start(calendar, TIMEZONE, args.route)
    current_date = datetime.strptime(args.startdate, '%Y%m%d').date()
    single_day = timedelta(days=1)
    days_since_last_pickup = 0
    bc_holidays = holidays.CountryHoliday('CAN', prov='BC')

    end_date = date(current_date.year, 12, 31)

    calendar = add_event_to_calendar(calendar, current_date, args.description, args.route)

    while current_date < end_date:

        current_date = current_date + single_day

        if current_date.weekday() < WEEKDAY_NUMBER and current_date not in bc_holidays:
            # only increment when it's a weekday and NOT a holiday
            days_since_last_pickup += 1

        if days_since_last_pickup >= WEEKDAYS_BETWEEN_PICKUPS:
            days_since_last_pickup = 0
            calendar = add_event_to_calendar(calendar, current_date, args.description, args.route)

    calendar = calendar_end(calendar)
    print_calendar(calendar, args.route)


if __name__ == "__main__":

    main()

