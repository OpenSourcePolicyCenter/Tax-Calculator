"""
Test example JSON policy reform files in taxcalc/reforms directory
"""
# CODING-STYLE CHECKS:
# pep8 --ignore=E402 test_reforms.py
# pylint --disable=locally-disabled test_reforms.py

import os
import glob
import json
import pytest
from taxcalc import Calculator, Policy  # pylint: disable=import-error
from taxcalc import Records, Behavior  # pylint: disable=import-error

# pylint: disable=too-many-lines


def test_reform_json(tests_path):
    """
    Check that each JSON reform file can be converted into a reform dictionary
    that can then be passed to the Policy class implement_reform() method.
    """
    reforms_path = os.path.join(tests_path, '..', 'reforms', '*.json')
    for jpf in glob.glob(reforms_path):
        # read contents of jpf (JSON parameter filename)
        jfile = open(jpf, 'r')
        jpf_text = jfile.read()
        # check that jpf_text has "policy" that can be implemented as a reform
        if '"policy"' in jpf_text:
            arrays_not_lists = True
            gdiffbase = {}
            gdiffresp = {}
            # pylint: disable=protected-access
            policy_dict = (
                Calculator._read_json_policy_reform_text(jpf_text,
                                                         arrays_not_lists,
                                                         gdiffbase, gdiffresp)
            )
            policy = Policy()
            policy.implement_reform(policy_dict)
        else:  # jpf_text is not a valid JSON policy reform file
            print('test-failing-filename: ' +
                  jpf)
            assert False


def reform_results(reform_dict, puf_data):
    """
    Return actual results of the reform specified in reform_dict.
    """
    # pylint: disable=too-many-locals
    # create current-law-policy Calculator object
    pol1 = Policy()
    rec1 = Records(data=puf_data)
    calc1 = Calculator(policy=pol1, records=rec1, verbose=False, behavior=None)
    # create reform Calculator object with possible behavioral responses
    start_year = reform_dict['start_year']
    beh2 = Behavior()
    if '_BE_cg' in reform_dict['value']:
        elasticity = reform_dict['value']['_BE_cg']
        del reform_dict['value']['_BE_cg']  # in order to have a valid reform
        beh_assump = {start_year: {'_BE_cg': elasticity}}
        beh2.update_behavior(beh_assump)
    reform = {start_year: reform_dict['value']}
    pol2 = Policy()
    pol2.implement_reform(reform)
    rec2 = Records(data=puf_data)
    calc2 = Calculator(policy=pol2, records=rec2, verbose=False, behavior=beh2)
    # increment both calculators to reform's start_year
    calc1.advance_to_year(start_year)
    calc2.advance_to_year(start_year)
    # calculate prereform and postreform output for several years
    output_type = reform_dict['output_type']
    num_years = 4
    results = list()
    for _ in range(0, num_years):
        calc1.calc_all()
        prereform = getattr(calc1.records, output_type)
        if calc2.behavior.has_response():
            calc_clp = calc2.current_law_version()
            calc2_br = Behavior.response(calc_clp, calc2)
            postreform = getattr(calc2_br.records, output_type)
        else:
            calc2.calc_all()
            postreform = getattr(calc2.records, output_type)
        diff = postreform - prereform
        weighted_sum_diff = (diff * calc1.records.s006).sum() * 1.0e-9
        results.append(weighted_sum_diff)
        calc1.increment_year()
        calc2.increment_year()
    # write actual results to actual_str
    reform_description = reform_dict['name']
    actual_str = '{}\n'.format(reform_description)
    actual_str += 'Tax-Calculator'
    for iyr in range(0, num_years):
        actual_str += ',{:.1f}'.format(results[iyr])
    return actual_str


