import sys
import numpy as np
import pandas as pd
from pandas import DataFrame
from collections import defaultdict
import matplotlib
import matplotlib.pyplot as plt

STATS_COLUMNS = ['_expanded_income', 'c00100', '_standard', 'c04470', 'c04600',
                 'c04800', 'c05200', 'c62100', 'c09600', 'c05800', 'c09200',
                 '_refund', 'c07100', '_iitax', '_fica', '_combined', 's006',
                 'e00200', 'MARS', 'n24']

# each entry in this array corresponds to the same entry in the array
# TABLE_LABELS below. this allows us to use TABLE_LABELS to map a
# label to the correct column in our distribution table

TABLE_COLUMNS = ['s006', 'c00100', 'num_returns_StandardDed', '_standard',
                 'num_returns_ItemDed', 'c04470', 'c04600', 'c04800', 'c05200',
                 'c62100', 'num_returns_AMT', 'c09600', 'c05800', 'c07100',
                 'c09200', '_refund', '_iitax', '_fica', '_combined']

TABLE_LABELS = ['Returns', 'AGI', 'Standard Deduction Filers',
                'Standard Deduction', 'Itemizers',
                'Itemized Deduction', 'Personal Exemption',
                'Taxable Income', 'Regular Tax', 'AMTI', 'AMT Filers', 'AMT',
                'Tax before Credits', 'Non-refundable Credits',
                'Tax before Refundable Credits', 'Refundable Credits',
                'Individual Income Tax Liabilities', 'Payroll Tax Liablities',
                'Combined Payroll and Individual Income Tax Liabilities']

# used in our difference table to label the columns
DIFF_TABLE_LABELS = ["Tax Units with Tax Cut", "Tax Units with Tax Increase",
                     "Count", "Average Tax Change", "Total Tax Difference",
                     "Percent with Tax Increase", "Percent with Tax Decrease",
                     "Share of Overall Change"]


LARGE_INCOME_BINS = [-1e14, 0, 9999, 19999, 29999, 39999, 49999, 74999, 99999,
                     200000, 1e14]

SMALL_INCOME_BINS = [-1e14, 0, 4999, 9999, 14999, 19999, 24999, 29999, 39999,
                     49999, 74999, 99999, 199999, 499999, 999999, 1499999,
                     1999999, 4999999, 9999999, 1e14]

WEBAPP_INCOME_BINS = [-1e14, 0, 9999, 19999, 29999, 39999, 49999, 74999, 99999,
                      199999, 499999, 1000000, 1e14]
EPSILON = 1e-3

EPSILON = 0.000000001


def extract_array(f):
    """
    A sanity check decorator. When combined with numba.vectorize
    or guvectorize, it provides the same capability as dataframe_vectorize
    or dataframe_guvectorize
    """
    def wrapper(*args, **kwargs):
        arrays = [arg.values for arg in args]
        return f(*arrays)
    return wrapper


def count_gt_zero(agg):
    return sum([1 for a in agg if a > 0])


def count_lt_zero(agg):
    return sum([1 for a in agg if a < 0])


def weighted_count_lt_zero(agg, col_name, tolerance=-0.001):
    return agg[agg[col_name] < tolerance]['s006'].sum()


def weighted_count_gt_zero(agg, col_name, tolerance=0.001):
    return agg[agg[col_name] > tolerance]['s006'].sum()


def weighted_count(agg):
    return agg['s006'].sum()


def weighted_mean(agg, col_name):
    return (float((agg[col_name] * agg['s006']).sum()) /
            float(agg['s006'].sum() + EPSILON))


def weighted_sum(agg, col_name):
    return (agg[col_name] * agg['s006']).sum()


def weighted_perc_inc(agg, col_name):
    return (float(weighted_count_gt_zero(agg, col_name)) /
            float(weighted_count(agg) + EPSILON))


def weighted_perc_dec(agg, col_name):
    return (float(weighted_count_lt_zero(agg, col_name)) /
            float(weighted_count(agg) + EPSILON))


def weighted_share_of_total(agg, col_name, total):
    return float(weighted_sum(agg, col_name)) / (float(total) + EPSILON)


