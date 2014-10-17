import pandas as pd
from pandas import DataFrame
import math
import numpy as np

output_filename = 'translationoutput.csv' 

from taxcalc.constants import *
from taxcalc.puf import *

def FilingStatus(puf):
    # Filing based on marital status
    global _sep
    global _txp
    if puf.MARS in (3, 6):
        _sep = 2
        _txp = 2
    else:
        _sep = 1
        _txp = 1
    
    return DataFrame(data=np.column_stack((_sep, _txp)),
                     columns=['_sep', '_txp'])

def Adj():
    # Adjustments
    global _feided
    global c02900
    _feided = np.maximum(e35300_0, e35600_0, + e35910_0)  # Form 2555

    x03150 = e03150
    c02900 = (x03150 + e03210 + e03600 + e03260 + e03270 + e03300
              + e03400 + e03500 + e03280 + e03900 + e04000 + e03700
              + e03220 + e03230
              + e03240
              + e03290)

    return DataFrame(data=np.column_stack((_feided, c02900)),
                     columns=['_feided', 'c02900'])

def CapGains():
    # Capital Gains
    global _ymod
    global _ymod1
    global c02700
    global c23650
    global c01000
    c23650 = e23250 + e22250 + e23660
    c01000 = np.maximum(-3000 / _sep, c23650)
    c02700 = np.minimum(_feided, _feimax[2013 - FLPDYR] * f2555)
    _ymod1 = (e00200 + e00300 + e00600 + e00700 + e00800 + e00900 + c01000
              + e01100 + e01200 + e01400 + e01700 +
              e02000 + e02100 + e02300 + e02600
              + e02610 + e02800 - e02540)
    _ymod2 = e00400 + (0.50 * e02400) - c02900
    _ymod3 = e03210 + e03230 + e03240 + e02615
    _ymod = _ymod1 + _ymod2 + _ymod3

    return DataFrame(data=np.column_stack((c23650, c01000, c02700, _ymod1,
                                           _ymod2, _ymod3, _ymod)),
                     columns=['c23650', 'c01000', 'c02700', '_ymod1', '_ymod2',
                               '_ymod3', '_ymod'])


def SSBenefits():
    # Social Security Benefit Taxation
    global c02500
    c02500 = np.where(np.logical_or(SSIND != 0, np.logical_or(MARS == 3, MARS == 6)), e02500,
                      np.where(_ymod < _ssb50[MARS - 1], 0,
                               np.where(np.logical_and(_ymod >= _ssb50[MARS - 1], _ymod < _ssb85[MARS - 1]), 0.5 * np.minimum(_ymod - _ssb50[MARS - 1], e02400),
                                        np.minimum(0.85 * (_ymod - _ssb85[MARS - 1]) + 0.50 * np.minimum(e02400, _ssb85[MARS - 1] - _ssb50[MARS - 1]), 0.85 * e02400
                                                   ))))

    return DataFrame(data=np.column_stack((c02500,e02500)),
                     columns=['c02500', 'e02500'])



def AGI():
    # Adjusted Gross Income
    global _posagi
    global c00100
    global c04600
    c02650 = _ymod1 + c02500 - c02700 + e02615  # Gross Income

    c00100 = c02650 - c02900
    _agierr = e00100 - c00100  # Adjusted Gross Income
    c00100 = np.where(_fixup >= 1, c00100 + _agierr, c00100)

    _posagi = np.maximum(c00100, 0)
    _ywossbe = e00100 - e02500
    _ywossbc = c00100 - c02500

    _prexmp = XTOT * _amex[FLPDYR - 2013]
    # Personal Exemptions (_phaseout smoothed)

    _dispc = np.zeros((dim,))
    _dispc = np.minimum(1, np.maximum(
        0, 0.02 * (_posagi - _exmpb[FLPDYR - 2013, MARS - 1]) / (2500 / _sep)))

    c04600 = _prexmp * (1 - _dispc)

    return DataFrame(data=np.column_stack((c02650, c00100, _agierr, _posagi,
                                           _ywossbe, _ywossbc, _prexmp,
                                           c04600)),
                     columns=['c02650', 'c00100', '_agierr', '_posagi',
                              '_ywossbe', '_ywossbc', '_prexmp', 'c04600'])
                              

def ItemDed(puf):
    # Itemized Deductions
    global c04470
    global c21060
    global c21040
    global c17000
    global c18300
    global c20800
    global _sit

    # Medical #
    c17750 = 0.075 * _posagi
    c17000 = np.maximum(0, e17500 - c17750)

    # State and Local Income Tax, or Sales Tax #
    _sit1 = np.maximum(e18400, e18425)
    _sit = np.maximum(_sit1, 0)
    _statax = np.maximum(_sit, e18450)

    # Other Taxes #
    c18300 = _statax + e18500 + e18800 + e18900

    # Casulty #
    c37703 = np.where(e20500 > 0, e20500 + 0.10 * _posagi, 0)
    c20500 = np.where(e20500 > 0, c37703 - 0.10 * _posagi, 0)

    # Miscellaneous #
    c20750 = 0.02 * _posagi
    if puf == True:
        c20400 = e20400
        c19200 = e19200
    else:
        c20400 = e20550 + e20600 + e20950
        c19200 = e19500 + e19570 + e19400 + e19550
    c20800 = np.maximum(0, c20400 - c20750)

    # Charity (assumes carryover is non-cash) #

    _lim50 = np.where(e19800 + e20100 + e20200 <= 0.20 *
                      _posagi, 0, np.minimum(0.50 * _posagi, e19800))
    _lim30 = np.where(e19800 + e20100 + e20200 <= 0.20 *
                      _posagi, 0, np.minimum(0.30 * _posagi, e20100 + e20200))

    c19700 = np.where(e19800 + e20100 + e20200 <= 0.20 * _posagi, 
        e19800 + e20100 + e20200, np.minimum(0.5 * _posagi, _lim30 + _lim50))
    # temporary fix!??

# Gross Itemized Deductions #
    c21060 = (e20900 + c17000 + c18300 + c19200 + c19700
              + c20500 + c20800 + e21000 + e21010)
    
    # Itemized Deduction Limitation
    _phase2 = np.where(MARS == 1, 200000, 0)
    _phase2 = np.where(MARS == 4, 250000, _phase2)
    _phase2 = np.where(np.logical_and(MARS != 1, MARS != 4), 300000, _phase2)

    _itemlimit = np.ones((dim,))
    _nonlimited = c17000 + c20500 + e19570 + e21010 + e20900
    _limitratio = _phase2/_sep 

    c04470 = c21060

    _itemlimit = np.where(np.logical_and(c21060 > _nonlimited,
                                         c00100 > _phase2 / _sep), 2, 1)
    _dedmin = np.where(np.logical_and(c21060 > _nonlimited,
                                      c00100 > _phase2 / _sep), 0.8 * (c21060 - _nonlimited), 0)
    _dedpho = np.where(np.logical_and(c21060 > _nonlimited,
                                      c00100 > _phase2 / _sep), 0.03 * np.maximum(0, _posagi - _phase2 / _sep), 0)
    c21040 = np.where(np.logical_and(c21060 > _nonlimited,
                                     c00100 > _phase2 / _sep), np.minimum(_dedmin, _dedpho), 0)
    c04470 = np.where(np.logical_and(c21060 > _nonlimited,
                                     c00100 > _phase2 / _sep), c21060 - c21040, c04470)

    outputs = (c17750, c17000, _sit1, _sit, _statax, c18300, c37703, c20500,
               c20750, c20400, c19200, c20800, _lim50, _lim30, c19700, c21060,
               _phase2, _itemlimit, _nonlimited, _limitratio, c04470,
               _itemlimit, _dedpho, _dedmin, c21040)
               
    header= ['c17750', 'c17000', '_sit1', '_sit', '_statax', 'c18300', 'c37703',
             'c20500', 'c20750', 'c20400', 'c19200', 'c20800', '_lim50',
             '_lim30', 'c19700', 'c21060', '_phase2', '_itemlimit',
             '_nonlimited', '_limitratio', 'c04470', '_itemlimit', '_dedpho',
             '_dedmin', 'c21040']

    return DataFrame(data=np.column_stack(outputs), columns=header)


