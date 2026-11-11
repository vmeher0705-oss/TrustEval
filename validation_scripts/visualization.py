from pathlib import Path
import warnings

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ============================================================
# GENERAL HELPERS
# ============================================================

def save_figure(fig, figures_dir, filename):
    figures_dir = Path(figures_dir)
    figures_dir.mkdir(parents=True, exist_ok=True)

    path = figures_dir / filename

    fig.tight_layout()
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)

    print(f"Figure saved: {path}")
    return path


def find_column(df, candidates):
    if df is None or not isinstance(df, pd.DataFrame):
        return None

    for column in candidates:
        if column in df.columns:
            return column

    return None


def numeric_column(df, candidates):
    column = find_column(df, candidates)

    if column is None:
        return None

    values = pd.to_numeric(df[column], errors="coerce")

    if values.notna().sum() == 0:
        return None

    return column


def skip_plot(name, reason):
    print(f"Skipping {name}: {reason}")


# ============================================================
# 1. FRAMEWORK COMPARISON
# ============================================================

def plot_framework_comparison(ci, figures_dir):

    if ci is None or ci.empty:
        return skip_plot("Framework comparison", "CI dataframe missing")

    framework = find_column(
        ci, ["framework", "agent_id", "framework_name"]
    )

    mean = numeric_column(
        ci, ["mean_composite", "mean_score", "composite_mean"]
    )

    lower = numeric_column(
        ci, ["ci_lower_95", "ci_lower", "lower_95",
             "lower_ci", "ci_lower_95_composite"]
    )

    upper = numeric_column(
        ci, ["ci_upper_95", "ci_upper", "upper_95",
             "upper_ci", "ci_upper_95_composite"]
    )

    if not all([framework, mean, lower, upper]):
        return skip_plot(
            "Framework comparison",
            f"Expected framework, mean and CI columns. Found: {ci.columns.tolist()}"
        )

    data = ci[[framework, mean, lower, upper]].copy()

    for col in [mean, lower, upper]:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    data = data.dropna()

    if data.empty:
        return skip_plot("Framework comparison", "No valid CI values")

    data = data.sort_values(mean, ascending=False)

    values = data[mean].to_numpy()
    lower_error = np.maximum(values - data[lower].to_numpy(), 0)
    upper_error = np.maximum(data[upper].to_numpy() - values, 0)

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(
        data[framework].astype(str),
        values,
        yerr=[lower_error, upper_error],
        capsize=6
    )

    ax.set_ylabel("Mean composite trust score")
    ax.set_title("Framework Comparison with 95% Confidence Intervals")
    ax.set_ylim(0, 1)
    ax.tick_params(axis="x", rotation=20)

    return save_figure(
        fig, figures_dir, "framework_comparison.png"
    )


# ============================================================
# 2. RANKING STABILITY
# ============================================================

def plot_ranking(ranking, figures_dir):

    if ranking is None:
        return skip_plot("Ranking stability", "Ranking data missing")

    if isinstance(ranking, pd.Series):
        data = ranking.dropna()

    elif isinstance(ranking, pd.DataFrame):
        if ranking.empty:
            return skip_plot("Ranking stability", "Empty ranking dataframe")

        if ranking.shape[1] == 1:
            data = ranking.iloc[:, 0].dropna()
        else:
            framework = find_column(
                ranking, ["framework", "agent_id", "framework_name"]
            )
            rank_col = find_column(
                ranking, ["rank", "ranking", "mean_rank"]
            )

            if not framework or not rank_col:
                return skip_plot(
                    "Ranking stability",
                    "Cannot identify framework and rank columns"
                )

            data = ranking.set_index(framework)[rank_col].dropna()

    elif isinstance(ranking, dict):
        data = pd.Series(ranking, dtype=float)

    else:
        return skip_plot("Ranking stability", "Unsupported ranking format")

    if data.empty:
        return skip_plot("Ranking stability", "No ranking values")

    data = pd.to_numeric(data, errors="coerce").dropna()
    data = data.sort_values()

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(data.index.astype(str), data.values)

    ax.set_ylabel("Framework rank")
    ax.set_title("Framework Ranking")
    ax.invert_yaxis()
    ax.tick_params(axis="x", rotation=20)

    return save_figure(
        fig, figures_dir, "ranking_stability.png"
    )


# ============================================================
# 3. SENSITIVITY ANALYSIS
# ============================================================

