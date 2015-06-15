"""
Testing file for calculate.py
"""

from pandas import DataFrame, concat
from taxcalc.calculate import *
from taxcalc.functions import *
from taxcalc.records import *
from taxcalc.parameters import *
import taxcalc.parameters as parameters
#from timer.timed_calculate import *


def to_csv(fname, df):
    """
    Save this dataframe to a CSV file with name 'fname' and containing
    a header with the column names of the dataframe.
    """
    df.to_csv(fname, float_format= '%1.3f', sep=',', header=True, index=False)



def run(puf=True):
    """
    Run each function defined in calculate.py, saving the ouput to a CSV file.
    'puf' set to True by default, to use the 'puf2.csv' as an input

    For functions returning an additional non-global variable in addition
    to the DataFrame to be printed, one line saves the dataFrame to be printed 
    first, and then saves the variable to be used by a following function second. 
    """

    # Create a Parameters object
    params = Parameters()

    # Create a Public Use File object

    tax_dta = pd.read_csv("puf.csv")

    blowup_factors = "./taxcalc/StageIFactors.csv"
    weights = "./taxcalc/WEIGHTS.csv"

    puf = Records(tax_dta, blowup_factors, weights)

    # Create a Calculator
    calc = Calculator(parameters=params, records=puf)
    # Dist_Corp_Inc_Tax(calc.params, calc.records)
    (agg_comp, agg_dividends, agg_capgains,
     agg_bonds, agg_self_employed) = calc.aggregate_measures()

    Dist_Corp_Inc_Tax(agg_comp, agg_dividends, agg_capgains,
                      agg_bonds, agg_self_employed, calc.params, calc.records)


if __name__ == '__main__':
    run()