def EI_FICA():
    global _sey
    global _setax
    # Earned Income and FICA #
    global _earned
    _sey = e00900 + e02100
    _fica = np.maximum(0, .153 * np.minimum(_ssmax[FLPDYR - 2013],
                                            e00200 + np.maximum(0, _sey) * 0.9235))
    _setax = np.maximum(0, _fica - 0.153 * e00200)
    _seyoff = np.where(_setax <= 14204, 0.5751 * _setax, 0.5 * _setax + 10067)

    c11055 = e11055

    _earned = np.maximum(0, e00200 + e00250 + e11055 + e30100 + _sey - _seyoff)

    outputs = (_sey, _fica, _setax, _seyoff, c11055, _earned)
    header = ['_sey', '_fica', '_setax', '_seyoff', 'c11055', '_earned']

    return DataFrame(data=np.column_stack(outputs), columns=header), _earned
                     

def StdDed():
    # Standard Deduction with Aged, Sched L and Real Estate #
    global c04800
    global c60000
    global _taxinc
    global _feitax
    global _standard

    c15100 = np.where(DSI == 1,
                      np.maximum(300 + _earned, _stded[FLPDYR - 2013, 6]), 0)

    _compitem = np.where(np.logical_and(e04470 > 0, e04470 < _stded[FLPDYR-2013, MARS-1]), 1, 0)
    
    c04100 = np.where(DSI == 1, np.minimum(_stded[FLPDYR - 2013, MARS - 1], c15100),
                      np.where(np.logical_or(_compitem == 1,
                                             np.logical_and(np.logical_and(3 <= MARS, MARS <= 6), MIdR == 1)),
                               0, _stded[FLPDYR - 2013, MARS - 1]))

    c04100 = c04100 + e15360
    _numextra = AGEP + AGES + PBI + SBI

    _txpyers = np.where(np.logical_or(np.logical_or(MARS == 2, MARS == 3),
                                      MARS == 3), 2, 1)
    c04200 = np.where(np.logical_and(_exact == 1,
                                     np.logical_or(MARS == 3, MARS == 5)),
                      e04200, _numextra * _aged[_txpyers - 1, FLPDYR - 2013])

    c15200 = c04200

    _standard = np.where(np.logical_and(np.logical_or(MARS == 3, MARS == 6),
                                        c04470 > 0),
                         0, c04100 + c04200)

    _othded = np.where(FDED == 1, e04470 - c04470, 0)
    #c04470 = np.where(np.logical_and(_fixup >= 2, FDED == 1), c04470 + _othded, c04470)
    c04100 = np.where(FDED == 1, 0, c04100)
    c04200 = np.where(FDED == 1, 0, c04200)
    _standard = np.where(FDED == 1, 0, _standard)

    c04500 = c00100 - np.maximum(c21060 - c21040,
                                 np.maximum(c04100, _standard + e37717))
    c04800 = np.maximum(0, c04500 - c04600 - e04805)

    c60000 = np.where(_standard > 0, c00100, c04500)
    c60000 = c60000 - e04805

    # Some taxpayers iteimize only for AMT, not regular tax
    _amtstd = np.zeros((dim,))
    c60000 = np.where(np.logical_and(np.logical_and(e04470 == 0,
                                                    t04470 > _amtstd),
                                     np.logical_and(f6251 == 1, _exact == 1)), c00100 - t04470, c60000)

    _taxinc = np.where(np.logical_and(c04800 > 0, _feided > 0),
                       c04800 + c02700, c04800)

    _feitax = np.zeros((dim,))
    _oldfei = np.zeros((dim,))

    _feitax = np.where(np.logical_and(c04800 > 0, _feided > 0), Taxer(
        inc_in=_feided, inc_out=_feitax, MARS=MARS), _feitax)
    _oldfei = np.where(np.logical_and(c04800 > 0, _feided > 0), Taxer(
        inc_in=c04800, inc_out=_oldfei, MARS=MARS), _oldfei)

    SDoutputs = (c15100, c04100, _numextra, _txpyers, c04200, c15200,
                 _standard, _othded, c04100, c04200, _standard, c04500,
                 c04800, c60000, _amtstd, _taxinc, _feitax, _oldfei)
                 
    header = ['c15100', 'c04100', '_numextra', '_txpyers', 'c04200', 'c15200',
              '_standard', '_othded', 'c04100', 'c04200', '_standard',
              'c04500', 'c04800', 'c60000', '_amtstd', '_taxinc', '_feitax',
              '_oldfei']

    return DataFrame(data=np.column_stack(SDoutputs),
                     columns=header)


def XYZD():
    global c24580
    global _xyztax

    _xyztax = np.zeros((dim,))
    c05200 = np.zeros((dim,))
    _xyztax = Taxer(inc_in=_taxinc, inc_out=_xyztax, MARS=MARS)
    c05200 = Taxer(inc_in=c04800, inc_out=c05200, MARS=MARS)

    return DataFrame(data=np.column_stack((_xyztax, c05200)),
                     columns=['_xyztax', 'c05200'])


def NonGain():
    _cglong = np.minimum(c23650, e23250) + e01100
    _noncg = np.zeros((dim,))

    return DataFrame(data=np.column_stack((_cglong, _noncg)),
                     columns=['_cglong', '_noncg'])


