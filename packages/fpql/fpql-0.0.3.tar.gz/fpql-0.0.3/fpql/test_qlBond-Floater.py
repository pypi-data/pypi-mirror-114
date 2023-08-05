import QuantLib as ql 
from ql_enums import *
from pymodels import *
from ql_utils import *
from ql_conventions import *
from termstructure import *
from samples import *

# use sample data
thebond, setting = sample_bondinfo()
vdate = "2021-01-05"

issue_date = datestr_to_qldate(thebond.issue_date)
maturity = datestr_to_qldate(thebond.maturity)
value_date = datestr_to_qldate(vdate)

ql.Settings.instance().evaluationDate = issue_date + 100
ql_period = ql.Period(ql_freq_tenor[setting.frequency])

frb = sample_FRB()

#for cf in frb.cashflows():
#    print(cf.date(), cf.amount())

clean_price = frb.dirtyPrice()
print(f"dirty_price using flat curve= {clean_price}")


#*************************************************************************
# VALUATION WITH A A CURVE

# Curve data

piecewise = sample_piecewise(vdate)
pw_handle = ql.YieldTermStructureHandle(piecewise)
frb_engine = ql.DiscountingBondEngine(pw_handle)
#Changing pricing engine doesnt seems to change the dirty price
frb.setPricingEngine(frb_engine)

dirty_price = frb.dirtyPrice()
print(f"dirty_price with piecewise = {clean_price}")