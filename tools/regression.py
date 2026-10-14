"""Design-based (complex-survey) regression for the BDHS analysis.

Two estimators, both fitted by weighted pseudo-likelihood, with the stratified, PSU-clustered
Taylor-linearised sandwich variance that ``tools/survey.py`` uses for everything else
(``survey::svydesign(ids = ~PSU, strata = ~Stratum, weights = ~w, nest = TRUE)`` and Stata's ``svyset``)::

    fit_logit(y, X, design, names)            binary outcome, logit link
    fit_ordinal_logit(y, X, design, names)    proportional-odds (cumulative-logit) model

``design`` is a ``tools.survey.SurveyDesign`` built on the same rows as ``y`` and ``X``.  ``X`` holds the
slope columns only: the intercept (logit) or the thresholds (ordinal) are added here.  Both functions
return a ``DesignFit`` with design-based standard errors, Wald tests and linear contrasts.

Inference follows ``survey::svyglm``: t reference distribution with the design degrees of freedom
(PSUs minus strata) for single coefficients, F(k, ddf) for joint Wald tests.  Pseudo-likelihood
quantities (``loglik``) are descriptive only: with unequal weights, likelihood-ratio tests, AIC and BIC
have no valid reference distribution, so use ``DesignFit.wald`` instead.

Validation: ``fit_logit`` reproduces ``SurveyDesign.glm_test`` (coefficient, standard error, p) to about
1e-13, and ``fit_ordinal_logit`` reproduces the coefficients of statsmodels' ``OrderedModel`` (same
weights, Newton-polished) to about 1e-8; Notebook 6 repeats both checks every time it runs, and also
confirms for each of its proportional-odds models that statsmodels' weighted log-likelihood equals this
one and has zero gradient at the solution.  Against R 4.3.3 / ``survey`` 4.2.1 (checked once; R is not a
dependency of this repository), 24 models (the four outcome versions x a 0-3, 0-2 or binary Burden x
without and with the Wealth x Burden term, with the Notebook 4 screen covariates) were refitted with
``svyolr`` (12 ordinal) and ``svyglm`` with a quasibinomial family (12 logistic): the largest coefficient
difference was 9e-5 and the largest relative difference in a standard error 2e-5 for the ordinal models
(consistent with ``svyolr``'s own optimiser tolerance: the Python solutions satisfy the weighted score
equations to about 1e-13), and 4e-12 and 1e-6 for the logistic ones.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import optimize, stats
from scipy.special import expit, logit

from tools.survey import SurveyDesign

__all__ = ["DesignFit", "fit_logit", "fit_ordinal_logit", "gvif"]


@dataclass
class DesignFit:
    """A fitted model: slope estimates with a design-based covariance, plus fit diagnostics."""

    kind: str                    # "logit" or "ordinal"
    names: list                  # names of the slope coefficients, in order
    beta: np.ndarray             # slope estimates (log odds ratios)
    vcov: np.ndarray             # design-based covariance of the slopes
    ddf: int                     # design degrees of freedom
    n: int
    n_params: int                # slopes + intercept / thresholds
    cutpoints: np.ndarray        # intercept (logit) or thresholds (ordinal)
    loglik: float                # weighted pseudo-log-likelihood (descriptive only)
    max_score: float             # largest |weighted score| / sum(w) at the optimum (should be ~0)
    converged: bool

    # ------------------------------------------------------------------ helpers
    def _idx(self, terms) -> list:
        return [self.names.index(t) for t in terms]

    def se(self) -> np.ndarray:
        return np.sqrt(np.diag(self.vcov))

    def _summarise(self, est, se) -> dict:
        t = stats.t.ppf(0.975, self.ddf)
        z = est / se if se > 0 else np.nan
        return dict(est=est, se=se, OR=float(np.exp(est)), lo=float(np.exp(est - t * se)),
                    hi=float(np.exp(est + t * se)), p=float(2 * stats.t.sf(abs(z), self.ddf)))

    # ------------------------------------------------------------------ results
    def table(self) -> pd.DataFrame:
        """One row per slope: odds ratio, 95% CI and design-based p."""
        se = self.se()
        rows = [dict(term=name, **self._summarise(b, s)) for name, b, s in zip(self.names, self.beta, se)]
        return pd.DataFrame(rows)[["term", "OR", "lo", "hi", "p", "est", "se"]]

    def wald(self, terms) -> dict:
        """Joint design-based Wald test that all ``terms`` are zero: F(k, ddf)."""
        idx = self._idx(terms)
        b, v = self.beta[idx], self.vcov[np.ix_(idx, idx)]
        k = len(idx)
        f = float(b @ np.linalg.solve(v, b)) / k
        return dict(F=f, df1=k, df2=self.ddf, p=float(stats.f.sf(f, k, self.ddf)))

    def contrast(self, weights: dict) -> dict:
        """Linear combination of slopes, e.g. ``{"Burden": 1, "Wealth × Burden": 2.0}``."""
        c = np.zeros(len(self.names))
        for term, wt in weights.items():
            c[self.names.index(term)] = wt
        return self._summarise(float(c @ self.beta), float(np.sqrt(c @ self.vcov @ c)))


# ---------------------------------------------------------------------------------------- logit
def fit_logit(y, X, design: SurveyDesign, names) -> DesignFit:
    """Weighted logistic regression with the stratified, PSU-clustered linearised variance."""
    y = np.asarray(y, float)
    X = np.asarray(X, float)
    w = design.w
    Xc = np.column_stack([np.ones(len(y)), X])
    fit = sm.GLM(y, Xc, family=sm.families.Binomial(), freq_weights=w).fit()
    beta = np.asarray(fit.params)
    mu = np.asarray(fit.fittedvalues)
    scores = Xc * (w * (y - mu))[:, None]
    bread = np.linalg.inv((Xc * (w * mu * (1 - mu))[:, None]).T @ Xc)
    vcov = bread @ design.linearised_cov(scores) @ bread
    max_score = float(np.abs(scores.sum(axis=0)).max() / w.sum())
    return DesignFit(
        kind="logit", names=list(names), beta=beta[1:], vcov=vcov[1:, 1:], ddf=design.degf(),
        n=len(y), n_params=Xc.shape[1], cutpoints=beta[:1],
        loglik=float(np.sum(w * (y * np.log(mu) + (1 - y) * np.log1p(-mu)))),
        max_score=max_score, converged=bool(fit.converged) and max_score < 1e-6,
    )


# ------------------------------------------------------------------------------------- ordinal
def fit_ordinal_logit(y, X, design: SurveyDesign, names) -> DesignFit:
    """Weighted proportional-odds model, ``P(Y <= j | x) = expit(theta_j - x'beta)``.

    ``y`` must be coded 0..J-1 with every level present.  Thresholds are parametrised as
    ``theta_0 = a_0``, ``theta_j = theta_{j-1} + exp(a_j)`` so they stay ordered.  The pseudo-likelihood
    is maximised with BFGS on analytic scores, polished with Newton steps, and the variance is the
    linearised sandwich ``H^-1 [cov of design-weighted scores] H^-1`` over strata and PSUs.
    """
    y = np.asarray(y).astype(int)
    X = np.asarray(X, float)
    n, m = X.shape
    levels = np.unique(y)
    if not np.array_equal(levels, np.arange(len(levels))):
        raise ValueError("outcome must be coded 0..J-1 with every level present")
    K = len(levels) - 1                                  # number of thresholds
    w = design.w
    sw = w.sum()

    def thresholds(a):
        th = np.empty(K)
        th[0] = a[0]
        if K > 1:
            th[1:] = a[0] + np.cumsum(np.exp(a[1:]))
        return th

    def parts(p):
        eta = X @ p[:m]
        ext = np.concatenate(([-np.inf], thresholds(p[m:]), [np.inf]))
        upper, lower = ext[y + 1] - eta, ext[y] - eta
        f_up, f_lo = expit(upper), expit(lower)
        prob = np.maximum(f_up - f_lo, 1e-300)
        return prob, f_up * (1 - f_up), f_lo * (1 - f_lo)

    def obs_scores(p):
        """n x (m + K) matrix of per-observation log-likelihood scores (unweighted)."""
        prob, d_up, d_lo = parts(p)
        a = p[m:]
        s_beta = X * ((d_lo - d_up) / prob)[:, None]
        s_th = np.zeros((n, K))
        has_up, has_lo = y <= K - 1, y >= 1
        s_th[np.flatnonzero(has_up), y[has_up]] += (d_up / prob)[has_up]
        s_th[np.flatnonzero(has_lo), y[has_lo] - 1] -= (d_lo / prob)[has_lo]
        jac = np.zeros((K, K))                           # d theta_j / d a_l
        jac[:, 0] = 1.0
        for l in range(1, K):
            jac[l:, l] = np.exp(a[l])
        return np.hstack([s_beta, s_th @ jac])

    nll = lambda p: -float(np.sum(w * np.log(parts(p)[0])))
    ngrad = lambda p: -(w[:, None] * obs_scores(p)).sum(axis=0)

    def num_hessian(p, h=1e-5):
        k = len(p)
        H = np.empty((k, k))
        for j in range(k):
            step = np.zeros(k)
            step[j] = h * max(1.0, abs(p[j]))
            H[:, j] = (ngrad(p + step) - ngrad(p - step)) / (2 * step[j])
        return (H + H.T) / 2

    # starting values: slopes 0, thresholds from the weighted marginal cumulative proportions
    cum = np.cumsum([w[y == j].sum() for j in range(K + 1)])[:K] / sw
    th0 = logit(cum)
    p0 = np.concatenate([np.zeros(m), [th0[0]], np.log(np.diff(th0))])

    res = optimize.minimize(lambda p: nll(p) / sw, p0, jac=lambda p: ngrad(p) / sw, method="BFGS",
                            options={"gtol": 1e-10, "maxiter": 5000})
    p = res.x
    for _ in range(8):                                   # Newton polish with backtracking
        g = ngrad(p)
        try:
            step = np.linalg.solve(num_hessian(p), g)
        except np.linalg.LinAlgError:
            break
        f0, t = nll(p), 1.0
        while t > 1e-4 and nll(p - t * step) > f0 + 1e-10:
            t /= 2
        if t <= 1e-4:
            break
        p = p - t * step
        if np.abs(t * step).max() < 1e-11:
            break

    H = num_hessian(p)
    eig_min = np.linalg.eigvalsh(H).min()
    max_score = float(np.abs(ngrad(p)).max() / sw)
    bread = np.linalg.inv(H)
    vcov = bread @ design.linearised_cov(w[:, None] * obs_scores(p)) @ bread
    return DesignFit(
        kind="ordinal", names=list(names), beta=p[:m], vcov=vcov[:m, :m], ddf=design.degf(), n=n,
        n_params=m + K, cutpoints=thresholds(p[m:]), loglik=-nll(p), max_score=max_score,
        converged=bool(max_score < 1e-6 and eig_min > 0),
    )


# ----------------------------------------------------------------------------------------- GVIF
def gvif(X: pd.DataFrame, groups: dict) -> pd.DataFrame:
    """Fox & Monette (1992) generalised VIF on the exact model matrix, one row per term.

    ``X`` holds the slope columns (no intercept); ``groups`` maps each term to its column names (a
    nominal variable's dummies share one term).  Reports ``GVIF^(1/(2*Df))``, comparable with a
    threshold of about 2 whatever the number of columns in a term.
    """
    cols = list(X.columns)
    R = np.corrcoef(X.to_numpy(float), rowvar=False)
    det_all = np.linalg.det(R)
    rows = []
    for term, members in groups.items():
        idx = [cols.index(c) for c in members]
        rest = [i for i in range(len(cols)) if i not in idx]
        df = len(idx)
        g = np.linalg.det(R[np.ix_(idx, idx)]) * (np.linalg.det(R[np.ix_(rest, rest)]) if rest else 1.0) / det_all
        rows.append(dict(term=term, Df=df, GVIF=g, **{"GVIF^(1/(2*Df))": g ** (1 / (2 * df))}))
    return pd.DataFrame(rows)
