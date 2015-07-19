""" OSPC Tax-Calculator taxcalc Parameters class.

PYLINT USAGE: pylint --disable=locally-disabled parameters.py
"""
from .utils import expand_array
import os
import json


DEFAULT_START_YEAR = 2013


class Parameters(object):
    """ Class that contains federal income tax parameters.
    """

    CUR_PATH = os.path.abspath(os.path.dirname(__file__))
    PARAM_FILENAME = "params.json"
    params_path = os.path.join(CUR_PATH, PARAM_FILENAME)


    # default inflation rates by year
    __rates = {2013:0.015, 2014:0.020, 2015:0.022, 2016:0.020, 2017:0.021,
               2018:0.022, 2019:0.023, 2020:0.024, 2021:0.024, 2022:0.024,
               2023:0.024, 2024:0.024}


    @classmethod
    def default_inflation_rate(cls, calyear):
        """ Return default inflation rate for specified calendar year.
        """
        return cls.__rates[calyear]


    @classmethod
    def from_file(cls, file_name, **kwargs):
        """ Read policy parameters from specified JSON file.
        """
        if file_name:
            with open(file_name) as pfile:
                params = json.loads(pfile.read())
        else:
            params = None
        return cls(data=params, **kwargs)


    def __init__(self, start_year=DEFAULT_START_YEAR, budget_years=12,
                 inflation_rate=None, inflation_rates=None, data=None):
        """ Parameters class constructor.
        """
        #pylint: disable=too-many-arguments

        if inflation_rate and inflation_rates:
            raise ValueError("Can only specify either one constant inflation"
                             " rate or a list of inflation rates")

        self._inflation_rates = None

        if inflation_rate:
            self._inflation_rates = [inflation_rate] * budget_years

        if inflation_rates:
            assert len(inflation_rates) == budget_years
            self._inflation_rates = [inflation_rates[start_year + i]
                                     for i in range(0, budget_years)]

        if not self._inflation_rates:
            self._inflation_rates = [self.__rates[start_year + i]
                                     for i in range(0, budget_years)]

        self._current_year = start_year
        self._start_year = start_year
        self._budget_years = budget_years

        if data:
            self._vals = data
        else:
            self._vals = default_data(metadata=True)

        # initialize parameter values
        for name, data in self._vals.items():
            cpi_inflated = data.get('cpi_inflated', False)
            values = data['value']
            setattr(self, name,
                    expand_array(values, inflate=cpi_inflated,
                                 inflation_rates=self._inflation_rates,
                                 num_years=budget_years))

        self.set_year(start_year)


    def update(self, year_mods):
        """Apply year_mods policy-parameter-reform dictionary to parameters.

        This method implements a policy reform, the provisions of
        which are specified in the year_mods dictionary, that changes
        the values of some policy parameters in this Parameters
        object.  This year_modes dictionary contains YEAR:MODS pairs,
        where the integer YEAR key indicates the calendar year for
        which the reform provisions in the MODS dictionary are
        implemented.  The MODS dictionary contains PARAM:VALUE pairs
        in which the PARAM is a string specifying the policy parameter
        (as used in the params.json default parameter file) and the
        VALUE is a Python list of of post-reform values for that
        PARAM.  Beginning in the year following the implementation of
        a reform provision, the parameter whose value has been changed
        by the reform continues to be inflation indexed or not be
        inflation indexed according to that parameter's cpi_inflated
        value in the params.json file.  But a reform can change the
        indexing status of a parameter by including in the MODS
        dictionary a PARAM_cpi:BOOLEAN pair that specifies the
        post-reform indexing status of the parameter.

        So, for example, to raise the OASDI (i.e., Old-Age, Survivors,
        and Disability Insurance) maximum taxable earnings beginning
        in 2018 to $500,000 and to continue indexing it in subsequent
        years as in current-law policy, the YEAR:MODS dictionary would
        be as follows:
        {2018: {"_SS_Earnings_c":[500000]}}.

        But to raise the maximum taxable earnings in 2018 to $500,000
        without any subsequent indexing in subsequent years, the
        YEAR:MODS dictionary would be as follows:
        {2018: {"_SS_Earnings_c":[500000], "_SS_Earnings_c_cpi":False}}.

        And to raise in 2018 the starting AGI for EITC phaseout for
        married filing jointly filing status (which can varies by
        number of children from zero to three of more and is inflation
        indexed), the YEAR:MODS dictionary would be as follows:
        {2018: {"_EITC_ps_MarriedJ":[8000, 8500, 9000, 9500]}}.

        Parameters
        ----------
        year_mods: dictionary of YEAR:MODS pairs

        Returns
        -------
        nothing

        """
        #pylint: disable=too-many-locals

        if not all(isinstance(key, int) for key in year_mods.keys()):
            raise ValueError("Every key must be a year, e.g. 2011, 2012, etc.")

        defaults = default_data(metadata=True)
        for year, mods in year_mods.items():

            num_years_to_expand = (self.start_year + self.budget_years) - year
            for name, values in mods.items():
                if name.endswith("_cpi"):
                    continue
                if name in defaults:
                    default_cpi = defaults[name].get('cpi_inflated', False)
                else:
                    default_cpi = False
                cpi_inflated = mods.get(name + "_cpi", default_cpi)

                if year == self.start_year and year == self.current_year:
                    nval = expand_array(values,
                                        inflate=cpi_inflated,
                                        inflation_rates=self._inflation_rates,
                                        num_years=num_years_to_expand)
                    setattr(self, name, nval)

                elif year <= self.current_year and year >= self.start_year:
                    # advance until parameters are in line with current year
                    offset_year = year - self.start_year
                    inf_rates = [self._inflation_rates[offset_year + i]
                                 for i in range(0, num_years_to_expand)]

                    nval = expand_array(values,
                                        inflate=cpi_inflated,
                                        inflation_rates=inf_rates,
                                        num_years=num_years_to_expand)

                    num_years_to_skip = self.current_year - year
                    if self.current_year > self.start_year:
                        cur_val = getattr(self, name)
                        offset = self.current_year - self.start_year
                        cur_val[offset:] = nval[num_years_to_skip:]
                    else:
                        setattr(self, name, nval[num_years_to_skip:])

                else: # year > current_year
                    msg = ("Can't specify a parameter for a year that is in"
                           " the future because we don't know how to fill in"
                           " the values for the years between {0} and {1}.")
                    raise ValueError(msg.format(self.current_year, year))

            # set up the '_X = [a, b,...]' variables as 'X = a'
            self.set_year(self._current_year)


    @property
    def current_year(self):
        """ Current policy parameter year property.
        """
        return self._current_year


    @property
    def start_year(self):
        """ First policy parameter year property.
        """
        return self._start_year


    @property
    def budget_years(self):
        """ Number of policy parameter years property.
        """
        return self._budget_years


    def increment_year(self):
        """ Move policy parameters to next year.
        """
        self._current_year += 1
        self.set_year(self._current_year)


    def set_year(self, year):
        """ Set policy parameters to values for specified year.
        """
        for name in self._vals:
            arr = getattr(self, name)
            setattr(self, name[1:], arr[year-self._start_year])


