# semba

**semba** is a Python package for bayesian and (soon) probabalistic structural equation modelling (SEM). The project is powered by the other SEM software [**semopy**](https://semopy.com) and probabalistic programming framework [**Numpyro**](https://num.pyro.ai). One can think of  **semba** as a bayesian offspring of **semopy**, and indeed, there is little difference between and the two in terms of usability.

## What semba has to offer?

**semba** is a very young package that, at the time of me writing this readme, is days old, and many features are still planned, yet at the moment its selling points are:

 - Impose arbitrary priors on model parameters;
 - Efficient parameter estimation by means of Markov Chain Monte Carlo (MCMC) methods;
 - *Almost* complete mimicria of **semopy** models and methods: no need to learn two different packages.

## What will semba offer in the foreseeable future?

 - Not *almost*, but a complete mimicria;
 - Bayesian treatment of the Gaussian Process SEM proposed [here](https://arxiv.org/abs/2106.01140) under the notion of `ModelGeneralizedEffects` that can be used to model complex phenomena such as spatial, temporal data or even both;
 - Probabalistic approach to SEM that lets user to impose arbitrary distribution assumptions on variables and to introduce complex nonlinearity.

## Where to start?

The best place to start is to get familar with **semopy** first at [its website](https://semopy.com) as there is no difference in core syntax.

Then, one can proceed to installing **semba** via pip:

```
pip install semba
```

See that using **semba** is no different from using **semopy**:
```
from semopy.examples import political_democracy as ex
import semba

desc, data = ex.get_model(), ex.get_data()
model = semba.Model(desc)
model.fit(data)
ins = model.inspect()
print(ins.head())
```
That produces an output:
```
       lval op   rval   Estimate       5.0%      95.0%        std      n_eff      r_hat
_b12  dem60  ~  ind60       1.32       0.72       1.86       0.35   1,098.38       1.00
_b13  dem65  ~  ind60       0.52       0.14       0.89       0.23   1,119.16       1.00
_b14  dem65  ~  dem60       0.90       0.71       1.07       0.11     479.93       1.00
_b1      x1  ~  ind60       1.00          -          -          -          -          -
_b2      x2  ~  ind60       2.17       1.94       2.39       0.14   1,028.65       1.00
```

## Imposing custom priors
After you learn about the [model syntax](https://semopy.com/syntax.html), you can impose priors onto model parameters by means of `PRIOR` operation, for example:
```
y ~ a1 * x1 + a2 * x2 + a3 * x3

PRIOR(Normal, loc=1, scale=0.1) a1 a2 a3
```
This will impose a normal prior on regression coefficients `a1, a2, a3` with a center at 1 and standard deviation 0.1.
`PRIOR` operation overrides default priors. In `semba`, the default priors for regression coefficients are normal with a scale 0.5,  covariances are normal and the default priors for variance parameters is half-normal, all centered at starting values.  Default priors can be overriden by using operations `PRIOR_LOADING`, `PRIOR_VARIANCE`, `PRIOR_COVARIANCE`, `PRIOR_VARIANCE_LATENT` and `PRIOR_COVARIANCE_LATENT`. The latter two are used for (co)variances of latent factors -- covariances are standard normal and variances are half-normal with a center at 1.0 (this is likely a subject to change in a future version to accomodate for a scenarios where variances are far-off from the regular range 0-10).

In `PRIORx` operations, any distribution can be supplied, as long as it is supported by **Numpyro** (see [documentation](http://num.pyro.ai/en/stable/distributions.html) for a list of available distribution).

## MCMC settings

Number of samples, burn-in (or warmup) iterations and number of chains can be supplied to the `fit` method via arguments `num_samples`, `num_warmup` and `num_chains` respectively. By default, `num_samples` is set to a number of parameters in a model times 30, and a number of warmup iterations is 1/5th of that. `num_chains` is set to 1 by default. 

**semba** relies on **Numpyro** MCMC kernels, and any **Numpyro** MCMC kernel is easily available to a user: one should pass a name of the kernel to the `solver` argument of the method `fit`. The default one is NUTS.

## More information
**semba** has its own little website at [bayes.semopy.com](https://bayes.semopy.com).

