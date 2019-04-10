import numpy as np



class Providers(object):

    def __init__(self, num_providers, starting_capital=10000,profit=1.0, ad_percent=0.02):
        self.starting_capital = starting_capital
        self.running_costs = 2
        self.conversion_rate = 0.05 # percentage of clicks that turn into a sale
        self.profit = profit # amount of profit per conversion
        self.ad_percent = ad_percent # percent of capital that is allocated to the ad budget
        self.num_providers = num_providers
        self.capital = []
        self.cost = []
        self.cost_ratio = 0.01 # percent of costs incurred proportional to capital
        self._init_providers()


    def _init_providers(self):
        providers = list(range(1,self.num_providers))
        capital = np.add(np.multiply(np.multiply(np.ones(self.num_providers),self.starting_capital),np.random.rand(self.num_providers)),100)
        self.capital = np.multiply(np.divide(capital,np.sum(capital)),self.starting_capital)
        # assumes running costs are fixed every round
        costs = np.multiply(np.ones(self.num_providers), self.running_costs)
        self.costs = costs

    def _cap_budget(self, ad_budget):
        max1=0
        index1 = 0
        max2=0
        index2 = 0
        for i,value in enumerate(ad_budget):
            if value > max1:
                max2 = max1
                index2 = index1
                max1=value
                index1=i

        ad_budget[index1] = min(max2*2, max1)
        #ad_budget[index1] = max1
        return ad_budget


    def _get_round_costs(self):
        # return round costs
        costs = np.multiply(np.multiply(np.ones(self.num_providers), self.cost_ratio), self.capital)
        return costs

    def get_round_ad_budget(self):
        ad_budgets = np.multiply(np.multiply(np.ones(self.num_providers), self.ad_percent), self.capital).tolist()
        return ad_budgets
        # return round ad_budet

    def after_round_update(self, ad_spend, clicks):
        costs = self._get_round_costs()
        revenue = np.multiply(np.array(clicks), self.conversion_rate*self.profit)
        # capital - ad_spend - running_costs + revenue
        self.capital = np.add(np.subtract(np.subtract(self.capital, costs), np.array(ad_spend)),revenue)
        return revenue

    def show_state(self):
        print(self.capital)

    def get_total_capital(self):
        return np.sum(self.capital)