def TaxGains():
    global c05750
    global c24517
    global _taxbc
    global c24516
    global c24520
    global c05700
    c24517 = np.zeros((dim,))
    c24520 = np.zeros((dim,))
    c24530 = np.zeros((dim,))
    c24540 = np.zeros((dim,))
    _dwks16 = np.zeros((dim,))

    _hasgain = np.zeros((dim,))

    _hasgain = np.where(np.logical_or(e01000 > 0, c23650 > 0), 1, _hasgain)
    _hasgain = np.where(np.logical_or(e23250 > 0, e01100 > 0), 1, _hasgain)
    _hasgain = np.where(e00650 > 0, 1, _hasgain)

    _dwks5 = np.where(
        np.logical_and(_taxinc > 0, _hasgain == 1), np.maximum(0, e58990 - e58980), 0)

    c00650 = e00650
    c24505 = np.where(
        np.logical_and(_taxinc > 0, _hasgain == 1), np.maximum(0, c00650 - _dwks5), 0)
    c24510 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), np.maximum(
        0, np.minimum(c23650, e23250)) + e01100, 0)
    # gain for tax computation

    c24510 = np.where(np.logical_and(
        _taxinc > 0, np.logical_and(_hasgain == 1, e01100 > 0)), e01100, c24510)
    # from app f 2008 drf

    _dwks9 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), np.maximum(
        0, c24510 - np.minimum(e58990, e58980)), 0)
    # e24516 gain less invest y

    c24516 = np.maximum(0, np.minimum(e23250, c23650)) + e01100
    c24580 = _xyztax

    c24516 = np.where(
        np.logical_and(_taxinc > 0, _hasgain == 1), c24505 + _dwks9, c24516)
    _dwks12 = np.where(np.logical_and(
        _taxinc > 0, _hasgain == 1), np.minimum(_dwks9, e24515 + e24518), 0)
    c24517 = np.where(
        np.logical_and(_taxinc > 0, _hasgain == 1), c24516 - _dwks12, 0)
    # gain less 25% and 28%

    c24520 = np.where(
        np.logical_and(_taxinc > 0, _hasgain == 1), np.maximum(0, _taxinc - c24517), 0)
    # tentative TI less schD gain

    c24530 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), np.minimum(
        _brk2[FLPDYR - 2013, MARS - 1], _taxinc), 0)
    # minimum TI for bracket

    _dwks16 = np.where(
        np.logical_and(_taxinc > 0, _hasgain == 1), np.minimum(c24520, c24530), 0)
    _dwks17 = np.where(
        np.logical_and(_taxinc > 0, _hasgain == 1), np.maximum(0, _taxinc - c24516), 0)
    c24540 = np.where(
        np.logical_and(_taxinc > 0, _hasgain == 1), np.maximum(_dwks16, _dwks17), 0)

    c24534 = np.where(
        np.logical_and(_taxinc > 0, _hasgain == 1), c24530 - _dwks16, 0)
    _dwks21 = np.where(
        np.logical_and(_taxinc > 0, _hasgain == 1), np.minimum(_taxinc, c24517), 0)
    c24597 = np.where(
        np.logical_and(_taxinc > 0, _hasgain == 1), np.maximum(0, _dwks21 - c24534), 0)
    # income subject to 15% tax

    c24598 = 0.15 * c24597  # actual 15% tax

    _dwks25 = np.where(
        np.logical_and(_taxinc > 0, _hasgain == 1), np.minimum(_dwks9, e24515), 0)
    _dwks26 = np.where(
        np.logical_and(_taxinc > 0, _hasgain == 1), c24516 + c24540, 0)
    _dwks28 = np.where(
        np.logical_and(_taxinc > 0, _hasgain == 1), np.maximum(0, _dwks26 - _taxinc), 0)
    c24610 = np.where(
        np.logical_and(_taxinc > 0, _hasgain == 1), np.maximum(0, _dwks25 - _dwks28), 0)
    c24615 = np.where(
        np.logical_and(_taxinc > 0, _hasgain == 1), 0.25 * c24610, 0)
    _dwks31 = np.where(np.logical_and(
        _taxinc > 0, _hasgain == 1), c24540 + c24534 + c24597 + c24610, 0)
    c24550 = np.where(
        np.logical_and(_taxinc > 0, _hasgain == 1), np.maximum(0, _taxinc - _dwks31), 0)
    c24570 = np.where(
        np.logical_and(_taxinc > 0, _hasgain == 1), 0.28 * c24550, 0)
    _addtax = np.zeros((dim,))
    _addtax = np.where(np.logical_and(_taxinc > 0, np.logical_and(
        _hasgain == 1, c24540 > _brk6[FLPDYR - 2013, MARS - 1])), 0.05 * c24517, _addtax)
    _addtax = np.where(np.logical_and(np.logical_and(_taxinc > 0, _hasgain == 1), np.logical_and(c24540 <= _brk6[
                       FLPDYR - 2013, MARS - 1], _taxinc > _brk6[FLPDYR - 2013, MARS - 1])), 0.05 * np.minimum(c04800 - _brk6[FLPDYR - 2013, MARS - 1], c24517), _addtax)

    c24560 = np.zeros((dim,))
    c24560 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), Taxer(
        inc_in=c24540, inc_out=c24560, MARS=MARS), c24560)

    _taxspecial = np.where(np.logical_and(
        _taxinc > 0, _hasgain == 1), c24598 + c24615 + c24570 + c24560 + _addtax, 0)

    c24580 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), np.minimum(
        _taxspecial, _xyztax), c24580)
    # e24580 schedule D tax

    c05100 = c24580
    c05100 = np.where(np.logical_and(
        c04800 > 0, _feided > 0), np.maximum(0, c05100 - _feitax), c05100)

    # Form 4972 - Lump Sum Distributions
    c05700 = np.zeros((dim,))

    c59430 = np.where(_cmp == 1, np.maximum(0, e59410 - e59420), 0)
    c59450 = np.where(_cmp == 1, c59430 + e59440, 0)  # income plus lump sum
    c59460 = np.where(_cmp == 1, np.maximum(
        0, np.minimum(0.5 * c59450, 10000)) - 0.2 * np.maximum(0, c59450 - 20000), 0)
    _line17 = np.where(_cmp == 1, c59450 - c59460, 0)
    _line19 = np.where(_cmp == 1, c59450 - c59460 - e59470, 0)
    _line22 = np.where(np.logical_and(_cmp == 1, c59450 > 0), np.maximum(
        0, e59440 - e59440 * c59460 / c59450), 0)

    _line30 = np.where(
        _cmp == 1, 0.1 * np.maximum(0, c59450 - c59460 - e59470), 0)

    _line31 = np.where(_cmp == 1,
                       0.11 * np.minimum(_line30, 1190)
                       + 0.12 *
                       np.minimum(2270 - 1190, np.maximum(0, _line30 - 1190))
                       + 0.14 *
                       np.minimum(4530 - 2270, np.maximum(0, _line30 - 2270))
                       + 0.15 *
                       np.minimum(6690 - 4530, np.maximum(0, _line30 - 4530))
                       + 0.16 *
                       np.minimum(9170 - 6690, np.maximum(0, _line30 - 6690))
                       + 0.18 *
                       np.minimum(11440 - 9170, np.maximum(0, _line30 - 9170))
                       + 0.20 *
                       np.minimum(
                           13710 - 11440, np.maximum(0, _line30 - 11440))
                       + 0.23 *
                       np.minimum(
                           17160 - 13710, np.maximum(0, _line30 - 13710))
                       + 0.26 *
                       np.minimum(
                           22880 - 17160, np.maximum(0, _line30 - 17160))
                       + 0.30 *
                       np.minimum(
                           28600 - 22880, np.maximum(0, _line30 - 22880))
                       + 0.34 *
                       np.minimum(
                           34320 - 28600, np.maximum(0, _line30 - 28600))
                       + 0.38 *
                       np.minimum(
                           42300 - 34320, np.maximum(0, _line30 - 34320))
                       + 0.42 *
                       np.minimum(
                           57190 - 42300, np.maximum(0, _line30 - 42300))
                       + 0.48 *
                       np.minimum(
                           85790 - 57190, np.maximum(0, _line30 - 57190)),
                       0)

    _line32 = np.where(_cmp == 1, 10 * _line31, 0)
    _line36 = np.where(np.logical_and(_cmp == 1, e59440 == 0), _line32, 0)
    _line33 = np.where(np.logical_and(_cmp == 1, e59440 > 0), 0.1 * _line22, 0)
    _line34 = np.where(np.logical_and(_cmp == 1, e59440 > 0),
                       0.11 * np.minimum(_line30, 1190)
                       + 0.12 *
                       np.minimum(2270 - 1190, np.maximum(0, _line30 - 1190))
                       + 0.14 *
                       np.minimum(4530 - 2270, np.maximum(0, _line30 - 2270))
                       + 0.15 *
                       np.minimum(6690 - 4530, np.maximum(0, _line30 - 4530))
                       + 0.16 *
                       np.minimum(9170 - 6690, np.maximum(0, _line30 - 6690))
                       + 0.18 *
                       np.minimum(11440 - 9170, np.maximum(0, _line30 - 9170))
                       + 0.20 *
                       np.minimum(
                           13710 - 11440, np.maximum(0, _line30 - 11440))
                       + 0.23 *
                       np.minimum(
                           17160 - 13710, np.maximum(0, _line30 - 13710))
                       + 0.26 *
                       np.minimum(
                           22880 - 17160, np.maximum(0, _line30 - 17160))
                       + 0.30 *
                       np.minimum(
                           28600 - 22880, np.maximum(0, _line30 - 22880))
                       + 0.34 *
                       np.minimum(
                           34320 - 28600, np.maximum(0, _line30 - 28600))
                       + 0.38 *
                       np.minimum(
                           42300 - 34320, np.maximum(0, _line30 - 34320))
                       + 0.42 *
                       np.minimum(
                           57190 - 42300, np.maximum(0, _line30 - 42300))
                       + 0.48 *
                       np.minimum(
                           85790 - 57190, np.maximum(0, _line30 - 57190)),
                       0)
    _line35 = np.where(np.logical_and(_cmp == 1, e59440 > 0), 10 * _line34, 0)
    _line36 = np.where(
        np.logical_and(_cmp == 1, e59440 > 0), np.maximum(0, _line32 - _line35), 0)
    # tax saving from 10 yr option
    c59485 = np.where(_cmp == 1, _line36, 0)
    c59490 = np.where(_cmp == 1, c59485 + 0.2 * np.maximum(0, e59400), 0)
    # pension gains tax plus

    c05700 = np.where(_cmp == 1, c59490, 0)

    _s1291 = e10105
    _parents = e83200_0
    c05750 = np.maximum(c05100 + _parents + c05700, e74400)
    _taxbc = c05750

    outputs = (e00650, _hasgain, _dwks5, c24505, c24510, _dwks9, c24516,
               c24580, c24516, _dwks12, c24517, c24520, c24530, _dwks16,
               _dwks17, c24540, c24534, _dwks21, c24597, c24598, _dwks25,
               _dwks26, _dwks28, c24610, c24615, _dwks31, c24550, c24570,
               _addtax, c24560, _taxspecial, c05100, c05700, c59430,
               c59450, c59460, _line17, _line19, _line22, _line30, _line31,
               _line32, _line36, _line33, _line34, _line35, c59485, c59490,
               c05700, _s1291, _parents, c05750, _taxbc)

    header = ['e00650', '_hasgain', '_dwks5', 'c24505', 'c24510', '_dwks9',
              'c24516', 'c24580', 'c24516', '_dwks12', 'c24517', 'c24520',
              'c24530', '_dwks16', '_dwks17', 'c24540', 'c24534', '_dwks21',
              'c24597', 'c24598', '_dwks25', '_dwks26', '_dwks28', 'c24610',
              'c24615', '_dwks31', 'c24550', 'c24570', '_addtax', 'c24560',
              '_taxspecial', 'c05100', 'c05700', 'c59430', 'c59450', 'c59460',
              '_line17', '_line19', '_line22', '_line30', '_line31',
              '_line32', '_line36', '_line33', '_line34', '_line35',
              'c59485', 'c59490', 'c05700', '_s1291', '_parents', 'c05750',
              '_taxbc']

    return DataFrame(data=np.column_stack(outputs),
                     columns=header) , c05750


