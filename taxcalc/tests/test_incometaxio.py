"""
Tests for Tax-Calculator IncomeTaxIO class.
"""
# CODING-STYLE CHECKS:
# pep8 --ignore=E402 test_incometaxio.py
# pylint --disable=locally-disabled test_incometaxio.py

import os
import tempfile
from io import StringIO
import pytest
import pandas as pd
from taxcalc import IncomeTaxIO  # pylint: disable=import-error


RAWINPUTFILE_FUNITS = 4
RAWINPUTFILE_CONTENTS = (
    u'RECID,MARS\n'
    u'    1,   2\n'
    u'    2,   1\n'
    u'    3,   4\n'
    u'    4,   6\n'
)


EXPECTED_OUTPUT = (  # from using RAWINPUTFILE_CONTENTS as input
    '1. 2021 0 0.00 0.00 0.00 -7.65 0.00 15.30 0.00 0.00 0.00 0.00 0.00 '
    '0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00\n'
    '2. 2021 0 0.00 0.00 0.00 -7.65 0.00 15.30 0.00 0.00 0.00 0.00 0.00 '
    '0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00\n'
    '3. 2021 0 0.00 0.00 0.00 -7.65 0.00 15.30 0.00 0.00 0.00 0.00 0.00 '
    '0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00\n'
    '4. 2021 0 0.00 0.00 0.00 0.00 0.00 15.30 0.00 0.00 0.00 0.00 0.00 '
    '0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00\n'
)


@pytest.yield_fixture
def rawinputfile():
    """
    Temporary input file that contains minimum required input variables.
    """
    ifile = tempfile.NamedTemporaryFile(suffix='.csv', mode='a', delete=False)
    ifile.write(RAWINPUTFILE_CONTENTS)
    ifile.close()
    # must close and then yield for Windows platform
    yield ifile
    if os.path.isfile(ifile.name):
        try:
            os.remove(ifile.name)
        except OSError:
            pass  # sometimes we can't remove a generated temporary file


@pytest.mark.parametrize("input_data, exact", [
    ('no-dot-csv-filename', True),
    (list(), False),
    ('bad_filename.csv', False),
])
def test_incorrect_creation_1(input_data, exact):
    """
    Ensure a ValueError is raised when created with invalid data pointers
    """
    with pytest.raises(ValueError):
        IncomeTaxIO(
            input_data=input_data,
            tax_year=2013,
            reform=None,
            assump=None,
            aging_input_data=False,
            exact_calculations=exact,
            output_records=False,
            csv_dump=False
        )


# for fixture args, pylint: disable=redefined-outer-name


@pytest.mark.parametrize("year, reform, assump", [
    (2013, list(), None),
    (2013, None, list()),
    (2001, None, None),
    (2099, None, None),
])
def test_incorrect_creation_2(rawinputfile, year, reform, assump):
    """
    Ensure a ValueError is raised when created with invalid parameters
    """
    with pytest.raises(ValueError):
        IncomeTaxIO(
            input_data=rawinputfile.name,
            tax_year=year,
            reform=reform,
            assump=assump,
            aging_input_data=False,
            exact_calculations=False,
            output_records=False,
            csv_dump=False
        )


def test_creation_with_aging(rawinputfile):
    """
    Test IncomeTaxIO instantiation with no policy reform and with aging.
    """
    IncomeTaxIO.show_iovar_definitions()
    taxyear = 2021
    inctax = IncomeTaxIO(input_data=rawinputfile.name,
                         tax_year=taxyear,
                         reform=None,
                         assump=None,
                         aging_input_data=True,
                         exact_calculations=False,
                         output_records=False,
                         csv_dump=False)
    assert inctax.tax_year() == taxyear


@pytest.yield_fixture
def reformfile0():
    """
    specify JSON text for reform
    """
    txt = """
    {
        "policy": {
            "_SS_Earnings_c": {"2016": [300000],
                               "2018": [500000],
                               "2020": [700000]}
        }
    }
    """
    rfile = tempfile.NamedTemporaryFile(mode='a', delete=False)
    rfile.write(txt + '\n')
    rfile.close()
    # Must close and then yield for Windows platform
    yield rfile
    os.remove(rfile.name)


def test_2(rawinputfile, reformfile0):
    """
    Test IncomeTaxIO calculate method with no output writing and no aging.
    """
    taxyear = 2021
    inctax = IncomeTaxIO(input_data=rawinputfile.name,
                         tax_year=taxyear,
                         reform=reformfile0.name,
                         assump=None,
                         aging_input_data=False,
                         exact_calculations=False,
                         output_records=False,
                         csv_dump=False)
    output = inctax.calculate()
    assert output == EXPECTED_OUTPUT


