# recycling-scheduler
A program to generate garbage and recycling pickup calendars through a .ics file

### Arguments:

- -s  --startdate   "first pickup date for this route - YYYYMMDD"
- -r  --route  "route description ex. 1n"
- -d  --description   "event description"
- -p  --prefix   "file name prefix"
- -w  --wekdays   "weekdays between events Default: ten weekdays or two weeks"

### Example

` py calendarDateGenerator.py -s 20220114 -r 1n -d "Oak Bay Garbage and Recycling Pickup" -p "oakbay_garbage_file_schedule_" `

File name is composed with Route, Prefix and ".ics" The command above would generate the following file name: `oakbay_garbage_file_schedule_1n.ics`

The calendar would start on the 14th of January 2022 and would create an event every 10 weekdays days. If there is a holiday in the days between events,
the next event will move forward a day. So every 10 business days