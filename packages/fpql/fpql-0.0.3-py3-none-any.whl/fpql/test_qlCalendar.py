import QuantLib as ql
from ql_utils import *

holidays = ["2021-01-01", "2021-05-01", "2020-12-25"]
theholidays = []
for holiday in holidays:
    thedate = {"date": holiday}
    theholiday = Holiday(**thedate)
    theholidays.append(theholiday)

#Test to check holidays
business_day = BusinessDay.mod_following
thedate = "2025-01-01"
calendar = create_calendar("test", holidays=theholidays)
print(f"Is {thedate} a holiday?: {calendar.isHoliday(datestr_to_qldate(thedate))}")
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
print(adv_date.ISO())

cal = ql.UnitedStates()
print(type(cal))