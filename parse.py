import datetime
import pdfplumber
import re
import calapi

from dateutil import parser

with pdfplumber.open("cal_lms_2024.pdf") as pdf:
    # @TODO: add ability to iterate through all PDF pages
    first_page = pdf.pages[0]
    pdfText = first_page.extract_text()

# Split by row into an array
split = pdfText.split("\n")

all_dates_in_iso = []
all_dates = []

# object to be sent to Google for cal event
batch_event_data = []

# Function to change the date into usable isoformat per Google cal
# standards/requirements. The year is kind of brute forced for now,
# may need to make this more dyanmic later, as this all relies on argument
# placement/consistent date formatting in the PDF
# def parse_date_iso(dateStr):
#     nums = [int(x) for x in dateStr.split("/")]
#     if len(nums) < 3 and nums[0] >= 8:
#         year = start_year
#     else:
#         year = end_year or 2024
#     dateStr += "/" + year
#     formatStr = "%m/%d/%Y"
#     datetimeObj = datetime.datetime.strptime(dateStr, formatStr)
#     all_dates_in_iso.append(datetimeObj.isoformat())
#     return datetimeObj.isoformat()

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

# Get user input to find keyword instead of hardcoding
keyword = input("Enter a keyword or event name: ")
start_year, end_year = input("Enter the start year and end year: ").split(", ")

# For every row in the PDF, pull the first item (which we know is date)
# Again, this is hardcoded because I know the PDF. It would probably
# need to be dynamic, as the placement could be different.
keyword_results = []

def find_keyword(row):
     if keyword.lower() in row.lower():
        keyword_results.append(row)
        # parseDate(row.split(" ")[0])

for row in split:
    # Filter only the rows that contain relevant data and assign it
    # to keyword_results array
    find_keyword(row)

# This takes rows that have a hyphen and fills in the dates within
# the date range
# @TODO: make this... actually work reliably
def parse_date_range(unformatted_date_range):
    print("parsing date range")
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
        event = {
        'summary': keyword,
        'start': {
            'date': str(parsed_date),
        },
        'end': {
            'date': str(parsed_date)
        }
    }
        print(event)
        # send to Google cal
        # calapi.main(event)

for item in keyword_results:
    # 1. check for range
    # 2. check for time
    # 3. check for date
    # if range > parse_date_range
    # if time and date > parse_iso
    # if date > 

    matchDate = re.search(r'\d*/\d*', item).group()
    matchDateRange = re.search(r'\d*/\d*\-\d*', item.replace(" ", ""))
    time = parse_time(str(item))
    print("TIME", time)
    
    if matchDate and time:
        date = parse_date(matchDate)
        parse_isoformat(date, time)

    if matchDateRange:
        parse_date_range(matchDateRange.group())
    # @TODO: move logic out of here and into parse_date
    elif matchDate:
        date = parse_date(matchDate)
        event = {
        'summary': keyword,
        'start': {
            'date': str(date),
        },
        'end': {
            'date': str(date)
        },
        'time': time
    }
        print(event)
    # send to Google cal
    # calapi.main(event)
    else:
        print("No dates found.")