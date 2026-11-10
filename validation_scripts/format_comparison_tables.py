
"""
TrustEval Member 3
Paper-ready comparison table generator.

Generates comparison_tables.md from the latest statistical
validation CSV outputs.

This version does NOT use human ratings.
It uses execution outcomes and task-level statistical validation.
"""

from pathlib import Path
import pandas as pd
import numpy as np


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

OUTPUT_DIR = PROJECT_ROOT / "outputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def load_csv(filename, required=False):

    path = OUTPUT_DIR / filename

    if not path.exists():

        if required:
            raise FileNotFoundError(
                f"Required validation output not found: {path}"
            )

        print(f"Warning: Optional file not found: {path}")

        return pd.DataFrame()

    return pd.read_csv(path)


def clean_value(value):

    if pd.isna(value):
        return ""

    if isinstance(value, (float, np.floating)):
        return f"{value:.4f}"

    return str(value)


def df_to_md(df, title):

    if df.empty:

        return (
            f"### {title}\n\n"
            "_No data available for this analysis._\n\n"
        )

    display_df = df.copy()

    display_df = display_df.fillna("")

    headers = [str(column) for column in display_df.columns]

    rows = []

    for row in display_df.itertuples(index=False, name=None):

        rows.append([
            clean_value(value).replace("|", "\\|").replace("\n", " ")
            for value in row
        ])

    markdown = []

    markdown.append(f"### {title}\n")

    markdown.append(
        "| " + " | ".join(headers) + " |"
    )

    markdown.append(
        "| " + " | ".join(["---"] * len(headers)) + " |"
    )

    for row in rows:

        markdown.append(
            "| " + " | ".join(row) + " |"
        )

    return "\n".join(markdown) + "\n\n"


def get_summary_value(summary, column, default="N/A"):

    if summary.empty or column not in summary.columns:
        return default

    return clean_value(summary.iloc[0][column])


def add_section(sections, dataframe, title, columns=None):

    if dataframe.empty:

        return

    display_df = dataframe.copy()

    if columns:

        available_columns = [
            column for column in columns
            if column in display_df.columns
        ]

        if available_columns:
            display_df = display_df[available_columns]

    sections.append(
        df_to_md(display_df, title)
    )


# ============================================================
# GENERATE COMPARISON TABLES
# ============================================================

