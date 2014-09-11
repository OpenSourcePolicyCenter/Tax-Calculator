import pandas as pd
import math
import numpy as np

output_filename = 'translationoutput.csv'

from puf_2_picle import unpicle
puf_dict = unpicle('test/y2.pickle')

# This should be dealt with so that we don't keep referencing the same array
# simply find all uses of this and figure out if they're called for (mostly not)
DIMARRAY = np.zeros((139651,))

<<<<<<< HEAD
y = {}
for n in namesCap:
	y[n] = np.array(x[str.lower(n)])
 
locals().update(y)

AGIR1 = agir1
MIdR = MIDR



_adctcrt = np.array([0.15])
 #Rate for additional ctc

_aged = np.array([[1500],[1200]]) 
#Extra std. ded. for aged

_almdep = np.array([6950]) 
#Child AMT Exclusion base

_almsp = np.array([179500]) 
#AMT bracket

_amex = np.array([3900]) 
#Personal Exemption

_amtage = np.array([24]) 
#Age for full AMT exclusion

_amtsep = np.array([232500]) 
#AMT Exclusion

_almsep = np.array([39375]) 
#Extra alminc for married sep

_agcmax = np.array([15000]) 
#??

_cgrate1 = np.array([0.10]) 
#Initial rate on long term gains

_cgrate2 = np.array([0.20]) 
#Normal rate on long term gains

_chmax = np.array([1000]) 
#Max Child Tax Credit per child 

_crmax = np.array([[487],[3250],[5372],[6044]]) 
#Max earned income credit

_dcmax = np.array([3000]) 
#Max dependent care expenses 

_dylim = np.array([3300]) 
#Limits for Disqualified Income

_ealim = np.array([3000]) 
#Max earn ACTC

_edphhs = np.array([63]) 
#End of educ phaseout - singles
=======
>>>>>>> 895f5863d50db2a04fa6872c0d66355c11140c20

AGIR1 = puf_dict['agir1']
MIdR = puf_dict['MIDR']


# import our special function for reading planX and planY (see json_io for details)
import json_io

planX = json_io.read_plans('test/planX.json')

<<<<<<< HEAD
_learn = np.array([10000]) 
#Expense limit for the LLC

_pcmax = np.array([35]) 
#Maximum Percentage for f2441

_phase = np.array([172250]) 
#Phase out for itemized

_rtbase = np.array([[0.0765], [0.3400], [0.4000], [0.4000]]) 
#EIC base rate

_rtless = np.array([[0.0765], [0.1598], [0.2106], [0.2106]]) 
#EIC _phaseout rate

_ssmax = np.array([115800]) 
#SS Maximum taxable earnings

_ymax = np.array([[7970], [17530], [17530], [17530]]) 
#Start of EIC _phaseout

_rt1 = np.array([0.1]) 
#10% rate

_rt2 = np.array([0.15]) 
#15% rate

_rt3 = np.array([0.25]) 
#25% rate

_rt4 = np.array([0.28]) 
#28% rate

_rt5 = np.array([0.33]) 
#33% rate

_rt6 = np.array([0.35]) 
#35% rate

_rt7 = np.array([0.396]) 
#39.6% rate

_amtys = np.array([112500, 150000, 75000, 112500, 150000, 75000]) 
#AMT Phaseout Start

_cphase = np.array([75000, 110000, 55000, 75000, 75000, 55000]) 
#Child Tax Credit Phase-Out

_thresx = np.array([200000, 250000, 125000, 200000, 250000, 125000]) 
#Threshold for add medicare

_ssb50 = np.array([25000, 32000, 0, 25000, 25000, 0]) 
#SS 50% taxability threshold

_ssb85 = np.array([34000, 44000, 0, 34000, 34000, 0]) 
#SS 85% taxability threshold 

_amtex = np.array([[51900, 80750, 40375, 51900, 80750, 40375], 
	[0, 0, 0, 0, 0, 0]]) 
#AMT Exclusion

_exmpb = np.array([[200000, 300000, 150000, 250000, 300000, 150000], 
	[0, 0, 0, 0, 0, 0]]) 
#Personal Exemption Amount 

_stded = np.array([[6100, 12200, 6100, 8950, 12200, 6100, 1000], 
	[0, 0, 0, 0, 0, 0, 0]])
 #Standard Deduction

_brk1 = np.array([[8925, 17850, 8925, 12750, 17850, 8925], 
	[0, 0, 0, 0, 0, 0]]) 
#10% tax rate thresholds

_brk2 = np.array([[36250, 72500, 36250, 48600, 72500, 36250], 
	[0, 0, 0, 0, 0, 0]])
 #15% tax rate thresholds

_brk3 = np.array([[87850, 146400, 73200, 125450, 146400, 73200], 
	[0, 0, 0, 0, 0, 0]]) 
#25% tax rate thresholds

_brk4 = np.array([[183250, 223050, 111525, 203150, 223050, 111525], 
	[0, 0, 0, 0, 0, 0]]) 
#28% tax rate thresholds

_brk5 = np.array([[398350, 398350, 199175, 398350, 398350, 199175], 
	[0, 0, 0, 0, 0, 0]]) 
#33% tax rate thresholds

_brk6 = np.array([[400000, 450000, 225000, 425000, 450000, 225000], 
	[0, 0, 0, 0, 0, 0]]) 
#25% tax rate thresholds


def Puf(): 
#Run this function data input is the PUF file
	
	global e35300_0 
	e35300_0 = np.zeros((dim,))
	global e35600_0 
	e35600_0 = np.zeros((dim,))
	global e35910_0 
	e35910_0 = np.zeros((dim,))
	global x03150 
	x03150 = np.zeros((dim,))
	global e03600 
	e03600 = np.zeros((dim,))
	global e03280 
	e03280 = np.zeros((dim,))
	global e03900 
	e03900 = np.zeros((dim,))
	global e04000 
	e04000 = np.zeros((dim,))
	global e03700 
	e03700 = np.zeros((dim,))
	global c23250 
	c23250 = np.zeros((dim,))
	global e22250 
	e22250 = np.zeros((dim,))
	global e23660 
	e23660 = np.zeros((dim,))
	global f2555 
	f2555 = np.zeros((dim,))
	global e02800 
	e02800 = np.zeros((dim,))
	global e02610 
	e02610 = np.zeros((dim,))
	global e02540 
	e02540 = np.zeros((dim,))
	global e02615 
	e02615 = np.zeros((dim,))
	global SSIND 
	SSIND = np.zeros((dim,))
	global e18400 
	e18400 = np.zeros((dim,))
	global e18800 
	e18800 = np.zeros((dim,))
	global e18900 
	e18900 = np.zeros((dim,))
	global e20950
	e20950 = np.zeros((dim,))
	global e19500 
	e19500 = np.zeros((dim,))
	global e19570 
	e19570 = np.zeros((dim,))
	global e19400 
	e19400 = np.zeros((dim,))
	global c20400
	c20400 = np.zeros((dim,))
	global e20200
	e20200 = np.zeros((dim,))
	global e20900 
	e20900 = np.zeros((dim,))
	global e21000 
	e21000 = np.zeros((dim,))
	global e21010 
	e21010 = np.zeros((dim,))
	global e02600
	e02600 = np.zeros((dim,))
	global _exact 
	_exact = np.zeros((dim,))
	global e11055
	e11055 = np.zeros((dim,))
	global e00250
	e00250 = np.zeros((dim,))
	global e30100
	e30100 = np.zeros((dim,))
	global _compitem 
	_compitem = np.zeros((dim,))
	global e15360
	e15360 = np.zeros((dim,))
	global e04200
	e04200 = np.zeros((dim,))
	global e04470
	e04470 = np.zeros((dim,))
	global e37717
	e37717 = np.zeros((dim,))
	global e04805
	e04805 = np.zeros((dim,))
	global AGEP 
	AGEP = np.zeros((dim,))
	global AGES
	AGES = np.zeros((dim,))
	global PBI 
	PBI = np.zeros((dim,))
	global SBI 
	SBI = np.zeros((dim,))
	global t04470 
	t04470 = np.zeros((dim,))
	global e23250
	e23250 = np.zeros((dim,))
	global e58980
	e58980 = np.zeros((dim,))
	global c00650
	c00650 = np.zeros((dim,))
	global e24583
	e24583 = np.zeros((dim,))
	global _fixup
	_fixup = np.zeros((dim,))
	global _cmp 
	_cmp = np.zeros((dim,))
	global e59440 
	e59440 = np.zeros((dim,))
	global e59470
	e59470 = np.zeros((dim,))
	global e59400
	e59400 = np.zeros((dim,))
	global e10105
	e10105 = np.zeros((dim,))
	global e83200_0
	e83200_0 = np.zeros((dim,))
	global e59410 
	e59410 = np.zeros((dim,))
	global e59420 
	e59420 = np.zeros((dim,))
	global e74400 
	e74400 = np.zeros((dim,))
	global x62720 
	x62720  = np.zeros((dim,))
	global x60260
	x60260 = np.zeros((dim,))
	global x60240
	x60240 = np.zeros((dim,))
	global x60220
	x60220 = np.zeros((dim,))
	global x60130 
	x60130 = np.zeros((dim,))
	global x62730
	x62730 = np.zeros((dim,))
	global e60290
	e60290 = np.zeros((dim,))
	global DOBYR 
	DOBYR = np.zeros((dim,))
	global SDOBYR
	SDOBYR = np.zeros((dim,))
	global DOBMD 
	DOBMD = np.zeros((dim,))
	global SDOBMD
	SDOBMD = np.zeros((dim,))
	global e62600
	e62600 = np.zeros((dim,))
	global x62740
	x62740 = np.zeros((dim,))
	global _fixeic
	_fixeic = np.zeros((dim,))
	global e32880 
	e32880 = np.zeros((dim,))
	global e32890
	e32890 = np.zeros((dim,))
	global CDOB1 
	CDOB1 = np.zeros((dim,))
	global CDOB2 
	CDOB2 = np.zeros((dim,))	
	global e32750 
	e32750 = np.zeros((dim,))
	global e32775
	e32775 = np.zeros((dim,))
	global e33420 
	e33420 = np.zeros((dim,))
	global e33430 
	e33430 = np.zeros((dim,))
	global e33450
	e33450 = np.zeros((dim,))
	global e33460 
	e33460 = np.zeros((dim,))
	global e33465
	e33465 = np.zeros((dim,))
	global e33470 
	e33470 = np.zeros((dim,))
	global x59560
	x59560 = np.zeros((dim,))
	global EICYB1 
	EICYB1 = np.zeros((dim,))
	global EICYB2 
	EICYB2 = np.zeros((dim,))
	global EICYB3
	EICYB3 = np.zeros((dim,))
	global e83080
	e83080 = np.zeros((dim,))
	global e25360
	e25360 = np.zeros((dim,))
	global e25430 
	e25430 = np.zeros((dim,))
	global e25470 
	e25470 = np.zeros((dim,))
	global e25400 
	e25400 = np.zeros((dim,))
	global e25500 
	e25500 = np.zeros((dim,))
	global e26210 
	e26210 = np.zeros((dim,))
	global e26340 
	e26340 = np.zeros((dim,))
	global e26205 
	e26205 = np.zeros((dim,))
	global e26320 
	e26320 = np.zeros((dim,))
	global e87482 
	e87482 = np.zeros((dim,))
	global e87487
	e87487 = np.zeros((dim,))
	global e87492
	e87492 = np.zeros((dim,))
	global e87497
	e87497 = np.zeros((dim,))
	global e87526
	e87526 = np.zeros((dim,))
	global e87522 
	e87522 = np.zeros((dim,))
	global e87524 
	e87524 = np.zeros((dim,))
	global e87528
	e87528 = np.zeros((dim,))
	global EDCRAGE 
	EDCRAGE = np.zeros((dim,))
	global e07960
	e07960 = np.zeros((dim,))
	global e07700 
	e07700 = np.zeros((dim,))
	global e07250 
	e07250 = np.zeros((dim,))
	global t07950
	t07950 = np.zeros((dim,))
	global e82882
	e82882 = np.zeros((dim,))
	global e82880
	e82880 = np.zeros((dim,))
	global e07500 
	e07500 = np.zeros((dim,))
	global e08000 
	e08000 = np.zeros((dim,))
	global e08001
	e08001 = np.zeros((dim,))
	global e07970 
	e07970 = np.zeros((dim,))
	global e07980 
	e07980 = np.zeros((dim,))
	global e10000
	e10000 = np.zeros((dim,))
	global e10100 
	e10100 = np.zeros((dim,))
	global e10050
	e10050 = np.zeros((dim,))
	global e10075
	e10075 = np.zeros((dim,))
	global e09805 
	e09805 = np.zeros((dim,))
	global e09710 
	e09710 = np.zeros((dim,))
	global e09720
	e09720 = np.zeros((dim,))
	global e87900 
	e87900 = np.zeros((dim,))
	global e87905
	e87905 = np.zeros((dim,))
	global e87681
	e87681 = np.zeros((dim,))
	global e87682 
	e87682 = np.zeros((dim,))
	global e11451 
	e11451 = np.zeros((dim,))
	global e11452 
	e11452 = np.zeros((dim,))
	global e11601
	e11601 = np.zeros((dim,))
	global e11602
	e11602 = np.zeros((dim,))
	global e60300
	e60300 = np.zeros((dim,))
	global e60860
	e60860 = np.zeros((dim,))
	global e60100
	e60100 = np.zeros((dim,))
	global e60840
	e60840 = np.zeros((dim,))
	global e60630
	e60630 = np.zeros((dim,))
	global e60550
	e60550 = np.zeros((dim,))
	global e60720 
	e60720 = np.zeros((dim,))
	global e60430
	e60430 = np.zeros((dim,))
	global e60500 
	e60500 = np.zeros((dim,))
	global e60340
	e60340 = np.zeros((dim,))
	global e60680
	e60680 = np.zeros((dim,))
	global e60600
	e60600 = np.zeros((dim,))
	global e60405
	e60405 = np.zeros((dim,))
	global e60440
	e60440 = np.zeros((dim,))
	global e60420 
	e60420 = np.zeros((dim,))
	global e60410
	e60410 = np.zeros((dim,))
	global e61400 
	e61400 = np.zeros((dim,))
	global e60660
	e60660 = np.zeros((dim,))
	global e60480 
	e60480 = np.zeros((dim,))
	global e62000
	e62000 = np.zeros((dim,))
	global e60250
	e60250 = np.zeros((dim,))
	global e40223
	e40223 = np.zeros((dim,))
	global SOIYR
	SOIYR = np.zeros((dim,))
	global xtxcr1xtxcr10
	xtxcr1xtxcr10 = np.zeros((dim,))
=======
>>>>>>> 895f5863d50db2a04fa6872c0d66355c11140c20