def add_weighted_decile_bins(df, num_bins=10,
                             income_measure='_expanded_income', labels=None):
    """

    Add a column of income bins based on each 10% (customizable) of the
    income_measure, weighted by s006.

    The default income_measure is `expanded_income`, but `c00100` also works.

    This function will server as a "grouper" later on.

    """

    # First, sort by income_measure
    df.sort(income_measure, inplace=True)
    # Next, do a cumulative sum by the weights
    df['cumsum_weights'] = np.cumsum(df['s006'].values)
    # Max value of cum sum of weights
    max_ = df['cumsum_weights'].values[-1]
    # Create 10 bins and labels based on this cumulative weight
    bins = [0] + list(np.arange(1, (num_bins + 1)) * (max_ / float(num_bins)))
    if not labels:
        labels = range(1, (num_bins + 1))
    #  Groupby weighted deciles
    df['bins'] = pd.cut(df['cumsum_weights'], bins, labels=labels)
    return df


def add_income_bins(df, compare_with="soi", bins=None, right=True,
                    income_measure='_expanded_income'):
    """

    Add a column of income bins of income_measure using pandas 'cut'.
    This will serve as a "grouper" later on.


    Parameters
    ----------
    df: DataFrame object
        the object to which we are adding bins

    compare_with: String, optional
        options for input: 'tpc', 'soi', 'webapp'
        determines which types of bins will be added
        default: 'soi'

    bins: iterable of scalars, optional income breakpoints.
            Follows pandas convention. The breakpoint is inclusive if
            right=True. This argument overrides any choice of compare_with.


    right : bool, optional
        Indicates whether the bins include the rightmost edge or not.
        If right == True (the default), then the bins [1,2,3,4]
        indicate (1,2], (2,3], (3,4].

    Returns
    -------
    df: DataFrame object
        the original input that bins have been added to

    """
    if not bins:
        if compare_with == "tpc":
            bins = LARGE_INCOME_BINS

        elif compare_with == "soi":
            bins = SMALL_INCOME_BINS

        elif compare_with == "webapp":
            bins = WEBAPP_INCOME_BINS

        else:
            msg = "Unknown compare_with arg {0}".format(compare_with)
            raise ValueError(msg)

    # Groupby income_measure bins
    df['bins'] = pd.cut(df[income_measure], bins, right=right)
    return df


def means_and_comparisons(df, col_name, gp, weighted_total):
    """

    Using grouped values, perform aggregate operations
    to populate
    df: DataFrame for full results of calculation
    col_name: the column name to calculate against
    gp: grouped DataFrame
    """

    # Who has a tax cut, and who has a tax increase
    diffs = gp.apply(weighted_count_lt_zero, col_name)
    diffs = DataFrame(data=diffs, columns=['tax_cut'])
    diffs['tax_inc'] = gp.apply(weighted_count_gt_zero, col_name)
    diffs['count'] = gp.apply(weighted_count)
    diffs['mean'] = gp.apply(weighted_mean, col_name)
    diffs['tot_change'] = gp.apply(weighted_sum, col_name)
    diffs['perc_inc'] = gp.apply(weighted_perc_inc, col_name)
    diffs['perc_cut'] = gp.apply(weighted_perc_dec, col_name)
    diffs['share_of_change'] = gp.apply(weighted_share_of_total,
                                        col_name, weighted_total)

    return diffs


def weighted(df, X):
    agg = df
    for colname in X:
        if not colname.startswith('s006'):
            agg[colname] = df[colname] * df['s006']
    return agg


def get_sums(df, na=False):
    """
    Gets the unweighted sum of each column, saving the col name
    and the corresponding sum

    Returns
    -------
    pandas.Series
    """
    sums = defaultdict(lambda: 0)

    for col in df.columns.tolist():
        if col != 'bins':
            if na:
                sums[col] = 'n/a'
            else:
                sums[col] = (df[col]).sum()

    return pd.Series(sums, name='sums')


def results(c):
    """
    Gets the results from the tax calculator and organizes them into a table

    Parameters
    ----------
    c : Calculator object

    Returns
    -------
    DataFrame object
    """
    outputs = []
    for col in STATS_COLUMNS:
        if hasattr(c, 'records') and hasattr(c, 'policy'):
            if hasattr(c.policy, col):
                outputs.append(getattr(c.policy, col))
            else:
                outputs.append(getattr(c.records, col))
        else:
            outputs.append(getattr(c, col))
    return DataFrame(data=np.column_stack(outputs), columns=STATS_COLUMNS)