def plot_sensitivity(sensitivity, figures_dir):

    if sensitivity is None or sensitivity.empty:
        return skip_plot("Sensitivity analysis", "Data missing")

    perturbation = find_column(
        sensitivity,
        ["perturbation", "perturbation_level",
         "weight_perturbation", "perturbation_fraction"]
    )

    if perturbation is None:
        return skip_plot(
            "Sensitivity analysis",
            f"No perturbation column found. Columns: {sensitivity.columns.tolist()}"
        )

    numeric_columns = [
        col for col in sensitivity.columns
        if col != perturbation
        and pd.to_numeric(sensitivity[col], errors="coerce").notna().any()
    ]

    if not numeric_columns:
        return skip_plot(
            "Sensitivity analysis",
            "No numeric sensitivity metrics found"
        )

    # Prefer ranking-agreement metrics where available.
    preferred = [
        col for col in numeric_columns
        if any(term in col.lower() for term in
               ["kendall", "tau", "rank", "stability"])
    ]

    metric = preferred[0] if preferred else numeric_columns[0]

    data = sensitivity[[perturbation, metric]].copy()

    data[perturbation] = pd.to_numeric(
        data[perturbation], errors="coerce"
    )
    data[metric] = pd.to_numeric(
        data[metric], errors="coerce"
    )

    data = data.dropna()

    if data.empty:
        return skip_plot("Sensitivity analysis", "No usable values")

    data = data.groupby(perturbation)[metric].mean().sort_index()

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(
        data.index,
        data.values,
        marker="o"
    )

    ax.set_xlabel("Weight perturbation")
    ax.set_ylabel(metric.replace("_", " ").title())
    ax.set_title("Sensitivity to Weight Perturbations")

    return save_figure(
        fig, figures_dir, "sensitivity_analysis.png"
    )


# ============================================================
# 4. ABLATION
# ============================================================

def plot_ablation(ablation, figures_dir):

    if ablation is None or ablation.empty:
        return skip_plot("Ablation", "Ablation dataframe missing")

    dimension = find_column(
        ablation, ["removed_dimension"]
    )

    change = numeric_column(
        ablation, ["mean_absolute_change"]
    )

    if not dimension or not change:
        return skip_plot(
            "Ablation",
            f"Required columns missing. Found: {ablation.columns.tolist()}"
        )

    data = ablation[
        ablation[dimension].astype(str).str.lower() != "none"
    ].copy()

    data[change] = pd.to_numeric(data[change], errors="coerce")
    data = data.dropna(subset=[change])
    data = data.sort_values(change)

    if data.empty:
        return skip_plot("Ablation", "No ablation dimensions available")

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.barh(
        data[dimension].astype(str),
        data[change]
    )

    ax.set_xlabel("Mean absolute change in composite score")
    ax.set_title("Ablation: Influence of Trust Dimensions")

    return save_figure(
        fig, figures_dir, "ablation_importance.png"
    )


# ============================================================
# 5. REPEATABILITY
# ============================================================

def plot_repeatability(trust, figures_dir):
    """Run-to-run spread: standard deviation of the repeated runs of each
    task, shown per framework (one point = one task x framework pair)."""

    required = {"task_id", "framework", "composite_score"}

    if trust is None or trust.empty or not required.issubset(trust.columns):
        return skip_plot(
            "Repeatability",
            "task_id, framework or composite_score column missing"
        )

    data = trust[["task_id", "framework", "composite_score"]].copy()
    data["composite_score"] = pd.to_numeric(
        data["composite_score"], errors="coerce"
    )
    data = data.dropna()

    spread = (
        data.groupby(["framework", "task_id"])["composite_score"]
        .std(ddof=0)
        .reset_index(name="std")
    )

    groups, labels = [], []

    for framework, group in spread.groupby("framework"):
        groups.append(group["std"].to_numpy())
        labels.append(str(framework))

    if not groups:
        return skip_plot("Repeatability", "No usable scores")

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.boxplot(groups, tick_labels=labels)

    ax.set_ylabel("Std. dev. of composite across repeated runs of a task")
    ax.set_title("Repeatability: Run-to-Run Variation per Task")
    ax.tick_params(axis="x", rotation=20)

    return save_figure(
        fig, figures_dir, "repeatability.png"
    )


# ============================================================
# 6. CROSS-DOMAIN VALIDATION
# ============================================================

