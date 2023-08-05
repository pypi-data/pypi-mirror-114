from samples import *
import QuantLib as ql 
from ql_enums import *
from pymodels import *
from ql_utils import *
from ql_conventions import *

########################################################################
# FIXED RATE LOANS WITH STRUCTURED PRINCIPALS AND RATES
# The module uses ql.Leg since only this classes cater for structured face 
# values and rates.
theloan, setting  = sample_structuredloaninfo()
issue_date = datestr_to_qldate(theloan.issue_date)
maturity = datestr_to_qldate(theloan.maturity)

ql.Settings.instance().evaluationDate = issue_date + 20

ql_period = ql.Period(ql_freq_tenor[setting.frequency])

loanleg = sample_floatingrate_structuredloan()
print(len(loanleg))
for loan in loanleg:
    print(loan.date(), loan.amount())
#Valuing loans with IRR
irr = ql.InterestRate(.05, 
                        ql_day_count[theloan.settings.day_count], 
                        ql.Simple, 
                        ql_frequency[theloan.settings.frequency])
loan_value = ql.CashFlows.npv(loanleg, irr, True)
print(f"loan value = {loan_value}")

#IRR
irr_rate = ql.CashFlows.yieldRate(loanleg, 
                    10_000_000, 
                    ql_day_count[theloan.settings.day_count], 
                    ql.Compounded, 
                    ql_frequency[theloan.settings.frequency],
                    True, 
                    issue_date)

print(f"IRR = {irr_rate}")





