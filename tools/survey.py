"""Design-based (complex-survey) estimation helpers for the BDHS analysis.

The BDHS is a stratified, two-stage cluster sample.  Ignoring that structure makes standard errors
too small, and ``statsmodels`` cannot express stratification, so this module implements the handful
of design-based quantities the notebooks need, using Taylor linearisation with the with-replacement
variance estimator that ``survey::svydesign(ids = ~PSU, strata = ~Stratum, weights = ~w, nest = TRUE)``
and Stata's ``svyset psu [pw=w], strata(stratum)`` use by default.

Validation: checked against R 4.3.3 / ``survey`` 4.2.1 on this project's data.
Proportions, standard errors, logit confidence intervals, subpopulation (``domain=``) estimates and
single-column ``glm_test`` coefficients, standard errors and p-values (binomial and gaussian, including
partial tests with adjustment terms) agree with ``svyciprop``, ``svyglm`` and
``regTermTest(method = "Wald", df = degf(design))`` to a relative difference of about 1e-5 or better.
The weighted rank-score test (``midrank`` + ``glm_test``) agrees with ``svyranktest`` to about three
significant figures (p = 1.887e-05 vs 1.885e-05, 0.00868 vs 0.00868); the small gap comes from how the
two implementations build the rank scores.  Not covered: models other than binomial / gaussian GLMs.

Typical use::

    from tools.survey import SurveyDesign

    design = SurveyDesign(weights=df["Sampling weight"], psu=df["PSU"], stratum=df["Stratum"])
    p, se, lo, hi = design.prop(df["Anxiety Binary"] == 1)
    out = design.glm_test(y, X, family="binomial")          # joint test of all columns of X
    out = design.glm_test(y, X, "binomial", domain=mask)    # restrict to a subpopulation, keep the full design

Subpopulations (``domain=``) matter: to analyse a subgroup correctly, build the design on the *whole*
sample and pass a boolean mask, rather than subsetting the data first.  Subsetting drops
PSUs that contain no subgroup members, which can change the variance (for the analytic sample itself it makes no difference, because every PSU contains analytic women: see Notebook 4).
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from scipy.special import expit, logit

__all__ = ["SurveyDesign"]


class SurveyDesign:
    """A stratified, PSU-clustered sample: one row per respondent, in a fixed order.

    Every method takes arrays aligned with the rows the design was built from.
    PSU ids only need to be unique within stratum (``nest=TRUE`` behaviour).
    """

    def __init__(self, weights, psu, stratum):
        self.w = np.asarray(weights, float)
        stratum = pd.Series(np.asarray(stratum))
        psu = pd.Series(np.asarray(psu))
        self.psu_idx = pd.factorize(stratum.astype(str) + "_" + psu.astype(str))[0]
        self.strat_idx = pd.factorize(stratum)[0]
        self.n = len(self.w)
        self.n_psu = int(self.psu_idx.max()) + 1
        self.n_strata = int(self.strat_idx.max()) + 1
        self._psu_strat = np.zeros(self.n_psu, int)
        self._psu_strat[self.psu_idx] = self.strat_idx

    # ------------------------------------------------------------------ bookkeeping
    def degf(self, domain=None) -> int:
        """Design degrees of freedom: PSUs minus strata, counted among rows with a positive weight
        in the domain (the convention of ``survey::degf`` on a subsetted design)."""
        m = np.ones(self.n, bool) if domain is None else np.asarray(domain, bool)
        psus = np.unique(self.psu_idx[m])
        return len(psus) - len(np.unique(self._psu_strat[psus]))

    def _mask(self, domain):
        return np.ones(self.n, bool) if domain is None else np.asarray(domain, bool)

    # ------------------------------------------------------------------ variance
    def linearised_cov(self, scores) -> np.ndarray:
        """Covariance of the weighted total of ``scores`` (n x p), with variance
        ``sum_h n_h/(n_h-1) * sum_j (u_hj - ubar_h)(u_hj - ubar_h)'`` over strata h and PSUs j.
        Rows outside a domain must already hold zero scores; ``n_h`` always counts every PSU in the
        design, which is what makes subpopulation variances correct."""
        scores = np.asarray(scores, float)
        if scores.ndim == 1:
            scores = scores[:, None]
        psu_tot = np.zeros((self.n_psu, scores.shape[1]))
        np.add.at(psu_tot, self.psu_idx, scores)
        cov = np.zeros((scores.shape[1], scores.shape[1]))
        for h in range(self.n_strata):
            t = psu_tot[self._psu_strat == h]
            n_h = len(t)
            if n_h > 1:
                d = t - t.mean(axis=0)
                cov += n_h / (n_h - 1) * d.T @ d
        return cov

    # ------------------------------------------------------------------ proportions / means
    def mean(self, y, domain=None):
        """Design-based (domain) mean and its standard error (ratio estimator, linearised)."""
        m = self._mask(domain)
        y = np.asarray(y, float)
        sw = self.w[m].sum()
        est = np.sum(self.w[m] * y[m]) / sw
        z = np.where(m, self.w * (y - est) / sw, 0.0)
        return est, float(np.sqrt(self.linearised_cov(z)[0, 0]))

    def prop(self, indicator, domain=None):
        """Design-based proportion with a logit-scale 95% CI (``svyciprop(method = "logit")``).
        Returns ``(p, se, lo, hi)``; the interval is NaN when p is 0 or 1."""
        p, se = self.mean(np.asarray(indicator, float), domain)
        if 0 < p < 1:
            t = stats.t.ppf(0.975, self.degf(domain))
            s = se / (p * (1 - p))
            return p, se, expit(logit(p) - t * s), expit(logit(p) + t * s)
        return p, se, np.nan, np.nan

    # ------------------------------------------------------------------ rank scores
    def midrank(self, y, domain=None) -> np.ndarray:
        """Weighted mid-rank score in (0, 1), ``(F_w(y) + F_w(y-)) / 2``, the rank score used by
        design-based rank tests (Lumley & Scott 2013).  Rows outside the domain get NaN."""
        m = self._mask(domain)
        y = np.asarray(y)
        s = pd.Series(self.w[m]).groupby(y[m]).sum().sort_index()
        cum = s.cumsum() / s.sum()
        mid = (cum + cum.shift(1).fillna(0)) / 2
        out = np.full(self.n, np.nan)
        out[m] = pd.Series(y[m]).map(mid).to_numpy()
        return out

    # ------------------------------------------------------------------ regression
    def glm_test(self, y, X, family: str = "binomial", domain=None, test=None) -> dict:
        """Weighted GLM (``"binomial"`` or ``"gaussian"``) with a linearised sandwich covariance.

        Tests all columns of ``X`` (an intercept is added) *jointly* - or only the columns listed in
        ``test`` (0-based positions within ``X``), keeping the rest as adjustment terms - with a
        design-based Wald test,
        referred to F(k, ddf) with ddf = ``degf(domain)`` - the same as
        ``survey::regTermTest(fit, ~terms, method = "Wald", df = degf(design))``.
        Returns ``p`` (design-based), ``p_adj`` (Stata-style adjusted F, differs only for k > 1),
        ``p_model`` (weighted model-based variance, ignoring the design), ``deff`` (mean ratio of
        design to model variance on the tested coefficients), ``wald``, ``k``, ``ddf`` and, for a
        single tested column, ``beta`` and ``se``.
        """
        m = self._mask(domain)
        y = np.asarray(y, float)
        X = np.column_stack([np.ones(self.n), np.asarray(X, float)])
        fam = sm.families.Binomial() if family == "binomial" else sm.families.Gaussian()
        fit = sm.GLM(y[m], X[m], family=fam, freq_weights=self.w[m]).fit()
        beta = np.asarray(fit.params)
        mu = np.zeros(self.n)
        mu[m] = np.asarray(fit.fittedvalues)
        wt = self.w * mu * (1 - mu) if family == "binomial" else self.w
        bread = np.linalg.inv((X[m] * wt[m][:, None]).T @ X[m])
        score = np.where(m[:, None], X * (self.w * (y - mu))[:, None], 0.0)
        v_design = bread @ self.linearised_cov(score) @ bread
        if family == "binomial":
            v_model = bread
        else:
            resid2 = np.sum(self.w[m] * (y[m] - mu[m]) ** 2)
            v_model = bread * resid2 / (self.w[m].sum() - X.shape[1])
        idx = list(range(1, X.shape[1])) if test is None else [1 + j for j in test]
        k, b = len(idx), beta[idx]
        vd, vm = v_design[np.ix_(idx, idx)], v_model[np.ix_(idx, idx)]
        wald = float(b @ np.linalg.solve(vd, b))
        ddf = self.degf(domain)
        out = dict(
            p=float(stats.f.sf(wald / k, k, ddf)),
            p_adj=float(stats.f.sf(wald * (ddf - k + 1) / (ddf * k), k, ddf - k + 1)),
            p_model=float(stats.chi2.sf(float(b @ np.linalg.solve(vm, b)), k)),
            deff=float(np.mean(np.diag(vd) / np.diag(vm))),
            wald=wald, k=k, ddf=ddf,
        )
        if k == 1:
            out.update(beta=float(b[0]), se=float(np.sqrt(vd[0, 0])))
        return out
