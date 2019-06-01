import math
import random
import numpy as np
from search_mechanics import SearchMechanics
from providers import Providers
import matplotlib.pyplot as plt
import argparse


def run_simulation(search_mechanic, provider, num_providers=30, days=365, num_requests=1000):
    random.seed(0)
    np.random.seed(0)

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
        #if day == 100:
        #    provider.capital[10] += 1000
        ad_budgets = provider.get_round_ad_budget()

        search_mechanic.start_round(day, ad_budgets)
        for i in range(0, num_requests):
            # check ad budget, any left given provider budgets?
            search_mechanic.run_query(day, i)

        (ad_spend, clicks, ranking) = search_mechanic.end_round()

        revenue = provider.after_round_update(ad_spend, clicks)
        #tad.append(np.sum(ad_spend))
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


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Search Economy Simulation")
    arg_parser.add_argument("-d", "--days",  help="Number of days (default = 100)", type=int, default=100)
    arg_parser.add_argument("-r", "--requests", type=int, default=1000,  help="Requests per day (default=1000)")
    arg_parser.add_argument("-p", "--providers",  help="Number of providers (default=30)", type=int, default=30)
    arg_parser.add_argument("-t", "--theta", help="Patience Parameter", type=float, default=0.5)
    arg_parser.add_argument("-a", "--ads", help="Number of Ads", type=int, default=1)
    arg_parser.add_argument("-c", "--cost", help="Cost of Ads", type=float, default=1.0)

    args = arg_parser.parse_args()

    num_days = args.days
    num_providers = args.providers
    num_requests = args.requests
    theta = args.theta
    num_ads = args.ads
    ad_cost = args.cost

    ad_prob = 0.175 + num_ads*0.025

    sm = SearchMechanics(num_providers=num_providers, num_ads=num_ads, ad_cost=ad_cost, ad_prob=ad_prob, doc_theta=theta, discount=1.0)
    prov = Providers(num_providers=num_providers, profit=2.0)
    run_simulation(search_mechanic=sm, provider=prov, num_providers=num_providers, days=num_days, num_requests=num_requests)
