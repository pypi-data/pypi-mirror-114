import pandas as pd
from ql_utils import *

issue_date = "2021-05-15"
maturity = "2025-03-01"
frequency = "6M"
holidays = ["2021-01-01", "2021-05-01", "2020-12-25"]
theholidays = []
for holiday in holidays:
    thedate = {"date": holiday}
    theholiday = Holiday(**thedate)
    theholidays.append(theholiday)
calendar = create_calendar("MYR",holidays=theholidays)
business_day = BusinessDay.mod_following
maturity_business_day = BusinessDay.no_adjustment
date_gen = DateGeneration.backward
#****************************************************************
# Note: Using qlSchedule to generate the dates requires issue_date
#       if the date_gen is DateGeneration.forward. For DateGeneration.backward
#       issue_date can be the value date. This may still however cause some
#       unexpected result from calculating the day count factor.
#       Hence, it is best that issue_date information is available.
schedules = qlSchedule(issue_date, maturity, frequency, calendar,
                business_day, maturity_business_day,
                date_gen)

schedules = list(schedules)
print(f"qlSchedule return {schedules}")

#*******************************************************************
# Note: Using qlMakeSchedule is the simplified version of qlSchedule
makeschedules = qlMakeScedule(issue_date, maturity, frequency)
makeschedules = list(makeschedules)
print(f"qlMakeSchedule return {makeschedules}")

#*******************************************************************
# Adjusting a date to a convention
datetoadjust = datestr_to_qldate("2022-02-28")
newdate = calendar.adjust(datetoadjust, ql_business_day[business_day])
print(f"old date: {datetoadjust} adjusted to: {newdate}")


#**********************************************************************
# advancing date based on convention
# One can advance the date forward or backward
adv_date= calendar.advance(datetoadjust, ql.Period(6,ql.Months),     
                            ql_business_day[business_day], False)
print(f"old date: {datetoadjust} advanced to: {adv_date}")
