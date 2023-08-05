import QuantLib as ql

from pym_ql_utils import *
from pymodels import *
from pym_ql_utils import *

value_date = "2021-01-05"
vdate = datestr_to_qldate(value_date)

#*************************************************************************
#CUSTOM CALENDAR
holidays = ["2021-01-01", "2021-05-01", "2020-12-25"]
theholidays = []
for holiday in holidays:
    thedate = {"date": holiday}
    theholiday = Holiday(**thedate)
    theholidays.append(theholiday)

calendar = create_calendar("test", holidays=theholidays)

ql.Settings.instance().evaluationDate = vdate

#**************************************************************
# YIELD CURVE
depo_rates = [
    {"tenor": "1M", "rate": 2.00},
    {"tenor": "2M", "rate": 2.05}, 
    {"tenor": "3M", "rate": 2.10},
    {"tenor": "6M", "rate": 2.20}
]

rates = []
for depo_rate in depo_rates:
    rate = Rate(**depo_rate)
    rates.append(rate)

depo_sett = {
    "start_basis": StartBasis.today, 
    "business_day": BusinessDay.mod_following,
    "day_count": DayCount.act_act_act365,
    "eom": False
    }
depo_setting = DepoSetting(**depo_sett)

depo_helpers = deporate_2_depohelpers(depo_setting, rates)
#print(f"depo_helpers = {depo_helpers}")


par_rates = [
    {"tenor": "1Y", "rate": 2.30},
    {"tenor": "2Y", "rate": 2.40}, 
    {"tenor": "3Y", "rate": 2.50},
    {"tenor": "5Y", "rate": 2.70},
    {"tenor": "7Y", "rate": 2.80},
    {"tenor": "10Y", "rate": 2.90},
    {"tenor": "20Y", "rate": 3.00},
    {"tenor": "30Y", "rate": 3.10}
]

parrates = []
for par_rate in par_rates:
    rate = Rate(**par_rate)
    parrates.append(rate)

par_sett = {
    "frequency": "Semi-Annual",
    "start_basis": 2,
    "day_count": "Actual/Actual (ISMA)",
    "business_day": "Modified Following",
    "terminate_business_day": "Modified Following",
    "date_gen": "Backward from maturity date",
    "is_eom":  False
}
par_setting = BondSetting(**par_sett)

bond_helpers = parrate_2_bondhelpers(value_date, par_setting, parrates)

rate_helpers = depo_helpers + bond_helpers

day_count = ql_day_count[par_setting.day_count]
yieldcurve = ql.PiecewiseLogCubicDiscount(vdate,
                             rate_helpers,
                             ql_day_count[par_setting.day_count])
rfcurve_handle = ql.YieldTermStructureHandle(yieldcurve)

#**********************************************************************
# CREDIT SPREADS
spreads = [
    {"tenor": "1M", "rate": 0.4},
    {"tenor": "2M", "rate": 0.45}, 
    {"tenor": "3M", "rate": 0.5},
    {"tenor": "6M", "rate": 0.55},
    {"tenor": "1Y", "rate": 0.6},
    {"tenor": "2Y", "rate": 0.65}, 
    {"tenor": "3Y", "rate": 0.75},
    {"tenor": "5Y", "rate": 0.85},
    {"tenor": "7Y", "rate": 0.95},
    {"tenor": "10Y", "rate": 1.1},
    {"tenor": "20Y", "rate": 1.3},
    {"tenor": "30Y", "rate": 1.5}
]


spread_handles = []
spread_dates = []
spread_quotes = []
for spread in spreads:
    spread_quote = ql.SimpleQuote(spread["rate"]/100)
    spread_quotes.append(spread_quote)
    spread_handle = ql.QuoteHandle(spread_quote)
    spread_handles.append(spread_handle)
    maturity = calendar.advance(vdate, get_qlPeriod(spread['tenor']))
    spread_dates.append(maturity)

spread_curve = ql.SpreadedLinearZeroInterpolatedTermStructure(
                        rfcurve_handle,
                        spread_handles,
                        spread_dates)
spread_curve_handle = ql.YieldTermStructureHandle(spread_curve)


#****************************************************************
# THE BOND
fv = 100_000_000.00
bondsetting = {
    "frequency":Frequency.semi_annual,
    "start_basis": StartBasis.today,
    "day_count": DayCount.act_act_isma,
    "business_day": BusinessDay.no_adjustment,
    "terminate_business_day": BusinessDay.no_adjustment,
    "date_gen": DateGeneration.backward,
    "is_eom":  True
}

setting = BondSetting(**bondsetting)
idate = "2021-01-05"
mdate = "2031-01-05"

bonddata = {"issue_date": idate, 
            "maturity": mdate, 
            "settings": setting, 
            "coupon": 0.029,
            "face_value": fv}
thebond = FixedRateBond(**bonddata)

issue_date = datestr_to_qldate(thebond.issue_date)
maturity = datestr_to_qldate(thebond.maturity)
ql_period = ql.Period(ql_freq_tenor[setting.frequency])

schedule = ql.Schedule(issue_date, 
                        maturity, 
                        ql_period, 
                        ql.WeekendsOnly(), 
                        ql_business_day[setting.business_day],
                        ql_business_day[setting.terminate_business_day],
                        ql_date_generation[setting.date_gen],
                        setting.is_eom)

fixbond = ql.FixedRateBond(0, fv, schedule, [thebond.coupon], ql_day_count[setting.day_count])

#************************************************************************************
# THE BOND ENGINE
rf_curve_engine = ql.DiscountingBondEngine(rfcurve_handle)
fixbond.setPricingEngine(rf_curve_engine)
value1 = fixbond.NPV()

bspread_engine = ql.DiscountingBondEngine(spread_curve_handle)
fixbond.setPricingEngine(bspread_engine)
value2 = fixbond.NPV()

spread_quotes[9].setValue(0.40/100)
spread_quotes[10].setValue(0.550/100)
value3 = fixbond.NPV()


print(f"value1 = {value1}, value2 = {value2}, value3 = {value3}")

