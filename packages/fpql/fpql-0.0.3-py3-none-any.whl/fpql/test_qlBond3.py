import QuantLib as ql 
from ql_enums import *
from pymodels import *
from ql_utils import *
from ql_conventions import *

#************************************************************************************
# VALUATION OF BONDS USING LEG CLASS
# Findings:
# 1. NPV and thus pricing is different from qlBond and ql.FixedRateBond
#************************************************************************************
fv = 100.00
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
mdate = "2029-01-05"

bonddata = {"issue_date": idate,
            "maturity": mdate, 
            "settings": setting, 
            "coupon": 0.05,
            "face_value": fv}
thebond = FixedRateBond(**bonddata)


issue_date = datestr_to_qldate(thebond.issue_date)
maturity = datestr_to_qldate(thebond.maturity)
ql.Settings.instance().evaluationDate = issue_date 
ql_period = ql.Period(ql_freq_tenor[setting.frequency])

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


items = len(lsche)
cashflows = []
for i in range(items):
    if i == 0:
        cf = ql.SimpleCashFlow(0.00, schedule[i])
    elif i == items - 1:
        cf = ql.SimpleCashFlow(interests[i-1].amount() + fv, lsche[i])
    else:
        cf = ql.SimpleCashFlow(interests[i-1].amount(), lsche[i])
    
    print(cf.date(), cf.amount(),cf)
    cashflows.append(cf)



#for cf in cashflows:
#    print(cf.date(), cf.amount())

leg = ql.Leg(cashflows)


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
print("***************************************************************************")
print(f"Dirty Price = {dirty_price}, Clean Price = {clean_price}, Accrued = {accrued}")
print(f"YTM = {ytm}")
#*******************************************************************************
#USING QL.FIXRATEBOND
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
print(f"BondFunctions.accruedAmount = {accrued}")
print(aprice + accrued)

print("***********************************************************************")
print("USING LEG")
npv = ql.CashFlows.npv(leg, rate, False, issue_date, issue_date)
#accrued = ql.CashFlows.accruedAmount(leg, rate, False, issue_date, issue_date)
price = npv/fv

yld = ql.CashFlows.yieldRate(leg, 
                            npv, 
                            ql_day_count[setting.day_count], 
                            ql.Compounded, 
                            ql_frequency[setting.frequency], 
                            True)
print(f"NPV = {npv}, price = {price}, yield = {yld}") #, accrued = {accrued}" )

