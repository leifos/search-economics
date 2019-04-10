import random
import numpy as np

class SearchMechanics(object):
    def __init__(self, num_providers=30, num_ads=3, ad_prob =0.1, ad_cost=1.0, ad_theta=0.3, doc_theta=0.6):
        self.num_ads = num_ads
        self.discount = 1.0
        self.ad_prob = ad_prob
        self.ad_cost = ad_cost
        self.ad_theta = ad_theta
        self.doc_theta = doc_theta
        self.num_providers = num_providers
        #starts the scenario with a random starting point for the ranking
        self.score = {}
        for i in range(0, num_providers):
            self.score[i] = random.randint(0,100)

        self.clicks = {}
        self.round_clicks = np.zeros(self.num_providers).tolist()
        self.ad_budgets = np.zeros(self.num_providers).tolist()
        self.ad_spend = np.zeros(self.num_providers).tolist()

    def get_name(self):
        return "ads-{}prob-{}cost-{}theta-{}".format(self.num_ads,self.ad_prob,self.ad_cost, self.doc_theta)

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

    def _make_click_prob(self):
        p_ads = np.divide(np.ones(self.num_ads), np.sum(np.ones(self.num_ads)))
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
        p = random.random()
        ps = click_probs[1]
        i = 0
        while (p > ps) and (i<len(click_probs)-1):
            i = i + 1
            ps = ps + click_probs[i]
        return i

    def start_round(self, ad_budgets):
        # set the budgets
        self.round_clicks = np.zeros(self.num_providers).tolist()
        self.clicks = {}
        for i in range(0, self.num_providers):
            self.clicks[i] = random.randint(0,100)
        self.ad_budgets = ad_budgets
        self.ad_spend = np.zeros(self.num_providers).tolist()

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


    def run_query(self):

        # check if there is revenue for ads
        # how many ads to show on the current page?
        ad_providers = self._get_ad_providers()
        num_ads = len(ad_providers)
        click_probs = self._make_click_prob()
        item_clicked = self._get_clicked_item(click_probs)
        ranked_providers = self._get_provider_ranking()

        # only if there are ads being shown.
        if item_clicked < num_ads:
            clicked_provider = ad_providers[item_clicked]
            self.ad_budgets[clicked_provider] = self.ad_budgets[clicked_provider] - self.ad_cost
            self.ad_spend[clicked_provider] = self.ad_spend[clicked_provider] + self.ad_cost
        else:
            # need to adjust for the position of the ads in the list. hack..
            # maybe make a prob to click an ad, and then a prob to click the position
            #print(i,item_clicked, num_ads)
            clicked_provider = ranked_providers[item_clicked-num_ads]
        # record the click in total clicks list
        self.clicks[clicked_provider] =  self.clicks[clicked_provider] + 1
        self.round_clicks[clicked_provider] += 1

    def end_round(self):

        # update the ranking score based on previous clicks
        scores = []
        for i in range(0, len(self.round_clicks)):
            self.score[i] = ((self.score[i] / (1.0+self.discount))+ self.round_clicks[i])
            scores.append(self.score[i])
        # return how much was spent on ads, and how many clicks per provider

        ranked_providers = self._get_provider_ranking()

        return (self.ad_spend, self.round_clicks, scores)