REFORM_CONTENTS = """
// Example of a reform file suitable for the read_json_param_files() function.
// This JSON file can contain any number of trailing //-style comments, which
// will be removed before the contents are converted from JSON to a dictionary.
// Within the "policy" object, the primary keys are parameters and
// secondary keys are years.
// Both the primary and secondary key values must be enclosed in quotes (").
// Boolean variables are specified as true or false (no quotes; all lowercase).
{
  "policy": {
    "_AMT_brk1": // top of first AMT tax bracket
    {"2015": [200000],
     "2017": [300000]
    },
    "_EITC_c": // maximum EITC amount by number of qualifying kids (0,1,2,3+)
    {"2016": [[ 900, 5000,  8000,  9000]],
     "2019": [[1200, 7000, 10000, 12000]]
    },
    "_II_em": // personal exemption amount (see indexing changes below)
    {"2016": [6000],
     "2018": [7500],
     "2020": [9000]
    },
    "_II_em_cpi": // personal exemption amount indexing status
    {"2016": false, // values in future years are same as this year value
     "2018": true   // values in future years indexed with this year as base
    },
    "_SS_Earnings_c": // social security (OASDI) maximum taxable earnings
    {"2016": [300000],
     "2018": [500000],
     "2020": [700000]
    },
    "_AMT_em_cpi": // AMT exemption amount indexing status
    {"2017": false, // values in future years are same as this year value
     "2020": true   // values in future years indexed with this year as base
    }
  }
}
"""


@pytest.yield_fixture
def reformfile1():
    """
    Temporary reform file with .json extension.
    """
    rfile = tempfile.NamedTemporaryFile(suffix='.json', mode='a', delete=False)
    rfile.write(REFORM_CONTENTS)
    rfile.close()
    # must close and then yield for Windows platform
    yield rfile
    if os.path.isfile(rfile.name):
        try:
            os.remove(rfile.name)
        except OSError:
            pass  # sometimes we can't remove a generated temporary file


@pytest.yield_fixture
def reformfile2():
    """
    Temporary reform file without .json extension.
    """
    rfile = tempfile.NamedTemporaryFile(mode='a', delete=False)
    rfile.write(REFORM_CONTENTS)
    rfile.close()
    # must close and then yield for Windows platform
    yield rfile
    if os.path.isfile(rfile.name):
        try:
            os.remove(rfile.name)
        except OSError:
            pass  # sometimes we can't remove a generated temporary file


ASSUMP_CONTENTS = """
// Example of an assump file suitable for the read_json_param_files() function.
// This JSON file can contain any number of trailing //-style comments, which
// will be removed before the contents are converted from JSON to a dictionary.
// Within each "consumption", "behavior", "growdiff_baseline" and
// "growdiff_response" object, the primary keys are parameters and
// the secondary keys are years.
// Both the primary and secondary key values must be enclosed in quotes (").
// Boolean variables are specified as true or false (no quotes; all lowercase).
{
  "title": "",
  "author": "",
  "date": "",
  "consumption": { "_MPC_e18400": {"2018": [0.05]} },
  "behavior": {},
  "growdiff_baseline": {},
  "growdiff_response": {}
}
"""


@pytest.yield_fixture
def assumpfile1():
    """
    Temporary assumption file with .json extension.
    """
    afile = tempfile.NamedTemporaryFile(suffix='.json', mode='a', delete=False)
    afile.write(ASSUMP_CONTENTS)
    afile.close()
    # must close and then yield for Windows platform
    yield afile
    if os.path.isfile(afile.name):
        try:
            os.remove(afile.name)
        except OSError:
            pass  # sometimes we can't remove a generated temporary file


@pytest.yield_fixture
def assumpfile2():
    """
    Temporary assumption file without .json extension.
    """
    afile = tempfile.NamedTemporaryFile(mode='a', delete=False)
    afile.write(ASSUMP_CONTENTS)
    afile.close()
    # must close and then yield for Windows platform
    yield afile
    if os.path.isfile(afile.name):
        try:
            os.remove(afile.name)
        except OSError:
            pass  # sometimes we can't remove a generated temporary file


def test_3(rawinputfile, reformfile1, assumpfile1):
    """
    Test IncomeTaxIO calculate method with no output writing and no aging,
    using file name for IncomeTaxIO constructor input_data.
    """
    taxyear = 2021
    inctax = IncomeTaxIO(input_data=rawinputfile.name,
                         tax_year=taxyear,
                         reform=reformfile1.name,
                         assump=assumpfile1.name,
                         aging_input_data=False,
                         exact_calculations=False,
                         output_records=False,
                         csv_dump=False)
    output = inctax.calculate()
    assert output == EXPECTED_OUTPUT


