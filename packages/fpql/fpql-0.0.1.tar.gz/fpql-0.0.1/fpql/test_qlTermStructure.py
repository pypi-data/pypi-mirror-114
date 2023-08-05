import QuantLib as ql

from pym_ql_utils import *
from pymodels import *
from pym_ql_utils import *

value_date = "2021-01-02"
vdate = datestr_to_qldate(value_date) 
ql.Settings.instance().evaluationDate = vdate

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
#print(f"bond_helpers = {bond_helpers}")

#The yield curve is constructed by putting the two helpers together.
rate_helpers = depo_helpers + bond_helpers

day_count = ql_day_count[par_setting.day_count]
yieldcurve = ql.PiecewiseLogCubicDiscount(vdate,
                             rate_helpers,
                             ql_day_count[par_setting.day_count])

spots = []
tenors = []
counter = 0
print(f"YIELD CURVE: {yieldcurve}")

print(f"LIST OF DATE FROM CURVES: {yieldcurve.dayCounter}")
compounding = ql.Compounded
freq = ql.Semiannual
d = datestr_to_qldate("2022-01-02") 
yrs = day_count.yearFraction(vdate, d)
print(f"YRS type {type(yrs)}")
zero_rate = yieldcurve.zeroRate(yrs, compounding, freq)
eq_rate = zero_rate.equivalentRate(day_count,
                                       compounding,
                                       freq,
                                       vdate,
                                       d).rate()
print(f"ZERO RATE IS {eq_rate*100}%")

for d in yieldcurve.dates():
    print(d)
    yrs = day_count.yearFraction(vdate, d)
    compounding = ql.Compounded
    freq = ql.Semiannual
    zero_rate = yieldcurve.zeroRate(yrs, compounding, freq)
    tenors.append(yrs)
    eq_rate = zero_rate.equivalentRate(day_count,
                                       compounding,
                                       freq,
                                       vdate,
                                       d)
    therate = eq_rate.rate()
    spots.append(therate*100)
    counter += 1

print(spots)
print(type(yieldcurve))