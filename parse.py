import datetime
import pdfplumber
import re
import calapi
from event import Event

from dateutil import parser

with pdfplumber.open("cal_lms_2024.pdf") as pdf:
    # @TODO: add ability to iterate through all PDF pages
    first_page = pdf.pages[0]
    pdfText = first_page.extract_text()

# Split by row into an array
splitPdf = pdfText.split("\n")

def parse_date(dateStr):
    nums = [int(x) for x in dateStr.split("/")]
    if len(nums) < 3 and nums[0] >= 8:
        year = start_year
    else:
        year = end_year or 2024
    date_formatted = year + "/" + dateStr
    formatStr = "%Y/%m/%d"
    datetimeObj = datetime.datetime.strptime(date_formatted, formatStr).date()
    print("PARSE DATE", datetimeObj)
    return datetimeObj

def parse_time(item):
    #@TODO
    print("Here's where we parse the time, if it's present")
    # check for time
    # try:
    #     parsed = parser.parse(x, fuzzy_with_tokens=True)
    #     print(parsed)
    # except ValueError as e:
    #     print(e)
    matchTime = re.search(r'(\d{1,2}\:\d{2}\s?(?:AM|PM|am|pm))', item)
    return matchTime.group() if matchTime else None


def parse_isoformat(parsed_date, time):
    #@TODO
    print("Here's where we combine the parsed date and potential parsed time to return an isoformat datetime")
    start_date_str = (str(parsed_date) + time).replace(" ", "")
    formatStr = "%Y-%m-%d%I:%M%p"
    datetimeObj = datetime.datetime.strptime(start_date_str, formatStr)
    print(datetimeObj.isoformat())
    return datetimeObj.isoformat()


def find_keyword(row):
     if keyword.lower() in row.lower():
        keyword_results.append(row)
        # parseDate(row.split(" ")[0])

def parse_range_create_events(unformatted_date_range):
    # split range into start and finish dates
    x = unformatted_date_range.split("-")
    first_date = re.split(r'[/-]', x[0])
    start_month = first_date[0]
    start_day = int(first_date[1])
    end_month = first_date[0] if len(x[1])<3 else re.split(r'[/-]', x[1])[0]
    end_day = int(x[1]) if len(x[1])<3 else re.split(r'[/-]', x[1])[1]
    print(start_month, start_day, end_month, end_day)

    # may need to change this to a more complex if loop
    # going cross year is going to require more logic than this list comp
    # maybe will need to check if end_month < start_month to see if it crosses
    # years. This would only within one calendar year   
    list_dates = [(start_month + '/' + str(x)) for x in range(start_day,end_day+1)]
    print(list_dates)

    for date in list_dates:
        parsed_date = parse_date(date)
        event = Event(keyword, str(parsed_date), str(parsed_date))
        print(event.createAllDayEvent())
        # send to Google cal
        # calapi.main(event)


# Get user input to find keyword instead of hardcoding, establish DS for results
keyword = input("Enter a keyword or event name: ")
start_year, end_year = input("Enter the start year and end year: ").split(", ")
keyword_results = []

for row in splitPdf:
    # Filter only the rows that contain relevant data/kw
    find_keyword(row)

for item in keyword_results:
    # 1. check for range
    matchDateRange = re.search(r'\d*/\d*\-\d*', item.replace(" ", ""))
    # 2. check for time
    time = parse_time(str(item))
    # 3. check for date
    matchDate = re.search(r'\d*/\d*', item).group()

    # if time and date > parse_iso
    if matchDate and time:
        date = parse_date(matchDate)
        parse_isoformat(date, time)
        event = Event(keyword, str(date), str(date))
        print(event.createTimeEvent())
        # send to Google cal
        # calapi.main(event.createTimeEvent())

    # if range > parse_date_range
    elif matchDateRange:
        parse_range_create_events(matchDateRange.group())
        # event is created in that method
    # if date > parse date
    elif matchDate:
        date = parse_date(matchDate)
        event = Event(keyword, str(date), str(date))
        print(event.createAllDayEvent())
        # send to Google cal
        # calapi.main(event.createAllDayEvent())
    else:
        print("No dates found.")