def default_data(metadata=False, start_year=None):
    """ Retrieve default parameters from default parameters file.
    """
    #pylint: disable=too-many-locals,too-many-branches

    if not os.path.exists(Parameters.params_path):
        from pkg_resources import resource_stream, Requirement
        path_in_egg = os.path.join("taxcalc", Parameters.PARAM_FILENAME)
        buf = resource_stream(Requirement.parse("taxcalc"), path_in_egg)
        _bytes = buf.read()
        as_string = _bytes.decode("utf-8")
        params = json.loads(as_string)
    else:
        with open(Parameters.params_path) as pfile:
            params = json.load(pfile)

    if start_year:
        for pdv in params.values(): # pdv = parameter dictionary value
            first_year = pdv.get('start_year', DEFAULT_START_YEAR)
            assert isinstance(first_year, int)

            if start_year < first_year:
                msg = "Can't set a start year of {0}, because it is before {1}"
                raise ValueError(msg.format(start_year, first_year))

            # set the new start year:
            pdv['start_year'] = start_year

            # work with the values
            vals = pdv['value']
            last_year_for_data = first_year + len(vals) - 1

            if last_year_for_data < start_year:
                if pdv['row_label']:
                    pdv['row_label'] = ["2015"]
                # need to produce new values
                new_val = vals[-1]
                if pdv['cpi_inflated'] is True:
                    for cyr in range(last_year_for_data, start_year):
                        ifactor = 1.0 + Parameters.default_inflation_rate(cyr)
                        if isinstance(new_val, list):
                            new_val = [x * ifactor for x in new_val]
                        else:
                            new_val *= ifactor
                # set the new values
                pdv['value'] = [new_val]

            else:
                # need to get rid of [first_year, ..., start_year-1] values
                years_to_chop = start_year - first_year
                if pdv['row_label']:
                    pdv['row_label'] = pdv['row_label'][years_to_chop:]
                pdv['value'] = pdv['value'][years_to_chop:]

    if metadata:
        return params
    else:
        return {key: val['value'] for key, val in params.items()}
