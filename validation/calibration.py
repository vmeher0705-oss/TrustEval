
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr


# ============================================================
# EXECUTION STATUS DEFINITIONS
# ============================================================

SUCCESS_STATUSES = {
    "success",
    "successful",
    "passed",
    "pass",
    "completed",
    "complete",
    "true",
    "1",
}

FAILURE_STATUSES = {
    "failure",
    "failed",
    "fail",
    "error",
    "false",
    "0",
}


# ============================================================
# CONVERT EXECUTION STATUS INTO BINARY OUTCOME
# ============================================================

def _status_to_binary(status):

    if pd.isna(status):
        return np.nan

    if isinstance(status, (bool, np.bool_)):
        return int(status)

    value = str(status).strip().lower()

    if value in SUCCESS_STATUSES:
        return 1

    if value in FAILURE_STATUSES:
        return 0

    return np.nan


# ============================================================
# SAFE CORRELATION
# ============================================================

def _safe_correlation(x, y, method="pearson"):

    x = pd.to_numeric(
        pd.Series(x),
        errors="coerce"
    )

    y = pd.to_numeric(
        pd.Series(y),
        errors="coerce"
    )

    valid = pd.DataFrame({
        "x": x,
        "y": y
    }).dropna()

    if len(valid) < 3:
        return np.nan, np.nan

    if (
        valid["x"].nunique() < 2
        or valid["y"].nunique() < 2
    ):
        return np.nan, np.nan

    if method == "pearson":

        result = pearsonr(
            valid["x"],
            valid["y"]
        )

    elif method == "spearman":

        result = spearmanr(
            valid["x"],
            valid["y"]
        )

    else:

        raise ValueError(
            "Method must be pearson or spearman."
        )

    return (
        float(result.statistic),
        float(result.pvalue)
    )


# ============================================================
# PREPARE EXECUTION DATA
# ============================================================

def _prepare_execution_data(trust_scores):

    required_columns = {
        "task_id",
        "framework",
        "composite_score",
        "status"
    }

    missing = (
        required_columns
        - set(trust_scores.columns)
    )

    if missing:

        raise ValueError(
            "Missing required columns: "
            + ", ".join(sorted(missing))
        )

    df = trust_scores.copy()

    df["composite_score"] = pd.to_numeric(
        df["composite_score"],
        errors="coerce"
    )

    df["outcome"] = df["status"].apply(
        _status_to_binary
    )

    return df


# ============================================================
# CALIBRATION / EXECUTION OUTCOME ANALYSIS
# ============================================================