def MUI(c05750):
    # Additional Medicare tax on unearned Income
    c05750 = c05750
    c05750 = np.where(c00100 > _thresx[MARS - 1], c05750 + 0.038 * np.minimum(
        e00300 + e00600 + np.maximum(0, c01000) + np.maximum(0, e02000), c00100 - _thresx[MARS - 1]), c05750)
	
    return DataFrame(data=np.column_stack((c05750,)),
                     columns=['c05750'])
    

def AMTI(puf):
    global c05800
    global _othtax
    global _agep
    global _ages
    c62720 = c24517 + x62720
    c60260 = e00700 + x60260
    c63100 = np.maximum(0, _taxbc - e07300)
    c60200 = np.minimum(c17000, 0.025 * _posagi)
    c60240 = c18300 + x60240
    c60220 = c20800 + x60220
    c60130 = c21040 + x60130
    c62730 = e24515 + x62730

    _amtded = c60200 + c60220 + c60240
    _amtded = np.where(c60000 <= 0, np.maximum(0, _amtded + c60000), _amtded)
    _addamt = np.where(np.logical_or(_exact == 0, np.logical_and(_exact == 1, _amtded + e60290 > 0)), _amtded + e60290 - c60130, 0)

    c62100 = np.where(_cmp == 1, (_addamt + e60300 + e60860 + e60100 + e60840 + e60630 + e60550
                                                            + e60720 + e60430 + e60500 + e60340 +
                                  e60680 + e60600 + e60405 + e60440
                                                            + e60420 + e60410 + e61400 + e60660 - c60260 - e60480 - e62000 + c60000), 0)

    c62100 = np.where(_cmp == 1, c62100 - e60250, c62100)

    _cmbtp = np.zeros((dim,))

    _edical = np.where(np.logical_and(puf == True, np.logical_or(_standard == 0, np.logical_and(
        _exact == 1, e04470 > 0))), np.maximum(0, e17500 - np.maximum(0, e00100) * 0.075), 0)

    _cmbtp = np.where(np.logical_and(puf == True, np.logical_and(np.logical_or(_standard == 0, np.logical_and(_exact == 1, e04470 > 0)), f6251 == 1)
                                     ), -1 * np.minimum(_edical, 0.025 * np.maximum(0, e00100)) + e62100 + c60260 + e04470 + e21040 - _sit - e00100 - e18500 - e20800, _cmbtp)

    c62100 = np.where(np.logical_and(puf == True, np.logical_or(_standard == 0, np.logical_and(_exact == 1, e04470 > 0))),
                      c00100 - c04470 + np.minimum(c17000, 0.025 * np.maximum(0, c00100)) + _sit + e18500 - c60260 + c20800 - c21040 + _cmbtp, c62100)

    _cmbtp = np.where(np.logical_and(puf == True, np.logical_and(
        _standard > 0, f6251 == 1)), e62100 - e00100 + c60260, _cmbtp)
    c62100 = np.where(
        np.logical_and(puf == True, _standard > 0), c00100 - c60260 + _cmbtp, c62100)

    x62100 = c62100

    _amtsepadd = np.where(np.logical_and(c62100 > _amtsep[FLPDYR - 2013], np.logical_or(MARS == 3, MARS == 6)), np.maximum(
        0, np.minimum(_almsep[FLPDYR - 2013], 0.25 * (c62100 - _amtsep[FLPDYR - 2013]))), 0)
    c62100 = np.where(np.logical_and(c62100 > _amtsep[
                      FLPDYR - 2013], np.logical_or(MARS == 3, MARS == 6)), c62100 + _amtsepadd, c62100)

    c62600 = np.maximum(0, _amtex[
                        FLPDYR - 2013, MARS - 1] - 0.25 * np.maximum(0, c62100 - _amtys[MARS - 1]))

    _agep = np.where(
        DOBYR > 0, np.ceil((12 * (FLPDYR - DOBYR) - DOBMD / 100) / 12), 0)
    _ages = np.where(
        SDOBYR > 0, np.ceil((12 * (FLPDYR - SDOBYR) - SDOBMD / 100) / 12), 0)

    c62600 = np.where(np.logical_and(
        _cmp == 1, np.logical_and(f6251 == 1, _exact == 1)), e62600, c62600)

    c62600 = np.where(np.logical_and(np.logical_and(_cmp == 1, _exact == 0), np.logical_and(
        _agep < _amtage[FLPDYR - 2013], _agep != 0)), np.minimum(c62600, _earned + _almdep[FLPDYR - 2013]), c62600)

    c62700 = np.maximum(0, c62100 - c62600)

    _alminc = c62700
    _amtfei = np.zeros((dim,))

    _alminc = np.where(
        c02700 > 0, np.maximum(0, c62100 - c62600 + c02700), _alminc)
    _amtfei = np.where(c02700 > 0, 0.26 * c02700 + 0.02 *
                       np.maximum(0, c02700 - _almsp[FLPDYR - 2013] / _sep), _amtfei)

    c62780 = 0.26 * _alminc + 0.02 * \
        np.maximum(0, _alminc - _almsp[FLPDYR - 2013] / _sep) - _amtfei

    c62900 = np.where(f6251 != 0, e62900, e07300)
    c63000 = c62780 - c62900

    c62740 = np.minimum(np.maximum(0, c24516 + x62740), c62720 + c62730)
    c62740 = np.where(c24516 == 0, c62720 + c62730, c62740)

    _ngamty = np.maximum(0, _alminc - c62740)

    c62745 = 0.26 * _ngamty + 0.02 * \
        np.maximum(0, _ngamty - _almsp[FLPDYR - 2013] / _sep)
    y62745 = _almsp[FLPDYR - 2013] / _sep
    _tamt2 = np.zeros((dim,))

    _amt5pc = np.zeros((dim,))
    _amt15pc = np.minimum(_alminc, c62720) - _amt5pc - np.minimum(np.maximum(
        0, _brk2[FLPDYR - 2013, MARS - 1] - c24520), np.minimum(_alminc, c62720))
    _amt15pc = np.where(c04800 == 0, np.maximum(
        0, np.minimum(_alminc, c62720) - _brk2[FLPDYR - 2013, MARS - 1]), _amt15pc)
    _amt25pc = np.minimum(_alminc, c62740) - np.minimum(_alminc, c62720)

    _amt25pc = np.where(c62730 == 0, 0, _amt25pc)
    c62747 = _cgrate1[FLPDYR - 2013] * _amt5pc
    c62755 = _cgrate2[FLPDYR - 2013] * _amt15pc
    c62770 = 0.25 * _amt25pc
    _tamt2 = c62747 + c62755 + c62770

    _amt = np.zeros((dim,))
    _amt = np.where(_ngamty > _brk6[
                    FLPDYR - 2013, MARS - 1], 0.05 * np.minimum(_alminc, c62740), _amt)
    _amt = np.where(np.logical_and(_ngamty <= _brk6[FLPDYR - 2013, MARS - 1], _alminc > _brk6[
                    FLPDYR - 2013, MARS - 1]), 0.05 * np.minimum(_alminc - _brk6[FLPDYR - 2013, MARS - 1], c62740), _amt)

    _tamt2 = _tamt2 + _amt

    c62800 = np.minimum(c62780, c62745 + _tamt2 - _amtfei)
    c63000 = c62800 - c62900
    c63100 = _taxbc - e07300 - c05700
    c63100 = c63100 + e10105

    c63100 = np.maximum(0, c63100)
    c63200 = np.maximum(0, c63000 - c63100)
    c09600 = c63200
    _othtax = e05800 - (e05100 + e09600)

    c05800 = _taxbc + c63200

    outputs = (c62720, c60260, c63100, c60200, c60240, c60220, c60130,
               c62730, _addamt, c62100, _cmbtp, _edical, _amtsepadd, c62600,
               _agep, _ages, c62600, c62700, _alminc, _amtfei, c62780,
               c62900, c63000, c62740, _ngamty, c62745, y62745, _tamt2,
               _amt5pc, _amt15pc, _amt25pc, c62747, c62755, c62770, _amt,
               c62800, c09600, _othtax, c05800)
               
    header = ['c62720', 'c60260', 'c63100', 'c60200', 'c60240', 'c60220',
              'c60130', 'c62730', '_addamt', 'c62100', '_cmbtp', '_edical',
              '_amtsepadd', 'c62600', '_agep', '_ages', 'c62600', 'c62700',
              '_alminc', '_amtfei', 'c62780', 'c62900', 'c63000', 'c62740',
              '_ngamty', 'c62745', 'y62745', '_tamt2', '_amt5pc', '_amt15pc',
              '_amt25pc', 'c62747', 'c62755', 'c62770', '_amt', 'c62800',
              'c09600', '_othtax', 'c05800']

    return DataFrame(data=np.column_stack(outputs),
                     columns=header), c05800
    