def plot_cross_domain(trust, figures_dir):

    required = {
        "domain", "framework", "composite_score"
    }

    if trust is None or not required.issubset(trust.columns):
        return skip_plot(
            "Cross-domain validation",
            "Required execution columns missing"
        )

    data = trust[
        ["domain", "framework", "composite_score"]
    ].copy()

    data["composite_score"] = pd.to_numeric(
        data["composite_score"], errors="coerce"
    )

    data = data.dropna()

    pivot = data.pivot_table(
        index="domain",
        columns="framework",
        values="composite_score",
        aggfunc="mean"
    )

    if pivot.empty:
        return skip_plot("Cross-domain validation", "No usable data")

    fig, ax = plt.subplots(figsize=(10, 6))

    pivot.plot(kind="bar", ax=ax)

    ax.set_xlabel("Domain")
    ax.set_ylabel("Mean composite trust score")
    ax.set_title("Framework Performance Across Domains")
    ax.set_ylim(0, 1)
    ax.tick_params(axis="x", rotation=30)
    ax.legend(title="Framework")

    return save_figure(
        fig, figures_dir, "cross_domain_performance.png"
    )


# ============================================================
# 7. LEAVE-ONE-TASK-OUT ROBUSTNESS
# ============================================================

def plot_leave_one_task_out(loto, figures_dir):

    if loto is None or loto.empty:
        return skip_plot("Leave-one-task-out", "Data missing")

    task = find_column(
        loto,
        ["task_id", "excluded_task", "removed_task", "task"]
    )

    tau = numeric_column(
        loto,
        ["kendall_tau_vs_full", "kendall_tau",
         "tau", "rank_correlation"]
    )

    if not task or not tau:
        return skip_plot(
            "Leave-one-task-out",
            f"Expected task and Kendall tau columns. Found: {loto.columns.tolist()}"
        )

    data = loto[[task, tau]].copy()
    data[tau] = pd.to_numeric(data[tau], errors="coerce")
    data = data.dropna()

    if data.empty:
        return skip_plot("Leave-one-task-out", "No usable values")

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(
        data[task].astype(str),
        data[tau]
    )

    ax.axhline(1.0, linestyle="--")
    ax.set_ylabel("Kendall's tau versus full ranking")
    ax.set_xlabel("Excluded task")
    ax.set_title("Leave-One-Task-Out Ranking Robustness")
    ax.set_ylim(-1, 1.05)
    ax.tick_params(axis="x", rotation=90)

    return save_figure(
        fig, figures_dir, "leave_one_task_out.png"
    )


# ============================================================
# 8. BASELINE COMPARISON
# ============================================================

def plot_baseline_comparison(baseline, figures_dir):

    if baseline is None or baseline.empty:
        return skip_plot("Baseline comparison", "Data missing")

    category = find_column(
        baseline,
        ["framework", "agent_id", "method", "system", "approach"]
    )

    metric = numeric_column(
        baseline,
        ["overall_mean", "mean_composite", "mean_score",
         "composite_score", "score"]
    )

    if not category or not metric:
        return skip_plot(
            "Baseline comparison",
            f"Required columns not found. Found: {baseline.columns.tolist()}"
        )

    data = baseline[[category, metric]].copy()
    data[metric] = pd.to_numeric(data[metric], errors="coerce")
    data = data.dropna()

    if data.empty:
        return skip_plot("Baseline comparison", "No numeric scores")

    data = data.groupby(category, as_index=False)[metric].mean()

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(
        data[category].astype(str),
        data[metric]
    )

    ax.set_ylabel("Overall mean score (720 runs)")
    ax.set_ylim(0, 1.05)
    ax.set_title("Baseline Comparison")
    ax.tick_params(axis="x", rotation=20)

    return save_figure(
        fig, figures_dir, "baseline_comparison.png"
    )


# ============================================================
# 9. EXECUTION OUTCOME COMPARISON
# ============================================================

def plot_success_vs_failure(trust, figures_dir):

    required = {"status", "composite_score"}

    if trust is None or not required.issubset(trust.columns):
        return skip_plot(
            "Success vs failure",
            "status or composite_score column missing"
        )

    data = trust[["status", "composite_score"]].copy()

    data["composite_score"] = pd.to_numeric(
        data["composite_score"], errors="coerce"
    )

    data = data.dropna(subset=["composite_score"])

    status = data["status"].astype(str).str.strip().str.lower()

    success_values = ["success", "successful", "completed"]

    successful = data.loc[
        status.isin(success_values), "composite_score"
    ]

    failed = data.loc[
        ~status.isin(success_values), "composite_score"
    ]

    if successful.empty or failed.empty:
        return skip_plot(
            "Success vs failure",
            "Both successful and failed execution scores are required"
        )

    fig, ax = plt.subplots(figsize=(7, 5))

    ax.boxplot(
        [successful.to_numpy(), failed.to_numpy()],
        tick_labels=[
            f"Success (n={len(successful)})",
            f"Failure (n={len(failed)})"
        ]
    )

    ax.set_ylabel("Composite trust score")
    ax.set_title("Composite Score by Execution Outcome")
    ax.set_ylim(0, 1)

    return save_figure(
        fig, figures_dir, "success_vs_failure.png"
    )


