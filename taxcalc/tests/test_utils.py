import os
import sys
import math
import filecmp
import tempfile
import numpy as np
import pandas as pd
import pytest
import numpy.testing as npt
from pandas import DataFrame, Series
from pandas.util.testing import assert_series_equal
CUR_PATH = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(CUR_PATH, '..', '..'))
from taxcalc import Policy, Records, Calculator
from taxcalc.utils import *

# use 1991 PUF-like data to emulate current puf.csv, which is private
TAXDATA_PATH = os.path.join(CUR_PATH, '..', 'altdata', 'puf91taxdata.csv.gz')
TAXDATA = pd.read_csv(TAXDATA_PATH, compression='gzip')
WEIGHTS_PATH = os.path.join(CUR_PATH, '..', 'altdata', 'puf91weights.csv.gz')
WEIGHTS = pd.read_csv(WEIGHTS_PATH, compression='gzip')

data = [[1.0, 2, 'a'],
        [-1.0, 4, 'a'],
        [3.0, 6, 'a'],
        [2.0, 4, 'b'],
        [3.0, 6, 'b']]

data_float = [[1.0, 2, 'a'],
              [-1.0, 4, 'a'],
              [0.0000000001, 3, 'a'],
              [-0.0000000001, 1, 'a'],
              [3.0, 6, 'a'],
              [2.0, 4, 'b'],
              [0.0000000001, 3, 'b'],
              [-0.0000000001, 1, 'b'],
              [3.0, 6, 'b']]


def test_expand_1D_short_array():
    x = np.array([4, 5, 9], dtype='i4')
    exp2 = np.array([9.0 * math.pow(1.02, i) for i in range(1, 8)])
    exp1 = np.array([4, 5, 9])
    exp = np.zeros(10)
    exp[:3] = exp1
    exp[3:] = exp2
    res = Policy.expand_1D(x, inflate=True, inflation_rates=[0.02] * 10,
                           num_years=10)
    npt.assert_allclose(exp, res, atol=0.0, rtol=1.0E-7)


def test_expand_1D_variable_rates():
    x = np.array([4, 5, 9], dtype='f4')
    irates = [0.02, 0.02, 0.03, 0.035]
    exp2 = []
    cur = 9.0
    exp = np.array([4, 5, 9, 9 * 1.03, 9 * 1.03 * 1.035])
    res = Policy.expand_1D(x, inflate=True, inflation_rates=irates,
                           num_years=5)
    npt.assert_allclose(exp.astype('f4', casting='unsafe'), res)


def test_expand_1D_scalar():
    x = 10.0
    exp = np.array([10.0 * math.pow(1.02, i) for i in range(0, 10)])
    res = Policy.expand_1D(x, inflate=True, inflation_rates=[0.02] * 10,
                           num_years=10)
    npt.assert_allclose(exp, res)


def test_expand_1D_accept_None():
    x = [4., 5., None]
    irates = [0.02, 0.02, 0.03, 0.035]
    exp = []
    cur = 5.0 * 1.02
    exp = [4., 5., cur]
    cur *= 1.03
    exp.append(cur)
    cur *= 1.035
    exp.append(cur)
    exp = np.array(exp)
    res = Policy.expand_array(x, inflate=True, inflation_rates=irates,
                              num_years=5)
    npt.assert_allclose(exp.astype('f4', casting='unsafe'), res)


def test_expand_2D_short_array():
    x = np.array([[1, 2, 3]], dtype=np.float64)
    val = np.array([1, 2, 3], dtype=np.float64)
    exp2 = np.array([val * math.pow(1.02, i) for i in range(1, 5)])
    exp1 = np.array([1, 2, 3], dtype=np.float64)
    exp = np.zeros((5, 3))
    exp[:1] = exp1
    exp[1:] = exp2
    res = Policy.expand_2D(x, inflate=True, inflation_rates=[0.02] * 5,
                           num_years=5)
    npt.assert_allclose(exp, res)


