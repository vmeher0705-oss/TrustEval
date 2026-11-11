
"""
TrustEval Member 3
Complete Statistical Validation Pipeline

Features:
- No human ratings used.
- Execution-based trust score validation.
- Task-level bootstrap confidence intervals.
- Framework ranking stability.
- Weight sensitivity analysis.
- Trust-dimension ablation.
- Execution repeatability.
- Cross-domain validation.
- Leave-one-task-out robustness.
- Baseline comparison.
- Execution outcome analysis.
- Task-cluster bootstrap.
- Failure reporting.
- Automatic figure generation.
- Automatic comparison_tables.md generation.
"""

from pathlib import Path
import sys
import pandas as pd


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

VALIDATION_DIR = PROJECT_ROOT / "validation"
RESULTS_DIR = PROJECT_ROOT / "results"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
FIGURES_DIR = OUTPUT_DIR / "figures"

TRUST_SCORES_PATH = RESULTS_DIR / "trust_scores.json"


# ============================================================
# PYTHON IMPORT PATH
# ============================================================

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(VALIDATION_DIR))
sys.path.insert(0, str(Path(__file__).resolve().parent))


# ============================================================
# IMPORT VALIDATION MODULES
# ============================================================

from data_loader import load_trust_scores

from confidence_intervals import (
    per_agent_confidence_intervals
)

from ranking_stability import (
    get_ranking,
    ranking_stability
)

from sensitivity_analysis import sensitivity_analysis

from repeatability import (
    repeatability_analysis,
    repeatability_summary
)

from ablation import ablation_study

from baseline_comparison import (
    compare_baseline_vs_trusteval
)

from cross_domain_validation import cross_domain_validation

from robustness_testing import (
    leave_one_task_out,
    robustness_summary
)

from calibration import (
    calibration_analysis,
    task_cluster_bootstrap,
    failure_sample_report,
    failure_distribution
)

from visualization import generate_all_validation_figures

from format_comparison_tables import generate_comparison_tables


# ============================================================
# CREATE OUTPUT DIRECTORIES
# ============================================================

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def save_dataframe(dataframe, filename):

    output_path = OUTPUT_DIR / filename

    dataframe.to_csv(output_path, index=False)

    print(f"Saved: {output_path}")

    return output_path


def save_dictionary(data, filename):

    dataframe = pd.DataFrame([data])

    return save_dataframe(dataframe, filename)


# ============================================================
# CHECK PROJECT STRUCTURE
# ============================================================

def check_project_structure():

    print("\nChecking project structure...")

    print(f"Project root: {PROJECT_ROOT}")
    print(f"Validation directory: {VALIDATION_DIR}")
    print(f"Results directory: {RESULTS_DIR}")
    print(f"Trust scores file: {TRUST_SCORES_PATH}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Figures directory: {FIGURES_DIR}")

    if not RESULTS_DIR.exists():

        raise FileNotFoundError(
            f"Results directory does not exist: {RESULTS_DIR}"
        )

    if not TRUST_SCORES_PATH.exists():

        raise FileNotFoundError(
            f"Could not find trust_scores.json: {TRUST_SCORES_PATH}"
        )

    if not VALIDATION_DIR.exists():

        raise FileNotFoundError(
            f"Validation directory does not exist: {VALIDATION_DIR}"
        )

    print("\ntrust_scores.json FOUND.")


# ============================================================
# VALIDATE INPUT DATA
# ============================================================

def validate_input_data(trust):

    required_columns = {
        "task_id",
        "framework",
        "domain",
        "repetition",
        "composite_score",
        "status"
    }

    missing_columns = required_columns - set(trust.columns)

    if missing_columns:

        raise ValueError(
            "Missing required trust score columns: "
            + ", ".join(sorted(missing_columns))
        )

    if trust.empty:

        raise ValueError(
            "The loaded trust scores dataframe is empty."
        )

    trust["composite_score"] = pd.to_numeric(
        trust["composite_score"],
        errors="coerce"
    )

    if trust["composite_score"].isna().any():

        raise ValueError(
            "Some composite scores are missing or non-numeric."
        )

    if not trust["composite_score"].between(0, 1).all():

        raise ValueError(
            "Composite scores must be between 0 and 1."
        )

    print("\nInput data validation successful.")

    return trust


# ============================================================
# MAIN PIPELINE
# ============================================================