def Puf(master_puf, dim_key='PUF DIM'):
    # dim = len(master_puf)
    with open('test/zeros.json') as defaults_file:
        default_var_names = json_io.load(defaults_file)
    dim = master_puf[dim_key]
    default_var_dict = dict((var, np.zeros((dim,))) 
        for var in default_var_names)
    # return dict(master_puf, **default_var_dict)
    master_puf.update(default_var_dict)
    


def FilingStatus():
    #Filing based on marital status
    global _sep
    global _txp
    _sep = np.where(np.logical_or(puf_dict['MARS'] == 3, puf_dict['MARS'] == 6), 2, 1)
    _txp = np.where(np.logical_or(puf_dict['MARS'] == 2, puf_dict['MARS'] == 5), 2, 1)

	outputs = (_sep, _txp)
	output = np.column_stack(outputs)
	np.savetxt('FilingStatus.csv', output, delimiter=',', 
		header = ('_sep, _txp') 
		, fmt = '%1.3f')


def Adj(): 
<<<<<<< HEAD
	#Adjustments
	global _feided 
	global c02900
	_feided = np.maximum(e35300_0, e35600_0, + e35910_0) #Form 2555

	x03150 = e03150
	c02900 = (x03150 + e03210 + e03600 + e03260 + e03270 + e03300 
		+ e03400 + e03500 + e03280 + e03900 + e04000 + e03700 
		+ e03220 + e03230
		+ e03240
		+ e03290)
	x02900 = c02900
=======
    #Adjustments
    global _feided 
    global c02900
    _feided = np.maximum(puf_dict['e35300_0'], puf_dict['e35600_0'], + puf_dict['e35910_0']) #Form 2555
    c02900 = (puf_dict['e03210'] + puf_dict['e03260'] + puf_dict['e03270'] + puf_dict['e03300'] + puf_dict['e03400'] + puf_dict['e03500'] + puf_dict['e03220'] 
    + puf_dict['e03230'] + puf_dict['e03240'] + puf_dict['e03290'] + puf_dict['x03150'] + puf_dict['e03600'] + puf_dict['e03280'] + puf_dict['e03900'] + puf_dict['e04000'] 
    + puf_dict['e03700']) 
    x02900 = c02900
>>>>>>> 895f5863d50db2a04fa6872c0d66355c11140c20

	outputs = (_feided, c02900)
	output = np.column_stack(outputs)
	np.savetxt('Adj.csv', output, delimiter=',', 
		header = ('_feided, c02900') 
		, fmt = '%1.3f')


def CapGains():
<<<<<<< HEAD
	#Capital Gains
	global _ymod
	global _ymod1
	global c02700
	global c23650
	global c01000
	c23650 = c23250 + e22250 + e23660 
	c01000 = np.maximum(-3000/_sep, c23650)
	c02700 = np.minimum(_feided, _feimax[2013-FLPDYR] * f2555) 
	_ymod1 = (e00200 + e00300 + e00600 + e00700 + e00800 + e00900 + c01000 
		+ e01100 + e01200 + e01400 + e01700 + e02000 + e02100 + e02300 + e02600 
		+ e02610 + e02800 - e02540)
	_ymod2 = e00400 + (0.50 * e02400) - c02900
	_ymod3 = e03210 + e03230 + e03240 + e02615
	_ymod = _ymod1 + _ymod2 + _ymod3
=======
    #Capital Gains
    global _ymod
    global _ymod1
    global c02700
    global c23650
    global c01000
    c23650 = puf_dict['c23250'] + puf_dict['e22250'] + puf_dict['e23660'] 
    c01000 = np.maximum(-3000/_sep, c23650)
    c02700 = np.minimum(_feided, planX['feimax'][2013-puf_dict['FLPDYR']] * puf_dict['f2555']) 
    _ymod1 = (puf_dict['e00200'] + puf_dict['e00300'] + puf_dict['e00600'] + puf_dict['e00700'] + puf_dict['e00800'] + puf_dict['e00900'] + c01000 
        + puf_dict['e01100'] + puf_dict['e01200'] + puf_dict['e01400'] + puf_dict['e01700'] + puf_dict['e02000'] + puf_dict['e02100'] + puf_dict['e02300'] + puf_dict['e02600'] 
        + puf_dict['e02610'] + puf_dict['e02800'] - puf_dict['e02540'])
    _ymod2 = puf_dict['e00400'] + puf_dict['e02400']/2 - c02900
    _ymod3 = puf_dict['e03210'] + puf_dict['e03230'] + puf_dict['e03240'] + puf_dict['e02615']
    _ymod = _ymod1 + _ymod2 + _ymod3
>>>>>>> 895f5863d50db2a04fa6872c0d66355c11140c20

	outputs = (c23650, c01000, c02700, _ymod1, _ymod2, _ymod3, _ymod)
	output = np.column_stack(outputs)
	np.savetxt('CapGains.csv', output, delimiter=',', 
		header = ('c23650, c01000, c02700, _ymod1, _ymod2, _ymod3, _ymod') 
		, fmt = '%1.3f')	


def SSBenefits():
<<<<<<< HEAD
	#Social Security Benefit Taxation
	global c02500	
	c02500 = np.where(np.logical_or(SSIND != 0, np.logical_or(MARS == 3, MARS == 6)), e02500, 
		np.where(_ymod < _ssb50[MARS-1], 0, 
			np.where(np.logical_and(_ymod >= _ssb50[MARS-1], _ymod < _ssb85[MARS-1]), 0.5 * np.minimum(_ymod - _ssb50[MARS-1], e02400),
				np.minimum(0.85 * (_ymod - _ssb85[MARS-1]) + 0.50 * np.minimum(e02400, _ssb85[MARS-1] - _ssb50[MARS-1]), 0.85 * e02400
					))))

	outputs = (c02500, e02500)
	output = np.column_stack(outputs)
	np.savetxt('SSBenefits.csv', output, delimiter=',', 
		header = ('c02500, e02500') 
		, fmt = '%1.3f')


=======
    #Social Security Benefit Taxation
    global c02500   
    c02500 = np.where(np.logical_or(puf_dict['SSIND'] != 0, 
        np.logical_and(puf_dict['MARS'] >= 3, puf_dict['MARS'] <= 6)), puf_dict['e02500'], 
        np.where(_ymod < planX['ssb50'][puf_dict['MARS']-1], 0, 
            np.where(np.logical_and(_ymod >= planX['ssb50'][puf_dict['MARS']-1], 
                _ymod < planX['ssb85'][puf_dict['MARS']-1]), 
                0.5 * np.minimum(_ymod - planX['ssb50'][puf_dict['MARS']-1], puf_dict['e02400']), 
                np.minimum(0.85 * (_ymod - planX['ssb85'][puf_dict['MARS']-1]) + 0.50 * 
                    np.minimum(puf_dict['e02400'], planX['ssb85'][puf_dict['MARS']-1] - planX['ssb50'][puf_dict['MARS']-1]), 
                    0.85 * puf_dict['e02400'])))) 
>>>>>>> 895f5863d50db2a04fa6872c0d66355c11140c20


def AGI():
    #Adjusted Gross Income  
    global _posagi
    global c00100
    global c04600
    c02650 = _ymod1 + c02500 - c02700 + puf_dict['e02615'] #Gross Income

    c00100 = c02650 - c02900
    _agierr = puf_dict['e00100'] - c00100  #Adjusted Gross Income
    c00100 = np.where(puf_dict['fixup'] >= 1, c00100 + _agierr, c00100)

    _posagi = np.maximum(c00100, 0)
    _ywossbe = puf_dict['e00100'] - puf_dict['e02500']
    _ywossbc = c00100 - c02500

    _prexmp = puf_dict['XTOT'] * planX['amex'][puf_dict['FLPDYR'] - 2013] 
    #Personal Exemptions (_phaseout smoothed)

<<<<<<< HEAD
	_dispc = np.zeros((dim,))
	_dispc = np.minimum(1, np.maximum(0, 0.02 * (_posagi - _exmpb[FLPDYR-2013, MARS-1])/(2500/_sep)))

	c04600 = _prexmp * (1 - _dispc)

	outputs = (c02650, c00100, _agierr, _posagi, _ywossbe, _ywossbc, _prexmp, c04600)
	output = np.column_stack(outputs)
	np.savetxt('AGI.csv', output, delimiter=',', 
		header = ('c02650, c00100, _agierr, _posagi, _ywossbe, _ywossbc, _prexmp, c04600') 
		, fmt = '%1.3f')



def ItemDed(puf): 
	#Itemized Deductions
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
		c02400 = e20550 + e20600 + e20950
		c19200 = e19500 + e19570 + e19400 + e19550
	c20800 = np.maximum(0, c20400 - c20750)

	# Charity (assumes carryover is non-cash) #

	_lim50 = np.where(e19800 + e20100 + e20200 <= 0.20 * _posagi, 0, np.minimum(0.50 * _posagi, e19800))
	_lim30 = np.where(e19800 + e20100 + e20200 <= 0.20 * _posagi, 0, np.minimum(0.30 * _posagi, e20100 + e20200))

	c19700 = np.where(e19800 + e20100 + e20200 <= 0.20 * _posagi, 
		e19800 + e20100 + e20200, _lim30 + _lim50)
=======
    c04600 = _prexmp 


def ItemDed(puf): 
    #Itemized Deductions
    global c04470
    global c21060
    global c21040
    global c17000
    global c18300
    global c20800
    global _sit

    # Medical #
    c17750 = 0.075 * _posagi 
    c17000 = np.maximum(0, puf_dict['e17500'] - c17750)

    # State and Local Income Tax, or Sales Tax #
    _sit1 = np.maximum(puf_dict['e18400'], puf_dict['e18425'])
    _sit = np.maximum(_sit1, 0)
    _statax = np.maximum(_sit, puf_dict['e18450'])

    # Other Taxes #
    c18300 = _statax + puf_dict['e18500'] + puf_dict['e18800'] + puf_dict['e18900']

    # Casulty #
    c37703 = np.where(puf_dict['e20500'] > 0, puf_dict['e20500'] + 0.10 * _posagi, 0)
    c20500 = np.where(puf_dict['e20500'] > 0, c37703 - 0.10 * _posagi, 0)

    # Miscellaneous #
    c20750 = 0.02 * _posagi 
    if puf == True: 
        puf_dict['c20400'] = puf_dict['e20400']
        c19200 = puf_dict['e19200'] 
    else: 
        c02400 = puf_dict['e20550'] + puf_dict['e20600'] + puf_dict['e20950']
        c19200 = puf_dict['e19500'] + puf_dict['e19570'] + puf_dict['e19400'] + puf_dict['e19550']
    c20800 = np.maximum(0, puf_dict['c20400'] - c20750)

    # Charity (assumes carryover is non-cash) #
    _lim50 = np.minimum(0.50 * _posagi, puf_dict['e19800'])
    _lim30 = np.minimum(0.30 * _posagi, puf_dict['e20100'] + puf_dict['e20200'])
    c19700 = np.where(puf_dict['e19800'] + puf_dict['e20100'] + puf_dict['e20200'] <= 0.20 * _posagi, 
        puf_dict['e19800'] + puf_dict['e20100'] + puf_dict['e20200'], _lim30 + _lim50)
>>>>>>> 895f5863d50db2a04fa6872c0d66355c11140c20
    #temporary fix!??

    # Gross Itemized Deductions #
    c21060 = (puf_dict['e20900'] + c17000 + c18300 + c19200 + c19700 
        + c20500 + c20800 + puf_dict['e21000'] + puf_dict['e21010'])
    
    # Itemized Deduction Limitation
<<<<<<< HEAD
	_phase2 = np.where(MARS == 1, 200000, 0)
	_phase2 = np.where(MARS == 4, 250000, _phase2)
	_phase2 = np.where(np.logical_and(MARS != 1, MARS != 4), 300000, _phase2)

	_itemlimit = np.ones((dim,))
	_c21060 = c21060
	_nonlimited = c17000 + c20500 + e19570 + e21010 + e20900
	_limitratio = _phase2/_sep 

	c04470 = c21060

	_itemlimit = np.where(np.logical_and(c21060 > _nonlimited, 
		c00100 > _phase2/_sep), 2, 1)
	_dedmin = np.where(np.logical_and(c21060 > _nonlimited, 
		c00100 > _phase2/_sep), 0.8 * (c21060 - _nonlimited), 0)
	_dedpho = np.where(np.logical_and(c21060 > _nonlimited, 
		c00100 > _phase2/_sep), 0.03 * np.maximum(0, _posagi - _phase2/_sep), 0)
	c21040 = np.where(np.logical_and(c21060 > _nonlimited, 
		c00100 > _phase2/_sep), np.minimum(_dedmin, _dedpho), 0)
	c04470 = np.where(np.logical_and(c21060 > _nonlimited, 
		c00100 > _phase2/_sep), c21060 - c21040, c04470)
=======
    _phase2 = np.where(puf_dict['MARS'] == 1, 200000, np.where(puf_dict['MARS'] == 4, 250000, 300000))

    _itemlimit = 1
    _c21060 = c21060
    _nonlimited = c17000 + c20500 + puf_dict['e19570'] + puf_dict['e21010'] + puf_dict['e20900']
    _limitratio = _phase2/_sep 

    _itemlimit = np.where(np.logical_and(c21060 > _nonlimited, 
        c00100 > _phase2/_sep), 2, 1)
    _dedmin = np.where(np.logical_and(c21060 > _nonlimited, 
        c00100 > _phase2/_sep), 0.8 * (c21060 - _nonlimited), 0)
    _dedpho = np.where(np.logical_and(c21060 > _nonlimited, 
        c00100 > _phase2/_sep), 0.03 * np.maximum(0, _posagi - _phase2/_sep), 0)
    c21040 = np.where(np.logical_and(c21060 > _nonlimited, 
        c00100 > _phase2/_sep), np.minimum(_dedmin, _dedpho), 0)
    c04470 = np.where(np.logical_and(c21060 > _nonlimited, 
        c00100 > _phase2/_sep), c21060 - c21040, c21060)
>>>>>>> 895f5863d50db2a04fa6872c0d66355c11140c20

	outputs = (c17750, c17000, _sit1, _sit, _statax, c18300, c37703, c20500, c20750, c20400, c19200, c20800, _lim50, _lim30, c19700, c21060, _phase2, _itemlimit, _nonlimited, _limitratio, c04470, _itemlimit, _dedpho, _dedmin, c21040)
	output = np.column_stack(outputs)
	np.savetxt('ItemDed.csv', output, delimiter=',', 
		header = ('c17750, c17000, _sit1, _sit, _statax, c18300, c37703, c20500, c20750, c20400, c19200, c20800, _lim50, _lim30, c19700, c21060, _phase2, _itemlimit, _nonlimited, _limitratio, c04470, _itemlimit, _dedpho, _dedmin, c21040') 
		, fmt = '%1.3f')