def F2441(puf, _earned):
    global c32880
    global c32890
    global c32800
    global _dclim
    _earned = _earned
    _earned = np.where(_fixeic == 1, e59560, _earned)
    c32880 = np.where(np.logical_and(MARS == 2, puf == True), 0.5 * _earned, 0)
    c32890 = np.where(np.logical_and(MARS == 2, puf == True), 0.5 * _earned, 0)
    c32880 = np.where(
        np.logical_and(MARS == 2, puf == False), np.maximum(0, e32880), c32880)
    c32890 = np.where(
        np.logical_and(MARS == 2, puf == False), np.maximum(0, e32890), c32890)
    c32880 = np.where(MARS != 2, _earned, c32880)
    c32890 = np.where(MARS != 2, _earned, c32890)

    _ncu13 = np.zeros((dim,))
    _ncu13 = np.where(puf == True, f2441, _ncu13)
    _ncu13 = np.where(
        np.logical_and(puf == False, CDOB1 > 0), _ncu13 + 1, _ncu13)
    _ncu13 = np.where(
        np.logical_and(puf == False, CDOB2 > 0), _ncu13 + 1, _ncu13)

    _dclim = np.minimum(_ncu13, 2) * _dcmax[FLPDYR - 2013]
    c32800 = np.minimum(np.maximum(e32800, e32750 + e32775), _dclim)

    outputs = (_earned, c32880, c32890, _ncu13, _dclim, c32800)
    header = ['_earned', 'c32880', 'c32890', '_ncu13', '_dclim', 'c32800']

    return DataFrame(data=np.column_stack(outputs), columns=header), c32800


def DepCareBen(c32800):
    global c33000
    c32800 = c32800
    # Part III ofdependent care benefits
    _seywage = np.where(np.logical_and(_cmp == 1, MARS == 2), np.minimum(
        c32880, np.minimum(c32890, np.minimum(e33420 + e33430 - e33450, e33460))), 0)
    _seywage = np.where(np.logical_and(_cmp == 1, MARS != 2), np.minimum(
        c32880, np.minimum(e33420 + e33430 - e33450, e33460)), _seywage)

    c33465 = np.where(_cmp == 1, e33465, 0)
    c33470 = np.where(_cmp == 1, e33470, 0)
    c33475 = np.where(
        _cmp == 1, np.maximum(0, np.minimum(_seywage, 5000 / _sep) - c33470), 0)
    c33480 = np.where(
        _cmp == 1, np.maximum(0, e33420 + e33430 - e33450 - c33465 - c33475), 0)
    c32840 = np.where(_cmp == 1, c33470 + c33475, 0)
    c32800 = np.where(_cmp == 1, np.minimum(
        np.maximum(0, _dclim - c32840), np.maximum(0, e32750 + e32775 - c32840)), c32800)

    c33000 = np.where(
        MARS == 2, np.maximum(0, np.minimum(c32800, np.minimum(c32880, c32890))), 0)
    c33000 = np.where(
        MARS != 2, np.maximum(0, np.minimum(c32800, _earned)), c33000)

    outputs = (_seywage, c33465, c33470, c33475, c33480, c32840, c32800,
               c33000)
    header = ['_seywage', 'c33465', 'c33470', 'c33475', 'c33480', 'c32840',
              'c32800', 'c33000']

    return DataFrame(data=np.column_stack(outputs),
                     columns=header)


def ExpEarnedInc():
    global c07180
    # Expenses limited to earned income

    _tratio = np.where(_exact == 1, np.ceil(
        np.maximum((c00100 - _agcmax[FLPDYR - 2013]) / 2000, 0)), 0)
    c33200 = np.where(_exact == 1, c33000 * 0.01 * np.maximum(20,
                                                              _pcmax[FLPDYR - 2013] - np.minimum(15, _tratio)), 0)
    c33200 = np.where(_exact != 1, c33000 * 0.01 * np.maximum(20, _pcmax[
                      FLPDYR - 2013] - np.maximum((c00100 - _agcmax[FLPDYR - 2013]) / 2000, 0)), c33200)

    c33400 = np.minimum(np.maximum(0, c05800 - e07300), c33200)
    # amount of the credit

    c07180 = np.where(e07180 == 0, 0, c33400)

    return DataFrame(data=np.column_stack((_tratio, c33200, c33400, c07180)),
                     columns=['_tratio', 'c33200', 'c33400', 'c07180'])

def RateRed(c05800):
    global c59560
    global c07970
    # rate reduction credit for 2001 only, is this needed?
    c05800 = c05800
    c07970 = np.zeros((dim,))

    c05800 = np.where(_fixup >= 3, c05800 + _othtax, c05800)

    c59560 = np.where(_exact == 1, x59560, _earned)

    return DataFrame(data=np.column_stack((c07970, c05800, c59560)),
                     columns=['c07970', 'c05800', 'c59560'])