# ============================================================
# 10. FAILURE DISTRIBUTION
# ============================================================

def plot_failure_distribution(failures, figures_dir):

    if failures is None or failures.empty:
        return skip_plot("Failure distribution", "No failure records")

    # Prefer a framework-level distribution if the CSV contains it.
    category = find_column(
        failures, ["framework", "agent_id", "task_id", "task"]
    )

    if category is None:
        return skip_plot(
            "Failure distribution",
            f"No task/framework column found: {failures.columns.tolist()}"
        )

    count = numeric_column(
        failures,
        ["n_failed", "failure_count", "failures", "n_failures", "count"]
    )

    if count:
        data = failures[[category, count]].copy()
        data[count] = pd.to_numeric(data[count], errors="coerce")
        data = data.dropna()
        summary = data.groupby(category)[count].sum()
    else:
        # If each row is a failed execution, count rows.
        summary = failures.groupby(category).size()

    summary = summary.sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.bar(
        summary.index.astype(str),
        summary.values
    )

    ax.set_ylabel("Number of failed executions")
    ax.set_title("Failure Distribution by Task or Framework")
    ax.tick_params(axis="x", rotation=30)

    return save_figure(
        fig, figures_dir, "failure_distribution.png"
    )


# ============================================================
# 11. TASK-CLUSTER BOOTSTRAP
# ============================================================

def plot_task_cluster_bootstrap(results, figures_dir):

    if not isinstance(results, dict) or not results:
        return skip_plot("Task-cluster bootstrap", "Summary missing")

    estimate = results.get("bootstrap_pearson_mean")
    lower = results.get("bootstrap_pearson_ci_lower")
    upper = results.get("bootstrap_pearson_ci_upper")

    if estimate is None or lower is None or upper is None:
        return skip_plot(
            "Task-cluster bootstrap",
            "Bootstrap estimate or confidence interval missing"
        )

    estimate = float(estimate)
    lower = float(lower)
    upper = float(upper)

    if not np.isfinite([estimate, lower, upper]).all():
        return skip_plot("Task-cluster bootstrap", "Invalid CI values")

    fig, ax = plt.subplots(figsize=(7, 3))

    ax.errorbar(
        [estimate],
        [0],
        xerr=[
            [max(estimate - lower, 0)],
            [max(upper - estimate, 0)]
        ],
        fmt="o",
        capsize=7
    )

    ax.axvline(0, linestyle="--")
    ax.set_yticks([])
    ax.set_xlabel("Pearson correlation")
    ax.set_title("Task-Cluster Bootstrap: Estimate and 95% CI")

    return save_figure(
        fig, figures_dir, "task_cluster_bootstrap.png"
    )


# ============================================================
# MAIN FIGURE GENERATOR
# ============================================================

def generate_all_validation_figures(
    output_dir,
    figures_dir,
    trust,
    ci,
    ranking,
    sensitivity,
    ablation,
    repeatability,
    cross_domain,
    loto,
    baseline,
    failure_counts,
    cluster_results
):

    output_dir = Path(output_dir)
    figures_dir = Path(figures_dir)

    figures_dir.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 65)
    print("GENERATING VALIDATION FIGURES")
    print("=" * 65)

    print("\nOutput directory:", output_dir.resolve())
    print("Figures directory:", figures_dir.resolve())

    plot_framework_comparison(ci, figures_dir)

    plot_ranking(ranking, figures_dir)

    plot_sensitivity(sensitivity, figures_dir)

    plot_ablation(ablation, figures_dir)

    # Uses original execution-level trust dataframe.
    plot_repeatability(trust, figures_dir)

    plot_cross_domain(trust, figures_dir)

    plot_leave_one_task_out(loto, figures_dir)

    plot_baseline_comparison(baseline, figures_dir)

    plot_success_vs_failure(trust, figures_dir)

    plot_failure_distribution(failure_counts, figures_dir)

    plot_task_cluster_bootstrap(cluster_results, figures_dir)

    print("\n" + "=" * 65)
    print("FIGURE GENERATION FINISHED")
    print("=" * 65)

    print("Figures saved in:", figures_dir.resolve())