def EI_FICA():
    global _sey
    global _setax
    # Earned Income and FICA #    
    global _earned
    _sey = puf_dict['e00900'] + puf_dict['e02100']
    _fica = np.maximum(0, .153 * np.minimum(planX['ssmax'][puf_dict['FLPDYR'] - 2013], 
        puf_dict['e00200'] + np.maximum(0, _sey) * 0.9235))
    _setax = np.maximum(0, _fica - 0.153 * puf_dict['e00200'])
    _seyoff = np.where(_setax <= 14204, 0.5751 * _setax, 0.5 * _setax + 10067)

    c11055 = puf_dict['e11055']

    _earned = np.maximum(0, puf_dict['e00200'] + puf_dict['e00250'] + puf_dict['e11055'] + puf_dict['e30100'] + _sey - _seyoff)

	outputs = (_sey, _fica, _setax, _seyoff, c11055, _earned)
	output = np.column_stack(outputs)
	np.savetxt('EIFICA.csv', output, delimiter=',', 
		header = ('_sey, _fica, _setax, _seyoff, c11055, _earned') 
		, fmt = '%1.3f')




def StdDed():
    # Standard Deduction with Aged, Sched L and Real Estate # 
    global c04800
    global c60000
    global _taxinc
    global _feitax
    global _standard

<<<<<<< HEAD

	c15100 = np.where(DSI == 1, 
		np.maximum(300 + _earned, _stded[FLPDYR-2013, 6]), 0)
=======
    c15100 = np.where(puf_dict['DSI'] == 1, 
        np.maximum(300 + _earned, planX['stded'][puf_dict['FLPDYR']-2013, 6]), 0)
>>>>>>> 895f5863d50db2a04fa6872c0d66355c11140c20

    c04100 = np.where(puf_dict['DSI'] == 1, np.minimum(planX['stded'][puf_dict['FLPDYR']-2013, puf_dict['MARS']-1], c15100), 
        np.where(np.logical_or(puf_dict['compitem'] == 1, 
            np.logical_and(np.logical_and(3<= puf_dict['MARS'], puf_dict['MARS'] <=6), MIdR == 1)), 
        0, planX['stded'][puf_dict['FLPDYR']-2013, puf_dict['MARS']-1]))


    c04100 = c04100 + puf_dict['e15360']
    _numextra = puf_dict['AGEP'] + puf_dict['AGES'] + puf_dict['PBI'] + puf_dict['SBI'] 

    _txpyers = np.where(np.logical_or(np.logical_or(puf_dict['MARS'] == 2, puf_dict['MARS'] == 3), 
        puf_dict['MARS'] == 3), 2, 1)
    c04200 = np.where(np.logical_and(puf_dict['exact'] == 1, 
        np.logical_or(puf_dict['MARS'] == 3, puf_dict['MARS'] == 5)), 
        puf_dict['e04200'], _numextra * planX['aged'][_txpyers -1, puf_dict['FLPDYR'] - 2013])

    c15200 = c04200

    _standard = np.where(np.logical_and(np.logical_or(puf_dict['MARS'] == 3, puf_dict['MARS'] == 6), 
        c04470 > 0), 
        0, c04100 + c04200)

    _othded = np.where(puf_dict['FDED'] == 1, puf_dict['e04470'] - c04470, 0)
    #c04470 = np.where(np.logical_and(puf_dict['fixup'] >= 2, puf_dict['FDED'] == 1), c04470 + _othded, c04470)
    c04100 = np.where(puf_dict['FDED'] == 1, 0, c04100)
    c04200 = np.where(puf_dict['FDED'] == 1, 0, c04200)
    _standard = np.where(puf_dict['FDED'] == 1, 0, _standard)


    c04500 = c00100 - np.maximum(c21060 - c21040, 
        np.maximum(c04100, _standard + puf_dict['e37717']))
    c04800 = np.maximum(0, c04500 - c04600 - puf_dict['e04805'])

    c60000 = np.where(_standard > 0, c00100, c04500)
    c60000 = c60000 - puf_dict['e04805']

    #Some taxpayers iteimize only for AMT, not regular tax
    # IK: why do we need _amtstd and not just compare with zero?
    _amtstd = DIMARRAY
    c60000 = np.where(np.logical_and(np.logical_and(puf_dict['e04470'] == 0, 
        puf_dict['t04470'] > _amtstd), 
        np.logical_and(puf_dict['f6251'] == 1, puf_dict['exact'] == 1)), c00100 - puf_dict['t04470'], c60000)

    _taxinc = np.where(np.logical_and(c04800 > 0, _feided > 0), 
        c04800 + c02700, c04800)
    
    _feitax = Taxer(inc_in= _feided, inc_out =[], mars= puf_dict['MARS'])
    _oldfei = Taxer(inc_in = c04800, inc_out =[], mars= puf_dict['MARS'])

<<<<<<< HEAD
	_feitax = np.where(np.logical_and(c04800 > 0, _feided > 0), Taxer(inc_in= _feided, inc_out =_feitax, MARS = MARS), _feitax)
	_oldfei = np.where(np.logical_and(c04800 > 0, _feided > 0), Taxer(inc_in = c04800, inc_out = _oldfei, MARS = MARS), _oldfei)


	SDoutputs = (c15100, c04100, _numextra, _txpyers, c04200, c15200, _standard, _othded, c04100, c04200, _standard, c04500, c04800, c60000, _amtstd, _taxinc, _feitax, _oldfei)
	SDoutput = np.column_stack(SDoutputs)
	np.savetxt('StdDed.csv', SDoutput, delimiter=',', 
		header = ('c15100, c04100, _numextra, _txpyers, c04200, c15200, _standard, _othded, c04100, c04200, _standard, c04500, c04800, c60000, _amtstd, _taxinc, _feitax, _oldfei') 
		, fmt = '%1.3f')

def XYZD():
	global c24580
	global _xyztax

	_xyztax = np.zeros((dim,))
	c05200 = np.zeros((dim,))
	_xyztax = Taxer(inc_in = _taxinc, inc_out = _xyztax, MARS= MARS)
	c05200 = Taxer(inc_in = c04800, inc_out = c05200, MARS = MARS)


	outputs = (_xyztax, c05200)
	output = np.column_stack(outputs)
	np.savetxt('XYZD.csv', output, delimiter=',', 
		header = ('_xyztax, c05200') 
		, fmt = '%1.3f')
	

def NonGain():
	_cglong = np.minimum(c23650, e23250) + e01100
	_noncg = np.zeros((dim,))
=======
    _feitax = np.where(np.logical_or(c04800 < 0, _feided < 0), 0, _feitax)

def XYZD():
    global c24580
    global _xyztax
    _xyztax = Taxer(inc_in = _taxinc, inc_out =[], mars= puf_dict['MARS'])
    c05200 = Taxer(inc_in = c04800, inc_out =[], mars= puf_dict['MARS'])
    

def NonGain():
    _cglong = np.minimum(c23650, puf_dict['e23250'] + puf_dict['e01100'])
>>>>>>> 895f5863d50db2a04fa6872c0d66355c11140c20

	outputs = (_cglong, _noncg)
	output = np.column_stack(outputs)
	np.savetxt('NonGain.csv', output, delimiter=',', 
		header = ('_cglong, _noncg') 
		, fmt = '%1.3f')

def TaxGains():
<<<<<<< HEAD
	global c05750
	global c24517
	global _taxbc
	global c24516
	global c24520
	global c05700
	c24517 = np.zeros((dim,))
	c24520 = np.zeros((dim,))
	c24530 = np.zeros((dim,))
	c24553 = np.zeros((dim,))
	c24540 = np.zeros((dim,))
	c24581 = np.zeros((dim,))
	c24542 = np.zeros((dim,)) 
	_dwks16 = np.zeros((dim,))

	_hasgain = np.zeros((dim,))

	_hasgain = np.where(np.logical_or(e01000 > 0, c23650 > 0), 1, _hasgain)
	_hasgain = np.where(np.logical_or(e23250 > 0, e01100 > 0), 1, _hasgain)
	_hasgain = np.where(e00650 > 0, 1, _hasgain)

	_dwks5 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), np.maximum(0, e58990 - e58980), 0)
	
	
	c00650 = e00650
	c24505 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), np.maximum(0, c00650 - _dwks5), 0)
	c24510 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), np.maximum(0, np.minimum(c23650, e23250)) + e01100, 0)
	#gain for tax computation

	c24510 = np.where(np.logical_and(_taxinc > 0, np.logical_and(_hasgain == 1, e01100 > 0)), e01100, c24510)
	#from app f 2008 drf

	_dwks9 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), np.maximum(0, c24510 - np.minimum(e58990, e58980)), 0)
	#e24516 gain less invest y 

	c24516 = np.maximum(0, np.minimum(e23250, c23650)) + e01100
	c24580 = _xyztax

	c24516 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), c24505 + _dwks9, c24516)
	_dwks12 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), np.minimum(_dwks9, e24515 + e24518), 0)
	c24517 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), c24516 -_dwks12, 0)
	#gain less 25% and 28%

	c24520 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), np.maximum(0, _taxinc -c24517), 0)
	#tentative TI less schD gain

	c24530 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), np.minimum(_brk2[FLPDYR-2013, MARS-1], _taxinc), 0)
	#minimum TI for bracket

	_dwks16 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), np.minimum(c24520, c24530), 0)
	_dwks17 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), np.maximum(0, _taxinc - c24516), 0)
	c24540 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), np.maximum(_dwks16, _dwks17), 0)

	c24534 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), c24530 - _dwks16, 0)
	_dwks21 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), np.minimum(_taxinc, c24517), 0)
	c24597 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), np.maximum(0, _dwks21 - c24534), 0)
	#income subject to 15% tax

	c24598 = 0.15 * c24597 #actual 15% tax

	_dwks25 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), np.minimum(_dwks9, e24515), 0)
	_dwks26 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), c24516 + c24540, 0)
	_dwks28 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), np.maximum(0, _dwks26 - _taxinc), 0)
	c24610 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), np.maximum(0, _dwks25 - _dwks28), 0)
	c24615 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), 0.25 * c24610, 0)
	_dwks31 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), c24540 + c24534 + c24597 + c24610, 0)
	c24550 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), np.maximum(0, _taxinc - _dwks31), 0)
	c24570 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), 0.28 * c24550, 0)
	_addtax = np.zeros((dim,))
	_addtax = np.where(np.logical_and(_taxinc > 0, np.logical_and(_hasgain == 1, c24540 > _brk6[FLPDYR-2013, MARS-1])), 0.05 * c24517, _addtax)
	_addtax = np.where(np.logical_and(np.logical_and(_taxinc > 0, _hasgain == 1), np.logical_and(c24540 <= _brk6[FLPDYR-2013, MARS-1], _taxinc > _brk6[FLPDYR-2013, MARS-1])), 0.05 * np.minimum(c04800 - _brk6[FLPDYR-2013, MARS-1], c24517), _addtax)

	c24560 = np.zeros((dim,))
	c24560 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), Taxer(inc_in = c24540, inc_out = c24560, MARS = MARS), c24560)

	_taxspecial = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), c24598 + c24615 + c24570 + c24560 + _addtax, 0)

	c24580 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), np.minimum(_taxspecial, _xyztax), c24580) 
	#e24580 schedule D tax

	c05100 = c24580
	c05100 = np.where(np.logical_and(c04800 > 0, _feided > 0), np.maximum(0, c05100 - _feitax), c05100)

	#Form 4972 - Lump Sum Distributions
	c05700 = np.zeros((dim,))

	c59430 = np.where(_cmp == 1, np.maximum(0, e59410 - e59420), 0)
	c59450 = np.where(_cmp == 1, c59430 + e59440, 0) #income plus lump sum
	c59460 = np.where(_cmp == 1, np.maximum(0, np.minimum(0.5 * c59450, 10000)) - 0.2 * np.maximum(0, c59450 - 20000), 0)
	_line17 = np.where(_cmp == 1, c59450 - c59460, 0)
	_line19 = np.where(_cmp == 1, c59450 - c59460 - e59470, 0)
	_line22 = np.where(np.logical_and(_cmp == 1, c59450 > 0), np.maximum(0, e59440 - e59440 * c59460/c59450),0)

	_line30 = np.where(_cmp == 1, 0.1 * np.maximum(0, c59450 - c59460 - e59470), 0)

	_line31 = np.where(_cmp == 1, 
		0.11 * np.minimum(_line30, 1190)
		+ 0.12 * np.minimum( 2270 - 1190, np.maximum(0, _line30 - 1190))
		+ 0.14 * np.minimum( 4530 - 2270, np.maximum(0, _line30 - 2270))
		+ 0.15 * np.minimum( 6690 - 4530, np.maximum(0, _line30 - 4530))
		+ 0.16 * np.minimum( 9170 - 6690, np.maximum(0, _line30 - 6690))
		+ 0.18 * np.minimum(11440 - 9170, np.maximum(0, _line30 - 9170))
		+ 0.20 * np.minimum(13710 - 11440, np.maximum(0, _line30 - 11440))
		+ 0.23 * np.minimum(17160 - 13710, np.maximum(0, _line30 - 13710))
		+ 0.26 * np.minimum(22880 - 17160, np.maximum(0, _line30 - 17160))
		+ 0.30 * np.minimum(28600 - 22880, np.maximum(0, _line30 - 22880))
		+ 0.34 * np.minimum(34320 - 28600, np.maximum(0, _line30 - 28600))
		+ 0.38 * np.minimum(42300 - 34320, np.maximum(0, _line30 - 34320))
		+ 0.42 * np.minimum(57190 - 42300, np.maximum(0, _line30 - 42300))
		+ 0.48 * np.minimum(85790 - 57190, np.maximum(0, _line30 - 57190)),
		0)

	_line32 = np.where(_cmp == 1, 10 * _line31, 0)
	_line36 = np.where(np.logical_and(_cmp == 1, e59440 == 0), _line32, 0)
	_line33 = np.where(np.logical_and(_cmp == 1, e59440 > 0), 0.1 * _line22, 0)
	_line34 = np.where(np.logical_and(_cmp == 1, e59440 > 0),
		0.11 * np.minimum(_line30, 1190)
		+ 0.12 * np.minimum( 2270 - 1190, np.maximum(0, _line30 - 1190))
		+ 0.14 * np.minimum( 4530 - 2270, np.maximum(0, _line30 - 2270))
		+ 0.15 * np.minimum( 6690 - 4530, np.maximum(0, _line30 - 4530))
		+ 0.16 * np.minimum( 9170 - 6690, np.maximum(0, _line30 - 6690))
		+ 0.18 * np.minimum(11440 - 9170, np.maximum(0, _line30 - 9170))
		+ 0.20 * np.minimum(13710 - 11440, np.maximum(0, _line30 - 11440))
		+ 0.23 * np.minimum(17160 - 13710, np.maximum(0, _line30 - 13710))
		+ 0.26 * np.minimum(22880 - 17160, np.maximum(0, _line30 - 17160))
		+ 0.30 * np.minimum(28600 - 22880, np.maximum(0, _line30 - 22880))
		+ 0.34 * np.minimum(34320 - 28600, np.maximum(0, _line30 - 28600))
		+ 0.38 * np.minimum(42300 - 34320, np.maximum(0, _line30 - 34320))
		+ 0.42 * np.minimum(57190 - 42300, np.maximum(0, _line30 - 42300))
		+ 0.48 * np.minimum(85790 - 57190, np.maximum(0, _line30 - 57190)),
		0)
	_line35 = np.where(np.logical_and(_cmp == 1, e59440 > 0), 10 * _line34, 0)
	_line36 = np.where(np.logical_and(_cmp == 1, e59440 > 0), np.maximum(0, _line32 - _line35), 0)
	#tax saving from 10 yr option
	c59485 = np.where(_cmp == 1, _line36, 0)
	c59490 = np.where(_cmp == 1, c59485 + 0.2 * np.maximum(0, e59400), 0)
	#pension gains tax plus

	c05700 = np.where(_cmp == 1, c59490, 0)

	_s1291 = e10105
	_parents = e83200_0
	c05750 = np.maximum(c05100 + _parents + c05700, e74400)
	_taxbc = c05750 
	x05750 = c05750 

	

	outputs = (e00650, _hasgain, _dwks5, c24505, c24510, _dwks9, c24516, c24580, c24516, _dwks12, c24517, c24520, c24530, _dwks16, _dwks17, c24540, c24534, _dwks21, c24597, c24598, _dwks25, _dwks26, _dwks28, c24610, c24615, _dwks31, c24550, c24570, _addtax, c24560, _taxspecial, c05100, c05700, c59430, c59450, c59460, _line17, _line19, _line22, _line30, _line31, _line32, _line36, _line33, _line34, _line35, c59485, c59490, c05700, _s1291, _parents, c05750, _taxbc)
	output = np.column_stack(outputs)
	np.savetxt('Taxgains.csv', output, delimiter=',', 
		header = ('e00650, _hasgain, _dwks5, c24505, c24510, _dwks9, c24516, c24580, c24516, _dwks12, c24517, c24520, c24530, _dwks16, _dwks17, c24540, c24534, _dwks21, c24597, c24598, _dwks25, _dwks26, _dwks28, c24610, c24615, _dwks31, c24550, c24570, _addtax, c24560, _taxspecial, c05100, c05700, c59430, c59450, c59460, _line17, _line19, _line22, _line30, _line31, _line32, _line36, _line33, _line34, _line35, c59485, c59490, c05700, _s1291, _parents, c05750, _taxbc') 
		, fmt = '%1.3f')

	return c05750

 