def test_expand_2D_variable_rates():
    x = np.array([[1, 2, 3]], dtype=np.float64)
    cur = np.array([1, 2, 3], dtype=np.float64)
    irates = [0.02, 0.02, 0.02, 0.03, 0.035]
    exp2 = []
    for i in range(0, 4):
        idx = i + len(x) - 1
        cur = np.array(cur * (1.0 + irates[idx]))
        print("cur is ", cur)
        exp2.append(cur)
    exp1 = np.array([1, 2, 3], dtype=np.float64)
    exp = np.zeros((5, 3), dtype=np.float64)
    exp[:1] = exp1
    exp[1:] = exp2
    res = Policy.expand_2D(x, inflate=True, inflation_rates=irates,
                           num_years=5)
    npt.assert_allclose(exp, res)


def test_create_tables():
    # create a current-law Policy object and Calculator object calc1
    policy1 = Policy()
    records1 = Records(data=TAXDATA, weights=WEIGHTS, start_year=2009)
    calc1 = Calculator(policy=policy1, records=records1)
    calc1.calc_all()
    # create a policy-reform Policy object and Calculator object calc2
    reform = {2013: {'_II_rt4': [0.56]}}
    policy2 = Policy()
    policy2.implement_reform(reform)
    records2 = Records(data=TAXDATA, weights=WEIGHTS, start_year=2009)
    calc2 = Calculator(policy=policy2, records=records2)
    calc2.calc_all()
    # create various distribution tables
    t2 = create_distribution_table(calc2, groupby="small_income_bins",
                                   result_type="weighted_sum")
    tdiff = create_difference_table(calc1, calc2, groupby="large_income_bins")
    tdiff_webapp = create_difference_table(calc1, calc2,
                                           groupby="webapp_income_bins")


def test_weighted_count_lt_zero():
    df1 = DataFrame(data=data, columns=['tax_diff', 's006', 'label'])
    grped = df1.groupby('label')
    diffs = grped.apply(weighted_count_lt_zero, 'tax_diff')
    exp = Series(data=[4, 0], index=['a', 'b'])
    exp.index.name = 'label'
    assert_series_equal(exp, diffs)
    df2 = DataFrame(data=data_float, columns=['tax_diff', 's006', 'label'])
    grped = df2.groupby('label')
    diffs = grped.apply(weighted_count_lt_zero, 'tax_diff')
    exp = Series(data=[4, 0], index=['a', 'b'])
    exp.index.name = 'label'
    assert_series_equal(exp, diffs)


def test_weighted_count_gt_zero():
    df1 = DataFrame(data=data, columns=['tax_diff', 's006', 'label'])
    grped = df1.groupby('label')
    diffs = grped.apply(weighted_count_gt_zero, 'tax_diff')
    exp = Series(data=[8, 10], index=['a', 'b'])
    exp.index.name = 'label'
    assert_series_equal(exp, diffs)
    df2 = DataFrame(data=data, columns=['tax_diff', 's006', 'label'])
    grped = df2.groupby('label')
    diffs = grped.apply(weighted_count_gt_zero, 'tax_diff')
    exp = Series(data=[8, 10], index=['a', 'b'])
    exp.index.name = 'label'
    assert_series_equal(exp, diffs)


def test_weighted_count():
    df = DataFrame(data=data, columns=['tax_diff', 's006', 'label'])
    grped = df.groupby('label')
    diffs = grped.apply(weighted_count)
    exp = Series(data=[12, 10], index=['a', 'b'])
    exp.index.name = 'label'
    assert_series_equal(exp, diffs)


def test_weighted_mean():
    df = DataFrame(data=data, columns=['tax_diff', 's006', 'label'])
    grped = df.groupby('label')
    diffs = grped.apply(weighted_mean, 'tax_diff')
    exp = Series(data=[16.0 / 12.0, 26.0 / 10.0], index=['a', 'b'])
    exp.index.name = 'label'
    assert_series_equal(exp, diffs)