def NumDep(puf):
    global c59660
    # Number of dependents for EIC

    _ieic = np.zeros((dim,))

    EICYB1_1 = np.where(EICYB1 < 0, 0.0, EICYB1)
    EICYB2_2 = np.where(EICYB2 < 0, 0.0, EICYB2)
    EICYB3_3 = np.where(EICYB3 < 0, 0.0, EICYB3)

    _ieic = np.where(puf == True, EIC, EICYB1_1 + EICYB2_2 + EICYB3_3)

    _ieic = _ieic.astype(int)

    # Modified AGI only through 2002

    _modagi = c00100 + e00400
    c59660 = np.zeros((dim,))

    _val_ymax = np.where(np.logical_and(MARS == 2, _modagi > 0), _ymax[
                         _ieic, FLPDYR - 2013] + _joint[FLPDYR - 2013], 0)
    _val_ymax = np.where(np.logical_and(_modagi > 0, np.logical_or(MARS == 1, np.logical_or(
        MARS == 4, np.logical_or(MARS == 5, MARS == 7)))), _ymax[_ieic, FLPDYR - 2013], _val_ymax)
    c59660 = np.where(np.logical_and(_modagi > 0, np.logical_or(MARS == 1, np.logical_or(MARS == 4, np.logical_or(MARS == 5, np.logical_or(
        MARS == 2, MARS == 7))))), np.minimum(_rtbase[_ieic, FLPDYR - 2013] * c59560, _crmax[_ieic, FLPDYR - 2013]), c59660)
    _preeitc = np.where(np.logical_and(_modagi > 0, np.logical_or(MARS == 1, np.logical_or(
        MARS == 4, np.logical_or(MARS == 5, np.logical_or(MARS == 2, MARS == 7))))), c59660, 0)

    c59660 = np.where(np.logical_and(np.logical_and(MARS != 3, MARS != 6), np.logical_and(_modagi > 0, np.logical_or(
        _modagi > _val_ymax, c59560 > _val_ymax))), np.maximum(0, c59660 - _rtless[_ieic, FLPDYR - 2013] * (np.maximum(_modagi, c59560) - _val_ymax)), c59660)
    _val_rtbase = np.where(np.logical_and(np.logical_and(
        MARS != 3, MARS != 6), _modagi > 0), _rtbase[_ieic, FLPDYR - 2013] * 100, 0)
    _val_rtless = np.where(np.logical_and(np.logical_and(
        MARS != 3, MARS != 6), _modagi > 0), _rtless[_ieic, FLPDYR - 2013] * 100, 0)

    _dy = np.where(np.logical_and(np.logical_and(MARS != 3, MARS != 6), _modagi > 0), e00400 + e83080 + e00300 + e00600
                   +
                   np.maximum(0, np.maximum(0, e01000) - np.maximum(0, e40223))
                   + np.maximum(0, np.maximum(0, e25360) -
                                e25430 - e25470 - e25400 - e25500)
                   + np.maximum(0, e26210 + e26340 + e27200 - np.absolute(e26205) - np.absolute(e26320)), 0)

    c59660 = np.where(np.logical_and(np.logical_and(MARS != 3, MARS != 6), np.logical_and(
        _modagi > 0, _dy > _dylim[FLPDYR - 2013])), 0, c59660)

    c59660 = np.where(np.logical_and(np.logical_and(_cmp == 1, _ieic == 0), np.logical_and(np.logical_and(
        SOIYR - DOBYR >= 25, SOIYR - DOBYR < 65), np.logical_and(SOIYR - SDOBYR >= 25, SOIYR - SDOBYR < 65))), 0, c59660)
    c59660 = np.where(np.logical_and(_ieic == 0, np.logical_or(np.logical_or(
        _agep < 25, _agep >= 65), np.logical_or(_ages < 25, _ages >= 65))), 0, c59660)

    outputs = (_ieic, EICYB1, EICYB2, EICYB3, _modagi, c59660,
               _val_ymax, _preeitc, _val_rtbase, _val_rtless, _dy)
    header = ['_ieic', 'EICYB1', 'EICYB2', 'EICYB3', '_modagi',
              'c59660', '_val_ymax', '_preeitc', '_val_rtbase',
              '_val_rtless', '_dy']

    return DataFrame(data=np.column_stack(outputs), columns=header)

def ChildTaxCredit():
    global _num
    global c07230
    global _precrd
    global _nctcr
    global c07220
    # Child Tax Credit

    c11070 = np.zeros((dim,))
    c07220 = np.zeros((dim,))
    c07230 = np.zeros((dim,))
    _precrd = np.zeros((dim,))

    _num = np.ones((dim,))
    _num = np.where(MARS == 2, 2, _num)

    _nctcr = np.zeros((dim,))
    _nctcr = np.where(SOIYR >= 2002, n24, _nctcr)
    _nctcr = np.where(
        np.logical_and(SOIYR < 2002, _chmax[FLPDYR - 2013] > 0), xtxcr1xtxcr10, _nctcr)
    _nctcr = np.where(
        np.logical_and(SOIYR < 2002, _chmax[FLPDYR - 2013] <= 0), XOCAH, _nctcr)

    _precrd = _chmax[FLPDYR - 2013] * _nctcr
    _ctcagi = c00100 + _feided

    _precrd = np.where(np.logical_and(_ctcagi > _cphase[MARS - 1], _exact == 1), np.maximum(
        0, _precrd - 50 * np.ceil(_ctcagi - _cphase[MARS - 1]) / 1000), _precrd)
    _precrd = np.where(np.logical_and(_ctcagi > _cphase[MARS - 1], _exact != 1), np.maximum(
        0, _precrd - 50 * (np.maximum(0, _ctcagi - _cphase[MARS - 1]) + 500) / 1000), _precrd)

    outputs = (c11070, c07220, c07230, _precrd, _num, _nctcr, _precrd, _ctcagi)
    header = ['c11070', 'c07220', 'c07230', '_precrd', '_num', '_nctcr',
              '_precrd', '_ctcagi']

    return DataFrame(data=np.column_stack(outputs), columns=header)


# def HopeCredit():
    # Hope credit for 1998-2009, I don't think this is needed
    # Leave blank for now, ask Dan
    # SAS lnies 951 - 972


def AmOppCr():
    global c87521
    # American Opportunity Credit 2009+
    c87482 = np.where(_cmp == 1, np.maximum(0, np.minimum(e87482, 4000)), 0)
    c87487 = np.where(_cmp == 1, np.maximum(0, np.minimum(e87487, 4000)), 0)
    c87492 = np.where(_cmp == 1, np.maximum(0, np.minimum(e87492, 4000)), 0)
    c87497 = np.where(_cmp == 1, np.maximum(0, np.minimum(e87497, 4000)), 0)

    c87483 = np.where(np.maximum(0, c87482 - 2000) == 0,
                      c87482, 2000 + 0.25 * np.maximum(0, c87482 - 2000))
    c87488 = np.where(np.maximum(0, c87487 - 2000) == 0,
                      c87487, 2000 + 0.25 * np.maximum(0, c87487 - 2000))
    c87493 = np.where(np.maximum(0, c87492 - 2000) == 0,
                      c87492, 2000 + 0.25 * np.maximum(0, c87492 - 2000))
    c87498 = np.where(np.maximum(0, c87497 - 2000) == 0,
                      c87497, 2000 + 0.25 * np.maximum(0, c87497 - 2000))

    c87521 = c87483 + c87488 + c87493 + c87498

    outputs = (c87482, c87487, c87492, c87497,
               c87483, c87488, c87493, c87498, c87521)
    header = ['c87482', 'c87487', 'c87492', 'c87497', 'c87483', 'c87488',
              'c87493', 'c87498', 'c87521']

    return DataFrame(data=np.column_stack(outputs), columns=header)