def MUI(c05750):
	#Additional Medicare tax on unearned Income 
	c05750 = c05750
	c05750 = np.where(c00100 > _thresx[MARS-1], c05750 + 0.038 * np.minimum(e00300 + e00600 + np.maximum(0, c01000) + np.maximum(0, e02000), c00100 - _thresx[MARS-1]), c05750)
	
	outputs = (c05750)
	output = np.column_stack(outputs)
	np.savetxt('MUI.csv', c05750, delimiter=',', 
		header = ('c05750') 
		, fmt = '%1.3f')
	
=======
    global c05750
    global c24517
    global _taxbc
    global c24516
    global c24520
    global c05700
    # IK: unused vars!
    # c24553 = DIMARRAY
    # c24581 = DIMARRAY
    # c24542 = DIMARRAY

    _hasgain = np.where(np.logical_or(puf_dict['e01000'] > 0, c23650 > 0), 1, 0)
    _hasgain = np.where(np.logical_or(puf_dict['e23250'] > 0, puf_dict['e01100'] > 0), 1, _hasgain)
    _hasgain = np.where(puf_dict['e00650'] > 0, 1, _hasgain)

    #significance of sum() function here in original SAS code?  
    _dwks5 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), np.maximum(0, puf_dict['e58990'] - puf_dict['e58980']), 0)
    c24505 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), np.maximum(0, puf_dict['c00650'] - _dwks5), 0)
    c24510 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), np.maximum(0, np.minimum(c23650, puf_dict['e23250'])) + puf_dict['e01100'], 0)
    #gain for tax computation

    c24510 = np.where(np.logical_and(_taxinc > 0, np.logical_and(_hasgain == 1, puf_dict['e01100'] > 0)), puf_dict['e01100'], c24510)
    #from app f 2008 drf

    _dwks9 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), np.maximum(0, c24510 - np.minimum(puf_dict['e58990'], puf_dict['e58980'])), 0)
    #puf_dict['e24516'] gain less invest y 

    c24516 = np.maximum(0, np.minimum(puf_dict['e23250'], c23650)) + puf_dict['e01100']
    c24580 = _xyztax

    c24516 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), c24505 + _dwks9, c24516)
    _dwks12 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), np.minimum(_dwks9, puf_dict['e24515'] + puf_dict['e24518']), 0)
    c24517 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), c24516 -_dwks12, 0)
    #gain less 25% and 28%

    c24520 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), np.maximum(0, _taxinc -c24517), 0)
    #tentative TI less schD gain

    c24530 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), np.minimum(planX['brk2'][puf_dict['FLPDYR']-2013, puf_dict['MARS']-1], _taxinc), 0)
    #minimum TI for bracket

    _dwks16 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), np.minimum(c24520, c24530), 0)
    _dwks17 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), np.maximum(0, _taxinc - c24516), 0)
    c24540 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), np.maximum(_dwks16, _dwks17), 0)

    c24534 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), c24530 - _dwks16, 0)
    _dwks21 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), np.minimum(_taxinc, c24517), 0)
    c24597 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), np.maximum(0, _dwks21 - c24534), 0)
    #income subject to 15% tax

    c24598 = 0.15 * c24597 #actual 15% tax

    _dwks25 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), np.minimum(_dwks9, puf_dict['e24515']), 0)
    _dwks26 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), c24516 + c24540, 0)
    _dwks28 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), np.maximum(0, _dwks25 - _taxinc), 0)
    c24610 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), np.maximum(0, _dwks25 - _dwks28), 0)
    c24615 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), 0.25 * c24610, 0)
    _dwks31 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), c24540 + c24534 + c24597 + c24610, 0)
    c24550 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), np.maximum(0, _taxinc - _dwks31), 0)
    c24570 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), 0.28 * c24550, 0)
    _addtax = np.where(np.logical_and(_taxinc > 0, np.logical_and(_hasgain == 1, c24540 > planX['brk6'][puf_dict['FLPDYR']-2013, puf_dict['MARS']-1])), 0.05 * c24517, 0.0)
    _addtax = np.where(np.logical_and(np.logical_and(_taxinc > 0, _hasgain == 1), np.logical_and(c24540 <= planX['brk6'][puf_dict['FLPDYR']-2013, puf_dict['MARS']-1], _taxinc > planX['brk6'][puf_dict['FLPDYR']-2013, puf_dict['MARS']-1])), 0.05 * np.minimum(c04800 - planX['brk6'][puf_dict['FLPDYR']-2013, puf_dict['MARS']-1], c24517), _addtax)

    c24560 = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), Taxer(inc_in = c24540, inc_out =[], mars= puf_dict['MARS']), 0)

    _taxspecial = np.where(np.logical_and(_taxinc > 0, _hasgain == 1), c24598 + c24615 + c24570 + c24560 + _addtax, 0)

    c05100 = c24580
    c05100 = np.where(np.logical_and(c04800 > 0, _feided > 0), np.maximum(0, c05100 - _feitax), c05100)

    #Form 4972 - Lump Sum Distributions

    c59430 = np.where(puf_dict['cmp'] == 1, np.maximum(0, puf_dict['e59410'] - puf_dict['e59420']), 0)
    c59450 = np.where(puf_dict['cmp'] == 1, c59430 + puf_dict['e59440'], 0) #income plus lump sum
    c59460 = np.where(puf_dict['cmp'] == 1, np.maximum(0, np.minimum(0.5 * c59450, 10000)) - 0.2 * np.maximum(0, c59450 - 20000), 0)
    _line17 = np.where(puf_dict['cmp'] == 1, c59450 - c59460, 0)
    _line19 = np.where(puf_dict['cmp'] == 1, c59450 - c59460 - puf_dict['e59470'], 0)
    _line22 = np.where(np.logical_and(puf_dict['cmp'] == 1, c59450 > 0), np.maximum(0, puf_dict['e59440'] - puf_dict['e59440'] * c59460/c59450),0)

    _line30 = np.where(puf_dict['cmp'] == 1, 0.1 * np.maximum(0, c59450 - c59460 - puf_dict['e59470']), 0)

    _line31 = np.where(puf_dict['cmp'] == 1, 
        0.11 * np.minimum(_line30, 1190)
        + 0.12 * np.minimum( 2270 - 1190, np.maximum(0, _line30 - 1190))
        + 0.14 * np.minimum( 4530 - 2270, np.maximum(0, _line30 - 2270))
        + 0.15 * np.minimum( 6690 - 4530, np.maximum(0, _line30 - 4530))
        + 0.16 * np.minimum( 9170 - 6690, np.maximum(0, _line30 - 6690))
        + 0.18 * np.minimum(11440 - 9170, np.maximum(0, _line30 - 9170))
        + 0.20 * np.minimum(13710 - 11440, np.maximum(0, _line30 - 11440))
        + 0.23 * np.minimum(17160 - 13710, np.maximum(0, _line30 - 13710))
        + 0.26 * np.minimum(22880 - 17160, np.maximum(0, _line30 - 17160))
        + 0.30 * np.minimum(28600 - 22880, np.maximum(0, _line30 - 22880))
        + 0.34 * np.minimum(34320 - 28600, np.maximum(0, _line30 - 28600))
        + 0.38 * np.minimum(42300 - 34320, np.maximum(0, _line30 - 34320))
        + 0.42 * np.minimum(57190 - 42300, np.maximum(0, _line30 - 42300))
        + 0.48 * np.minimum(85790 - 57190, np.maximum(0, _line30 - 57190)),
        0)

    _line32 = np.where(puf_dict['cmp'] == 1, 10 * _line31, 0)
    _line36 = np.where(np.logical_and(puf_dict['cmp'] == 1, puf_dict['e59440'] == 0), _line32, 0)
    _line33 = np.where(np.logical_and(puf_dict['cmp'] == 1, puf_dict['e59440'] > 0), 0.1 * _line22, 0)
    _line34 = np.where(np.logical_and(puf_dict['cmp'] == 1, puf_dict['e59440'] > 0),
        0.11 * np.minimum(_line30, 1190)
        + 0.12 * np.minimum( 2270 - 1190, np.maximum(0, _line30 - 1190))
        + 0.14 * np.minimum( 4530 - 2270, np.maximum(0, _line30 - 2270))
        + 0.15 * np.minimum( 6690 - 4530, np.maximum(0, _line30 - 4530))
        + 0.16 * np.minimum( 9170 - 6690, np.maximum(0, _line30 - 6690))
        + 0.18 * np.minimum(11440 - 9170, np.maximum(0, _line30 - 9170))
        + 0.20 * np.minimum(13710 - 11440, np.maximum(0, _line30 - 11440))
        + 0.23 * np.minimum(17160 - 13710, np.maximum(0, _line30 - 13710))
        + 0.26 * np.minimum(22880 - 17160, np.maximum(0, _line30 - 17160))
        + 0.30 * np.minimum(28600 - 22880, np.maximum(0, _line30 - 22880))
        + 0.34 * np.minimum(34320 - 28600, np.maximum(0, _line30 - 28600))
        + 0.38 * np.minimum(42300 - 34320, np.maximum(0, _line30 - 34320))
        + 0.42 * np.minimum(57190 - 42300, np.maximum(0, _line30 - 42300))
        + 0.48 * np.minimum(85790 - 57190, np.maximum(0, _line30 - 57190)),
        0)
    _line35 = np.where(np.logical_and(puf_dict['cmp'] == 1, puf_dict['e59440'] > 0), 10 * _line34, 0)
    _line36 = np.where(np.logical_and(puf_dict['cmp'] == 1, puf_dict['e59440'] > 0), np.maximum(0, _line32 - _line35), 0)
    #tax saving from 10 yr option
    c59485 = np.where(puf_dict['cmp'] == 1, _line36, 0)
    c59490 = np.where(puf_dict['cmp'] == 1, c59485 + 0.2 * np.maximum(0, puf_dict['e59400']), 0)
    #pension gains tax plus

    c05700 = np.where(puf_dict['cmp'] == 1, c59490, 0)

    _s1291 = puf_dict['e10105']
    _parents = puf_dict['e83200_0']
    c05750 = np.maximum(c05100 + _parents + c05700, puf_dict['e74400'])
    _taxbc = c05750 
    x05750 = c05750 

    return c05750

 
def MUI(c05750):
    #Additional Medicare tax on unearned Income 
    c05750 = c05750
    c00100[5] = 100000000
    c05750[6] = 1234
    c05750 = np.where(c00100 > planX['thresx'][puf_dict['MARS']-1], 0.038 * np.minimum(puf_dict['e00300'] + puf_dict['e00600'] + np.maximum(0, c01000) + np.maximum(0, puf_dict['e02000']), c00100 - planX['thresx'][puf_dict['MARS']-1]), c05750)
    
    
>>>>>>> 895f5863d50db2a04fa6872c0d66355c11140c20

def AMTI(puf):
    global c05800
    global _othtax
    global _agep
    global _ages
    c62720 = c24517 + puf_dict['x62720'] 
    c60260 = puf_dict['e00700'] + puf_dict['x60260']
    c63100 = np.maximum(0, _taxbc - puf_dict['e07300'])
    c60200 = np.minimum(c17000, 0.025 * _posagi)
    c60240 = c18300 + puf_dict['x60240']
    c60220 = c20800 + puf_dict['x60220']
    c60130 = c21040 + puf_dict['x60130'] 
    c62730 = puf_dict['e24515'] + puf_dict['x62730']

    _addamt = np.where(np.logical_or(puf_dict['exact'] == 0, np.logical_and(puf_dict['exact'] == 1, c60200 + c60220 + c60240 + puf_dict['e60290'] > 0)), c60200 + c60240 + c60220 + puf_dict['e60290'] - c60130, 0)

<<<<<<< HEAD
	c62100 = np.where(_cmp == 1, (_addamt + e60300 + e60860 + e60100 + e60840 + e60630 + e60550 
								+ e60720 + e60430 + e60500 + e60340 + e60680 + e60600 + e60405 + e60440 
								+ e60420 + e60410 + e61400 + e60660 - c60260 - e60480 - e62000 + c60000), 0)
