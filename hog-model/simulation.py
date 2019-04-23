import math
import random
import numpy as np
from search_mechanics import SearchMechanics
from providers import Providers
import matplotlib.pyplot as plt


def run_simulation(search_mechanic, provider, num_providers=30,days=365, num_requests=1000):
    random.seed(12345)
    np.random.seed(12345)

    print("Starting Capital: ", provider.get_total_capital())
    #print(provider.show_state())

    tcap = []
    tcap.append(provider.capital)
    tad = []
    talive = []
    trank = []
    trev = []
    tclicks = []

    for day in range(0, days):

        ad_budgets = provider.get_round_ad_budget()

        search_mechanic.start_round(ad_budgets)
        for i in range(0, num_requests):
            # check ad budget, any left given provider budgets?
            search_mechanic.run_query()

        (ad_spend, clicks, ranking) = search_mechanic.end_round()

        revenue = provider.after_round_update(ad_spend, clicks)
        tad.append(np.sum(ad_spend))
        trank.append(ranking)
        tcap.append(provider.capital)
        trev.append(np.sum(revenue))
        tclicks.append(clicks)
        alive = 0
        for c in list(provider.capital):
            if c > 100:
                alive = alive + 1
        talive.append(alive)

        tad.append(np.sum(np.array(np.array(ad_spend))))
        r = round(np.sum(revenue),2)
        ar = round(prov.get_total_capital(),2)
        ads = round(np.sum(ad_spend),2)
        print("Day: {}\tTotal Capital: {}\tRevenue:{}\t AdSpend: {} Alive: {}".format(day, ar, r, ads, alive))

    ntcap = np.array(tcap)
    ntrank = np.array(trank)
    ntad = np.array(tad)
    ntrev = np.array(trev)
    ntclicks = np.array(tclicks)
    print(search_mechanic.get_name())
    print("Ending Capital: ",  list(np.sum(ntcap, axis=1))[-1])
    print("Total Ad Revenue Over Period:",  np.sum(tad))
    print("Total Revenue", np.sum(ntrev))




    plt.figure(figsize =(8,16))
    plt.tight_layout(pad=2.0, w_pad=5.0, h_pad=5.0)
    plt.subplot(4, 1, 1)
    plt.plot(ntcap)
    plt.title("Simulation {}".format(search_mechanic.get_name()))
    #plt.xlabel("Days")
    plt.ylabel("Total Capital")

    plt.subplot(4, 1, 2)
    plt.plot(ntclicks)
    #plt.title("Active Firms")
    plt.ylabel("Clicks")

    plt.subplot(4, 1, 3)
    plt.plot(tad)
    plt.ylabel("Ad Revenue")
    plt.xlabel("Days")

    plt.subplot(4, 1, 4)
    plt.plot(ntrank)
    plt.ylabel("Provider Score")
    plt.xlabel("Days")

    plt_name = "sim-{}.png".format(search_mechanic.get_name())
    plt.savefig(plt_name)
    plt.show()



num_providers = 30
sm = SearchMechanics(num_providers=num_providers, num_ads=1, ad_cost=1.0, ad_prob=0.3, doc_theta=0.5, discount=1.0)
prov = Providers(num_providers=num_providers, profit=2.0)
run_simulation(search_mechanic=sm, provider=prov,num_providers=num_providers, days=100,num_requests=1000)