def weighted_avg_allcols(df, cols, income_measure='_expanded_income'):
    diff = DataFrame(df.groupby('bins', as_index=False).apply(weighted_mean,
                                                              income_measure),
                     columns=[income_measure])
    for col in cols:
        if (col == "s006" or col == 'num_returns_StandardDed' or
                col == 'num_returns_ItemDed' or col == 'num_returns_AMT'):
            diff[col] = df.groupby('bins', as_index=False)[col].sum()[col]
        elif col != income_measure:
            diff[col] = df.groupby('bins', as_index=False).apply(weighted_mean,
                                                                 col)

    return diff


def add_columns(res):
    # weight of returns with positive AGI and
    # itemized deduction greater than standard deduction
    res['c04470'] = res['c04470'].where(((res['c00100'] > 0) &
                                        (res['c04470'] > res['_standard'])),
                                        0)

    # weight of returns with positive AGI and itemized deduction
    res['num_returns_ItemDed'] = res['s006'].where(((res['c00100'] > 0) &
                                                   (res['c04470'] > 0)),
                                                   0)

    # weight of returns with positive AGI and standard deduction
    res['num_returns_StandardDed'] = res['s006'].where(((res['c00100'] > 0) &
                                                       (res['_standard'] > 0)),
                                                       0)

    # weight of returns with positive Alternative Minimum Tax (AMT)
    res['num_returns_AMT'] = res['s006'].where(res['c09600'] > 0, 0)

    return res


def create_mtr_graph(calcX, calcY, MARS, weights, income_measure='c00100',
                     kid_cap=1000, kid_flo=0, combined_or_IIT='Combined'):
    """
    The create_mtr_graph function plots the mtr w.r.t different income measure.

    The function also allows filtering different MARS values, choosing from
    different weighting measurements as well as setting cap and floor for
    number of kids.

    Notice that the second calculator, calcY, is optional.
    """
    # get the mtr w.r.t iit and combined liability
    a, mtr_iit_x, mtr_combined_x = calcX.mtr()
    a, mtr_iit_y, mtr_combined_y = calcY.mtr()

    # call the results function to organize results in a table
    df_x = results(calcX)
    df_y = results(calcY)
    df_x['mtr_iit'] = mtr_iit_x
    df_y['mtr_iit'] = mtr_iit_y
    df_x['mtr_combined'] = mtr_combined_x
    df_y['mtr_combined'] = mtr_combined_y

    df_y[income_measure] = df_x[income_measure]

    # call the add_weighted_decile_bins function with 100 bins, that is, with
    # each 1% of the income_measure.
    df_x = add_weighted_decile_bins(df_x, 100, income_measure)
    df_y = add_weighted_decile_bins(df_y, 100, income_measure)

    # filtered the records according to inputed parameters
    df_filtered_x = df_x[(df_x['MARS'] == MARS) & (df_x['n24'] >= kid_flo) &
                         (df_x['n24'] <= kid_cap)].copy()
    df_filtered_y = df_y[(df_y['MARS'] == MARS) & (df_x['n24'] >= kid_flo) &
                         (df_x['n24'] <= kid_cap)].copy()

    # create a GroupBy object with 100 groups
    gp_x = df_filtered_x.groupby('bins', as_index=False)
    gp_y = df_filtered_y.groupby('bins', as_index=False)

    # create a series of size 100, and get the desired mtr
    if combined_or_IIT == 'Combined':
        wmtr_x = gp_x.apply(weights, 'mtr_combined')
        wmtr_y = gp_y.apply(weights, 'mtr_combined')
    elif combined_or_IIT == 'IIT':
        wmtr_x = gp_x.apply(weights, 'mtr_iit')
        wmtr_y = gp_y.apply(weights, 'mtr_iit')

    # create a DataFrame out of this with a default index
    wmtrx_df = DataFrame(data=wmtr_x, columns=['w_mtr'])
    wmtry_df = DataFrame(data=wmtr_y, columns=['w_mtr'])

    # add the bin labels
    wmtrx_df['bins'] = np.arange(1, 101)
    wmtry_df['bins'] = np.arange(1, 101)

    # join df_x and apply on the bin, carrying along 'wmtr'
    rsltx = pd.merge(df_filtered_x[['bins']], wmtrx_df, how='left')
    rslty = pd.merge(df_filtered_y[['bins']], wmtry_df, how='left')

    # put that column in df_filtered_x, disregarding index of rslt
    df_filtered_x['w_mtr'] = rsltx['w_mtr'].values
    df_filtered_y['w_mtr'] = rslty['w_mtr'].values

    df_filtered_x.drop_duplicates(subset='bins', inplace=True)
    df_filtered_y.drop_duplicates(subset='bins', inplace=True)

    # plot the mtr against bins, notice that only one plot will be
    # generated if two calculators are the same
    layer = plt.figure()
    layer.suptitle("MARS = %d, Kid Range: [%d, %d]" % (MARS, kid_cap, kid_flo),
                   fontsize=12, fontweight='bold')

    plt.plot(df_filtered_x.bins, df_filtered_x.w_mtr, label="Baseline")

    background = layer.add_subplot(111)
    layer.subplots_adjust(top=0.85)

    background.set_xlabel('Income Percentiles' + '(' + income_measure + ')')
    background.set_ylabel('Marginal Tax Rate' + '(' + combined_or_IIT + ')')
    if calcX != calcY:
        plt.plot(df_filtered_y.bins, df_filtered_y.w_mtr, label="Reform")
        plt.legend(loc='upper left')