def test_weighted_sum():
    df = DataFrame(data=data, columns=['tax_diff', 's006', 'label'])
    grped = df.groupby('label')
    diffs = grped.apply(weighted_sum, 'tax_diff')
    exp = Series(data=[16.0, 26.0], index=['a', 'b'])
    exp.index.name = 'label'
    assert_series_equal(exp, diffs)


def test_weighted_perc_inc():
    df = DataFrame(data=data, columns=['tax_diff', 's006', 'label'])
    grped = df.groupby('label')
    diffs = grped.apply(weighted_perc_inc, 'tax_diff')
    exp = Series(data=[8. / 12., 1.0], index=['a', 'b'])
    exp.index.name = 'label'
    assert_series_equal(exp, diffs)


def test_weighted_perc_dec():
    df = DataFrame(data=data, columns=['tax_diff', 's006', 'label'])
    grped = df.groupby('label')
    diffs = grped.apply(weighted_perc_dec, 'tax_diff')
    exp = Series(data=[4. / 12., 0.0], index=['a', 'b'])
    exp.index.name = 'label'
    assert_series_equal(exp, diffs)


def test_weighted_share_of_total():
    df = DataFrame(data=data, columns=['tax_diff', 's006', 'label'])
    grped = df.groupby('label')
    diffs = grped.apply(weighted_share_of_total, 'tax_diff', 42.0)
    exp = Series(data=[16.0 / (42. + EPSILON), 26.0 / (42.0 + EPSILON)],
                 index=['a', 'b'])
    exp.index.name = 'label'
    assert_series_equal(exp, diffs)


def test_add_income_bins():
    data = np.arange(1, 1e6, 5000)
    df = DataFrame(data=data, columns=['_expanded_income'])
    bins = [-1e14, 0, 9999, 19999, 29999, 39999, 49999, 74999, 99999,
            200000, 1e14]
    df = add_income_bins(df, compare_with="tpc", bins=None)
    grpd = df.groupby('bins')
    grps = [grp for grp in grpd]
    for g, num in zip(grps, bins[1:-1]):
        assert g[0].endswith(str(num) + "]")
    grpdl = add_income_bins(df, compare_with="tpc", bins=None, right=False)
    grpdl = grpdl.groupby('bins')
    grps = [grp for grp in grpdl]
    for g, num in zip(grps, bins[1:-1]):
        assert g[0].endswith(str(num) + ")")


def test_add_income_bins_soi():
    data = np.arange(1, 1e6, 5000)
    df = DataFrame(data=data, columns=['_expanded_income'])
    bins = [-1e14, 0, 4999, 9999, 14999, 19999, 24999, 29999, 39999,
            49999, 74999, 99999, 199999, 499999, 999999, 1499999,
            1999999, 4999999, 9999999, 1e14]
    df = add_income_bins(df, compare_with="soi", bins=None)
    grpd = df.groupby('bins')
    grps = [grp for grp in grpd]
    for g, num in zip(grps, bins[1:-1]):
        assert g[0].endswith(str(num) + "]")
    grpdl = add_income_bins(df, compare_with="soi", bins=None, right=False)
    grpdl = grpdl.groupby('bins')
    grps = [grp for grp in grpdl]
    for g, num in zip(grps, bins[1:-1]):
        assert g[0].endswith(str(num) + ")")


def test_add_income_bins_specify_bins():
    data = np.arange(1, 1e6, 5000)
    df = DataFrame(data=data, columns=['_expanded_income'])
    bins = [-1e14, 0, 4999, 9999, 14999, 19999, 29999, 32999, 43999,
            1e14]
    df = add_income_bins(df, bins=bins)
    grpd = df.groupby('bins')
    grps = [grp for grp in grpd]
    for g, num in zip(grps, bins[1:-1]):
        assert g[0].endswith(str(num) + "]")
    grpdl = add_income_bins(df, bins=bins, right=False)
    grpdl = grpdl.groupby('bins')
    grps = [grp for grp in grpdl]
    for g, num in zip(grps, bins[1:-1]):
        assert g[0].endswith(str(num) + ")")