def test_4(reformfile2, assumpfile2):
    """
    Test IncomeTaxIO calculate method with no output writing and no aging,
    using DataFrame for IncomeTaxIO constructor input_data.
    """
    input_stream = StringIO(RAWINPUTFILE_CONTENTS)
    input_dataframe = pd.read_csv(input_stream)
    taxyear = 2021
    inctax = IncomeTaxIO(input_data=input_dataframe,
                         tax_year=taxyear,
                         reform=reformfile2.name,
                         assump=assumpfile2.name,
                         aging_input_data=False,
                         exact_calculations=False,
                         output_records=False,
                         csv_dump=False)
    output = inctax.calculate()
    assert output == EXPECTED_OUTPUT


def test_5(rawinputfile, reformfile1):
    """
    Test IncomeTaxIO calculate method with no output writing and no aging and
    no reform, using the output_records option.
    """
    taxyear = 2020
    inctax = IncomeTaxIO(input_data=rawinputfile.name,
                         tax_year=taxyear,
                         reform=reformfile1.name,
                         assump=None,
                         aging_input_data=False,
                         exact_calculations=False,
                         output_records=True,
                         csv_dump=False)
    inctax.output_records(writing_output_file=False)
    assert inctax.tax_year() == taxyear


def test_6(rawinputfile):
    """
    Test IncomeTaxIO calculate method with no output writing and no aging and
    no reform, using the csv_dump option.
    """
    taxyear = 2021
    inctax = IncomeTaxIO(input_data=rawinputfile.name,
                         tax_year=taxyear,
                         reform=None,
                         assump=None,
                         aging_input_data=False,
                         exact_calculations=False,
                         output_records=False,
                         csv_dump=True)
    inctax.csv_dump(writing_output_file=False)
    assert inctax.tax_year() == taxyear


LUMPSUM_REFORM_CONTENTS = """
{
  "policy": {
    "_LST": {"2013": [200]}
  }
}
"""


@pytest.yield_fixture
def lumpsumreformfile():
    """
    Temporary reform file without .json extension.
    """
    rfile = tempfile.NamedTemporaryFile(mode='a', delete=False)
    rfile.write(LUMPSUM_REFORM_CONTENTS)
    rfile.close()
    # must close and then yield for Windows platform
    yield rfile
    if os.path.isfile(rfile.name):
        try:
            os.remove(rfile.name)
        except OSError:
            pass  # sometimes we can't remove a generated temporary file


def test_7(reformfile1, lumpsumreformfile):
    """
    Test IncomeTaxIO calculate method with no output writing using ceeu option.
    """
    taxyear = 2020
    recdict = {'RECID': 1, 'MARS': 1, 'e00300': 100000, 's006': 1e8}
    recdf = pd.DataFrame(data=recdict, index=[0])

    inctax = IncomeTaxIO(input_data=recdf,
                         tax_year=taxyear,
                         reform=reformfile1.name,
                         assump=None,
                         aging_input_data=False,
                         exact_calculations=False,
                         output_records=False,
                         csv_dump=False)
    output = inctax.calculate(writing_output_file=False, output_ceeu=True)
    assert inctax.tax_year() == taxyear
    assert len(output) > 0

    inctax = IncomeTaxIO(input_data=recdf,
                         tax_year=taxyear,
                         reform=lumpsumreformfile.name,
                         assump=None,
                         aging_input_data=False,
                         exact_calculations=False,
                         output_records=False,
                         csv_dump=False)
    output = inctax.calculate(writing_output_file=False, output_ceeu=True)
    assert inctax.tax_year() == taxyear
    assert len(output) > 0


BAD_ASSUMP_CONTENTS = """
{
  "consumption": {
  },
  "behavior": {
      "_BE_sub": {"2020": [0.05]}
  },
  "growdiff_baseline": {
  },
  "growdiff_response": {
      "_ABOOK": {"2015": [-0.01]}
  }
}
"""


@pytest.yield_fixture
def assumpfile3():
    """
    Temporary assumption file with .json extension.
    """
    afile = tempfile.NamedTemporaryFile(suffix='.json', mode='a', delete=False)
    afile.write(BAD_ASSUMP_CONTENTS)
    afile.close()
    # must close and then yield for Windows platform
    yield afile
    if os.path.isfile(afile.name):
        try:
            os.remove(afile.name)
        except OSError:
            pass  # sometimes we can't remove a generated temporary file


def test_9(reformfile2, assumpfile3):
    """
    Test IncomeTaxIO constructor with illegal assumptions.
    """
    input_stream = StringIO(RAWINPUTFILE_CONTENTS)
    input_dataframe = pd.read_csv(input_stream)
    taxyear = 2022
    with pytest.raises(ValueError):
        IncomeTaxIO(input_data=input_dataframe,
                    tax_year=taxyear,
                    reform=reformfile2.name,
                    assump=assumpfile3.name,
                    aging_input_data=False,
                    exact_calculations=False,
                    output_records=False,
                    csv_dump=False)