def create_distribution_table(calc, groupby, result_type,
                              income_measure='_expanded_income',
                              baseline_calc=None, diffs=False):

    """
    Gets results given by the tax calculator, sorts them based on groupby, and
        manipulates them based on result_type. Returns these as a table

    Parameters
    ----------
    calc : the Calculator object
    groupby : String object
        options for input: 'weighted_deciles', 'small_income_bins',
        'large_income_bins', 'webapp_income_bins';
        determines how the columns in the resulting DataFrame are sorted
    result_type : String object
        options for input: 'weighted_sum' or 'weighted_avg';
        determines how the data should be manipulated
    baseline_calc : A Calculator object
        carries the baseline plan
    diffs : boolean
        indicates showing the results from reform or the difference between
        the baseline and reform. Turn this switch to True if you want to see
        the difference

    Notes
    -----
    Taxpayer Characteristics:
        c04470 : Total itemized deduction

        c00100 : AGI (Defecit)

        c09600 : Alternative minimum tax

        s006 : used to weight population

    Returns
    -------
    DataFrame object
    """
    res = results(calc)
    res = add_columns(res)

    if baseline_calc is not None:
        if calc.current_year != baseline_calc.current_year:
            msg = 'The baseline calculator is not on the same year as reform.'
            raise ValueError(msg)
        baseline_income_measure = income_measure + '_baseline'
        res_base = results(baseline_calc)
        res[baseline_income_measure] = res_base[income_measure]
        income_measure = baseline_income_measure

        if diffs:
            res_base = add_columns(res_base)
            res = res.subtract(res_base)
            res['s006'] = res_base['s006']

    # sorts the data
    if groupby == "weighted_deciles":
        df = add_weighted_decile_bins(res, income_measure=income_measure)
    elif groupby == "small_income_bins":
        df = add_income_bins(res, compare_with="soi",
                             income_measure=income_measure)
    elif groupby == "large_income_bins":
        df = add_income_bins(res, compare_with="tpc",
                             income_measure=income_measure)
    elif groupby == "webapp_income_bins":
        df = add_income_bins(res, compare_with="webapp",
                             income_measure=income_measure)
    else:
        err = ("groupby must be either 'weighted_deciles' or"
               "'small_income_bins' or 'large_income_bins' or"
               "'webapp_income_bins'")
        raise ValueError(err)

    # manipulates the data
    pd.options.display.float_format = '{:8,.0f}'.format
    if result_type == "weighted_sum":
        df = weighted(df, STATS_COLUMNS)
        gp_mean = df.groupby('bins', as_index=False)[TABLE_COLUMNS].sum()
        gp_mean.drop('bins', axis=1, inplace=True)
        sum_row = get_sums(df)[TABLE_COLUMNS]
    elif result_type == "weighted_avg":
        gp_mean = weighted_avg_allcols(df, TABLE_COLUMNS,
                                       income_measure=income_measure)
        sum_row = get_sums(df, na=True)[TABLE_COLUMNS]
    else:
        err = ("result_type must be either 'weighted_sum' or 'weighted_avg")
        raise ValueError(err)

    return gp_mean.append(sum_row)