def test_add_income_bins_raises():
    data = np.arange(1, 1e6, 5000)
    df = DataFrame(data=data, columns=['_expanded_income'])
    with pytest.raises(ValueError):
        df = add_income_bins(df, compare_with="stuff")


def test_add_weighted_decile_bins():
    df = DataFrame(data=data, columns=['_expanded_income', 's006', 'label'])
    df = add_weighted_decile_bins(df)
    assert 'bins' in df
    bin_labels = df['bins'].unique()
    default_labels = set(range(1, 11))
    for lab in bin_labels:
        assert lab in default_labels
    # Custom labels
    custom_labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    df = add_weighted_decile_bins(df, labels=custom_labels)
    assert 'bins' in df
    bin_labels = df['bins'].unique()
    for lab in bin_labels:
        assert lab in custom_labels


def test_add_columns():
    cols = [[1000, 40, -10, 0, 10],
            [100, 8, 9, 100, 20],
            [-1000, 38, 90, 800, 30]]
    df = DataFrame(data=cols,
                   columns=['c00100', 'c04470', '_standard', 'c09600', 's006'])
    add_columns(df)
    npt.assert_array_equal(df.c04470, np.array([40, 0, 0]))
    npt.assert_array_equal(df.num_returns_ItemDed, np.array([10, 0, 0]))
    npt.assert_array_equal(df.num_returns_StandardDed, np.array([0, 20, 0]))
    npt.assert_array_equal(df.num_returns_AMT, np.array([0, 20, 30]))


def test_dist_table_sum_row():
    # Create a default Policy object
    policy1 = Policy()
    records1 = Records(data=TAXDATA, weights=WEIGHTS, start_year=2009)
    # Create a Calculator
    calc1 = Calculator(policy=policy1, records=records1)
    calc1.calc_all()
    t1 = create_distribution_table(calc1, groupby="small_income_bins",
                                   result_type="weighted_sum")
    t2 = create_distribution_table(calc1, groupby="large_income_bins",
                                   result_type="weighted_sum")
    npt.assert_allclose(t1[-1:], t2[-1:])
    t3 = create_distribution_table(calc1, groupby="small_income_bins",
                                   result_type="weighted_avg")


def test_diff_table_sum_row():
    # create a current-law Policy object and Calculator calc1
    policy1 = Policy()
    records1 = Records(data=TAXDATA, weights=WEIGHTS, start_year=2009)
    calc1 = Calculator(policy=policy1, records=records1)
    calc1.calc_all()
    # create a policy-reform Policy object and Calculator calc2
    reform = {2013: {'_II_rt4': [0.56]}}
    policy2 = Policy()
    policy2.implement_reform(reform)
    records2 = Records(data=TAXDATA, weights=WEIGHTS, start_year=2009)
    calc2 = Calculator(policy=policy2, records=records2)
    calc2.calc_all()
    # create two difference tables and compare their content
    tdiff1 = create_difference_table(calc1, calc2, groupby="small_income_bins")
    tdiff2 = create_difference_table(calc1, calc2, groupby="large_income_bins")
    non_digit_cols = ['mean', 'perc_inc', 'perc_cut', 'share_of_change']
    digit_cols = [x for x in tdiff1.columns.tolist() if
                  x not in non_digit_cols]
    npt.assert_allclose(tdiff1[digit_cols][-1:], tdiff2[digit_cols][-1:])
    assert np.array_equal(tdiff1[non_digit_cols][-1:],
                          tdiff2[non_digit_cols][-1:])


