from samples import *
import QuantLib as ql 
from ql_enums import *
from pymodels import *
from ql_utils import *
from ql_conventions import *
from samples import *


#calendar = ql.Malaysia()
thebond, setting = sample_bondinfo()

issue_date = datestr_to_qldate(thebond.issue_date)
maturity = datestr_to_qldate(thebond.maturity)

ql.Settings.instance().evaluationDate = issue_date

bond = sample_qlbond()

print("********************TESTING USING FIXEDRATEBOND*********************************")
fixbond = sample_fixedratebond()

rate = ql.InterestRate(0.05, ql_day_count[setting.day_count], 
                        ql.Compounded, 
                        ql_frequency[setting.frequency])

print("*************RISK WITH QL BOND USING BOND FUNCTIONS*************")
risks = sample_bondrisk(bond, rate)
print(risks)

print("*************RISK WITH FIXEDRATEBOND USING BOND FUNCTIONS*************")
risks = sample_bondrisk(fixbond, rate)
print(risks)
