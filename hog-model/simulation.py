import math

MAX_RATE = 5.0


class provider:

    def __init__(self):
        self.capital = 1000
        self.level = 1      #for conversion rate
        self.ad_policy = 1     #for ad budget
        self.inv_policy = 1
        self.position = 0
        self.size = 1       #for running costs
        self.inv_total = 0

        self.ad_budget = 0
        self.inv_budget = 0




    def calc_allocation(self):
        """
        :return: per round running costs, ad budget, investment
        """


    def get_conversion_rate(self):
        rate = (self.level + 1.0)/2.0
        return min(rate, MAX_RATE)


    def get_running_costs(self):
        return math.log(self.size * 10.0)


    def set_ad_budget(self):
        """
        default ad budget policy plus 1, so up to 11% of capital can be put toward ads
        :return:
        """
        ad = min(self.ad_policy, 10)
        return math.floor( ((ad+1.0)/100.0) * self.capital)


    def get_investment(self):
        inv = min(self.inv_policy, 10)
        return math.floor( ((inv+1.0)/100.0) * self.capital)

    def update(self):
        """

        :return:
        """