def calibration_analysis(trust_scores):

    """
    Descriptive association between TrustEval scores
    and observed execution outcomes.

    This is NOT human-rating validation.

    Ordinary correlation p-values are retained for
    reference only and must not be interpreted as
    independent-observation statistical evidence.

    Task-cluster uncertainty is assessed separately.
    """

    df = _prepare_execution_data(trust_scores)

    df = df.dropna(
        subset=["composite_score"]
    ).copy()

    known = df.dropna(
        subset=["outcome"]
    ).copy()

    n_runs = len(df)

    n_known = len(known)

    n_successful = int(
        (known["outcome"] == 1).sum()
    )

    n_failed = int(
        (known["outcome"] == 0).sum()
    )

    n_unknown = n_runs - n_known

    success_rate = (
        n_successful / n_known
        if n_known > 0 else np.nan
    )

    failure_rate = (
        n_failed / n_known
        if n_known > 0 else np.nan
    )

    successful_scores = known.loc[
        known["outcome"] == 1,
        "composite_score"
    ]

    failed_scores = known.loc[
        known["outcome"] == 0,
        "composite_score"
    ]

    mean_successful_score = (
        float(successful_scores.mean())
        if len(successful_scores) else np.nan
    )

    mean_failed_score = (
        float(failed_scores.mean())
        if len(failed_scores) else np.nan
    )

    score_gap = (
        mean_successful_score - mean_failed_score
        if (
            np.isfinite(mean_successful_score)
            and np.isfinite(mean_failed_score)
        )
        else np.nan
    )

    # --------------------------------------------------------
    # DESCRIPTIVE CORRELATIONS
    # --------------------------------------------------------

    pearson_r, pearson_p = _safe_correlation(
        known["composite_score"],
        known["outcome"],
        method="pearson"
    )

    spearman_rho, spearman_p = _safe_correlation(
        known["composite_score"],
        known["outcome"],
        method="spearman"
    )

    # --------------------------------------------------------
    # FAILURE DISTRIBUTION
    # --------------------------------------------------------

    failed = known[
        known["outcome"] == 0
    ]

    n_tasks_with_failures = (
        failed["task_id"].nunique()
    )

    n_frameworks_with_failures = (
        failed["framework"].nunique()
    )

    small_failure_sample = n_failed < 30

    if n_failed == 0:

        failure_warning = (
            "No failed executions were observed. "
            "Success-versus-failure comparisons "
            "cannot be established."
        )

    elif small_failure_sample:

        failure_warning = (
            f"Only {n_failed} failed executions were "
            f"observed among {n_known} known outcomes. "
            "This is a very small failure sample. "
            "Failure-group comparisons and correlations "
            "are exploratory and should not support "
            "strong statistical conclusions."
        )

    else:

        failure_warning = (
            "The failure count is at least 30. "
            "Task-level dependence must still be considered."
        )

    # --------------------------------------------------------
    # RESULTS
    # --------------------------------------------------------

    results = {

        "n_runs": n_runs,

        "n_runs_with_known_outcome": n_known,

        "n_runs_with_unknown_outcome": n_unknown,

        "n_successful_runs": n_successful,

        "n_failed_runs": n_failed,

        "n_tasks_with_failures": n_tasks_with_failures,

        "n_frameworks_with_failures": n_frameworks_with_failures,

        "mean_composite": float(
            df["composite_score"].mean()
        ) if n_runs else np.nan,

        "std_composite": float(
            df["composite_score"].std()
        ) if n_runs > 1 else np.nan,

        "median_composite": float(
            df["composite_score"].median()
        ) if n_runs else np.nan,

        "success_rate": success_rate,

        "failure_rate": failure_rate,

        "mean_score_successful_runs": mean_successful_score,

        "mean_score_failed_runs": mean_failed_score,

        "success_failure_score_gap": score_gap,

        "pearson_r": pearson_r,

        "pearson_p_descriptive_only": pearson_p,

        "spearman_rho": spearman_rho,

        "spearman_p_descriptive_only": spearman_p,

        "small_failure_sample": small_failure_sample,

        "failure_sample_warning": failure_warning,

        "correlation_interpretation": (
            "Pearson and Spearman correlations are "
            "descriptive exploratory associations. "
            "Their ordinary p-values assume independent "
            "observations and are not treated as valid "
            "inferential evidence because executions "
            "are clustered within tasks."
        ),

        "uncertainty_method": (
            "Task-cluster bootstrap"
        )
    }

    return results


# ============================================================
# EXPLICIT FAILURE SAMPLE REPORT
# ============================================================

def failure_sample_report(trust_scores):

    """
    Return every failed execution explicitly.

    This allows the research paper to report the actual
    failure sample rather than only reporting its percentage.
    """

    df = _prepare_execution_data(trust_scores)

    failed = df[
        df["outcome"] == 0
    ].copy()

    columns = [
        "task_id",
        "framework",
        "status",
        "composite_score"
    ]

    if "repetition" in failed.columns:
        columns.insert(2, "repetition")

    return (
        failed[columns]
        .sort_values(
            ["task_id", "framework"]
        )
        .reset_index(drop=True)
    )


# ============================================================
# FAILURE DISTRIBUTION BY TASK AND FRAMEWORK
# ============================================================

def failure_distribution(trust_scores):

    """
    Report successful and failed execution counts
    separately for each task and framework.
    """

    df = _prepare_execution_data(trust_scores)

    known = df.dropna(
        subset=["outcome"]
    ).copy()

    if known.empty:

        return pd.DataFrame(
            columns=[
                "task_id",
                "framework",
                "n_successful",
                "n_failed",
                "n_known"
            ]
        )

    known["successful"] = (
        known["outcome"] == 1
    ).astype(int)

    known["failed"] = (
        known["outcome"] == 0
    ).astype(int)

    distribution = (
        known.groupby(
            ["task_id", "framework"],
            as_index=False
        )
        .agg(
            n_successful=("successful", "sum"),
            n_failed=("failed", "sum"),
            n_known=("outcome", "count")
        )
    )

    return distribution