def main():

    print("\n")
    print("=" * 75)
    print("TrustEval — Member 3 Statistical Validation")
    print("=" * 75)

    # --------------------------------------------------------
    # 1. CHECK PROJECT STRUCTURE
    # --------------------------------------------------------

    check_project_structure()

    # --------------------------------------------------------
    # 2. LOAD TRUST SCORES
    # --------------------------------------------------------

    print("\nLoading Member 2 trust scores...")

    trust = load_trust_scores(TRUST_SCORES_PATH)

    trust = validate_input_data(trust)

    print(f"\nLoaded {len(trust)} execution runs.")
    print(f"Tasks: {trust['task_id'].nunique()}")
    print(f"Frameworks: {trust['framework'].nunique()}")
    print(f"Domains: {trust['domain'].nunique()}")
    print(f"Repetitions: {trust['repetition'].nunique()}")

    print("\nFrameworks:")
    print(trust["framework"].dropna().unique())

    # ========================================================
    # 3. CONFIDENCE INTERVALS
    # ========================================================

    print("\n[1/12] Task-level bootstrap confidence intervals")

    ci = per_agent_confidence_intervals(trust)

    print(ci.to_string(index=False))

    save_dataframe(ci, "confidence_intervals.csv")

    # ========================================================
    # 4. RANKING STABILITY
    # ========================================================

    print("\n[2/12] Framework ranking stability")

    ranking = get_ranking(trust)

    stability = ranking_stability(trust)

    print("\nFramework ranking:")
    print(ranking.sort_values().to_string())

    print("\nRanking stability:")
    print(stability)

    save_dictionary(
        stability,
        "ranking_stability.csv"
    )

    # ========================================================
    # 5. SENSITIVITY ANALYSIS
    # ========================================================

    print("\n[3/12] Domain-aware weight sensitivity")

    sensitivity_results = []

    for perturbation in (0.10, 0.20, 0.30):

        print(
            f"\nTesting ±{perturbation * 100:.0f}% "
            "weight perturbation..."
        )

        result = sensitivity_analysis(
            trust,
            perturbation=perturbation,
            n_trials=500,
            seed=42
        )

        sensitivity_results.append(result)

    sensitivity = pd.concat(
        sensitivity_results,
        ignore_index=True
    )

    print(sensitivity.to_string(index=False))

    save_dataframe(
        sensitivity,
        "sensitivity_analysis.csv"
    )

    # ========================================================
    # 6. ABLATION STUDY
    # ========================================================

    print("\n[4/12] Trust-dimension ablation")

    ablation = ablation_study(trust)

    print(ablation.to_string(index=False))

    save_dataframe(
        ablation,
        "ablation_study.csv"
    )

    # ========================================================
    # 7. REPEATABILITY
    # ========================================================

    print("\n[5/12] Repeatability across repeated executions")

    repeatability = repeatability_analysis(trust)

    print(repeatability.head(20).to_string(index=False))

    repeatability_result = repeatability_summary(
        repeatability
    )

    print("\nRepeatability summary:")
    print(repeatability_result)

    save_dataframe(
        repeatability,
        "repeatability.csv"
    )

    # ========================================================
    # 8. CROSS-DOMAIN VALIDATION
    # ========================================================

    print("\n[6/12] Cross-domain ranking consistency")

    cross_domain = cross_domain_validation(trust)

    print(cross_domain.to_string(index=False))

    save_dataframe(
        cross_domain,
        "cross_domain_validation.csv"
    )

    # ========================================================
    # 9. LEAVE-ONE-TASK-OUT ROBUSTNESS
    # ========================================================

    print("\n[7/12] Leave-one-task-out robustness")

    loto = leave_one_task_out(trust)

    print(loto.head(20).to_string(index=False))

    loto_summary = robustness_summary(loto)

    print("\nRobustness summary:")
    print(loto_summary)

    save_dataframe(
        loto,
        "robustness_leave_one_task_out.csv"
    )

    # ========================================================
    # 10. BASELINE COMPARISON
    # ========================================================

    print("\n[8/12] Baseline comparison")

    baseline = compare_baseline_vs_trusteval(trust)

    print(baseline.to_string(index=False))

    save_dataframe(
        baseline,
        "baseline_comparison.csv"
    )

    # ========================================================
    # 11. EXECUTION OUTCOME ANALYSIS
    # ========================================================

    print("\n[9/12] Execution outcome analysis")

    calibration = calibration_analysis(trust)

    print("\nExecution outcome results:")

    for key, value in calibration.items():

        print(f"{key}: {value}")

    save_dictionary(
        calibration,
        "calibration.csv"
    )

    # ========================================================
    # 12. TASK-CLUSTER BOOTSTRAP
    # ========================================================

    print("\n[10/12] Task-cluster bootstrap")

    cluster_results = task_cluster_bootstrap(
        trust,
        n_bootstrap=2000,
        seed=42
    )

    print("\nTask-cluster bootstrap results:")

    for key, value in cluster_results.items():

        print(f"{key}: {value}")

    save_dictionary(
        cluster_results,
        "task_cluster_bootstrap.csv"
    )

    # ========================================================
    # 13. FAILED EXECUTION SAMPLE
    # ========================================================

    print("\n[11/12] Reporting individual failed executions")

    failures = failure_sample_report(trust)

    print("\nFailed execution sample:")

    if failures.empty:

        print("No failed executions found.")

    else:

        print(failures.to_string(index=False))

    print(f"\nTotal failed executions: {len(failures)}")

    save_dataframe(
        failures,
        "failure_sample.csv"
    )

    # ========================================================
    # 14. FAILURE DISTRIBUTION
    # ========================================================

    print("\n[12/12] Reporting failures by task and framework")

    failure_counts = failure_distribution(trust)

    print("\nFailure distribution:")

    print(failure_counts.to_string(index=False))

    save_dataframe(
        failure_counts,
        "failure_distribution.csv"
    )

    # ========================================================
    # 15. OVERALL VALIDATION SUMMARY
    # ========================================================

    print("\nGenerating overall validation summary...")

    summary = pd.DataFrame([{

        "n_runs": len(trust),

        "n_tasks": trust["task_id"].nunique(),

        "n_frameworks": trust["framework"].nunique(),

        "n_domains": trust["domain"].nunique(),

        "n_repetitions_max": (
            trust.groupby(
                ["task_id", "framework"]
            )["repetition"].count().max()
        ),

        "n_successful_runs": calibration[
            "n_successful_runs"
        ],

        "n_failed_runs": calibration[
            "n_failed_runs"
        ],

        "success_rate": calibration[
            "success_rate"
        ],

        "failure_rate": calibration[
            "failure_rate"
        ],

        "n_tasks_with_failures": calibration[
            "n_tasks_with_failures"
        ],

        "mean_composite": trust[
            "composite_score"
        ].mean(),

        "std_composite": trust[
            "composite_score"
        ].std(),

        "bootstrap_pearson_mean": cluster_results[
            "bootstrap_pearson_mean"
        ],

        "bootstrap_ci_lower": cluster_results[
            "bootstrap_pearson_ci_lower"
        ],

        "bootstrap_ci_upper": cluster_results[
            "bootstrap_pearson_ci_upper"
        ]

    }])

    save_dataframe(
        summary,
        "validation_summary.csv"
    )

    # ========================================================
    # 16. GENERATE ALL VALIDATION FIGURES
    # ========================================================

    print("\nGenerating all validation figures...")

    generate_all_validation_figures(
        output_dir=OUTPUT_DIR,
        figures_dir=FIGURES_DIR,
        trust=trust,
        ci=ci,
        ranking=ranking,
        sensitivity=sensitivity,
        ablation=ablation,
        repeatability=repeatability,
        cross_domain=cross_domain,
        loto=loto,
        baseline=baseline,
        failure_counts=failure_counts,
        cluster_results=cluster_results
    )

    # ========================================================
    # 17. GENERATE COMPARISON TABLES
    # ========================================================

    print("\nGenerating comparison_tables.md...")

    comparison_path = generate_comparison_tables(
        output_dir=OUTPUT_DIR
    )

    print(
        "\nComparison tables successfully generated:"
    )

    print(comparison_path)

    # ========================================================
    # 18. COMPLETE
    # ========================================================

    print("\n")
    print("=" * 75)
    print("VALIDATION COMPLETE")
    print("=" * 75)

    print(f"\nAll validation outputs were saved to:\n{OUTPUT_DIR}")

    print(f"\nFigures saved to:\n{FIGURES_DIR}")

    print(f"\nComparison report:\n{comparison_path}")

    print("\nHuman ratings were NOT used.")

    print(
        f"\nThe Member 3 pipeline validated {len(trust)} "
        "execution runs."
    )

    print("=" * 75)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()