=======
>>>>>>> 895f5863d50db2a04fa6872c0d66355c11140c20

    c62100 = np.where(puf_dict['cmp'] == 1, _addamt + puf_dict['e60300'] + puf_dict['e60860'] + puf_dict['e60100'] + puf_dict['e60840'] + puf_dict['e60630'] + puf_dict['e60550'] + puf_dict['e60720'] + puf_dict['e60430'] + puf_dict['e60500'] + puf_dict['e60340'] + puf_dict['e60680'] + puf_dict['e60600'] + puf_dict['e60405'] + puf_dict['e60440'] + puf_dict['e60420'] + puf_dict['e60410'] + puf_dict['e61400'] + puf_dict['e60660'] - c60260 - puf_dict['e60480'] - puf_dict['e62000'] + c60000, 0)


    c62100 = np.where(puf_dict['cmp'] == 1, c62100 - puf_dict['e60250'], c62100)

    _edical = np.where(np.logical_and(puf == True, np.logical_or(_standard == 0, np.logical_and(puf_dict['exact'] == 1, puf_dict['e04470'] > 0))), np.maximum(0, puf_dict['e17500'] - np.maximum(0, puf_dict['e00100']) * 0.075), 0)

    _cmbtp = np.where(np.logical_and(puf == True, np.logical_and(np.logical_or(_standard == 0, np.logical_and(puf_dict['exact'] == 1, puf_dict['e04470'] > 0)), puf_dict['f6251'] == 1)), -1 * np.minimum(_edical, 0.025 * np.maximum(0, puf_dict['e00100'])) + puf_dict['e62100'] + c60260 + puf_dict['e04470'] + puf_dict['e21040'] - _sit - puf_dict['e00100'] - puf_dict['e18500'] - puf_dict['e20800'], 0)

    c62100 = np.where(np.logical_and(puf == True, np.logical_or(_standard == 0, np.logical_and(puf_dict['exact'] == 1, puf_dict['e04470'] > 0))), c00100 - c04470 + np.minimum(c17000, 0.025 * np.maximum(0, c00100)) + _sit + puf_dict['e18500'] - c60260 + c20800 - c21040 + _cmbtp, c62100)

<<<<<<< HEAD
	_cmbtp = np.where(np.logical_and(puf == True, np.logical_and(_standard > 0, f6251 == 1)), e62100 - e00100 + c60260, _cmbtp)
	c62100 = np.where(np.logical_and(puf == True, _standard > 0), c00100 - c60260 + _cmbtp, c62100)
=======
    _cmbtp = np.where(np.logical_and(puf == True, np.logical_and(_standard > 0, puf_dict['f6251'] == 1)), puf_dict['e62100'] - puf_dict['e00100'] + c60260, _cmbtp)
    c62100 = np.where(np.logical_and(puf == True, np.logical_and(_standard > 0, puf_dict['f6251'] == 1)), c00100 - c60260 + _cmbtp, c62100)
>>>>>>> 895f5863d50db2a04fa6872c0d66355c11140c20

    x62100 = c62100

    _amtsepadd = np.where(np.logical_and(c62100 > planX['amtsep'][puf_dict['FLPDYR']-2013], np.logical_or(puf_dict['MARS'] == 3, puf_dict['MARS'] == 6)), np.maximum(0, np.minimum(planX['almsep'][puf_dict['FLPDYR']-2013], 0.25 * (c62100 - planX['amtsep'][puf_dict['FLPDYR']-2013]))), 0)
    c62100 = np.where(np.logical_and(c62100 > planX['amtsep'][puf_dict['FLPDYR']-2013], np.logical_or(puf_dict['MARS'] == 3, puf_dict['MARS'] == 6)), c62100 + _amtsepadd, c62100)

    c62600 = np.maximum(0, planX['amtex'][puf_dict['FLPDYR']-2013, puf_dict['MARS']-1] - 0.25 * np.maximum(0, c62100 - planX['amtys'][puf_dict['MARS']-1]))

    _agep = np.where(puf_dict['DOBYR'] > 0, np.ceil((12 * (puf_dict['FLPDYR'] - puf_dict['DOBYR']) - puf_dict['DOBMD']/100)/12), 0)
    _ages = np.where(puf_dict['SDOBYR'] > 0, np.ceil((12 * (puf_dict['FLPDYR'] - puf_dict['SDOBYR']) - puf_dict['SDOBMD']/100)/12), 0)

    c62600 = np.where(np.logical_and(puf_dict['cmp'] == 1, np.logical_and(puf_dict['f6251'] == 1, puf_dict['exact'] == 1)), puf_dict['e62600'], c62600)

<<<<<<< HEAD
	c62600 = np.where(np.logical_and(np.logical_and(_cmp == 1, _exact == 0), np.logical_and(_agep < _amtage[FLPDYR-2013], _agep != 0)), np.minimum(c62600, _earned + _almdep[FLPDYR-2013]), c62600)
=======
    #puf_dict['cmp'] == 1 and puf_dict['exact'] == 0 and (_agep < amtage and agep =/= 0)

    c62600 = np.where(np.logical_and(np.logical_and(puf_dict['cmp'] == 1, puf_dict['exact'] == 0), np.logical_and(_agep < planX['amtage'][puf_dict['FLPDYR']-2013], _agep != 0)), np.minimum(c62600, _earned + planX['almdep'][puf_dict['FLPDYR']-2013]), c62600)
>>>>>>> 895f5863d50db2a04fa6872c0d66355c11140c20

    c62700 = np.maximum(0, c62100 - c62600)

    _alminc = c62700

    _alminc = np.where(c02700 > 0, np.maximum(0, c62100 - c62600 + c02700), _alminc)
    # CHECK IF WE WANT TO SET THIS TO ZERO
    _amtfei = np.where(c02700 > 0, 0.26 * c02700 + 0.02 * np.maximum(0, c02700 - planX['almsp'][puf_dict['FLPDYR']-2013]/_sep), 0)

    c62780 = 0.26 * _alminc + 0.02 * np.maximum(0, _alminc - planX['almsp'][puf_dict['FLPDYR']-2013]/_sep) - _amtfei

    c62900 = np.where(puf_dict['f6251'] != 0, puf_dict['e62900'], puf_dict['e07300']) 
    c63000 = c62780 - c62900

    c62740 = np.minimum(np.maximum(0, c24516 + puf_dict['x62740']), c62720 + c62730)
    c62740 = np.where(c24516 == 0, c62720 + c62730, c62740)

    _ngamty = np.maximum(0, _alminc - c62740)

    c62745 = 0.26 * _ngamty + 0.02 * np.maximum(0, _ngamty - planX['almsp'][puf_dict['FLPDYR']-2013]/_sep)
    y62745 = planX['almsp'][puf_dict['FLPDYR']-2013]/_sep

    _amt5pc = DIMARRAY
    _amt15pc = np.minimum(_alminc, c62720) - _amt5pc - np.minimum(np.maximum(0, planX['brk2'][puf_dict['FLPDYR']-2013, puf_dict['MARS']-1] - c24520), np.minimum(_alminc, c62720))
    _amt15pc = np.where(c04800 == 0, np.maximum(0, np.minimum(_alminc, c62720) - planX['brk2'][puf_dict['FLPDYR']-2013, puf_dict['MARS']-1]), _amt15pc)
    _amt25pc = np.minimum(_alminc, c62740) - np.minimum(_alminc, c62720)

    _amt25pc = np.where(c62730 == 0, 0, _amt25pc)
    c62747 = planX['cgrate1'][puf_dict['FLPDYR']-2013] * _amt5pc
    c62755 = planX['cgrate2'][puf_dict['FLPDYR']-2013] * _amt15pc
    c62770 = 0.25 * _amt25pc
    _tamt2 = c62747 + c62755 + c62770

<<<<<<< HEAD

	_amt = np.zeros((dim,))
	_amt = np.where(_ngamty > _brk6[FLPDYR-2013, MARS-1], 0.05 * np.minimum(_alminc, c62740), _amt)
	_amt = np.where(np.logical_and(_ngamty <= _brk6[FLPDYR-2013, MARS-1], _alminc > _brk6[FLPDYR-2013, MARS-1]), 0.05 * np.minimum(_alminc - _brk6[FLPDYR-2013, MARS-1], c62740), _amt)

	_tamt2 = _tamt2 + _amt

	c62800 = np.minimum(c62780, c62745 + _tamt2 - _amtfei)
	c63000 = c62800 - c62900 
	c63100 = _taxbc - e07300 - c05700 
	c63100 = c63100 + e10105
=======
    # AMT referenced in np.where before its assigned, setting to zero
    # check this though
    _amt = np.where(_ngamty > planX['brk6'][puf_dict['FLPDYR']-2013, puf_dict['MARS']-1], 0.05 * np.minimum(_alminc, c62740), 0)
    _amt = np.where(np.logical_and(_ngamty <= planX['brk6'][puf_dict['FLPDYR']-2013, puf_dict['MARS']-1], _alminc > planX['brk6'][puf_dict['FLPDYR']-2013, puf_dict['MARS']-1]), 0.05 * np.minimum(_alminc - planX['brk6'][puf_dict['FLPDYR']-2013, puf_dict['MARS']-1], c62740), _amt)

    c62800 = np.minimum(c62780, c62745 + _tamt2 - _amtfei)
    c63000 = c62800 - c62900 
    c63100 = _taxbc - puf_dict['e07300'] - c05700 
    c63100 = c63100 + puf_dict['e10105']
>>>>>>> 895f5863d50db2a04fa6872c0d66355c11140c20

    c63100 = np.maximum(0, c63100)
    c63200 = np.maximum(0, c63000 - c63100)
    c09600 = c63200
    _othtax = puf_dict['e05800'] - (puf_dict['e05100'] + puf_dict['e09600'])

    c05800 = _taxbc + c63200

	outputs = (c62720, c60260, c63100, c60200, c60240, c60220, c60130, c62730, _addamt, c62100, _cmbtp, _edical, _amtsepadd, c62600, _agep, _ages, c62600, c62700, _alminc, _amtfei, c62780, c62900, c63000, c62740, _ngamty, c62745, y62745, _tamt2, _amt5pc, _amt15pc, _amt25pc, c62747, c62755, c62770, _amt, c62800, c09600, _othtax, c05800)
	output = np.column_stack(outputs)
	np.savetxt('AMTI.csv', output, delimiter=',', 
		header = ('c62720, c60260, c63100, c60200, c60240, c60220, c60130, c62730, _addamt, c62100, _cmbtp, _edical, _amtsepadd, c62600, _agep, _ages, c62600, c62700, _alminc, _amtfei, c62780, c62900, c63000, c62740, _ngamty, c62745, y62745, _tamt2, _amt5pc, _amt15pc, _amt25pc, c62747, c62755, c62770, _amt, c62800, c09600, _othtax, c05800') 
		, fmt = '%1.3f')

def F2441(puf, _earned):
<<<<<<< HEAD
	global c32880
	global c32890
	global c32800
	global _dclim
	_earned = _earned
	_earned = np.where(_fixeic == 1, e59560, _earned)
	c32880 = np.where(np.logical_and(MARS == 2, puf == True), 0.5 * _earned, 0)
	c32890 = np.where(np.logical_and(MARS == 2, puf == True), 0.5 * _earned, 0)
	c32880 = np.where(np.logical_and(MARS == 2, puf == False), np.maximum(0, e32880), c32880)
	c32890 = np.where(np.logical_and(MARS == 2, puf == False), np.maximum(0, e32890), c32890)
	c32880 = np.where(MARS != 2, _earned, c32880)
	c32890 = np.where(MARS != 2, _earned, c32890)	

	_ncu13 = np.zeros((dim,))
	_ncu13 = np.where(puf == True, f2441, _ncu13)
	_ncu13 = np.where(np.logical_and(puf == False, CDOB1 > 0), _ncu13 + 1, _ncu13)
	_ncu13 = np.where(np.logical_and(puf == False, CDOB2 > 0), _ncu13 + 1, _ncu13)

	_dclim = np.minimum(_ncu13, 2) * _dcmax[FLPDYR-2013]
	c32800 = np.minimum(np.maximum(e32800, e32750 + e32775), _dclim)

	outputs = (_earned, c32880, c32890, _ncu13, _dclim, c32800)
	output = np.column_stack(outputs)
	np.savetxt('F2441.csv', output, delimiter=',', 
		header = ('_earned, c32880, c32890, _ncu13, _dclim, c32800') 
		, fmt = '%1.3f')

def DepCareBen(c32800):
	global c33000
	c32800 = c32800
	#Part III ofdependent care benefits
	_seywage = np.where(np.logical_and(_cmp == 1, MARS == 2), np.minimum(c32880, np.minimum(c32890, np.minimum(e33420 + e33430 - e33450, e33460))), 0)
	_seywage = np.where(np.logical_and(_cmp == 1, MARS != 2), np.minimum(c32880, np.minimum(e33420 + e33430 - e33450, e33460)), _seywage)

	c33465 = np.where(_cmp == 1, e33465, 0)
	c33470 = np.where(_cmp == 1, e33470, 0)
	c33475 = np.where(_cmp == 1, np.maximum(0, np.minimum(_seywage, 5000/_sep) - c33470), 0)
	c33480 = np.where(_cmp == 1, np.maximum(0, e33420 + e33430 - e33450 - c33465 - c33475), 0)
	c32840 = np.where(_cmp == 1, c33470 + c33475, 0)
	c32800 = np.where(_cmp == 1, np.minimum(np.maximum(0, _dclim - c32840), np.maximum(0, e32750 + e32775 - c32840)), c32800)
=======
    global c32880
    global c32890
    global _dclim
    _earned = _earned
    _earned = np.where(puf_dict['fixeic'] == 1, puf_dict['e59560'], _earned)
    c32880 = np.where(np.logical_and(puf_dict['MARS'] == 2, puf == True), 0.5 * _earned, 0)
    c32890 = np.where(np.logical_and(puf_dict['MARS'] == 2, puf == True), 0.5 * _earned, 0)
    c32880 = np.where(np.logical_and(puf_dict['MARS'] == 2, puf == False), np.maximum(0, puf_dict['e32880']), c32880)
    c32890 = np.where(np.logical_and(puf_dict['MARS'] == 2, puf == False), np.maximum(0, puf_dict['e32890']), c32890)
    c32880 = np.where(puf_dict['MARS'] != 2, _earned, c32880)
    c32890 = np.where(puf_dict['MARS'] != 2, _earned, c32890)   

    # check if setting nu13 to zero by default is best
    _ncu13 = np.where(puf == True, puf_dict['f2441'], 0)
    _ncu13 = np.where(np.logical_and(puf == False, puf_dict['CDOB1'] > 0), _ncu13 + 1, _ncu13)
    _ncu13 = np.where(np.logical_and(puf == False, puf_dict['CDOB2'] > 0), _ncu13 + 1, _ncu13)

    _dclim = np.minimum(_ncu13, 2) * planX['dcmax'][puf_dict['FLPDYR']-2013]
    c32800 = np.minimum(np.maximum(puf_dict['e32800'], puf_dict['e32750'] + puf_dict['e32775']), _dclim)

