###Searh Economics Simulation


Consider the following context, we have a number of service providers ($n_sp$), each of them compete for customers who are interested in obtaining the service - for example it could be to book a hotel, buy insurance, complete a tax return, and so forth. Each day the search engine recieves a number of requests ($n_{req}$) in which the service providers are returned in response to the request (e.g. query). 

If a customer visits their website, then there is a probability that this click will be converted to a sale ($p_sale$) and the service provider stands to make a profit $\pi$ from the sale. 

The way that they attract customers (in this simulation) is through clicks via the search engine result page. The higher their landing page, the higher the probability of that their page will be clicked. We assume that all service providers provide similar, substitutable services (i.e. essentially perfect substitutes).

Servicer providers can try to promote their service by pay for advertising on the search engine result page.

The search engine decides how many advertising slots ($n_{ads}$), and the cost of an ad ($c_{ad}$). In practice the cost of an ad is typically determined by auction among providers but here we assume it is fixed (initially). Currently, the search engine randomly selects which service providers fills the ad slots (of course, in practice the choice is based on what would maximise expected payoff).

When customers enter a query to the search engine for the service in question, then there is some probability that they will select an advertisement with probability, $p_{ad}$ and some probability that they will select an organic result, $1-p_{ad}$.

If they select an advertisement, they do so with a uniform probability (currently), while if they select an organic result, they do so according to an RBP user model where $\theta$ specifies the patience of the user i,e, higher $\theta$, implies that users are more likely to inspect results lower down in the list - and thus there is a greater chance of them clicking them. 

The search engine randomly assigns a score to each provider at the beginning of the simulation, and updates the score each round based on how many clicks that service provider recieves. The score is discounted by a factor of $\alpha$, such that:
\begin{equation}
s_{score} \leftarrow  \frac{s_{score}}{1+\alpha}  + s_{clicks} 
\end{equation}


The simulation is run over a number of days $n_{days}$ and each day it assumed that a number of requests are recieved $n_{reqs}$ (currently fixed). Each service provider starts the simulation with a certain amount of capital $s_{cap}$, which is randomly allocated, and total $S_{cap} = \sum_{s} s_{cap} = m$. This is so the simulation starts from a similar starting point each time it is run. 

At the beginning of the day (turn), each service provider sets their advertising budgets. The advertising budget $s_{budget} is set based on a percentage $S_{pad}$ of the servicer provider's capitial $s_{cap}$. Currently, $s_{pad}=0.02$ and is fixed for all servicer providers. So each round they allocate 2 percent of their capital to advertising i.e. the max amount of budget that they are willing to spend on ads that day. Of course, different providers will vary how much they allocate depending on their internal strategy - so this is a simplifying assumption. Essentially, the more capitial a service provider has the larger their advertising budget.

This means that the maximium ad revenue would be equal to the $\sum_{s} s_{cap} * s_{pad}$, assuming enough requests came in during the day which had an ad click. 

At the end of the day, the total capital each service provider has is, currently, based on three factors: (1) their daily costs, (2) amount spent on advertisting, and (3) the amount of revenue.

The daily costs are assumed to be a fixed proportion of their capital, $s_{cp} = k$, so the cost is $s_{cost} = k . s_{cap}$.

The amount spent on advertising is based on the number of ad clicks $s_{clicked-ads}$ and the cost of ads (which is currently fixed) $v$, so $s_{ad-cost} = v . s_{clicked-ads}$

The amount of revenue is directly proportional to the number of clicks  $s_{clicks}$ obtained in the day, and is based on the conversion rate $r$ and the profit $\pi$. So the $s_{revenue} = r . \pi . s_{clicks}$.

At the end of the day the captial of service providers is updated as follows:
\begin{equation}
s_{cap} \leftarrow s_{cap} - S_{cost} - s_{ad-cost} + S_{revenue}
\end{equation}






\subsection{Market Parameters}
\begin{itemize}
$n_sp$ - number of service providers starting in the market
$n_{days}$ - number of days to run the simulation
$n_{reqs}$ - number of requests relevant to the service providers where a click was observed
$S_{cap}$ - total amount of capital at the start of simulation
\end{itemize}

\subsection{Search Engine / User Parameters}
\begin{itemize}
$n_{ads}$ - number of ad slots on the SERP
$c_{ad}$ - cost of the adverts
$p_{ad}$ - probability of an ad being clicked, and ad is then uniformly clicked
$1-p{ad}$ - probabiltiy of an organic result being clicked
$\theta$ - if an organic, then an RBP user model, with $\theta$ patience
$\alpha$ - the amount of discount applied to the past score
\end{itemize}

\subsection{Provider Parameters}
\begin{itemize}
$s_{budget} - the advertising budget of the service provider $s$
$s_{pad}$ - the percentage of capital to be allocated as budget
$s_{cap}$ - the amount of capital that the service provider has available
$p_sale$ - percentage of clicks converted to sales
$\pi$ - amount of profit a provider makes for a sale
\end{itemize}






