def test_row_classifier():
    # create a current-law Policy object and Calculator calc1
    policy1 = Policy()
    records1 = Records(data=TAXDATA, weights=WEIGHTS, start_year=2009)
    calc1 = Calculator(policy=policy1, records=records1)
    calc1.calc_all()
    calc1_s006 = create_distribution_table(calc1,
                                           groupby="webapp_income_bins",
                                           result_type="weighted_sum").s006
    # create a policy-reform Policy object and Calculator calc2
    reform = {2013: {"_ALD_StudentLoan_HC": [1]}}
    policy2 = Policy()
    policy2.implement_reform(reform)
    records2 = Records(data=TAXDATA, weights=WEIGHTS, start_year=2009)
    calc2 = Calculator(policy=policy2, records=records2)
    calc2.calc_all()
    calc2_s006 = create_distribution_table(calc2,
                                           groupby="webapp_income_bins",
                                           result_type="weighted_sum",
                                           baseline_calc=calc1).s006
    # use weighted sum of weights in each cell to check classifer
    npt.assert_array_equal(calc1_s006, calc2_s006)


def test_expand_2D_already_filled():
    _II_brk2 = [[36000, 72250, 36500, 48600, 72500, 36250],
                [38000, 74000, 36900, 49400, 73800, 36900],
                [40000, 74900, 37450, 50200, 74900, 37450]]
    res = Policy.expand_2D(_II_brk2, inflate=True, inflation_rates=[0.02] * 5,
                           num_years=3)
    npt.assert_array_equal(res, np.array(_II_brk2))


def test_expand_2D_partial_expand():
    _II_brk2 = [[36000, 72250, 36500, 48600, 72500, 36250],
                [38000, 74000, 36900, 49400, 73800, 36900],
                [40000, 74900, 37450, 50200, 74900, 37450]]
    # We have three years worth of data, need 4 years worth,
    # but we only need the inflation rate for year 3 to go
    # from year 3 -> year 4
    inf_rates = [0.02, 0.02, 0.03]
    exp1 = 40000 * 1.03
    exp2 = 74900 * 1.03
    exp3 = 37450 * 1.03
    exp4 = 50200 * 1.03
    exp5 = 74900 * 1.03
    exp6 = 37450 * 1.03
    exp = [[36000, 72250, 36500, 48600, 72500, 36250],
           [38000, 74000, 36900, 49400, 73800, 36900],
           [40000, 74900, 37450, 50200, 74900, 37450],
           [exp1, exp2, exp3, exp4, exp5, exp6]]
    res = Policy.expand_2D(_II_brk2, inflate=True, inflation_rates=inf_rates,
                           num_years=4)
    npt.assert_array_equal(res, exp)


def test_strip_Nones():
    x = [None, None]
    assert Policy.strip_Nones(x) == []
    x = [1, 2, None]
    assert Policy.strip_Nones(x) == [1, 2]
    x = [[1, 2, 3], [4, None, None]]
    assert Policy.strip_Nones(x) == [[1, 2, 3], [4, -1, -1]]


def test_expand_2D_accept_None():
    _II_brk2 = [[36000, 72250, 36500, 48600, 72500, 36250],
                [38000, 74000, 36900, 49400, 73800, 36900],
                [40000, 74900, 37450, 50200, 74900, 37450],
                [41000, None, None, None, None, None]]
    exp1 = 74900 * 1.02
    exp2 = 37450 * 1.02
    exp3 = 50200 * 1.02
    exp4 = 74900 * 1.02
    exp5 = 37450 * 1.02
    exp = [[36000, 72250, 36500, 48600, 72500, 36250],
           [38000, 74000, 36900, 49400, 73800, 36900],
           [40000, 74900, 37450, 50200, 74900, 37450],
           [41000, exp1, exp2, exp3, exp4, exp5]]
    exp = np.array(exp).astype('i4', casting='unsafe')
    res = Policy.expand_array(_II_brk2, inflate=True,
                              inflation_rates=[0.02] * 5,
                              num_years=4)
    npt.assert_array_equal(res, exp)

    user_mods = {2016: {u'_II_brk2': _II_brk2}}
    pol = Policy(start_year=2013)
    pol.implement_reform(user_mods)
    pol.set_year(2019)
    irates = Policy.default_inflation_rates()
    # The 2019 policy should be the combination of the user-defined
    # value and CPI-inflated values from 2018
    exp_2019 = [41000.] + [(1 + irates[2018]) * i for i in _II_brk2[2][1:]]
    exp_2019 = np.array(exp_2019)
    npt.assert_array_equal(pol.II_brk2, exp_2019)