def DepCareBen():
    global c33000
    #Part III ofdependent care benefits
    _seywage = np.where(np.logical_and(puf_dict['cmp'] == 1, puf_dict['MARS'] == 2), np.minimum(c32880, np.minimum(c32890, np.minimum(puf_dict['e33420'] + puf_dict['e33430'] - puf_dict['e33450'], puf_dict['e33460']))), 0)
    _seywage = np.where(np.logical_and(puf_dict['cmp'] == 1, puf_dict['MARS'] != 2), np.minimum(c32880, np.minimum(puf_dict['e33420'] + puf_dict['e33430'] - puf_dict['e33450'], puf_dict['e33460'])), _seywage)

    c33465 = np.where(puf_dict['cmp'] == 1, puf_dict['e33465'], 0)
    c33470 = np.where(puf_dict['cmp'] == 1, puf_dict['e33470'], 0)
    c33475 = np.where(puf_dict['cmp'] == 1, np.maximum(0, np.minimum(_seywage, 5000/_sep) - c33470), 0)
    c33480 = np.where(puf_dict['cmp'] == 1, np.maximum(0, puf_dict['e33420'] + puf_dict['e33430'] - puf_dict['e33450'] - c33465 - c33475), 0)
    c32840 = np.where(puf_dict['cmp'] == 1, c33470 + c33475, 0)
    c32800 = np.where(puf_dict['cmp'] == 1, np.minimum(np.maximum(0, _dclim - c32840), np.maximum(0, puf_dict['e32750'] + puf_dict['e32775'] - c32840)), 0)
>>>>>>> 895f5863d50db2a04fa6872c0d66355c11140c20

    c33000 = np.where(puf_dict['MARS'] == 2, np.maximum(0, np.minimum(c32800, np.minimum(c32880, c32890))), 0)
    c33000 = np.where(puf_dict['MARS'] != 2, np.maximum(0, np.minimum(c32800, _earned)), c33000)

	outputs = (_seywage, c33465, c33470, c33475, c33480, c32840, c32800, c33000)
	output = np.column_stack(outputs)
	np.savetxt('DepCareBen.csv', output, delimiter=',', 
		header = ('_seywage, c33465, c33470, c33475, c33480, c32840, c32800, c33000') 
		, fmt = '%1.3f')

def ExpEarnedInc():
    global c07180
    #Expenses limited to earned income

    _tratio  = np.where(puf_dict['exact'] == 1, np.ceil(np.maximum((c00100 - planX['agcmax'][puf_dict['FLPDYR']-2013])/2000, 0)), 0)
    c33200 = np.where(puf_dict['exact'] == 1, c33000 * 0.01 * np.maximum(20, planX['pcmax'][puf_dict['FLPDYR']-2013] - np.minimum(15, _tratio)), 0)
    c33200 = np.where(puf_dict['exact'] != 1, c33000 * 0.01 * np.maximum(20, planX['pcmax'][puf_dict['FLPDYR']-2013] - np.maximum((c00100 - planX['agcmax'][puf_dict['FLPDYR']-2013])/2000, 0)), c33200)

    c33400 = np.minimum(np.maximum(0, c05800 - puf_dict['e07300']), c33200)
    #amount of the credit

    c07180 = np.where(puf_dict['e07180'] == 0, 0, c33400)

	outputs = (_tratio, c33200, c33400, c07180)
	output = np.column_stack(outputs)
	np.savetxt('ExpEarnedInc.csv', output, delimiter=',', 
		header = ('_tratio, c33200, c33400, c07180') 
		, fmt = '%1.3f')


def RateRed(c05800):
    global c59560
    global c07970
    #rate reduction credit for 2001 only, is this needed?
    c05800 = c05800 
    c07970 = DIMARRAY
    # what is the purpose of below line?
    x07970 = c07970

    c05800 = np.where(puf_dict['fixup'] >= 3, c05800 + _othtax, c05800)

    c59560 = np.where(puf_dict['exact'] == 1, puf_dict['x59560'], _earned)

	outputs = (c07970, c05800, c59560)
	output = np.column_stack(outputs)
	np.savetxt('RateRed.csv', output, delimiter=',', 
		header = ('c07970, c05800, c59560') 
		, fmt = '%1.3f')



def NumDep(puf):
    global c59660
    #Number of dependents for puf_dict['EIC'] 

    EICYB1_1 = np.where(puf_dict['EICYB1'] < 0, 0.0, puf_dict['EICYB1'])
    EICYB2_2 = np.where(puf_dict['EICYB2'] < 0, 0.0, puf_dict['EICYB2'])
    EICYB3_3 = np.where(puf_dict['EICYB3'] < 0, 0.0, puf_dict['EICYB3'])

    _ieic = np.where(puf == True, puf_dict['EIC'], EICYB1_1 + EICYB2_2 + EICYB3_3)

    _ieic = _ieic.astype(int)

    print(_ieic)
    print(_ieic.dtype)

<<<<<<< HEAD
	#Modified AGI only through 2002 
=======

    #Modified AGI only through 2002 

    _modagi = c00100 + puf_dict['e00400']
>>>>>>> 895f5863d50db2a04fa6872c0d66355c11140c20

    _val_ymax = np.where(np.logical_and(puf_dict['MARS'] == 2, _modagi > 0), planX['ymax'][_ieic-1, puf_dict['FLPDYR']-2013] + planX['joint'][puf_dict['FLPDYR']-2013], 0)
    _val_ymax = np.where(np.logical_and(_modagi > 0, np.logical_or(puf_dict['MARS'] == 1, np.logical_or(puf_dict['MARS'] == 4, np.logical_or(puf_dict['MARS'] == 5, puf_dict['MARS'] == 7)))), planX['ymax'][_ieic-1, puf_dict['FLPDYR']-2013], _val_ymax)
    c59660 = np.where(np.logical_and(_modagi > 0, np.logical_or(puf_dict['MARS'] == 1, np.logical_or(puf_dict['MARS'] == 4, np.logical_or(puf_dict['MARS'] == 5, np.logical_or(puf_dict['MARS'] == 2, puf_dict['MARS'] == 7))))), np.minimum(planX['rtbase'][_ieic-1, puf_dict['FLPDYR']-2013] * c59560, planX['crmax'][_ieic-1, puf_dict['FLPDYR']-2013]), c59560)
    _preeitc =  np.where(np.logical_and(_modagi > 0, np.logical_or(puf_dict['MARS'] == 1, np.logical_or(puf_dict['MARS'] == 4, np.logical_or(puf_dict['MARS'] == 5, np.logical_or(puf_dict['MARS'] == 2, puf_dict['MARS'] == 7))))), c59660, 0)

<<<<<<< HEAD
	_val_ymax = np.where(np.logical_and(MARS == 2, _modagi > 0), _ymax[_ieic, FLPDYR-2013] + _joint[FLPDYR-2013], 0)
	_val_ymax = np.where(np.logical_and(_modagi > 0, np.logical_or(MARS == 1, np.logical_or(MARS == 4, np.logical_or(MARS == 5, MARS == 7)))), _ymax[_ieic, FLPDYR-2013], _val_ymax)
	c59660 = np.where(np.logical_and(_modagi > 0, np.logical_or(MARS == 1, np.logical_or(MARS == 4, np.logical_or(MARS == 5, np.logical_or(MARS == 2, MARS == 7))))), np.minimum(_rtbase[_ieic, FLPDYR-2013] * c59560, _crmax[_ieic, FLPDYR-2013]), c59660)
	_preeitc =  np.where(np.logical_and(_modagi > 0, np.logical_or(MARS == 1, np.logical_or(MARS == 4, np.logical_or(MARS == 5, np.logical_or(MARS == 2, MARS == 7))))), c59660, 0)

	c59660 = np.where(np.logical_and(np.logical_and(MARS != 3, MARS != 6), np.logical_and(_modagi > 0, np.logical_or(_modagi > _val_ymax, c59560 > _val_ymax))), np.maximum(0, c59660 - _rtless[_ieic, FLPDYR-2013] * (np.maximum(_modagi, c59560) - _val_ymax)), c59660)
	_val_rtbase = np.where(np.logical_and(np.logical_and(MARS != 3, MARS != 6), _modagi > 0), _rtbase[_ieic, FLPDYR-2013] * 100, 0)
	_val_rtless = np.where(np.logical_and(np.logical_and(MARS != 3, MARS != 6), _modagi > 0), _rtless[_ieic, FLPDYR-2013] * 100, 0)
=======
    c59660 = np.where(np.logical_and(np.logical_and(puf_dict['MARS'] != 3, puf_dict['MARS'] != 6), np.logical_and(_modagi > 0, np.logical_or(_modagi > _val_ymax, c59560 > _val_ymax))), np.maximum(0, c59660 - planX['rtless'][_ieic-1, puf_dict['FLPDYR']-2013] * (np.maximum(_modagi, c59560) - _val_ymax)), c59560)
    _val_rtbase = np.where(np.logical_and(np.logical_and(puf_dict['MARS'] != 3, puf_dict['MARS'] != 6), _modagi > 0), planX['rtbase'][_ieic-1, puf_dict['FLPDYR']-2013] * 100, 0)
    _val_rtless = np.where(np.logical_and(np.logical_and(puf_dict['MARS'] != 3, puf_dict['MARS'] != 6), _modagi > 0), planX['rtless'][_ieic-1, puf_dict['FLPDYR']-2013] * 100, 0)

    _dy = np.where(np.logical_and(np.logical_and(puf_dict['MARS'] != 3, puf_dict['MARS'] != 6), _modagi > 0), puf_dict['e00400'] + puf_dict['e83080'] + puf_dict['e00300'] + puf_dict['e00600'] 
        + np.maximum(0, np.maximum(0, puf_dict['e01000']) - np.maximum(0, puf_dict['e40223']))
        + np.maximum(0, np.maximum(0, puf_dict['e25360']) - puf_dict['e25430'] - puf_dict['e25470'] - puf_dict['e25400'] - puf_dict['e25500'])
        + np.maximum(0, puf_dict['e26210'] + puf_dict['e26340'] + puf_dict['e27200'] - np.absolute(puf_dict['e26205']) - np.absolute(puf_dict['e26320'])), 0)
>>>>>>> 895f5863d50db2a04fa6872c0d66355c11140c20

    c59660 = np.where(np.logical_and(np.logical_and(puf_dict['MARS'] != 3, puf_dict['MARS'] != 6), np.logical_and(_modagi > 0, _dy > planX['dylim'][puf_dict['FLPDYR']-2013])), 0, c59660)

    c59660 = np.where(np.logical_and(np.logical_and(puf_dict['cmp'] == 1, _ieic == 0), np.logical_and(np.logical_and(puf_dict['SOIYR'] - puf_dict['DOBYR'] >= 25, puf_dict['SOIYR'] - puf_dict['DOBYR'] < 65), np.logical_and(puf_dict['SOIYR'] - puf_dict['SDOBYR'] >= 25, puf_dict['SOIYR'] - puf_dict['SDOBYR'] < 65))), 0, c59660)
    c59660 = np.where(np.logical_and(_ieic == 0, np.logical_or(np.logical_or(_agep < 25, _agep >= 65), np.logical_or(_ages < 25, _ages >= 65))), 0, c59660)

	outputs = (_ieic, EICYB1, EICYB2, EICYB3, _modagi, c59660, _val_ymax, _preeitc, _val_rtbase, _val_rtless, _dy)
	output = np.column_stack(outputs)
	np.savetxt('NumDep.csv', output, delimiter=',', 
		header = ('_ieic, EICYB1, EICYB2, EICYB3, _modagi, c59660, _val_ymax, _preeitc, _val_rtbase, _val_rtless, _dy') 
		, fmt = '%1.3f')



def ChildTaxCredit():
<<<<<<< HEAD
	global _num
	global c07230
	global _precrd
	global _nctcr
	global c07220
	#Child Tax Credit

	c11070 = np.zeros((dim,))
	c07220 = np.zeros((dim,))
	c07230 = np.zeros((dim,))
	_precrd = np.zeros((dim,))


	_num = np.ones((dim,))
	_num = np.where(MARS == 2, 2, _num)

	_nctcr = np.zeros((dim,))
	_nctcr = np.where(SOIYR >= 2002, n24, _nctcr)
	_nctcr = np.where(np.logical_and(SOIYR < 2002, _chmax[FLPDYR-2013] > 0), xtxcr1xtxcr10, _nctcr)
	_nctcr = np.where(np.logical_and(SOIYR < 2002, _chmax[FLPDYR-2013] <= 0), XOCAH, _nctcr)

	_precrd = _chmax[FLPDYR-2013] * _nctcr 
	_ctcagi = c00100 + _feided
=======
    global _num
    global c07230
    global _precrd
    global _nctcr
    #Child Tax Credit
    #This var actually gets used in nonedcredit and c1040
    c07230 = DIMARRAY

    _num = np.where(puf_dict['MARS'] == 2, 2, 1)

    _nctcr = puf_dict['n24']

    _precrd = planX['chmax'][puf_dict['FLPDYR']-2013] * _nctcr 
    _ctcagi = puf_dict['e00100'] + _feided
>>>>>>> 895f5863d50db2a04fa6872c0d66355c11140c20

    _precrd = np.where(np.logical_and(_ctcagi > planX['cphase'][puf_dict['MARS']-1], puf_dict['exact'] == 1), np.maximum(0, _precrd - 50 * np.ceil(np.maximum(0, _ctcagi - planX['cphase'][puf_dict['MARS']-1])/1000)), 0)
    _precrd = np.where(np.logical_and(_ctcagi > planX['cphase'][puf_dict['MARS']-1], puf_dict['exact'] != 1), np.maximum(0, _precrd - 50 * (np.maximum(0, _ctcagi - planX['cphase'][puf_dict['MARS']-1]) + 500)/1000), _precrd)

	outputs = (c11070, c07220, c07230, _precrd, _num, _nctcr, _precrd, _ctcagi)
	output = np.column_stack(outputs)
	np.savetxt('ChildTaxCredit.csv', output, delimiter=',', 
		header = ('c11070, c07220, c07230, _precrd, _num, _nctcr, _precrd, _ctcagi') 
		, fmt = '%1.3f')
#def HopeCredit():
    #Hope credit for 1998-2009, I don't think this is needed 
    #Leave blank for now, ask Dan
    #SAS lnies 951 - 972

