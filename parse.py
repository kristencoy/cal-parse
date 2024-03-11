import datetime
import pdfplumber
import re
import calapi

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
def parse_date_iso(dateStr):
    nums = [int(x) for x in dateStr.split("/")]
    if len(nums) < 3 and nums[0] >= 8:
        year = start_year
    else:
        year = end_year or 2024
    dateStr += "/" + year
    formatStr = "%m/%d/%Y"
    datetimeObj = datetime.datetime.strptime(dateStr, formatStr)
    all_dates_in_iso.append(datetimeObj.isoformat())
    return datetimeObj.isoformat()

def parse_date(dateStr):
    nums = [int(x) for x in dateStr.split("/")]
    if len(nums) < 3 and nums[0] >= 8:
        year = start_year
    else:
        year = end_year or 2024
    dateFormatted = year + "/" + dateStr
    formatStr = "%Y/%m/%d"
    datetimeObj = datetime.datetime.strptime(dateFormatted, formatStr).date()
    all_dates.append(datetimeObj)
    return datetimeObj

def parse_time():
    #@TODO
    print("Here's where we parse the time, if it's present")

def parse_isoformat(parsed_date, parsed_time):
    #@TODO
    print("Here's where we combine the parsed date and potential parsed time to return an isoformat datetime")

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
def parse_date_range(item):
    # x = re.findall(r'\d+[/]\d+', item)
    x = re.findall(r'\d+', item)
    if len(x)<4:
        rangeStr = x[0] + "/" + x[1], x[0] + "/" + x[2]
        print(rangeStr)
        for i in range(int(x[1]), int(x[2])+1):
            print(x[0]+"/"+str(i))
    elif len(x) == 4:
        print("We need to handle multiple months here")

for item in keyword_results:
    print(item)
    match = re.search(r'\d*/\d*', item).group()

    # if contains -, send to another parsing function
    # Maybe flag "-" check on and off? It's trigger with the age
    # ranges in the soccer schedule

    # Need a better way to find ranges. Maybe matching a
    # regex pattern with a range would be better
    if "-" in item:
        # parse_date_range(item)
        print("Hold for now") # because it's not yet functional
    else:
        iso = parse_date(match)
        print(iso)

    event = {
        'summary': keyword,
        'start': {
            'date': str(iso),
        },
        'end': {
            'date': str(iso)
        }
    }

    # send to Google cal
    # calapi.main(event)

    print(event)

# print(all_dates)