def generate_comparison_tables(output_dir=None):

    global OUTPUT_DIR

    if output_dir is not None:
        OUTPUT_DIR = Path(output_dir)
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("\nGenerating paper-ready comparison tables...")

    sections = []

    # --------------------------------------------------------
    # LOAD VALIDATION OUTPUTS
    # --------------------------------------------------------

    summary = load_csv("validation_summary.csv", required=True)

    ci = load_csv("confidence_intervals.csv")

    ranking = load_csv("ranking_stability.csv")

    sensitivity = load_csv("sensitivity_analysis.csv")

    ablation = load_csv("ablation_study.csv")

    repeatability = load_csv("repeatability.csv")

    cross_domain = load_csv("cross_domain_validation.csv")

    loto = load_csv("robustness_leave_one_task_out.csv")

    baseline = load_csv("baseline_comparison.csv")

    calibration = load_csv("calibration.csv")

    bootstrap = load_csv("task_cluster_bootstrap.csv")

    failures = load_csv("failure_sample.csv")

    failure_distribution = load_csv("failure_distribution.csv")

    # --------------------------------------------------------
    # EXPERIMENTAL CONFIGURATION
    # --------------------------------------------------------

    n_runs = get_summary_value(summary, "n_runs")

    n_tasks = get_summary_value(summary, "n_tasks")

    n_frameworks = get_summary_value(summary, "n_frameworks")

    n_domains = get_summary_value(summary, "n_domains")

    n_success = get_summary_value(
        summary, "n_successful_runs"
    )

    n_failed = get_summary_value(
        summary, "n_failed_runs"
    )

    n_repetitions = get_summary_value(
        summary, "n_repetitions_max"
    )

    sections.append(
        f"""# TrustEval Statistical Validation Results

> Automatically generated from the latest Member 3 validation outputs.
> Human ratings were not used in this validation.

## 1. Experimental Configuration

| Parameter | Value |
|---|---:|
| Agent frameworks | {n_frameworks} |
| Tasks | {n_tasks} |
| Domains | {n_domains} |
| Maximum repetitions per task-framework pair | {n_repetitions} |
| Total execution runs | {n_runs} |
| Successful executions | {n_success} |
| Failed executions | {n_failed} |
| Human ratings used | No |

"""
    )

    # --------------------------------------------------------
    # TABLE 1: FRAMEWORK COMPARISON
    # --------------------------------------------------------

    add_section(
        sections,
        ci,
        "Table 1: Framework Comparison (Composite Trust Score and 95% Bootstrap CI)",
        [
            "agent_id",
            "mean_composite",
            "ci_lower_95",
            "ci_upper_95",
            "n_tasks"
        ]
    )

    # --------------------------------------------------------
    # TABLE 2: RANKING STABILITY
    # --------------------------------------------------------

    add_section(
        sections,
        ranking,
        "Table 2: Framework Ranking Stability",
        [
            "mean_kendall_tau",
            "std_kendall_tau",
            "min_kendall_tau",
            "n_bootstrap_samples"
        ]
    )

    # --------------------------------------------------------
    # TABLE 3: SENSITIVITY ANALYSIS
    # --------------------------------------------------------

    add_section(
        sections,
        sensitivity,
        "Table 3: Domain-Aware Weight Sensitivity Analysis",
        [
            "perturbation",
            "mean_kendall_tau",
            "min_kendall_tau",
            "max_kendall_tau",
            "n_trials"
        ]
    )

    # --------------------------------------------------------
    # TABLE 4: ABLATION STUDY
    # --------------------------------------------------------

    add_section(
        sections,
        ablation,
        "Table 4: Trust-Dimension Ablation Study",
        [
            "removed_dimension",
            "mean_score",
            "mean_absolute_change",
            "kendall_tau_vs_full"
        ]
    )

    # --------------------------------------------------------
    # TABLE 5: REPEATABILITY
    # --------------------------------------------------------

    if not repeatability.empty:

        repeatability_summary = pd.DataFrame([{
            "n_task_agent_pairs": len(repeatability),

            "mean_std_across_pairs": (
                repeatability["std_composite"].mean()
                if "std_composite" in repeatability.columns
                else np.nan
            ),

            "max_std_across_pairs": (
                repeatability["std_composite"].max()
                if "std_composite" in repeatability.columns
                else np.nan
            ),

            "mean_range_across_pairs": (
                repeatability["range_composite"].mean()
                if "range_composite" in repeatability.columns
                else np.nan
            ),
        }])

        add_section(
            sections,
            repeatability_summary,
            "Table 5: Repeatability Summary",
        )

        add_section(
            sections,
            repeatability,
            "Table 6: Task-Level Repeatability Results",
            [
                "task_id",
                "agent_id",
                "n_repetitions",
                "mean_composite",
                "std_composite",
                "range_composite",
                "coefficient_of_variation"
            ]
        )

    # --------------------------------------------------------
    # TABLE 7: CROSS-DOMAIN VALIDATION
    # --------------------------------------------------------

    add_section(
        sections,
        cross_domain,
        "Table 7: Cross-Domain Ranking Consistency",
        [
            "domain",
            "n_tasks",
            "n_runs",
            "kendall_tau_vs_overall"
        ]
    )

    # --------------------------------------------------------
    # TABLE 8: LEAVE-ONE-TASK-OUT ROBUSTNESS
    # --------------------------------------------------------

    if not loto.empty:

        loto_summary = pd.DataFrame([{
            "n_task_removals": len(loto),

            "mean_kendall_tau": (
                loto["kendall_tau"].mean()
                if "kendall_tau" in loto.columns
                else np.nan
            ),

            "min_kendall_tau": (
                loto["kendall_tau"].min()
                if "kendall_tau" in loto.columns
                else np.nan
            ),

            "max_kendall_tau": (
                loto["kendall_tau"].max()
                if "kendall_tau" in loto.columns
                else np.nan
            ),

            "ranking_stability_rate": (
                (loto["kendall_tau"] == 1).mean()
                if "kendall_tau" in loto.columns
                else np.nan
            ),

            "top_framework_change_rate": (
                loto["top_framework_changed"].mean()
                if "top_framework_changed" in loto.columns
                else np.nan
            )
        }])

        add_section(
            sections,
            loto_summary,
            "Table 8: Leave-One-Task-Out Robustness Summary"
        )

        add_section(
            sections,
            loto,
            "Table 9: Individual Leave-One-Task-Out Results"
        )

    # --------------------------------------------------------
    # TABLE 10: BASELINE COMPARISON
    # --------------------------------------------------------

    add_section(
        sections,
        baseline,
        "Table 10: TrustEval Versus Baseline Methods"
    )

    # --------------------------------------------------------
    # TABLE 11: EXECUTION OUTCOME ANALYSIS
    # --------------------------------------------------------

    add_section(
        sections,
        calibration,
        "Table 11: Execution Outcome Association Analysis"
    )

    # --------------------------------------------------------
    # TABLE 12: TASK-CLUSTER BOOTSTRAP
    # --------------------------------------------------------

    add_section(
        sections,
        bootstrap,
        "Table 12: Task-Cluster Bootstrap Uncertainty Analysis"
    )

    # --------------------------------------------------------
    # TABLE 13: FAILED EXECUTION SAMPLE
    # --------------------------------------------------------

    add_section(
        sections,
        failures,
        "Table 13: Failed Execution Sample"
    )

    # --------------------------------------------------------
    # TABLE 14: FAILURE DISTRIBUTION
    # --------------------------------------------------------

    add_section(
        sections,
        failure_distribution,
        "Table 14: Failure Distribution by Task and Framework"
    )

    # --------------------------------------------------------
    # METHODOLOGICAL NOTES
    # --------------------------------------------------------

    sections.append(
        """## Statistical Interpretation and Methodological Notes

1. TrustEval composite scores are evaluated using task-level
   statistical validation.

2. Confidence intervals use task-level bootstrap resampling.

3. Ranking stability evaluates consistency in framework rankings.

4. Sensitivity analysis evaluates the effect of perturbing
   dimension weights.

5. Ablation analysis measures the effect of removing individual
   trust dimensions.

6. Repeatability evaluates variation across repeated executions
   of the same task-framework pair.

7. Cross-domain validation evaluates ranking consistency
   across different task domains.

8. Leave-one-task-out analysis evaluates whether framework
   rankings depend heavily on individual tasks.

9. Execution outcome analysis compares composite scores with
   observed successful and failed executions.

10. Task-cluster bootstrap resamples complete task clusters
    to estimate uncertainty in the score-outcome association.

11. Only six failed executions were observed in the supplied
    experimental results. Failure-related comparisons are
    exploratory and should not support strong statistical claims.

12. Correlation p-values are descriptive only. Ordinary
    run-level correlation tests do not account for dependence
    among executions from the same tasks.

13. No human ratings or human-judgment correlation analysis
    were used.

14. These results evaluate execution-based consistency and
    robustness. They do not establish probability calibration
    against human judgments.

---

## Reproducibility

To regenerate these tables, execute:

```bash
python validation_scripts/run_all.py
```

The generated report is:

`outputs/comparison_tables.md`

"""
    )

    # --------------------------------------------------------
    # WRITE MARKDOWN FILE
    # --------------------------------------------------------

    output_path = OUTPUT_DIR / "comparison_tables.md"

    output = "".join(sections)

    with open(output_path, "w", encoding="utf-8") as file:

        file.write(output)

    print("\n" + "=" * 65)

    print("COMPARISON TABLE GENERATION COMPLETE")

    print("=" * 65)

    print(f"\nGenerated {len(sections) - 1} report sections.")

    print(f"Output: {output_path}")

    return output_path


# ============================================================
# RUN DIRECTLY
# ============================================================

if __name__ == "__main__":

    generate_comparison_tables()