def AmOppCr():
    global c87521
    #American Opportunity Credit 2009+ 
    c87482 = np.where(puf_dict['cmp'] == 1, np.maximum(0, np.minimum(puf_dict['e87482'], 4000)), 0)
    c87487 = np.where(puf_dict['cmp'] == 1, np.maximum(0, np.minimum(puf_dict['e87487'], 4000)), 0)
    c87492 = np.where(puf_dict['cmp'] == 1, np.maximum(0, np.minimum(puf_dict['e87492'], 4000)), 0)
    c87497 = np.where(puf_dict['cmp'] == 1, np.maximum(0, np.minimum(puf_dict['e87497'], 4000)), 0)

    c87483 = np.where(np.maximum(0, c87482 - 2000) == 0, c87482, 2000 + 0.25 * np.maximum(0, c87482 - 2000))
    c87488 = np.where(np.maximum(0, c87487 - 2000) == 0, c87487, 2000 + 0.25 * np.maximum(0, c87487 - 2000))
    c87493 = np.where(np.maximum(0, c87492 - 2000) == 0, c87492, 2000 + 0.25 * np.maximum(0, c87492 - 2000))
    c87498 = np.where(np.maximum(0, c87497 - 2000) == 0, c87497, 2000 + 0.25 * np.maximum(0, c87497 - 2000))

    c87521 = c87483 + c87488 + c87493 + c87498

	outputs = (c87482, c87487, c87492, c87497, c87483, c87488, c87493, c87498, c87521)
	output = np.column_stack(outputs)
	np.savetxt('AmOppCr.csv', output, delimiter=',', 
		header = ('c87482, c87487, c87492, c87497, c87483, c87488, c87493, c87498, c87521') 
		, fmt = '%1.3f')

def LLC(puf):
    #Lifetime Learning Credit
    global c87550

    c87540 = np.where(puf == True, np.minimum(puf_dict['e87530'], planX['learn'][puf_dict['FLPDYR']-2013]), 0)
    c87550 = np.where(puf == True, 0.2 * c87540, 0)

    c87530 = np.where(puf == False, puf_dict['e87526'] + puf_dict['e87522'] + puf_dict['e87524'] + puf_dict['e87528'], 0)
    c87540 = np.where(puf == False, np.minimum(c87530, planX['learn'][puf_dict['FLPDYR']-2013]), c87540)
    c87550 = np.where(puf == False, 0.2 * c87540, c87550)

	outputs = (c87540, c87550, c87530)
	output = np.column_stack(outputs)
	np.savetxt('LLC.csv', output, delimiter=',', 
		header = ('c87540, c87550, c87530') 
		, fmt = '%1.3f')

def RefAmOpp():
    #Refundable American Opportunity Credit 2009+

    c87654 = np.where(np.logical_and(puf_dict['cmp'] == 1, c87521 > 0), 90000 * _num, 0)
    c87656 = np.where(np.logical_and(puf_dict['cmp'] == 1, c87521 > 0), c00100, 0)
    c87658 = np.where(np.logical_and(puf_dict['cmp'] == 1, c87521 > 0), np.maximum(0, c87654 - c87656), 0)
    c87660 = np.where(np.logical_and(puf_dict['cmp'] == 1, c87521 > 0), 10000 * _num, 0)
    c87662 = np.where(np.logical_and(puf_dict['cmp'] == 1, c87521 > 0), 1000 * np.minimum(1, c87658/c87660), 0)
    c87664 = np.where(np.logical_and(puf_dict['cmp'] == 1, c87521 > 0), c87662 * c87521/1000, 0)
    c87666 = np.where(np.logical_and(puf_dict['cmp'] == 1, np.logical_and(c87521 > 0, puf_dict['EDCRAGE'] == 1)), 0, 0.4 * c87664)
    c10960 = np.where(np.logical_and(puf_dict['cmp'] == 1, c87521 > 0), c87666, 0)
    c87668 = np.where(np.logical_and(puf_dict['cmp'] == 1, c87521 > 0), c87664 - c87666, 0)
    c87681 = np.where(np.logical_and(puf_dict['cmp'] == 1, c87521 > 0), c87666, 0)

	outputs = (c87654, c87656, c87658, c87660, c87662, c87664, c87666, c10960, c87668, c87681)
	output = np.column_stack(outputs)
	np.savetxt('RefAmOpp.csv', output, delimiter=',', 
		header = ('c87654, c87656, c87658, c87660, c87662, c87664, c87666, c10960, c87668, c87681') 
		, fmt = '%1.3f')


def NonEdCr(c87550):
<<<<<<< HEAD
	global c07220
	#Nonrefundable Education Credits

	#Form 8863 Tentative Education Credits
	c87560 = c87550

	#Phase Out
	c87570 = np.where(MARS == 2, _edphhm[FLPDYR-2013] * 1000, _edphhs[FLPDYR-2013] * 1000)
	c87580 = c00100
	c87590 = np.maximum(0, c87570 - c87580)
	c87600 = 10000 * _num
	c87610 = np.minimum(1, c87590/c87600)
	c87620 = c87560 * c87610

	_ctc1 = c07180 + e07200 + c07230
	_ctc2 = np.zeros((dim,))

	_ctc2 = e07240 + e07960 + e07260 + e07300
	_regcrd = _ctc1 + _ctc2
	_exocrd = e07700 + e07250
	_exocrd = _exocrd + t07950 
	_ctctax = c05800 - _regcrd - _exocrd
	c07220 = np.minimum(_precrd, np.maximum(0, _ctctax)) 
	#lt tax owed
=======
    global c07220
    #Nonrefundable Education Credits

    #Form 8863 Tentative Education Credits
    c87560 = c87550

    #Phase Out
    c87570 = np.where(puf_dict['MARS'] == 2, planX['edphhm'][puf_dict['FLPDYR']-2013] * 1000, planX['edphhs'][puf_dict['FLPDYR']-2013] * 1000)
    c87580 = c00100
    c87590 = np.maximum(0, c87570 - c87580)
    c87600 = 10000 * _num
    c87610 = np.minimum(1, c87590/c87600)
    c87620 = c87560 * c87610

    _ctc1 = c07180 + puf_dict['e07200'] + c07230

    _ctc2 = puf_dict['e07240'] + puf_dict['e07960'] + puf_dict['e07260']
    _regcrd = _ctc1 + _ctc2
    _exocrd = puf_dict['e07700'] + puf_dict['e07250']
    _exocrd = _exocrd + puf_dict['t07950'] 
    _ctctax = c05800 - _regcrd - _exocrd
    c07220 = np.minimum(_precrd, np.maximum(0, _ctctax)) 
    #lt tax owed
>>>>>>> 895f5863d50db2a04fa6872c0d66355c11140c20

	outputs = (c87560, c87570, c87580, c87590, c87600, c87610, c87620, _ctc1, _ctc2, _regcrd, _exocrd, _ctctax, c07220)
	output = np.column_stack(outputs)
	np.savetxt('NonEdCr.csv', output, delimiter=',', 
		header = ('c87560, c87570, c87580, c87590, c87600, c87610, c87620, _ctc1, _ctc2, _regcrd, _exocrd, _ctctax, c07220') 
		, fmt = '%1.3f')

def AddCTC(puf):
    #Additional Child Tax Credit

    #Part I of 2005 form 8812
    c82925 = np.where(_nctcr > 0, _precrd, 0)
    c82930 = np.where(_nctcr > 0, c07220, 0)
    c82935 = np.where(_nctcr > 0, c82925 - c82930, 0)
    #CTC not applied to tax

    c82880 = np.where(_nctcr > 0, np.maximum(0, puf_dict['e00200'] + puf_dict['e82882'] + puf_dict['e30100'] + np.maximum(0, _sey) - 0.5 * _setax), 0)
    c82880 = np.where(np.logical_and(_nctcr > 0, puf_dict['exact'] == 1), puf_dict['e82880'], c82880)
    h82880 = np.where(_nctcr > 0, c82880, 0)
    c82885 = np.where(_nctcr > 0, np.maximum(0, c82880 - planX['ealim'][puf_dict['FLPDYR']-2013]), 0)
    c82890 = np.where(_nctcr > 0, planX['adctcrt'][puf_dict['FLPDYR']-2013] * c82885, 0)

    #Part II of 2005 form 8812
    c82900 = np.where(np.logical_and(_nctcr > 2, c82890 < c82935), 0.0765 * np.minimum(planX['ssmax'][puf_dict['FLPDYR']-2013], c82880), 0)
    c82905 = np.where(np.logical_and(_nctcr > 2, c82890 < c82935), puf_dict['e03260'] + puf_dict['e09800'], 0)
    c82910 = np.where(np.logical_and(_nctcr > 2, c82890 < c82935), c82900 + c82905, 0)
    c82915 = np.where(np.logical_and(_nctcr > 2, c82890 < c82935), c59660 + puf_dict['e11200'], 0)
    c82920 = np.where(np.logical_and(_nctcr > 2, c82890 < c82935), np.maximum(0, c82910 - c82915), 0)
    c82937 = np.where(np.logical_and(_nctcr > 2, c82890 < c82935), np.maximum(c82890, c82920), 0)

<<<<<<< HEAD
	#Part II of 2005 form 8812
	c82940 = np.where(np.logical_and(_nctcr > 2, c82890 >= c82935), c82935, c82940)
	c82940 = np.where(np.logical_and(_nctcr > 2, c82890 < c82935), np.minimum(c82935, c82937), c82940)

	c11070 = np.where(_nctcr > 0, c82940, 0)

	e59660 = np.where(np.logical_and(puf == True, _nctcr > 0), e59680 + e59700 + e59720, 0)
	_othadd = np.where(_nctcr > 0, e11070 - c11070, 0)

	c11070 = np.where(np.logical_and(_nctcr > 0, _fixup >= 4), c11070 + _othadd, c11070)

	outputs = (c82940, c82925, c82930, c82935, c82880, h82880, c82885, c82890, c82900, c82905, c82910, c82915, c82920, c82937, c82940, c11070, e59660, _othadd)
	output = np.column_stack(outputs)
	np.savetxt('AddCTC.csv', output, delimiter=',', 
		header = ('c82940, c82925, c82930, c82935, c82880, h82880, c82885, c82890, c82900, c82905, c82910, c82915, c82920, c82937, c82940, c11070, e59660, _othadd') 
		, fmt = '%1.3f')
=======
    #Part II of 2005 form 8812
    c82940 = np.where(np.logical_and(_nctcr <= 2, c82890 > 0), np.minimum(c82890, c82935), c82890)
    c82940 = np.where(np.logical_and(_nctcr > 2, c82890 >= c82935), c82935, c82940)
    c82940 = np.where(np.logical_and(_nctcr > 2, c82890 < c82935), np.minimum(c82935, c82937), c82940)

    c11070 = c82940

    e59660 = np.where(puf == True, puf_dict['e59680'] + puf_dict['e59700'] + puf_dict['e59720'], 0)
    _othadd = puf_dict['e11070'] - c11070

    c11070 = np.where(puf_dict['fixup'] >= 4, c11070 + _othadd, c11070)

    # if c11070 eq 0 then do over _a8812; _a8812 = 0;end;
    # What does this line mean? -- Ask Dan
>>>>>>> 895f5863d50db2a04fa6872c0d66355c11140c20

# def F5405():
    #Form 5405 First-Time Homebuyer Credit
    #not needed

<<<<<<< HEAD
	c64450 = np.zeros((dim,))
	outputs = (c64450)
	output = np.column_stack(outputs)
	np.savetxt('F4505.csv', c64450, delimiter=',', 
		header = ('c64450') 
		, fmt = '%1.3f')
=======
    # c64450 = DIMARRAY
>>>>>>> 895f5863d50db2a04fa6872c0d66355c11140c20

def C1040(puf):
    global c08795
    global c09200
    global c07100 
    global _eitc
    #Credits 1040 line 48

<<<<<<< HEAD
	x07400 = e07400
	c07100 = (e07180 + e07200 + c07220 + c07230 + e07250 
		+ e07600 + e07260 + c07970 + e07300 + x07400 
		+ e07500 + e07700 + e08000)
=======
    c07100 = puf_dict['e07180'] + puf_dict['e07200'] + c07220 + c07230 + puf_dict['e07250'] + puf_dict['e07600'] + puf_dict['e07600'] + puf_dict['e07260'] + c07970 + puf_dict['e07300'] + puf_dict['x07400'] + puf_dict['e07500'] + puf_dict['e07700'] + puf_dict['e08000']
>>>>>>> 895f5863d50db2a04fa6872c0d66355c11140c20

    y07100 = c07100

<<<<<<< HEAD
	c07100 = c07100 + e07240
	c07100 = c07100 + e08001
	c07100 = c07100 + e07960 + e07970
	c07100 = np.where(SOIYR >= 2009, c07100 + e07980, c07100)
=======
    c07100 = c07100 + puf_dict['e07240']
    c07100 = c07100 + puf_dict['e08001']
    c07100 = c07100 + puf_dict['e07960'] + puf_dict['e07970']
    c07100 = c07100 + puf_dict['e07980']
>>>>>>> 895f5863d50db2a04fa6872c0d66355c11140c20

    x07100 = c07100
    c07100 = np.minimum(c07100, c05800)

    #Tax After credits 1040 line 52

    _eitc = c59660
    c08795 = np.maximum(0, c05800 - c07100)

    c08800 = c08795
    e08795 = np.where(puf == True, puf_dict['e08800'], 0)

    #Tax before refundable credits

    c09200 = c08795 + puf_dict['e09900'] + puf_dict['e09400'] + puf_dict['e09800'] + puf_dict['e10000'] + puf_dict['e10100']
    c09200 = c09200 + puf_dict['e09700']
    c09200 = c09200 + puf_dict['e10050']
    c09200 = c09200 + puf_dict['e10075']
    c09200 = c09200 + puf_dict['e09805']
    c09200 = c09200 + puf_dict['e09710'] + puf_dict['e09720']

	outputs = (c07100, y07100, x07100, c08795, c08800, e08795, c09200)
	output = np.column_stack(outputs)
	np.savetxt('C1040.csv', output, delimiter=',', 
		header = ('c07100, y07100, x07100, c08795, c08800, e08795, c09200') 
		, fmt = '%1.3f')

def DEITC():
    global c59700
    #check this variable
    global c10950 
    c10950 = DIMARRAY
    #Decomposition of EITC 

    c59680 = np.where(np.logical_and(c08795 > 0, np.logical_and(c59660 > 0, c08795 <= c59660)), c08795, 0)
    _comb = np.where(np.logical_and(c08795 > 0, np.logical_and(c59660 > 0, c08795 <= c59660)), c59660 - c59680, 0)

    c59680 = np.where(np.logical_and(c08795 > 0, np.logical_and(c59660 > 0, c08795 > c59660)), c59660, c59680)
    _comb = np.where(np.logical_and(c08795 > 0, np.logical_and(c59660 > 0, c08795 > c59660)), 0, _comb)

    c59700 = np.where(np.logical_and(c08795 > 0, np.logical_and(c59660 > 0, np.logical_and(_comb > 0, np.logical_and(c09200 - c08795 > 0, c09200 - c08795 > _comb)))), _comb, 0)
    c59700 = np.where(np.logical_and(c08795 > 0, np.logical_and(c59660 > 0, np.logical_and(_comb > 0, np.logical_and(c09200 - c08795 > 0, c09200 - c08795 <= _comb)))), c09200 - c08795, c59700)
    c59720 = np.where(np.logical_and(c08795 > 0, np.logical_and(c59660 > 0, np.logical_and(_comb > 0, np.logical_and(c09200 - c08795 > 0, c09200 - c08795 <= _comb)))), c59660 - c59680 - c59700, 0)

