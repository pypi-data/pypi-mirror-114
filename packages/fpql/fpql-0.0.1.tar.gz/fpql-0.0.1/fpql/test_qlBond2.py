import QuantLib as ql 
from ql_enums import *
from pymodels import *
from ql_utils import *
from ql_conventions import *


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
idate = "2021-01-04"
mdate = "2029-01-04"

bonddata = {"issue_date": idate, 
            "maturity": mdate, 
            "settings": setting, 
            "coupon": 0.05,
            "face_value": fv}
thebond = FixedRateBond(**bonddata)

issue_date = datestr_to_qldate(thebond.issue_date)
maturity = datestr_to_qldate(thebond.maturity)
print(type(issue_date))
ql.Settings.instance().evaluationDate = issue_date + 1
ql_period = ql.Period(ql_freq_tenor[setting.frequency])
#print(ql_period)
#1. Create Schedule
schedule = ql.Schedule(issue_date, 
                        maturity, 
                        ql_period, 
                        ql.WeekendsOnly(), 
                        ql_business_day[setting.business_day],
                        ql_business_day[setting.terminate_business_day],
                        ql_date_generation[setting.date_gen],
                        setting.is_eom)
lsche = list(schedule)
#print(lsche)
interest = ql.FixedRateLeg(schedule, ql_day_count[setting.day_count], [fv], [thebond.coupon])
interests = list(interest)

#for inter in interests:
#    print(inter.amount())
#    print(inter.date())
bond = ql.Bond(0, ql.WeekendsOnly(), issue_date, interest)
dirty_price = bond.dirtyPrice(0.05, 
                            ql_day_count[setting.day_count], 
                            ql.Compounded, 
                            ql_frequency[setting.frequency])
clean_price = bond.cleanPrice(0.05, 
                            ql_day_count[setting.day_count], 
                            ql.Compounded, 
                            ql_frequency[setting.frequency])
ytm = bond.bondYield(100.00, 
                    ql_day_count[setting.day_count], 
                    ql.Compounded, 
                    ql_frequency[setting.frequency], 
                    issue_date, 1e-08, 100)

accrued = ql.BondFunctions.accruedAmount(bond)
print("********************TESTING USING QLBOND*********************************")
print(f"Dirty Price = {dirty_price}, Clean Price = {clean_price}, Accrued = {accrued}")
print(f"YTM = {ytm}")

print("********************TESTING USING FIXEDRATEBOND*********************************")
fixbond = ql.FixedRateBond(0, fv, schedule, [thebond.coupon], ql_day_count[setting.day_count])

rate = ql.InterestRate(0.05, ql_day_count[setting.day_count], 
                        ql.Compounded, 
                        ql_frequency[setting.frequency])
fb_clean_price = ql.BondFunctions.cleanPrice(fixbond, rate)
print(fb_clean_price)
amount = ql.BondFunctions.nextCashFlowAmount(fixbond)
print(f"Next CashFlow amount = {amount}")

amount = ql.BondFunctions.previousCashFlowAmount(fixbond)
print(f"Previous CashFlow amount = {amount}")


crv = ql.FlatForward(0, ql.WeekendsOnly(), 0.05, ql_day_count[setting.day_count],
                    ql.Compounded, ql_frequency[setting.frequency])
aprice = ql.BondFunctions.cleanPrice(fixbond, rate)
print(f"Price Using Flat Forward = {aprice}")
accrued = ql.BondFunctions.accruedAmount(fixbond)
accruedP = ql.BondFunctions.accruedPeriod(fixbond)
print(f"BondFunctions.accruedAmount = {accrued}, BondFunctions.accruedPeriod = {accruedP}")
print(aprice + accrued)
print()


print("***************TESTING FIXRATEBOND USING ENGINE**********************")
#print("**** FINALLY IGNORE BOND ENGINE ******")
yts = ql.YieldTermStructureHandle(crv)
engine = ql.DiscountingBondEngine(yts)
#fixbond.setPricingEngine(engine)
settlement = fixbond.settlementValue(99.99792267910406)
#cleanPrice = fixbond.cleanPrice()
cleanPrice = fixbond.cleanPrice(0.05, 
                                ql_day_count[setting.day_count],
                                ql.Compounded,
                                ql_frequency[setting.frequency])
dirtyPrice = fixbond.dirtyPrice(0.05, 
                                ql_day_count[setting.day_count],
                                ql.Compounded,
                                ql_frequency[setting.frequency])
ytm = fixbond.bondYield(99.99792267910406, 
                                ql_day_count[setting.day_count],
                                ql.Compounded,
                                ql_frequency[setting.frequency])

bps = ql.BondFunctions.bps(fixbond, rate)
duration = ql.BondFunctions.duration(fixbond, rate, ql.Duration.Macaulay)
modified_duration = ql.BondFunctions.duration(bond, rate, ql.Duration.Modified)
convexity = ql.BondFunctions.convexity(fixbond, rate)
basis_point_value = ql.BondFunctions.basisPointValue(fixbond, rate)
yield_value_basis_point = ql.BondFunctions.yieldValueBasisPoint(fixbond, rate)

print(f"settlement = {settlement}, cleanPrice = {cleanPrice}")
print(f"accrued = {fixbond.accruedAmount()}")
print(f"dirty price = {dirtyPrice}")
print(f"YTM = {ytm}")
print(f"bps = {bps}, basis_point_value = {basis_point_value}, yield_value_basis_point = {yield_value_basis_point}")
print(f"duration = {duration}, modified_duration = {modified_duration}, convexity = {convexity}")
print(type(fixbond.frequency()))