def LLC(puf):
    # Lifetime Learning Credit
    global c87550

    c87540 = np.where(
        puf == True, np.minimum(e87530, _learn[FLPDYR - 2013]), 0)
    c87550 = np.where(puf == True, 0.2 * c87540, 0)

    c87530 = np.where(puf == False, e87526 + e87522 + e87524 + e87528, 0)
    c87540 = np.where(
        puf == False, np.minimum(c87530, _learn[FLPDYR - 2013]), c87540)
    c87550 = np.where(puf == False, 0.2 * c87540, c87550)

    outputs = (c87540, c87550, c87530)
    header = ['c87540', 'c87550', 'c87530']
    return DataFrame(data=np.column_stack(outputs), columns=header), c87550


def RefAmOpp():
    # Refundable American Opportunity Credit 2009+

    c87668 = np.zeros((dim,))

    c87654 = np.where(np.logical_and(_cmp == 1, c87521 > 0), 90000 * _num, 0)
    c87656 = np.where(np.logical_and(_cmp == 1, c87521 > 0), c00100, 0)
    c87658 = np.where(
        np.logical_and(_cmp == 1, c87521 > 0), np.maximum(0, c87654 - c87656), 0)
    c87660 = np.where(np.logical_and(_cmp == 1, c87521 > 0), 10000 * _num, 0)
    c87662 = np.where(np.logical_and(_cmp == 1, c87521 > 0),
                      1000 * np.minimum(1, c87658 / c87660), 0)
    c87664 = np.where(
        np.logical_and(_cmp == 1, c87521 > 0), c87662 * c87521 / 1000, 0)
    c87666 = np.where(np.logical_and(
        _cmp == 1, np.logical_and(c87521 > 0, EDCRAGE == 1)), 0, 0.4 * c87664)
    c10960 = np.where(np.logical_and(_cmp == 1, c87521 > 0), c87666, 0)
    c87668 = np.where(
        np.logical_and(_cmp == 1, c87521 > 0), c87664 - c87666, 0)
    c87681 = np.where(np.logical_and(_cmp == 1, c87521 > 0), c87666, 0)

    outputs = (c87654, c87656, c87658, c87660, c87662,
               c87664, c87666, c10960, c87668, c87681)
    header = ['c87654', 'c87656', 'c87658', 'c87660', 'c87662', 'c87664',
              'c87666', 'c10960', 'c87668', 'c87681']
    return DataFrame(data=np.column_stack(outputs), columns=header)


def NonEdCr(c87550):
    global c07220
    # Nonrefundable Education Credits

    # Form 8863 Tentative Education Credits
    c87560 = c87550

    # Phase Out
    c87570 = np.where(
        MARS == 2, _edphhm[FLPDYR - 2013] * 1000, _edphhs[FLPDYR - 2013] * 1000)
    c87580 = c00100
    c87590 = np.maximum(0, c87570 - c87580)
    c87600 = 10000 * _num
    c87610 = np.minimum(1, c87590 / c87600)
    c87620 = c87560 * c87610

    _ctc1 = c07180 + e07200 + c07230
    _ctc2 = np.zeros((dim,))

    _ctc2 = e07240 + e07960 + e07260 + e07300
    _regcrd = _ctc1 + _ctc2
    _exocrd = e07700 + e07250
    _exocrd = _exocrd + t07950
    _ctctax = c05800 - _regcrd - _exocrd
    c07220 = np.minimum(_precrd, np.maximum(0, _ctctax))
    # lt tax owed

    outputs = (c87560, c87570, c87580, c87590, c87600, c87610,
               c87620, _ctc1, _ctc2, _regcrd, _exocrd, _ctctax, c07220)
    header = ['c87560', 'c87570', 'c87580', 'c87590', 'c87600', 'c87610',
              'c87620', '_ctc1', '_ctc2', '_regcrd', '_exocrd', '_ctctax',
              'c07220']
    return DataFrame(data=np.column_stack(outputs), columns=header)


def AddCTC(puf):
    # Additional Child Tax Credit

    c82940 = np.zeros((dim,))

    # Part I of 2005 form 8812
    c82925 = np.where(_nctcr > 0, _precrd, 0)
    c82930 = np.where(_nctcr > 0, c07220, 0)
    c82935 = np.where(_nctcr > 0, c82925 - c82930, 0)
    # CTC not applied to tax

    c82880 = np.where(_nctcr > 0, np.maximum(
        0, e00200 + e82882 + e30100 + np.maximum(0, _sey) - 0.5 * _setax), 0)
    c82880 = np.where(np.logical_and(_nctcr > 0, _exact == 1), e82880, c82880)
    h82880 = np.where(_nctcr > 0, c82880, 0)
    c82885 = np.where(
        _nctcr > 0, np.maximum(0, c82880 - _ealim[FLPDYR - 2013]), 0)
    c82890 = np.where(_nctcr > 0, _adctcrt[FLPDYR - 2013] * c82885, 0)

    # Part II of 2005 form 8812
    c82900 = np.where(np.logical_and(_nctcr > 2, c82890 < c82935),
                      0.0765 * np.minimum(_ssmax[FLPDYR - 2013], c82880), 0)
    c82905 = np.where(
        np.logical_and(_nctcr > 2, c82890 < c82935), e03260 + e09800, 0)
    c82910 = np.where(
        np.logical_and(_nctcr > 2, c82890 < c82935), c82900 + c82905, 0)
    c82915 = np.where(
        np.logical_and(_nctcr > 2, c82890 < c82935), c59660 + e11200, 0)
    c82920 = np.where(
        np.logical_and(_nctcr > 2, c82890 < c82935), np.maximum(0, c82910 - c82915), 0)
    c82937 = np.where(
        np.logical_and(_nctcr > 2, c82890 < c82935), np.maximum(c82890, c82920), 0)

    # Part II of 2005 form 8812
    c82940 = np.where(
        np.logical_and(_nctcr > 2, c82890 >= c82935), c82935, c82940)
    c82940 = np.where(
        np.logical_and(_nctcr > 2, c82890 < c82935), np.minimum(c82935, c82937), c82940)

    c11070 = np.where(_nctcr > 0, c82940, 0)

    e59660 = np.where(
        np.logical_and(puf == True, _nctcr > 0), e59680 + e59700 + e59720, 0)
    _othadd = np.where(_nctcr > 0, e11070 - c11070, 0)

    c11070 = np.where(
        np.logical_and(_nctcr > 0, _fixup >= 4), c11070 + _othadd, c11070)

    outputs = (c82940, c82925, c82930, c82935, c82880, h82880, c82885, c82890,
               c82900, c82905, c82910, c82915, c82920, c82937, c82940, c11070,
               e59660, _othadd)

    header = ['c82940', 'c82925', 'c82930', 'c82935', 'c82880', 'h82880',
              'c82885', 'c82890', 'c82900', 'c82905', 'c82910', 'c82915',
              'c82920', 'c82937', 'c82940', 'c11070', 'e59660', '_othadd']

    return DataFrame(data=np.column_stack(outputs), columns=header)


def F5405():
    # Form 5405 First-Time Homebuyer Credit
    #not needed

    c64450 = np.zeros((dim,))
    return DataFrame(data=np.column_stack((c64450,)), columns=['c64450'])