# ============================================================
# TASK-CLUSTER BOOTSTRAP
# ============================================================

def task_cluster_bootstrap(
    trust_scores,
    n_bootstrap=2000,
    seed=42
):

    """
    Estimate uncertainty in the Pearson correlation
    by resampling complete task clusters.

    All executions belonging to a sampled task are
    retained together.

    The resulting interval is a task-cluster bootstrap
    interval, not an ordinary independent-run interval.
    """

    if n_bootstrap < 1:

        raise ValueError(
            "n_bootstrap must be at least 1."
        )

    df = _prepare_execution_data(
        trust_scores
    )

    df = df.dropna(
        subset=[
            "task_id",
            "composite_score",
            "outcome"
        ]
    ).copy()

    task_ids = (
        df["task_id"]
        .drop_duplicates()
        .tolist()
    )

    n_tasks = len(task_ids)

    if n_tasks < 2:

        raise ValueError(
            "At least two distinct tasks are required."
        )

    # --------------------------------------------------------
    # GROUP ALL EXECUTIONS BY TASK
    # --------------------------------------------------------

    task_groups = {
        task_id: df[
            df["task_id"] == task_id
        ]
        for task_id in task_ids
    }

    rng = np.random.default_rng(seed)

    correlations = []

    # --------------------------------------------------------
    # BOOTSTRAP
    # --------------------------------------------------------

    for _ in range(n_bootstrap):

        sampled_task_ids = rng.choice(
            task_ids,
            size=n_tasks,
            replace=True
        )

        sample = pd.concat(
            [
                task_groups[task_id]
                for task_id in sampled_task_ids
            ],
            ignore_index=True
        )

        if sample["outcome"].nunique() < 2:
            continue

        if sample["composite_score"].nunique() < 2:
            continue

        r, _ = _safe_correlation(
            sample["composite_score"],
            sample["outcome"],
            method="pearson"
        )

        if np.isfinite(r):
            correlations.append(r)

    # --------------------------------------------------------
    # INTERVAL
    # --------------------------------------------------------

    n_valid = len(correlations)

    if n_valid > 0:

        bootstrap_mean = float(
            np.mean(correlations)
        )

        lower_bound = float(
            np.percentile(
                correlations,
                2.5
            )
        )

        upper_bound = float(
            np.percentile(
                correlations,
                97.5
            )
        )

    else:

        bootstrap_mean = np.nan
        lower_bound = np.nan
        upper_bound = np.nan

    # --------------------------------------------------------
    # FAILURE DISTRIBUTION ACROSS TASKS
    # --------------------------------------------------------

    failed = df[
        df["outcome"] == 0
    ]

    n_failure_tasks = (
        failed["task_id"].nunique()
    )

    if n_valid < 100:

        warning = (
            "Fewer than 100 valid bootstrap replicates. "
            "The interval may be unstable."
        )

    elif n_failure_tasks < 2:

        warning = (
            "Failures occurred in fewer than two tasks. "
            "Task-cluster uncertainty for the outcome "
            "association is particularly limited."
        )

    elif n_failure_tasks < 5:

        warning = (
            "Failures occurred in fewer than five tasks. "
            "The cluster-bootstrap interval should be "
            "interpreted cautiously because failure "
            "information is concentrated in very few tasks."
        )

    else:

        warning = (
            "Inspect the failure distribution and the "
            "number of valid replicates before interpretation."
        )

    return {

        "n_tasks": n_tasks,

        "n_tasks_with_failures": n_failure_tasks,

        "n_failed_runs": len(failed),

        "n_bootstrap_requested": n_bootstrap,

        "n_bootstrap_valid": n_valid,

        "bootstrap_pearson_mean": bootstrap_mean,

        "bootstrap_pearson_ci_lower": lower_bound,

        "bootstrap_pearson_ci_upper": upper_bound,

        "bootstrap_warning": warning,

        "bootstrap_method": (
            "Resampling complete task clusters with replacement"
        )
    }