@pytest.mark.requires_pufcsv
def test_r1(puf_subsample):
    """
    Comparison test 1
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_FICA_ss_trt": [0.134]},
        "name": "Increase OASDI payroll tax rate by 1 pts",
        "output_type": "payrolltax",
        "compare_with": {}
    }
    """
    expected_res = ('Increase OASDI payroll tax rate by 1 pts'
                    '\n'
                    'Tax-Calculator,63.1,65.6,69.1,71.7')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r2(puf_subsample):
    """
    Comparison test 2
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_SS_Earnings_c": [177500]},
        "name": "Increase OASDI maximum taxable earnings to $177,500",
        "output_type": "payrolltax",
        "compare_with": {"Budget Options": [40, 46, 49, 51]}
    }
    """
    expected_res = ('Increase OASDI maximum taxable earnings to $177,500'
                    '\n'
                    'Tax-Calculator,48.7,57.3,53.4,55.1')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r3(puf_subsample):
    """
    Comparison test 3
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_FICA_mc_trt": [0.039]},
        "name": "Increase HI payroll tax rate by 1 pts",
        "output_type": "payrolltax",
        "compare_with": {"Budget Options": [73, 77, 82, 87]}
    }
    """
    expected_res = ('Increase HI payroll tax rate by 1 pts'
                    '\n'
                    'Tax-Calculator,75.1,78.7,82.2,85.3')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r4(puf_subsample):
    """
    Comparison test 4
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_AMEDT_ec": [[210000, 260000, 135000, 210000, 210000]]},
        "name": "Increase Additional Medicare Tax exclusion by $10,000",
        "output_type": "payrolltax",
        "compare_with": {}
    }
    """
    expected_res = ('Increase Additional Medicare Tax exclusion by $10,000'
                    '\n'
                    'Tax-Calculator,-0.3,-0.3,-0.3,-0.3')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r5(puf_subsample):
    """
    Comparison test 5
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_AMEDT_rt": [0.01]},
        "name": "Increase Additional Medicare Tax rate by 0.1 pts",
        "output_type": "payrolltax",
        "compare_with": {}
    }
    """
    expected_res = ('Increase Additional Medicare Tax rate by 0.1 pts'
                    '\n'
                    'Tax-Calculator,0.8,0.8,0.9,1.0')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r6(puf_subsample):
    """
    Comparison test 6
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_SS_thd50": [[0, 0, 0, 0, 0]],
                  "_SS_thd85": [[0, 0, 0, 0, 0]],
                  "_SS_percentage1": [1],
                  "_SS_percentage2": [1]},
        "name": "All OASDI benefits included in AGI",
        "output_type": "iitax",
        "compare_with": {"Tax Expenditure": [39.3, 41.5, 44.1, 46.8],
                         "Budget Options": [35, 37, 38, 40]}
    }
    """
    expected_res = ('All OASDI benefits included in AGI'
                    '\n'
                    'Tax-Calculator,39.2,40.2,41.3,43.4')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r7(puf_subsample):
    """
    Comparison test 7
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_ALD_KEOGH_SEP_hc": [1]},
        "name": "No deduction for KEOGH/SEP contributions",
        "output_type": "iitax",
        "compare_with": {"Tax Expenditure": [8.7, 10.0, 11.4, 16.2]}
    }
    """
    expected_res = ('No deduction for KEOGH/SEP contributions'
                    '\n'
                    'Tax-Calculator,7.9,8.1,8.5,8.7')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r8(puf_subsample):
    """
    Comparison test 8
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_ALD_StudentLoan_hc": [1]},
        "name": "No deduction for student-loan interest",
        "output_type": "iitax",
        "compare_with": {"Tax Expenditure": [1.8, 1.9, 1.9, 2.1]}
    }
    """
    expected_res = ('No deduction for student-loan interest'
                    '\n'
                    'Tax-Calculator,1.8,2.0,2.1,2.2')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r9(puf_subsample):
    """
    Comparison test 9
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_ALD_SelfEmploymentTax_hc": [1]},
        "name": "Eliminate adjustment for self-employment tax",
        "output_type": "iitax",
        "compare_with": {}
    }
    """
    expected_res = ('Eliminate adjustment for self-employment tax'
                    '\n'
                    'Tax-Calculator,3.7,3.9,4.3,4.5')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r10(puf_subsample):
    """
    Comparison test 10
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_ALD_SelfEmp_HealthIns_hc": [1]},
        "name": "Eliminate adjustment for self-employed health insurance",
        "output_type": "iitax",
        "compare_with": {}
    }
    """
    expected_res = ('Eliminate adjustment for self-employed health insurance'
                    '\n'
                    'Tax-Calculator,5.5,5.6,5.8,5.8')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r11(puf_subsample):
    """
    Comparison test 11
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_ALD_Alimony_hc": [1]},
        "name": "Eliminate adjustment for alimony payments",
        "output_type": "iitax",
        "compare_with": {}
    }
    """
    expected_res = ('Eliminate adjustment for alimony payments'
                    '\n'
                    'Tax-Calculator,3.1,3.3,3.5,3.4')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r12(puf_subsample):
    """
    Comparison test 12
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_ALD_EarlyWithdraw_hc": [1]},
        "name": "Eliminate adjustment for forfeited interest penalty",
        "output_type": "iitax",
        "compare_with": {}
    }
    """
    expected_res = ('Eliminate adjustment for forfeited interest penalty'
                    '\n'
                    'Tax-Calculator,0.0,0.0,0.1,0.1')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r13(puf_subsample):
    """
    Comparison test 13
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_II_em": [5000]},
        "name": "Increase personal and dependent exemption amount by $1000",
        "output_type": "iitax",
        "compare_with": {}
    }
    """
    expected_res = ('Increase personal and dependent exemption amount by $1000'
                    '\n'
                    'Tax-Calculator,-33.0,-35.2,-40.0,-41.5')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r14(puf_subsample):
    """
    Comparison test 14
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_II_em_ps": [[268250, 319900, 164950, 294040, 319900]]},
        "name": "Increase personal exemption phaseout starting AGI by $10,000",
        "output_type": "iitax",
        "compare_with": {}
    }
    """
    expected_res = ('Increase personal exemption phaseout starting AGI '
                    'by $10,000'
                    '\n'
                    'Tax-Calculator,-0.1,-0.1,-0.1,-0.2')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r15(puf_subsample):
    """
    Comparison test 15
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_II_prt": [0.03]},
        "name": "Increase personal exemption phaseout rate by 1 pts",
        "output_type": "iitax",
        "compare_with": {}
    }
    """
    expected_res = ('Increase personal exemption phaseout rate by 1 pts'
                    '\n'
                    'Tax-Calculator,0.3,0.3,0.3,0.3')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r16(puf_subsample):
    """
    Comparison test 16
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_STD": [[6400, 12700, 6400, 9350, 12700]]},
        "name": "Increase standard deduction by $100",
        "output_type": "iitax",
        "compare_with": {}
    }
    """
    expected_res = ('Increase standard deduction by $100'
                    '\n'
                    'Tax-Calculator,-1.0,-2.6,-4.1,-4.3')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r17(puf_subsample):
    """
    Comparison test 17
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_STD_Aged": [[1650, 1350, 1350, 1650, 1650]]},
        "name": "Increase additional stdded for aged/blind by $100",
        "output_type": "iitax",
        "compare_with": {}

    }
    """
    expected_res = ('Increase additional stdded for aged/blind by $100'
                    '\n'
                    'Tax-Calculator,-0.3,-0.3,-0.5,-0.5')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r18(puf_subsample):
    """
    Comparison test 18
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_ID_RealEstate_hc": [1]},
        "name": "Eliminate real estate itemded",
        "output_type": "iitax",
        "compare_with": {"Tax Expenditure": [34.0, 36.4, 38.8, 41.0]}
    }
    """
    expected_res = ('Eliminate real estate itemded'
                    '\n'
                    'Tax-Calculator,35.7,37.8,39.7,41.5')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r19(puf_subsample):
    """
    Comparison test 19
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_ID_InterestPaid_hc": [1]},
        "name": "Eliminate interest-paid itemded",
        "output_type": "iitax",
        "compare_with": {"Tax Expenditure": [74.8, 81.6, 87.8, 93.2]}
    }
    """
    expected_res = ('Eliminate interest-paid itemded'
                    '\n'
                    'Tax-Calculator,70.6,76.0,80.8,85.4')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r20(puf_subsample):
    """
    Comparison test 20
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_ID_StateLocalTax_hc": [1],
                  "_ID_RealEstate_hc": [1]},
        "name": "Eliminate both real-estate and state-local-tax itemded",
        "output_type": "iitax",
        "compare_with": {"Tax Expenditure": [74.8, 81.6, 87.8, 93.2]}
    }
    """
    expected_res = ('Eliminate both real-estate and state-local-tax itemded'
                    '\n'
                    'Tax-Calculator,98.9,104.8,110.5,115.7')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r21(puf_subsample):
    """
    Comparison test 21
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_ID_StateLocalTax_hc": [1]},
        "name": "Eliminate state-local-tax itemded",
        "output_type": "iitax",
        "compare_with": {"Tax Expenditure": [59.2, 63.0, 66.9, 70.7]}
    }
    """
    expected_res = ('Eliminate state-local-tax itemded'
                    '\n'
                    'Tax-Calculator,66.1,69.5,73.0,76.3')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r22(puf_subsample):
    """
    Comparison test 22
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_ID_Medical_hc": [1]},
        "name": "Eliminate medical itemded",
        "output_type": "iitax",
        "compare_with": {"Tax Expenditure": [11.0, 12.4, 12.7, 13.9]}
    }
    """
    expected_res = ('Eliminate medical itemded'
                    '\n'
                    'Tax-Calculator,6.9,7.4,6.9,7.2')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r23(puf_subsample):
    """
    Comparison test 23
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_ID_Casualty_hc": [1]},
        "name": "Eliminate casualty itemded",
        "output_type": "iitax",
        "compare_with": {"Tax Expenditure": [0.4, 0.5, 0.5, 0.5]}
    }
    """
    expected_res = ('Eliminate casualty itemded'
                    '\n'
                    'Tax-Calculator,0.5,0.5,0.6,0.6')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r24(puf_subsample):
    """
    Comparison test 24
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_ID_Charity_hc": [1]},
        "name": "Eliminate charity itemded",
        "output_type": "iitax",
        "compare_with": {"Tax Expenditure": [45.6, 47.0, 48.5, 50.1]}
    }
    """
    expected_res = ('Eliminate charity itemded'
                    '\n'
                    'Tax-Calculator,48.1,51.1,53.8,56.4')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r25(puf_subsample):
    """
    Comparison test 25
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_ID_Miscellaneous_frt": [0.03]},
        "name": "Increase AGI floor for miscellaneous itemded by 1 pts",
        "output_type": "iitax",
        "compare_with": {}
    }
    """
    expected_res = ('Increase AGI floor for miscellaneous itemded by 1 pts'
                    '\n'
                    'Tax-Calculator,2.1,2.2,2.3,2.4')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r26(puf_subsample):
    """
    Comparison test 26
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_ID_crt": [0.9]},
        "name": "Increase itemded maximum phaseout from 80% to 90%",
        "output_type": "iitax",
        "compare_with": {}
    }
    """
    expected_res = ('Increase itemded maximum phaseout from 80% to 90%'
                    '\n'
                    'Tax-Calculator,0.1,0.1,0.1,0.1')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r27(puf_subsample):
    """
    Comparison test 27
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_ID_ps": [[248250, 299900, 144950, 274050, 299900]]},
        "name": "Increase itemded phaseout starting AGI by $10,000",
        "output_type": "iitax",
        "compare_with": {}
    }
    """
    expected_res = ('Increase itemded phaseout starting AGI by $10,000'
                    '\n'
                    'Tax-Calculator,0.1,0.1,0.0,0.0')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r28(puf_subsample):
    """
    Comparison test 28
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_ID_prt": [0.04]},
        "name": "Increase itemded phaseout rate by 1 pts",
        "output_type": "iitax",
        "compare_with": {}
    }
    """
    expected_res = ('Increase itemded phaseout rate by 1 pts'
                    '\n'
                    'Tax-Calculator,4.2,4.4,4.6,4.7')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r29(puf_subsample):
    """
    Comparison test 29
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_ID_BenefitSurtax_crt": [0.06],
                  "_ID_BenefitSurtax_trt": [1]},
        "name": "Limit tax value of itemded to 6% of AGI",
        "output_type": "iitax",
        "compare_with": {"Budget Options": [11, 9, 8, 7]}
    }
    """
    expected_res = ('Limit tax value of itemded to 6% of AGI'
                    '\n'
                    'Tax-Calculator,20.8,21.9,22.9,24.3')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r30(puf_subsample):
    """
    Comparison test 30
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_CG_rt1": [0.02],
                  "_CG_rt2": [0.17],
                  "_CG_rt3": [0.22],
                  "_AMT_CG_rt1": [0.02],
                  "_AMT_CG_rt2": [0.17],
                  "_AMT_CG_rt3": [0.22]},
        "name": "Raise LTCG/QDIV tax rates by 2 pts, no behavioral response",
        "output_type": "iitax",
        "compare_with": {}
    }
    """
    expected_res = ('Raise LTCG/QDIV tax rates by 2 pts, '
                    'no behavioral response'
                    '\n'
                    'Tax-Calculator,18.8,20.5,20.9,21.3')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r31(puf_subsample):
    """
    Comparison test 31
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_CG_rt1": [0.02],
                  "_CG_rt2": [0.17],
                  "_CG_rt3": [0.22],
                  "_AMT_CG_rt1": [0.02],
                  "_AMT_CG_rt2": [0.17],
                  "_AMT_CG_rt3": [0.22],
                  "_BE_cg": [-3.67]},
        "name": "Raise LTCG/QDIV tax rates by 2 pts, with behavioral response",
        "output_type": "iitax",
        "compare_with": {"Budget Options": [4.6, 5, 5.3, 5.6]}
    }
    """
    expected_res = ('Raise LTCG/QDIV tax rates by 2 pts, '
                    'with behavioral response'
                    '\n'
                    'Tax-Calculator,4.3,4.5,4.6,4.7')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r32(puf_subsample):
    """
    Comparison test 32
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_II_rt1": [0.11],
                  "_II_rt2": [0.16],
                  "_II_rt3": [0.26],
                  "_II_rt4": [0.29],
                  "_II_rt5": [0.34],
                  "_II_rt6": [0.36],
                  "_II_rt7": [0.406],
                  "_PT_rt1": [0.11],
                  "_PT_rt2": [0.16],
                  "_PT_rt3": [0.26],
                  "_PT_rt4": [0.29],
                  "_PT_rt5": [0.34],
                  "_PT_rt6": [0.36],
                  "_PT_rt7": [0.406]},
        "name": "Increase tax rate in each bracket by 1 pts",
        "output_type": "iitax",
        "compare_with": {"Budget Options": [56, 60, 65, 69]}
    }
    """
    expected_res = ('Increase tax rate in each bracket by 1 pts'
                    '\n'
                    'Tax-Calculator,59.4,61.9,64.6,67.1')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r33(puf_subsample):
    """
    Comparison test 33
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_II_rt1": [0.10],
                  "_II_rt2": [0.15],
                  "_II_rt3": [0.25],
                  "_II_rt4": [0.29],
                  "_II_rt5": [0.34],
                  "_II_rt6": [0.36],
                  "_II_rt7": [0.406],
                  "_PT_rt1": [0.10],
                  "_PT_rt2": [0.15],
                  "_PT_rt3": [0.25],
                  "_PT_rt4": [0.29],
                  "_PT_rt5": [0.34],
                  "_PT_rt6": [0.36],
                  "_PT_rt7": [0.406]},
        "name": "Increase top four rates by 1 pts",
        "output_type": "iitax",
        "compare_with": {"Budget Options": [11, 12, 14, 15]}
    }
    """
    expected_res = ('Increase top four rates by 1 pts'
                    '\n'
                    'Tax-Calculator,13.7,14.3,14.9,15.4')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r34(puf_subsample):
    """
    Comparison test 34
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_II_rt1": [0.10],
                  "_II_rt2": [0.15],
                  "_II_rt3": [0.25],
                  "_II_rt4": [0.28],
                  "_II_rt5": [0.33],
                  "_II_rt6": [0.36],
                  "_II_rt7": [0.406],
                  "_PT_rt1": [0.10],
                  "_PT_rt2": [0.15],
                  "_PT_rt3": [0.25],
                  "_PT_rt4": [0.28],
                  "_PT_rt5": [0.33],
                  "_PT_rt6": [0.36],
                  "_PT_rt7": [0.406]},
        "name": "Increase top two rates by 1 pts",
        "output_type": "iitax",
        "compare_with": {"Budget Options": [7, 8, 9, 10]}
    }
    """
    expected_res = ('Increase top two rates by 1 pts'
                    '\n'
                    'Tax-Calculator,8.8,9.1,9.4,9.7')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r35(puf_subsample):
    """
    Comparison test 35
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_AMT_em": [[54600, 84400, 42700, 54600, 84400]]},
        "name": "Increase AMT exemption amount by $1000",
        "output_type": "iitax",
        "compare_with": {}
    }
    """
    expected_res = ('Increase AMT exemption amount by $1000'
                    '\n'
                    'Tax-Calculator,-1.1,-2.4,-3.9,-4.0')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r36(puf_subsample):
    """
    Comparison test 36
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_AMT_em_ps": [[129200, 168900, 89450, 129200, 168900]]},
        "name": "Increase AMT exemption phaseout starting AMTI by $10,000",
        "output_type": "iitax",
        "compare_with": {}
    }
    """
    expected_res = ('Increase AMT exemption phaseout starting AMTI by $10,000'
                    '\n'
                    'Tax-Calculator,-2.5,-3.2,-4.1,-4.2')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r37(puf_subsample):
    """
    Comparison test 37
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_AMT_prt": [0.27]},
        "name": "Increase AMT exemption phaseout rate by 2 pts",
        "output_type": "iitax",
        "compare_with": {}
    }
    """
    expected_res = ('Increase AMT exemption phaseout rate by 2 pts'
                    '\n'
                    'Tax-Calculator,2.6,2.8,3.0,3.1')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r38(puf_subsample):
    """
    Comparison test 38
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_AMT_rt1": [0.28]},
        "name": "Increase AMT rate under the surtax threshold by 2 pts",
        "output_type": "iitax",
        "compare_with": {}
    }
    """
    expected_res = ('Increase AMT rate under the surtax threshold by 2 pts'
                    '\n'
                    'Tax-Calculator,27.4,29.6,31.5,32.6')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r39(puf_subsample):
    """
    Comparison test 39
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_AMT_rt2": [0.04]},
        "name": "Increase AMT rate above the surtax threshold by 2 pts",
        "output_type": "iitax",
        "compare_with": {}
    }
    """
    expected_res = ('Increase AMT rate above the surtax threshold by 2 pts'
                    '\n'
                    'Tax-Calculator,8.7,9.4,10.0,10.5')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r40(puf_subsample):
    """
    Comparison test 40
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_AMT_brk1": [195400]},
        "name": "Increase AMT surtax threshold by $10,000",
        "output_type": "iitax",
        "compare_with": {}
    }
    """
    expected_res = ('Increase AMT surtax threshold by $10,000'
                    '\n'
                    'Tax-Calculator,-0.5,-0.6,-0.8,-0.9')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r41(puf_subsample):
    """
    Comparison test 41
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_CTC_c": [0, 0, 0, 0, 0, 0, 0, 0, 0]},
        "name": "Eliminate child tax credit",
        "output_type": "iitax",
        "compare_with": {"Tax Expenditure": [57.3, 57.0, 57.1, 56.8]}
    }
    """
    expected_res = ('Eliminate child tax credit'
                    '\n'
                    'Tax-Calculator,51.3,50.9,50.2,49.8')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r42(puf_subsample):
    """
    Comparison test 42
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_CTC_prt": [0.06]},
        "name": "Increase child tax credit phaseout rate by 1 pts",
        "output_type": "iitax",
        "compare_with": {}
    }
    """
    expected_res = ('Increase child tax credit phaseout rate by 1 pts'
                    '\n'
                    'Tax-Calculator,0.5,0.5,0.5,0.5')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r43(puf_subsample):
    """
    Comparison test 43
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_CTC_ps": [[76000, 111000, 56000, 76000, 76000]]},
        "name": "Increase child tax credit phaseout starting MAGI by $1000",
        "output_type": "iitax",
        "compare_with": {}
    }
    """
    expected_res = ('Increase child tax credit phaseout starting MAGI by $1000'
                    '\n'
                    'Tax-Calculator,-0.2,-0.2,-0.2,-0.2')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r44(puf_subsample):
    """
    Comparison test 44
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_EITC_rt": [[0, 0, 0, 0]]},
        "name": "Total EITC cost",
        "output_type": "iitax",
        "compare_with": {"Tax Expenditure": [70.4, 71.1, 72.2, 69.9]}
    }
    """
    expected_res = ('Total EITC cost'
                    '\n'
                    'Tax-Calculator,67.3,67.0,67.4,69.1')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r45(puf_subsample):
    """
    Comparison test 45
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_EITC_prt": [[0.0865, 0.1698, 0.2206, 0.2206]]},
        "name": "Increase EITC phaseout rate by 1 pts",
        "output_type": "iitax",
        "compare_with": {}
    }
    """
    expected_res = ('Increase EITC phaseout rate by 1 pts'
                    '\n'
                    'Tax-Calculator,1.2,1.1,1.1,1.2')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r46(puf_subsample):
    """
    Comparison test 46
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_EITC_ps": [[9240, 19110, 19110, 19110]]},
        "name": "Increase EITC phaseout starting AGI by $1000",
        "output_type": "iitax",
        "compare_with": {}
    }
    """
    expected_res = ('Increase EITC phaseout starting AGI by $1000'
                    '\n'
                    'Tax-Calculator,-2.1,-2.6,-3.1,-3.2')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r47(puf_subsample):
    """
    Comparison test 47
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_EITC_c": [[603, 3459, 5648, 6342]]},
        "name": "Increase maximum EITC amount by $100",
        "output_type": "iitax",
        "compare_with": {}
    }
    """
    expected_res = ('Increase maximum EITC amount by $100'
                    '\n'
                    'Tax-Calculator,-1.9,-3.0,-4.1,-4.2')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r48(puf_subsample):
    """
    Comparison test 48
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_ACTC_rt": [0.17]},
        "name": "Increase additional child tax credit rate by 2 pts",
        "output_type": "iitax",
        "compare_with": {}
    }
    """
    expected_res = ('Increase additional child tax credit rate by 2 pts'
                    '\n'
                    'Tax-Calculator,-0.9,-0.8,-0.8,-0.8')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r49(puf_subsample):
    """
    Comparison test 49
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_ACTC_ChildNum": [2]},
        "name": "Lower additional CTC minimum number of children to two",
        "output_type": "iitax",
        "compare_with": {}
    }
    """
    expected_res = ('Lower additional CTC minimum number of children to two'
                    '\n'
                    'Tax-Calculator,0.0,0.0,0.0,0.0')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r50(puf_subsample):
    """
    Comparison test 50
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_NIIT_rt": [0]},
        "name": "Eliminate Net Investment Income Tax",
        "output_type": "iitax",
        "compare_with": {"Tax Expenditure": [-32.6, -34.7, -36.6, -38.9]}
    }
    """
    expected_res = ('Eliminate Net Investment Income Tax'
                    '\n'
                    'Tax-Calculator,-36.4,-39.7,-40.6,-41.6')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r51(puf_subsample):
    """
    Comparison test 51
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_NIIT_thd": [[210000, 260000, 135000, 210000, 260000]]},
        "name": "Increase Net Investment Income Tax threshold by $10,000",
        "output_type": "iitax",
        "compare_with": {}
    }
    """
    expected_res = ('Increase Net Investment Income Tax threshold by $10,000'
                    '\n'
                    'Tax-Calculator,-0.4,-0.5,-0.5,-0.5')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r52(puf_subsample):
    """
    Comparison test 52
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_II_credit": [[1000, 1000, 1000, 1000, 1000]]},
        "name": "New $1000 personal refundable credit, no phaseout",
        "output_type": "iitax",
        "compare_with": {}
    }
    """
    expected_res = ('New $1000 personal refundable credit, no phaseout'
                    '\n'
                    'Tax-Calculator,-164.4,-170.2,-177.1,-184.0')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r53(puf_subsample):
    """
    Comparison test 53
    """
    reform_json = """
    {
        "start_year": 2015,
        "value": {"_II_credit": [[1000, 1000, 1000, 1000, 1000]],
                  "_II_credit_ps": [[10000, 10000, 10000, 10000, 10000]],
                  "_II_credit_prt": [0.01]},
        "name": "New $1000 personal refundable credit, 0.01 po above $10K AGI",
        "output_type": "iitax",
        "compare_with": {}
    }
    """
    expected_res = ('New $1000 personal refundable credit, 0.01 po '
                    'above $10K AGI'
                    '\n'
                    'Tax-Calculator,-107.7,-110.9,-115.3,-119.9')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r54(puf_subsample):
    """
    Comparison test 54
    """
    reform_json = """
    {
        "start_year": 2017,
        "value": {"_FST_AGI_trt": [0.3],
                  "_FST_AGI_thd_lo": [[1.0e6, 1.0e6, 0.5e6, 1.0e6, 1.0e6]],
                  "_FST_AGI_thd_hi": [[2.0e6, 2.0e6, 1.0e6, 2.0e6, 2.0e6]]},
        "name": "Increase FST rate from zero to 0.30 beginning in 2017",
        "output_type": "iitax",
        "compare_with": {"Tax Foundation": [321, "ten-year(2016-25)",
                                            "static", "estimate"]}
    }
    """
    expected_res = ('Increase FST rate from zero to 0.30 beginning in 2017'
                    '\n'
                    'Tax-Calculator,42.2,43.3,42.7,43.5')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res


@pytest.mark.requires_pufcsv
def test_r55(puf_subsample):
    """
    Comparison test 55
    """
    reform_json = """
    {
        "start_year": 2017,
        "value": {"_ID_AmountCap_rt": [0.02],
                  "_ID_AmountCap_Switch":
                  [[false, true, true, false, false, false, false]]},
        "name": "Limit amount of S&L deduction to 2% AGI",
        "output_type": "iitax",
        "compare_with": {"Budget Options": [44.1, 86.6, 87.1, 91.2]}
    }
    """
    expected_res = ('Limit amount of S&L deduction to 2% AGI'
                    '\n'
                    'Tax-Calculator,86.2,90.3,94.6,98.9')
    actual_res = reform_results(json.loads(reform_json), puf_subsample)
    assert actual_res == expected_res
