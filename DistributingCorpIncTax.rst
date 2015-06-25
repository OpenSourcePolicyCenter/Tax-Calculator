=============================================
Distributing the Corporate Income Tax in OSPC
=============================================
-------------
Maria Messick
-------------

The OSPC Tax-Calculator distributes the corporate income tax to individuals, both capital owners and wage earners. In the absence of this corporate income tax, both capital owners and wage earners would receive higher incomes; therefore, the Tax-Calculator imputes how much of the tax is borne by individuals, adding this to each individual’s expanded income measure. The Tax Policy Center allocates 40% to normal returns and 60% to supernormal returns. TPC then says that the burden on owners of capital that have normal returns can be shifted 50% to labor; therefore, TPC assigns 20% to labor, 20% to normal returns, and 60% to supernormal. However, the Joint Committee on Taxation does not distinguish between normal and supernormal returns to capital and thus allocates 75% of the burden to owners of domestic capital and 25% to wage earners. Where many tax calculators decide on a distribution amount to wage earners and capital owners, OSPC leaves this as a parameter open for the user to change to his/her preference. The OSPC allows a user to specify amount of burden allocated to normal and supernormal returns and then the user may allocate, separately, how the burden for normal and supernormal can be shifted to labor. OSPC assumes that these percentages are achieved in the long run and that the long run is completed at the end of the ten-year budget window, if the legislation is enacted in the first year. Since shifting the burden of the corporate income tax to labor is a long-term development, then in the short run, or year one of the budget window, all revenue from the tax is allocated to capital. Over the ten-year budget window, more and more of the burden in shifted to labor until at the end of the budget window, the given percentages are achieved[1]_.

The way OSPC accounts for the share of the corporate income tax borne by labor is first to calculate each individual’s compensation share. This is done by summing the individual’s wages, benefits given by the employer, and the untaxed voluntary contribution to his/her retirement plans[2]_ and dividing it by the aggregate compensation[3]_ people earn in the economy. Next, this compensation share is multiplied by the percent borne by labor and multiplied again by the aggregate revenue from the corporate income tax[4]_.  

The way OSPC accounts for the share of the corporate income tax borne by supernormal returns to capital is by taking the percent given to distribute to supernormal returns multiplied by the aggregate revenue collected from the tax multiplied by the sum of the individual’s share of the total of dividends in the market times 0.6 and the individual’s share of the capital gains in the market times 0.6[5]_. 

The way OSPC accounts for the share of the corporate income tax borne by normal returns to capital is by taking the percent given to distribute to normal returns multiplied by the aggregate revenue collected from the tax multiplied by the sum of the individual’s share of the total dividends in the domestic market times 0.4 and the individual’s share of the capital gains in the domestic market times 0.4 and the individual’s share of self-employment and pass-through income times 0.4 and the individual’s share of the bonds in the domestic market[6]_. 

OSPC’s model for labor is limited by lack of information regarding payroll taxes and benefits given by an individual’s employer. Currently, OSPC uses the sum of wages, employer provided benefit for dependent care, Archer MSA, and retirement savings contribution credit to determine an individual’s compensation, but this leaves many other factors out, such as employer’s contribution to health insurance and other contributions to retirement plans[7]_.  Limitations on share to capital come from OSPC’s lack of data regarding IRA holdings, 401(k) account ownership, and other self-employment and pass-through income. 

Say the United States collects $100 in corporate tax revenue one year and person 1 receives $60.34 in wages, $20.50 in pass-through income, $2.00 in dividends, $5.50 in net capital gains, and $34.20 in bond revenue in that year. Person 2 receives $82.30 in wages, $15.00 in pass-through income, $20.00 in dividends, $20.25 in net capital gains, and $13.70 in that year. For the purposes of this example, we make the assumption that 20% of the tax is distributed to labor, 20% to normal returns, and 60% to supernormal returns for that year. From this example and using the logic for distributing the corporate income tax outlined above, person 1 will bear 27.29% (8.46% for labor, 9.70% for normal returns, and 9.13% for supernormal returns) and person 2 will bear 72.71% (11.54% for labor, 10.30% for normal returns, and 50.87%) of the burden of the corporate income tax. Thus person 1 pays $27.29 and person 2 pays $72.71 of that $100 revenue.


..[1] Following assumptions made by the Joint Committee on Taxation.

..[2]This sum is calculated in the initialization for a Record object in records.py.

..[3]Aggregate compensation is calculated in the method aggregate_measures in calculate.py (along with all aggregate measures used).

..[4]Calculated in the method Dist_Corp_Inc_Tax in functions.py

..[5]This measure is modeled after that done by the JCT. Calculated in the method Dist_Corp_Inc_Tax in functions.py

..[6]Discernment between assets that have a certain percentage from normal returns and supernormal returns was adapted from the Tax Policy Center.

..[7]This measure is modeled after that done by the JCT. Calculated in the method Dist_Corp_Inc_Tax in functions.py