def create_difference_table(calc1, calc2, groupby,
                            income_measure='_expanded_income',
                            income_to_present='_iitax'):
    """
    Gets results given by the two different tax calculators and outputs
        a table that compares the differing results.
        The table is sorted according the the groupby input.
        Notice that you always needs to run calc_all() for each year
        before generating diffs table from this function. You can check
        what year your calculator is using the current_year attribute
        of your calculator. (usage: calc1.current_year)

    Parameters
    ----------
    calc1: the baseline Calculator on year t
    calc2: the reform Calculator on year t
    groupby: String
        options for input: 'weighted_deciles', 'small_income_bins',
        'large_income_bins', 'webapp_income_bins'
        determines how the columns in the resulting DataFrame are sorted
    income_measure : string
        options for input: '_expanded_income', '_iitax'
        classifier of income bins/deciles
    income_to_present : string
        options for input: '_iitax', '_fica', '_combined'

    Returns
    -------
    DataFrame object
    """

    res1 = results(calc1)
    res2 = results(calc2)

    baseline_income_measure = income_measure + '_baseline'
    res2[baseline_income_measure] = res1[income_measure]
    income_measure = baseline_income_measure

    if groupby == "weighted_deciles":
        df = add_weighted_decile_bins(res2, income_measure=income_measure)
    elif groupby == "small_income_bins":
        df = add_income_bins(res2, compare_with="soi",
                             income_measure=income_measure)
    elif groupby == "large_income_bins":
        df = add_income_bins(res2, compare_with="tpc",
                             income_measure=income_measure)
    elif groupby == "webapp_income_bins":
        df = add_income_bins(res2, compare_with="webapp",
                             income_measure=income_measure)
    else:
        err = ("groupby must be either"
               "'weighted_deciles' or 'small_income_bins'"
               "or 'large_income_bins' or 'webapp_income_bins'")
        raise ValueError(err)

    # Difference in plans
    # Positive values are the magnitude of the tax increase
    # Negative values are the magnitude of the tax decrease

    res2['tax_diff'] = res2[income_to_present] - res1[income_to_present]

    diffs = means_and_comparisons(res2, 'tax_diff',
                                  df.groupby('bins', as_index=False),
                                  (res2['tax_diff'] * res2['s006']).sum())

    sum_row = get_sums(diffs)[diffs.columns.tolist()]
    diffs = diffs.append(sum_row)

    pd.options.display.float_format = '{:8,.0f}'.format
    srs_inc = ["{0:.2f}%".format(val * 100) for val in diffs['perc_inc']]
    diffs['perc_inc'] = pd.Series(srs_inc, index=diffs.index)

    srs_cut = ["{0:.2f}%".format(val * 100) for val in diffs['perc_cut']]
    diffs['perc_cut'] = pd.Series(srs_cut, index=diffs.index)

    srs_change = ["{0:.2f}%".format(val * 100)
                  for val in diffs['share_of_change']]
    diffs['share_of_change'] = pd.Series(srs_change, index=diffs.index)

    # columns containing weighted values relative to the binning mechanism
    non_sum_cols = [x for x in diffs.columns.tolist()
                    if 'mean' in x or 'perc' in x]
    for col in non_sum_cols:
        diffs.loc['sums', col] = 'n/a'

    return diffs


def ascii_output(csv_filename, ascii_filename):
    """
    Converts csv output from Calculator into ascii output with uniform
    columns and transposes data so columns are rows and rows are columns.
    In an ipython notebook, you can import this function from the utils module.
    """
    # list of integers corresponding to the number(s) of the row(s) in the
    # csv file, only rows in list will be recorded in final output
    # if left as [], results in entire file being converted to ascii
    # put in order from smallest to largest, for example:
    # recids = [33180, 64023, 68020, 74700, 84723, 98001, 107039, 108820]
    recids = [1, 4, 5]
    # Number of characters in each column, must be whole nonnegative integer
    col_size = 15
    df = pd.read_csv(csv_filename, dtype=object)
    # keeps only listed recid's
    if recids != []:
        def f(x):
            return x - 1
        recids = map(f, recids)  # maps recids to correct index in df
        df = df.ix[recids]
    # does transposition
    out = df.T.reset_index()
    # formats data into uniform columns
    fstring = '{:' + str(col_size) + '}'
    out = out.applymap(fstring.format)
    out.to_csv(ascii_filename, header=False, index=False,
               delim_whitespace=True, sep='\t')
