import random
import numpy as np
import logging


class SearchMechanics(object):
    def __init__(self, num_providers=30, num_ads=3, ad_prob =0.1, ad_cost=1.0, ad_theta=0.3, doc_theta=0.6, discount=0.0):
        self.num_ads = num_ads
        self.discount = discount
        self.ad_prob = ad_prob
        self.ad_cost = ad_cost
        self.ad_theta = ad_theta
        self.doc_theta = doc_theta
        self.num_providers = num_providers
        #starts the scenario with a random starting point for the ranking
        self.score = {}
        self.clicks = {}
        for i in range(0, num_providers):
            self.score[i] = np.random.randint(low=0, high=num_providers)
            self.clicks[i] = self.score[i]

        self.round_clicks = np.zeros(self.num_providers).tolist()
        self.ad_clicks = np.zeros(self.num_providers).tolist()
        self.ad_budgets = np.zeros(self.num_providers).tolist()
        self.ad_spend = np.zeros(self.num_providers).tolist()

        logging.basicConfig(filename='example.log', level=logging.DEBUG)

    def get_name(self):
        return "ads-{}prob-{}cost-{}theta-{}".format(self.num_ads,round(self.ad_prob,2),self.ad_cost, self.doc_theta)

    def _make_click_prob_old(self, doc_theta, ad_theta, num_providers, num_ads):
        p_ads = np.dot(np.ones(num_ads), ad_theta)
        cvec = np.dot(np.ones(num_providers), doc_theta)
        cvec_prod = np.cumprod(cvec)
        cvec_prod = np.pad(cvec_prod,(1,0),'constant',constant_values=(1.0))
        w1 = np.divide( 1.0, np.sum(cvec_prod))
        w_tail = np.multiply(cvec_prod[1:len(cvec_prod)],w1)
        p_docs = np.append(w1, w_tail[0:num_providers-1])
        p_both = np.concatenate([p_ads,p_docs])
        click_prob =  np.divide(p_both, np.sum(p_both)).tolist()
        return click_prob

    def _make_click_prob(self, num_ads):
        p_ads = np.divide(np.ones(num_ads), np.sum(np.ones(num_ads)))
        p_ads = np.multiply(p_ads, self.ad_prob)

        cvec = np.dot(np.ones(self.num_providers), self.doc_theta)
        cvec_prod = np.cumprod(cvec)
        cvec_prod = np.pad(cvec_prod,(1,0),'constant',constant_values=(1.0))
        w1 = np.divide( 1.0, np.sum(cvec_prod))
        w_tail = np.multiply(cvec_prod[1:len(cvec_prod)],w1)
        p_docs = np.append(w1, w_tail[0:self.num_providers-1])

        p_docs = np.multiply(p_docs, 1.0-self.ad_prob)
        p_both = np.concatenate([p_ads,p_docs])
        return p_both

    def _get_provider_ranking(self):
        ranking = sorted(self.score, key=self.score.__getitem__, reverse=True)
        return ranking

    def _get_clicked_item(self, click_probs):
        p = np.random.random()
        ps = click_probs[0]
        i = 0
        n = len(click_probs) - 1
        while (p > ps) and (i<n):
            i = i + 1
            ps = ps + click_probs[i]

        return i

    def start_round(self, day, ad_budgets):
        # set the budgets
        self.round_clicks = np.zeros(self.num_providers).tolist()
        self.ad_clicks = np.zeros(self.num_providers).tolist()
        self.ad_budgets = ad_budgets
        self.ad_spend = np.zeros(self.num_providers).tolist()
        ad_providers = self._get_ad_providers()
        ranked_providers = self._get_provider_ranking()
        logging.debug("Day: {} Ad Providers: {} Ranked Providers {}".format(day,  ad_providers,  ranked_providers))

    def _get_ad_providers(self):
        # returns a list of ad providers,
        # depending on budget and current ad costs, and max number of ads
        can_pay = np.subtract(self.ad_budgets, self.ad_cost)
        ad_providers = []
        for i in range(0,len(can_pay)):
            if can_pay[i] > 0.0:
                ad_providers.append(i)

        num_ads = min(len(ad_providers), self.num_ads)

        #randomly select ads from the ad_providers.

        #TODO(leifos): Permutate the list, and cut at num_ads
        ad_providers = np.random.permutation(ad_providers)
        return ad_providers[0:num_ads]


    def run_query(self, day, request):


        # check if there is revenue for ads
        # how many ads to show on the current page?
        ad_providers = self._get_ad_providers()
        num_ads = len(ad_providers)
        #print(ad_providers, num_ads)
        click_probs = self._make_click_prob(num_ads)
        item_clicked = self._get_clicked_item(click_probs)
        ranked_providers = self._get_provider_ranking()

        #print([ad_providers, ranked_providers])
        # only if there are ads being shown.
        if item_clicked < num_ads:
            clicked_provider = ad_providers[item_clicked]
            self.ad_budgets[clicked_provider] = self.ad_budgets[clicked_provider] - self.ad_cost
            self.ad_spend[clicked_provider] = self.ad_spend[clicked_provider] + self.ad_cost
            self.ad_clicks[clicked_provider] = self.ad_clicks[clicked_provider] + 1
        else:
            # need to adjust for the position of the ads in the list. hack..
            # maybe make a prob to click an ad, and then a prob to click the position
            #print(i,item_clicked, num_ads)
            n = item_clicked-num_ads
            #print(ranked_providers, n)
            clicked_provider = ranked_providers[item_clicked-num_ads]
        #print("Item:{} Clicked: {}".format(item_clicked, clicked_provider))
        # record the click in total clicks list
        self.clicks[clicked_provider] = self.clicks[clicked_provider] + 1
        self.round_clicks[clicked_provider] += 1
        #logging.debug("Day: {} Request: {} Click Pos: {} Provider Selected: {}".format(day, request, item_clicked, clicked_provider))

    def end_round(self):

        #print(self.round_clicks)
        #print(self.ad_clicks)
        #print(self.score)
        # update the ranking score based on previous clicks
        scores = []
        for i in range(0, len(self.round_clicks)):
            self.score[i] = ((self.score[i] / (1.0+self.discount)) + self.round_clicks[i])
            scores.append(self.score[i])
        # return how much was spent on ads, and how many clicks per provider

        ranked_providers = self._get_provider_ranking()

        return self.ad_spend, self.round_clicks, scores