def test_expand_2D_accept_None_additional_row():
    _II_brk2 = [[36000, 72250, 36500, 48600, 72500, 36250],
                [38000, 74000, 36900, 49400, 73800, 36900],
                [40000, 74900, 37450, 50200, 74900, 37450],
                [41000, None, None, None, None, None],
                [43000, None, None, None, None, None]]
    exp1 = 74900 * 1.02
    exp2 = 37450 * 1.02
    exp3 = 50200 * 1.02
    exp4 = 74900 * 1.02
    exp5 = 37450 * 1.02
    exp6 = exp1 * 1.03
    exp7 = exp2 * 1.03
    exp8 = exp3 * 1.03
    exp9 = exp4 * 1.03
    exp10 = exp5 * 1.03
    exp = [[36000, 72250, 36500, 48600, 72500, 36250],
           [38000, 74000, 36900, 49400, 73800, 36900],
           [40000, 74900, 37450, 50200, 74900, 37450],
           [41000, exp1, exp2, exp3, exp4, exp5],
           [43000, exp6, exp7, exp8, exp9, exp10]]
    inflation_rates = [0.015, 0.02, 0.02, 0.03]
    res = Policy.expand_array(_II_brk2, inflate=True,
                              inflation_rates=inflation_rates, num_years=5)
    npt.assert_array_equal(res, exp)

    user_mods = {2016: {u'_II_brk2': _II_brk2}}
    pol = Policy(start_year=2013)
    pol.implement_reform(user_mods)
    pol.set_year(2020)
    irates = Policy.default_inflation_rates()
    # The 2020 policy should be the combination of the user-defined
    # value and CPI-inflated values from 2018
    exp_2020 = [43000.] + [(1 + irates[2019]) * (1 + irates[2018]) * i
                           for i in _II_brk2[2][1:]]
    exp_2020 = np.array(exp_2020)
    npt.assert_allclose(pol.II_brk2, exp_2020)


@pytest.yield_fixture
def csvfile():
    txt = ("A,B,C,D,EFGH\n"
           "1,2,3,4,0\n"
           "5,6,7,8,0\n"
           "9,10,11,12,0\n"
           "100,200,300,400,500\n"
           "123.45,678.912,000.000,87,92")
    f = tempfile.NamedTemporaryFile(mode="a", delete=False)
    f.write(txt + "\n")
    f.close()
    # Must close and then yield for Windows platform
    yield f
    os.remove(f.name)


@pytest.yield_fixture
def asciifile():
    x = (
        "A              \t1              \t100            \t123.45         \n"
        "B              \t2              \t200            \t678.912        \n"
        "C              \t3              \t300            \t000.000        \n"
        "D              \t4              \t400            \t87             \n"
        "EFGH           \t0              \t500            \t92             "
    )
    f = tempfile.NamedTemporaryFile(mode="a", delete=False)
    f.write(x + "\n")
    f.close()
    # Must close and then yield for Windows platform
    yield f
    os.remove(f.name)


def test_ascii_output_function(csvfile, asciifile):
    output_test = tempfile.NamedTemporaryFile(mode="a", delete=False)
    ascii_output(csv_filename=csvfile.name, ascii_filename=output_test.name)
    assert filecmp.cmp(output_test.name, asciifile.name)
    output_test.close()
    os.remove(output_test.name)