def C1040(puf):
    global c08795
    global c09200
    global c07100
    global _eitc
    # Credits 1040 line 48

    x07400 = e07400
    c07100 = (e07180 + e07200 + c07220 + c07230 + e07250
              + e07600 + e07260 + c07970 + e07300 + x07400
              + e07500 + e07700 + e08000)

    y07100 = c07100

    c07100 = c07100 + e07240
    c07100 = c07100 + e08001
    c07100 = c07100 + e07960 + e07970
    c07100 = np.where(SOIYR >= 2009, c07100 + e07980, c07100)

    x07100 = c07100
    c07100 = np.minimum(c07100, c05800)

    # Tax After credits 1040 line 52

    _eitc = c59660
    c08795 = np.maximum(0, c05800 - c07100)

    c08800 = c08795
    e08795 = np.where(puf == True, e08800, 0)

    # Tax before refundable credits

    c09200 = c08795 + e09900 + e09400 + e09800 + e10000 + e10100
    c09200 = c09200 + e09700
    c09200 = c09200 + e10050
    c09200 = c09200 + e10075
    c09200 = c09200 + e09805
    c09200 = c09200 + e09710 + e09720

    outputs = (c07100, y07100, x07100, c08795, c08800, e08795, c09200)
    header = ['c07100', 'y07100', 'x07100', 'c08795', 'c08800', 'e08795',
              'c09200']
    return DataFrame(data=np.column_stack(outputs), columns=header), _eitc


def DEITC():
    global c59700
    global c10950
    # Decomposition of EITC

    c59680 = np.where(np.logical_and(
        c08795 > 0, np.logical_and(c59660 > 0, c08795 <= c59660)), c08795, 0)
    _comb = np.where(np.logical_and(
        c08795 > 0, np.logical_and(c59660 > 0, c08795 <= c59660)), c59660 - c59680, 0)

    c59680 = np.where(np.logical_and(
        c08795 > 0, np.logical_and(c59660 > 0, c08795 > c59660)), c59660, c59680)
    _comb = np.where(np.logical_and(
        c08795 > 0, np.logical_and(c59660 > 0, c08795 > c59660)), 0, _comb)

    c59700 = np.where(np.logical_and(c08795 > 0, np.logical_and(c59660 > 0, np.logical_and(
        _comb > 0, np.logical_and(c09200 - c08795 > 0, c09200 - c08795 > _comb)))), _comb, 0)
    c59700 = np.where(np.logical_and(c08795 > 0, np.logical_and(c59660 > 0, np.logical_and(
        _comb > 0, np.logical_and(c09200 - c08795 > 0, c09200 - c08795 <= _comb)))), c09200 - c08795, c59700)
    c59720 = np.where(np.logical_and(c08795 > 0, np.logical_and(c59660 > 0, np.logical_and(
        _comb > 0, np.logical_and(c09200 - c08795 > 0, c09200 - c08795 <= _comb)))), c59660 - c59680 - c59700, 0)

    c59680 = np.where(np.logical_and(c08795 == 0, c59660 > 0), 0, c59680)
    c59700 = np.where(np.logical_and(c08795 == 0, np.logical_and(
        c59660 > 0, np.logical_and(c09200 > 0, c09200 > c59660))), c59660, c59700)
    c59700 = np.where(np.logical_and(c08795 == 0, np.logical_and(
        c59660 > 0, np.logical_and(c09200 > 0, c09200 < c59660))), c09200, c59700)
    c59720 = np.where(np.logical_and(c08795 == 0, np.logical_and(
        c59660 > 0, np.logical_and(c09200 > 0, c09200 < c59660))), c59660 - c59700, c59720)
    c59720 = np.where(np.logical_and(
        c08795 == 0, np.logical_and(c59660 > 0, c09200 <= 0)), c59660 - c59700, c59720)

    # Ask dan about this section of code! Line 1231 - 1241

    _compb = np.where(np.logical_or(c08795 < 0, c59660 <= 0), 0, 0)
    c59680 = np.where(np.logical_or(c08795 < 0, c59660 <= 0), 0, c59680)
    c59700 = np.where(np.logical_or(c08795 < 0, c59660 <= 0), 0, c59700)
    c59720 = np.where(np.logical_or(c08795 < 0, c59660 <= 0), 0, c59720)

    c07150 = c07100 + c59680
    c07150 = c07150 
    c10950 = np.zeros((dim,))

    outputs = (c59680, c59700, c59720, _comb, c07150, c10950)
    header = ['c59680', 'c59700', 'c59720', '_comb', 'c07150', 'c10950']

    return DataFrame(data=np.column_stack(outputs), columns=header)


def SOIT(_eitc):
    _eitc = _eitc

    # SOI Tax (Tax after non-refunded credits plus tip penalty)
    c10300 = c09200 - e10000 - e59680 - c59700
    c10300 = c10300 - e11070
    c10300 = c10300 - e11550
    c10300 = c10300 - e11580
    c10300 = c10300 - e09710 - e09720 - e11581 - e11582
    c10300 = c10300 - e87900 - e87905 - e87681 - e87682
    c10300 = c10300 - c10300 - c10950 - e11451 - e11452
    c10300 = c09200 - e09710 - e09720 - e10000 - e11601 - e11602
    c10300 = np.maximum(c10300, 0)

    # Ignore refundable partof _eitc to obtain SOI income tax

    _eitc = np.where(c09200 <= _eitc, c09200, _eitc)
    c10300 = np.where(c09200 <= _eitc, 0, c10300)

    outputs = (c10300, _eitc)
    header = ['c10300', '_eitc']
    return DataFrame(data=np.column_stack(outputs), columns=header)


def Taxer(inc_in, inc_out, MARS):
    low = np.where(inc_in < 3000, 1, 0)
    med = np.where(np.logical_and(inc_in >= 3000, inc_in < 100000), 1, 0)

    _a1 = inc_in * 0.01
    _a2 = np.floor(_a1)
    _a3 = _a2 * 100
    _a4 = (_a1 - _a2) * 100

    _a5 = np.zeros((dim,))
    _a5 = np.where(np.logical_and(low == 1, _a4 < 25), 13, _a5)
    _a5 = np.where(
        np.logical_and(low == 1, np.logical_and(_a4 >= 25, _a4 < 50)), 38, _a5)
    _a5 = np.where(
        np.logical_and(low == 1, np.logical_and(_a4 >= 50, _a4 < 75)), 63, _a5)
    _a5 = np.where(np.logical_and(low == 1, _a4 >= 75), 88, _a5)

    _a5 = np.where(np.logical_and(med == 1, _a4 < 50), 25, _a5)
    _a5 = np.where(np.logical_and(med == 1, _a4 >= 50), 75, _a5)

    _a5 = np.where(inc_in == 0, 0, _a5)

    _a6 = np.where(np.logical_or(low == 1, med == 1), _a3 + _a5, inc_in)

    _a6 = inc_in

    inc_out = (_rt1[FLPDYR - 2013] * np.minimum(_a6, _brk1[FLPDYR - 2013, MARS - 1])
               + _rt2[FLPDYR - 2013]
               * np.minimum(_brk2[FLPDYR - 2013, MARS - 1] - _brk1[FLPDYR - 2013, MARS - 1],
                            np.maximum(0., _a6 - _brk1[FLPDYR - 2013, MARS - 1]))
               + _rt3[FLPDYR - 2013]
               * np.minimum(_brk3[FLPDYR - 2013, MARS - 1] - _brk2[FLPDYR - 2013, MARS - 1],
                            np.maximum(0., _a6 - _brk2[FLPDYR - 2013, MARS - 1]))
               + _rt4[FLPDYR - 2013]
               * np.minimum(_brk4[FLPDYR - 2013, MARS - 1] - _brk3[FLPDYR - 2013, MARS - 1],
                            np.maximum(0., _a6 - _brk3[FLPDYR - 2013, MARS - 1]))
               + _rt5[FLPDYR - 2013]
               * np.minimum(_brk5[FLPDYR - 2013, MARS - 1] - _brk4[FLPDYR - 2013, MARS - 1],
                            np.maximum(0., _a6 - _brk4[FLPDYR - 2013, MARS - 1]))
               + _rt6[FLPDYR - 2013]
               * np.minimum(_brk6[FLPDYR - 2013, MARS - 1] - _brk5[FLPDYR - 2013, MARS - 1],
                            np.maximum(0., _a6 - _brk5[FLPDYR - 2013, MARS - 1]))
               + _rt7[FLPDYR - 2013] * np.maximum(0., _a6 - _brk6[FLPDYR - 2013, MARS - 1]))

    return inc_out