<<<<<<< HEAD
	c59680 = np.where(np.logical_and(c08795 == 0, c59660 > 0), 0, c59680)
	c59700 = np.where(np.logical_and(c08795 == 0, np.logical_and(c59660 > 0, np.logical_and(c09200 > 0, c09200 > c59660))), c59660, c59700)
	c59700 = np.where(np.logical_and(c08795 == 0, np.logical_and(c59660 > 0, np.logical_and(c09200 > 0, c09200 < c59660))), c09200, c59700)
	c59720 = np.where(np.logical_and(c08795 == 0, np.logical_and(c59660 > 0, np.logical_and(c09200 > 0, c09200 < c59660))), c59660 - c59700, c59720)
	c59720 = np.where(np.logical_and(c08795 == 0, np.logical_and(c59660 > 0, c09200 <= 0)), c59660 - c59700, c59720)
=======
    c59680 = np.where(np.logical_and(c08795 == 0, c59660 > 0), 0, c59680)
    c59700 = np.where(np.logical_and(c08795 == 0, np.logical_and(c59660 > 0, np.logical_and(c09200 > 0, c09200 > c59660))), c59660, c59700)
    c59700 = np.where(np.logical_and(c08795 == 0, np.logical_and(c59660 > 0, c09200 <= 0)), c09200, c59700)
    c59720 = np.where(np.logical_and(c08795 == 0, np.logical_and(c59660 > 0, c09200 <= 0)), c59660 - c59700, c59720)
>>>>>>> 895f5863d50db2a04fa6872c0d66355c11140c20

    #Ask dan about this section of code! Line 1231 - 1241

<<<<<<< HEAD
	_compb = np.where(np.logical_or(c08795 < 0, c59660 <= 0), 0, 0)
	c59680 = np.where(np.logical_or(c08795 < 0, c59660 <= 0), 0, c59680)
	c59700 = np.where(np.logical_or(c08795 < 0, c59660 <= 0), 0, c59700)
	c59720 = np.where(np.logical_or(c08795 < 0, c59660 <= 0), 0, c59720)
=======
    _compb = np.where(np.logical_and(c08795 <= 0, c59660 <= 0), 0, 0)
    c59680 = np.where(np.logical_and(c08795 <= 0, c59660 <= 0), 0, c59680)
    c59700 = np.where(np.logical_and(c08795 <= 0, c59660 <= 0), 0, c59700)
    c59720 = np.where(np.logical_and(c08795 <= 0, c59660 <= 0), 0, c59720)
>>>>>>> 895f5863d50db2a04fa6872c0d66355c11140c20

    c07150 = c07100 + c59680
    c07150 = c07150

	outputs = (c59680, c59700, c59720, _comb, c07150, c10950)
	output = np.column_stack(outputs)
	np.savetxt('DEITC.csv', output, delimiter=',', 
		header = ('c59680, c59700, c59720, _comb, c07150, c10950') 
		, fmt = '%1.3f')

def SOIT(_eitc):
<<<<<<< HEAD
	_eitc = _eitc

	#SOI Tax (Tax after non-refunded credits plus tip penalty)
	c10300 = c09200 - e10000 - e59680 - c59700
	c10300 = c10300 - e11070
	c10300 = c10300 - e11550
	c10300 = c10300 - e11580
	c10300 = c10300 - e09710 - e09720 - e11581 - e11582
	c10300 = c10300 - e87900 - e87905 - e87681 - e87682
	c10300 = c10300 - c10300 - c10950 - e11451 - e11452
	c10300 = c09200 - e09710 - e09720 - e10000 - e11601 - e11602
	c10300 = np.maximum(c10300 , 0)

	#Ignore refundable partof _eitc to obtain SOI income tax

	_eitc = np.where(c09200 <= _eitc, c09200, _eitc)
	c10300 = np.where(c09200 <= _eitc, 0, c10300)

	outputs = (c10300, _eitc)
	output = np.column_stack(outputs)
	np.savetxt('SOIT.csv', output, delimiter=',', 
		header = ('c10300, _eitc') 
		, fmt = '%1.3f')




def Taxer(inc_in, inc_out, MARS):
	low = np.where(inc_in < 3000, 1, 0)
	med = np.where(np.logical_and(inc_in >= 3000, inc_in < 100000), 1, 0)

	_a1 = inc_in * 0.01
	_a2 = np.floor(_a1)
	_a3 = _a2*100
	_a4 = (_a1 - _a2) * 100

	_a5 = np.zeros((dim,))
	_a5 = np.where(np.logical_and(low == 1, _a4 < 25), 13, _a5)
	_a5 = np.where(np.logical_and(low == 1, np.logical_and(_a4 >= 25, _a4 < 50)), 38, _a5)
	_a5 = np.where(np.logical_and(low == 1, np.logical_and(_a4 >= 50, _a4 < 75)), 63, _a5)
	_a5 = np.where(np.logical_and(low == 1, _a4 >= 75), 88, _a5)

	_a5 = np.where(np.logical_and(med == 1, _a4 < 50), 25, _a5)
	_a5 = np.where(np.logical_and(med == 1, _a4 >= 50), 75, _a5)

	_a5 = np.where(inc_in == 0, 0, _a5)

	_a6 = np.where(np.logical_or(low==1, med ==1), _a3 + _a5, inc_in)

	_a6 = inc_in

	inc_out = (_rt1[FLPDYR-2013] * np.minimum(_a6, _brk1[FLPDYR-2013, MARS-1])
		+ _rt2[FLPDYR-2013] 
		* np.minimum(_brk2[FLPDYR-2013, MARS-1] - _brk1[FLPDYR-2013, MARS-1],
			np.maximum(0., _a6 - _brk1[FLPDYR-2013, MARS-1]))
		+ _rt3[FLPDYR-2013]
		* np.minimum(_brk3[FLPDYR-2013, MARS-1] - _brk2[FLPDYR-2013, MARS-1],
			np.maximum(0., _a6 - _brk2[FLPDYR-2013, MARS-1]))
		+ _rt4[FLPDYR-2013]
		* np.minimum(_brk4[FLPDYR-2013, MARS-1] - _brk3[FLPDYR-2013, MARS-1],
			np.maximum(0., _a6 - _brk3[FLPDYR-2013, MARS-1]))
		+ _rt5[FLPDYR-2013]
		* np.minimum(_brk5[FLPDYR-2013, MARS-1] - _brk4[FLPDYR-2013, MARS-1],
			np.maximum(0., _a6 - _brk4[FLPDYR-2013, MARS-1]))
		+ _rt6[FLPDYR-2013]
		* np.minimum(_brk6[FLPDYR-2013, MARS-1] - _brk5[FLPDYR-2013, MARS-1],
			np.maximum(0., _a6 - _brk5[FLPDYR-2013, MARS-1]))
		+ _rt7[FLPDYR-2013] * np.maximum(0., _a6 -_brk6[FLPDYR-2013, MARS-1]))

	return inc_out


def Test(puf):
	if puf == True:
		Puf()
	FilingStatus()
	Adj()
	CapGains()
	SSBenefits()
	AGI()
	ItemDed(puf)
	EI_FICA()
	StdDed()
	XYZD()
	NonGain()
	TaxGains()
	MUI(c05750 = c05750)
	AMTI(puf)
	F2441(puf, _earned = _earned)
	DepCareBen(c32800 = c32800)
	ExpEarnedInc()
	RateRed(c05800 = c05800)
	NumDep(puf)
	ChildTaxCredit()
	AmOppCr()
	LLC(puf)
	RefAmOpp()
	NonEdCr(c87550 = c87550)
	AddCTC(puf)
	F5405()
	C1040(puf)
	DEITC()
	SOIT(_eitc = _eitc)



=======
    _eitc = _eitc

    #SOI Tax (Tax after non-refunded credits plus tip penalty)
    c10300 = c09200 - puf_dict['e10000'] - puf_dict['e59680'] - c59700
    c10300 = c10300 - puf_dict['e11070']
    c10300 = c10300 - puf_dict['e11550']
    c10300 = c10300 - puf_dict['e11580']
    c10300 = c10300 - puf_dict['e09710'] - puf_dict['e09720'] - puf_dict['e11581'] - puf_dict['e11582']
    c10300 = c10300 - puf_dict['e87900'] - puf_dict['e87905'] - puf_dict['e87681'] - puf_dict['e87682']
    c10300 = c10300 - c10300 - c10950 - puf_dict['e11451'] - puf_dict['e11452']
    c10300 = c09200 - puf_dict['e09710'] - puf_dict['e09720'] - puf_dict['e10000'] - puf_dict['e11601'] - puf_dict['e11602']
    c10300 = np.maximum(c10300 , 0)

    #Ignore refundable partof _eitc to obtain SOI income tax

    _eitc = np.where(c09200 <= _eitc, c09200, _eitc)
    c10300 = np.where(c09200 <= _eitc, 0, c10300)






def Taxer(inc_in, inc_out, mars):
    low = np.where(inc_in < 3000, 1, 0)
    med = np.where(np.logical_and(inc_in >= 3000, inc_in < 100000), 1, 0)

    _a1 = inc_in/100
    _a2 = np.floor(_a1)
    _a3 = _a2*100
    _a4 = (_a1 - _a2) * 100

    _a5 = np.where(np.logical_and(low == 1, _a4 < 25), 13, 0)
    _a5 = np.where(np.logical_and(low == 1, np.logical_and(_a4 >= 25, _a4 < 50)), 38, _a5)
    _a5 = np.where(np.logical_and(low == 1, np.logical_and(_a4 >= 50, _a4 < 75)), 63, _a5)
    _a5 = np.where(np.logical_and(low == 1, _a4 >= 75), 88, _a5)

    _a5 = np.where(np.logical_and(med == 1, _a4 < 50), 25, _a5)
    _a5 = np.where(np.logical_and(med == 1, _a4 >= 50), 75, _a5)

    _a5 = np.where(inc_in == 0, 0, _a5)

    _a6 = np.where(np.logical_or(low==1, med ==1), _a3 + _a5, inc_in)

    inc_out = (planX['rt1'][puf_dict['FLPDYR']-2013] * np.minimum(_a6, planX['brk1'][puf_dict['FLPDYR']-2013, mars-1])
        + planX['rt2'][puf_dict['FLPDYR']-2013] 
        * np.minimum(planX['brk2'][puf_dict['FLPDYR']-2013, mars-1] - planX['brk1'][puf_dict['FLPDYR']-2013, mars-1],
            np.maximum(0, _a6 - planX['brk1'][puf_dict['FLPDYR']-2013, mars-1]))
        + planX['rt3'][puf_dict['FLPDYR']-2013]
        * np.minimum(planX['brk3'][puf_dict['FLPDYR']-2013, mars-1] - planX['brk2'][puf_dict['FLPDYR']-2013, mars-1],
            np.maximum(0, _a6 - planX['brk2'][puf_dict['FLPDYR']-2013, mars-1]))
        + planX['rt4'][puf_dict['FLPDYR']-2013]
        * np.minimum(planX['brk4'][puf_dict['FLPDYR']-2013, mars-1] - planX['brk3'][puf_dict['FLPDYR']-2013, mars-1],
            np.maximum(0, _a6 - planX['brk3'][puf_dict['FLPDYR']-2013, mars-1]))
        + planX['rt5'][puf_dict['FLPDYR']-2013]
        * np.minimum(planX['brk5'][puf_dict['FLPDYR']-2013, mars-1] - planX['brk4'][puf_dict['FLPDYR']-2013, mars-1],
            np.maximum(0, _a6 - planX['brk4'][puf_dict['FLPDYR']-2013, mars-1]))
        + planX['rt6'][puf_dict['FLPDYR']-2013]
        * np.minimum(planX['brk6'][puf_dict['FLPDYR']-2013, mars-1] - planX['brk5'][puf_dict['FLPDYR']-2013, mars-1],
            np.maximum(0, _a6 - planX['brk5'][puf_dict['FLPDYR']-2013, mars-1]))
        + planX['rt7'][puf_dict['FLPDYR']-2013] * np.maximum(0, _a6 -planX['brk6'][puf_dict['FLPDYR']-2013, mars-1]))

    return inc_out


def write_out_csv(outputs, out_name):
    output = np.column_stack(outputs)

    np.savetxt('output.csv', output, delimiter=',', 
        header = ('_sep, _txp, _feided, c02900, _ymod, c02700, c02500, _posagi,' 
            'c00100, c04600, c04470, c21060, _earned, c04800, c60000, c05750') 
        , fmt = '%1.3f')


def write_out_json(outputs, out_name):
    out_labels = (
        '_sep', '_txp', '_feided', 'c02900', '_ymod', 'c02700', 'c02500', 
        '_posagi','c00100', 'c04600', 'c04470', 'c21060', '_earned', 'c04800',
         'c60000', 'c05750')
    out_dict = dict(zip(out_labels, outputs))
    with open(out_name, 'w') as out_file:
        json_io.dump(out_dict, out_file, cls=json_io.NumpyArrayJSON, indent=1)


def Test(deficient_puf, puf_dict):
    if deficient_puf:
        puf_dict = Puf(puf_dict)
    FilingStatus()
    Adj()
    CapGains()
    SSBenefits()
    AGI()
    ItemDed(deficient_puf)
    EI_FICA()
    StdDed()
    XYZD()
    NonGain()
    TaxGains()
    MUI(c05750 = c05750)
    AMTI(deficient_puf)
    F2441(deficient_puf, _earned = _earned)
    DepCareBen()
    ExpEarnedInc()
    RateRed(c05800 = c05800)
    NumDep(deficient_puf)
    ChildTaxCredit()
    AmOppCr()
    LLC(deficient_puf)
    RefAmOpp()
    NonEdCr(c87550 = c87550)
    AddCTC(deficient_puf)
    # F5405()
    C1040(deficient_puf)
    DEITC()
    SOIT(_eitc = _eitc)

    outputs = (_sep, _txp, _feided, c02900, _ymod, c02700, c02500, _posagi, 
        c00100, c04600, c04470, c21060, _earned, c04800, c60000, c05750)

    write_out_json(outputs, 'output.json')
    # write_out_csv(outputs, 'output.csv')



Test(True, puf_dict)
>>>>>>> 895f5863d50db2a04fa6872c0d66355c11140c20
