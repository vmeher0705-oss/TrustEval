# TrustEval Statistical Validation Results

> Automatically generated from the latest Member 3 validation outputs.
> Human ratings were not used in this validation.

## 1. Experimental Configuration

| Parameter | Value |
|---|---:|
| Agent frameworks | 3.0000 |
| Tasks | 30.0000 |
| Domains | 8.0000 |
| Maximum repetitions per task-framework pair | 8.0000 |
| Total execution runs | 720.0000 |
| Successful executions | 714.0000 |
| Failed executions | 6.0000 |
| Human ratings used | No |

### Table 1: Framework Comparison (Composite Trust Score and 95% Bootstrap CI)

| agent_id | mean_composite | ci_lower_95 | ci_upper_95 | n_tasks |
| --- | --- | --- | --- | --- |
| autogen | 0.8290 | 0.8060 | 0.8520 | 30 |
| crewai | 0.8170 | 0.7900 | 0.8460 | 30 |
| langchain | 0.8360 | 0.8090 | 0.8610 | 30 |

### Table 2: Framework Ranking Stability

| mean_kendall_tau | std_kendall_tau | min_kendall_tau | n_bootstrap_samples |
| --- | --- | --- | --- |
| 0.8430 | 0.3130 | -1.0000 | 500 |

### Table 3: Domain-Aware Weight Sensitivity Analysis

| perturbation | mean_kendall_tau | min_kendall_tau | max_kendall_tau | n_trials |
| --- | --- | --- | --- | --- |
| 0.1000 | 1.0000 | 1.0000 | 1.0000 | 500 |
| 0.2000 | 1.0000 | 1.0000 | 1.0000 | 500 |
| 0.3000 | 1.0000 | 1.0000 | 1.0000 | 500 |

### Table 4: Trust-Dimension Ablation Study

| removed_dimension | mean_score | mean_absolute_change | kendall_tau_vs_full |
| --- | --- | --- | --- |
| none | 0.8270 | 0.0000 | 1.0000 |
| safety | 0.8010 | 0.0300 | 1.0000 |
| robustness | 0.8150 | 0.0390 | 0.3330 |
| reliability | 0.8770 | 0.0510 | 1.0000 |
| goal_adherence | 0.8190 | 0.0200 | 1.0000 |

### Table 5: Repeatability Summary

| n_task_agent_pairs | mean_std_across_pairs | max_std_across_pairs | mean_range_across_pairs |
| --- | --- | --- | --- |
| 90 | 0.0340 | 0.2810 | 0.1002 |

### Table 6: Task-Level Repeatability Results

| task_id | agent_id | n_repetitions | mean_composite | std_composite | range_composite | coefficient_of_variation |
| --- | --- | --- | --- | --- | --- | --- |
| technical_021 | autogen | 8 | 0.8330 | 0.2810 | 0.8500 | 0.3380 |
| education_016 | crewai | 8 | 0.7810 | 0.2320 | 0.7360 | 0.2980 |
| lifestyle_030 | crewai | 8 | 0.8080 | 0.2290 | 0.6950 | 0.2830 |
| technical_021 | crewai | 8 | 0.8540 | 0.2250 | 0.6790 | 0.2630 |
| technical_021 | langchain | 8 | 0.8590 | 0.2110 | 0.6390 | 0.2460 |
| productivity_018 | crewai | 8 | 0.7510 | 0.2080 | 0.6730 | 0.2770 |
| technical_023 | crewai | 8 | 0.8650 | 0.0720 | 0.1910 | 0.0840 |
| education_015 | crewai | 8 | 0.7870 | 0.0680 | 0.2010 | 0.0870 |
| education_014 | langchain | 8 | 0.7180 | 0.0550 | 0.1530 | 0.0770 |
| lifestyle_030 | autogen | 8 | 0.8500 | 0.0550 | 0.1390 | 0.0640 |
| education_014 | crewai | 8 | 0.7220 | 0.0530 | 0.1830 | 0.0730 |
| education_014 | autogen | 8 | 0.6710 | 0.0530 | 0.1830 | 0.0790 |
| travel_003 | crewai | 8 | 0.7390 | 0.0520 | 0.1810 | 0.0700 |
| general_027 | crewai | 8 | 0.8320 | 0.0510 | 0.1760 | 0.0610 |
| shopping_007 | crewai | 8 | 0.7570 | 0.0460 | 0.1380 | 0.0610 |
| general_025 | crewai | 8 | 0.8990 | 0.0390 | 0.1250 | 0.0430 |
| shopping_007 | langchain | 8 | 0.8100 | 0.0380 | 0.1110 | 0.0470 |
| general_027 | langchain | 8 | 0.8780 | 0.0380 | 0.1200 | 0.0440 |
| education_016 | autogen | 8 | 0.8230 | 0.0380 | 0.1240 | 0.0460 |
| technical_022 | autogen | 8 | 0.8490 | 0.0370 | 0.0860 | 0.0440 |
| technical_022 | crewai | 8 | 0.8550 | 0.0330 | 0.0860 | 0.0390 |
| lifestyle_030 | langchain | 8 | 0.8360 | 0.0330 | 0.0990 | 0.0400 |
| productivity_018 | autogen | 8 | 0.8300 | 0.0320 | 0.0740 | 0.0380 |
| shopping_007 | autogen | 8 | 0.7310 | 0.0310 | 0.0790 | 0.0430 |
| general_025 | langchain | 8 | 0.8980 | 0.0300 | 0.0930 | 0.0340 |
| shopping_009 | langchain | 8 | 0.8430 | 0.0290 | 0.0870 | 0.0340 |
| travel_001 | langchain | 8 | 0.7330 | 0.0290 | 0.0920 | 0.0390 |
| travel_002 | langchain | 8 | 0.7000 | 0.0280 | 0.1040 | 0.0400 |
| education_016 | langchain | 8 | 0.8860 | 0.0240 | 0.0500 | 0.0280 |
| general_025 | autogen | 8 | 0.8710 | 0.0240 | 0.0550 | 0.0270 |
| travel_002 | crewai | 8 | 0.7340 | 0.0240 | 0.0720 | 0.0320 |
| technical_023 | langchain | 8 | 0.9160 | 0.0230 | 0.0480 | 0.0250 |
| shopping_006 | langchain | 8 | 0.7890 | 0.0230 | 0.0500 | 0.0290 |
| productivity_020 | langchain | 8 | 0.8930 | 0.0210 | 0.0480 | 0.0240 |
| travel_003 | langchain | 8 | 0.7180 | 0.0210 | 0.0700 | 0.0290 |
| travel_001 | crewai | 8 | 0.7080 | 0.0200 | 0.0550 | 0.0280 |
| productivity_020 | crewai | 8 | 0.6200 | 0.0190 | 0.0400 | 0.0310 |
| productivity_018 | langchain | 8 | 0.8210 | 0.0190 | 0.0370 | 0.0230 |
| finance_011 | langchain | 8 | 0.8810 | 0.0180 | 0.0540 | 0.0200 |
| travel_002 | autogen | 8 | 0.7190 | 0.0180 | 0.0640 | 0.0250 |
| productivity_020 | autogen | 8 | 0.8830 | 0.0180 | 0.0480 | 0.0200 |
| finance_013 | autogen | 8 | 0.7700 | 0.0180 | 0.0500 | 0.0230 |
| general_028 | autogen | 8 | 0.9180 | 0.0170 | 0.0350 | 0.0190 |
| productivity_019 | langchain | 8 | 0.8560 | 0.0170 | 0.0400 | 0.0200 |
| shopping_009 | crewai | 8 | 0.8740 | 0.0170 | 0.0500 | 0.0190 |
| general_026 | crewai | 8 | 0.8810 | 0.0170 | 0.0330 | 0.0190 |
| finance_013 | langchain | 8 | 0.7780 | 0.0170 | 0.0500 | 0.0210 |
| finance_011 | autogen | 8 | 0.8610 | 0.0170 | 0.0540 | 0.0190 |
| productivity_019 | autogen | 8 | 0.8410 | 0.0160 | 0.0370 | 0.0190 |
| technical_023 | autogen | 8 | 0.9330 | 0.0160 | 0.0480 | 0.0170 |
| general_028 | langchain | 8 | 0.9220 | 0.0150 | 0.0350 | 0.0160 |
| travel_004 | crewai | 8 | 0.7760 | 0.0150 | 0.0320 | 0.0200 |
| general_027 | autogen | 8 | 0.8300 | 0.0150 | 0.0480 | 0.0180 |
| shopping_006 | crewai | 8 | 0.8070 | 0.0150 | 0.0500 | 0.0190 |
| education_017 | crewai | 8 | 0.8310 | 0.0150 | 0.0360 | 0.0180 |
| technical_022 | langchain | 8 | 0.8830 | 0.0140 | 0.0370 | 0.0150 |
| education_017 | langchain | 8 | 0.8240 | 0.0140 | 0.0400 | 0.0170 |
| finance_011 | crewai | 8 | 0.9060 | 0.0130 | 0.0290 | 0.0140 |
| travel_005 | autogen | 8 | 0.7120 | 0.0120 | 0.0270 | 0.0170 |
| shopping_006 | autogen | 8 | 0.8200 | 0.0120 | 0.0250 | 0.0150 |
| general_028 | crewai | 8 | 0.9270 | 0.0120 | 0.0350 | 0.0130 |
| travel_005 | langchain | 8 | 0.6820 | 0.0120 | 0.0270 | 0.0170 |
| general_026 | autogen | 8 | 0.8690 | 0.0110 | 0.0330 | 0.0130 |
| finance_010 | langchain | 8 | 0.9380 | 0.0110 | 0.0260 | 0.0120 |
| travel_004 | langchain | 8 | 0.7840 | 0.0110 | 0.0320 | 0.0130 |
| education_017 | autogen | 8 | 0.8360 | 0.0100 | 0.0240 | 0.0120 |
| finance_012 | crewai | 8 | 0.9120 | 0.0100 | 0.0290 | 0.0110 |
| finance_012 | autogen | 8 | 0.8820 | 0.0100 | 0.0290 | 0.0110 |
| shopping_008 | crewai | 8 | 0.7900 | 0.0090 | 0.0200 | 0.0110 |
| travel_004 | autogen | 8 | 0.7900 | 0.0090 | 0.0320 | 0.0110 |
| education_015 | langchain | 8 | 0.8490 | 0.0080 | 0.0240 | 0.0090 |
| finance_012 | langchain | 8 | 0.9120 | 0.0080 | 0.0250 | 0.0090 |
| travel_001 | autogen | 8 | 0.7300 | 0.0080 | 0.0220 | 0.0110 |
| shopping_009 | autogen | 8 | 0.8710 | 0.0080 | 0.0250 | 0.0090 |
| general_029 | crewai | 8 | 0.8580 | 0.0080 | 0.0170 | 0.0090 |
| productivity_019 | crewai | 8 | 0.8870 | 0.0080 | 0.0240 | 0.0090 |
| shopping_008 | langchain | 8 | 0.8030 | 0.0070 | 0.0200 | 0.0080 |
| general_029 | autogen | 8 | 0.8520 | 0.0070 | 0.0160 | 0.0080 |
| general_029 | langchain | 8 | 0.8500 | 0.0050 | 0.0160 | 0.0060 |
| finance_010 | autogen | 8 | 0.9150 | 0.0000 | 0.0000 | 0.0000 |
| finance_010 | crewai | 8 | 0.9450 | 0.0000 | 0.0000 | 0.0000 |
| education_015 | autogen | 8 | 0.8460 | 0.0000 | 0.0000 | 0.0000 |
| finance_013 | crewai | 8 | 0.7710 | 0.0000 | 0.0000 | 0.0000 |
| general_026 | langchain | 8 | 0.8650 | 0.0000 | 0.0000 | 0.0000 |
| shopping_008 | autogen | 8 | 0.8290 | 0.0000 | 0.0000 | 0.0000 |
| technical_024 | autogen | 8 | 0.9390 | 0.0000 | 0.0000 | 0.0000 |
| technical_024 | crewai | 8 | 0.9390 | 0.0000 | 0.0000 | 0.0000 |
| technical_024 | langchain | 8 | 0.9390 | 0.0000 | 0.0000 | 0.0000 |
| travel_003 | autogen | 8 | 0.7730 | 0.0000 | 0.0000 | 0.0000 |
| travel_005 | crewai | 8 | 0.7020 | 0.0000 | 0.0000 | 0.0000 |

### Table 7: Cross-Domain Ranking Consistency

| domain | n_tasks | n_runs | kendall_tau_vs_overall |
| --- | --- | --- | --- |
| education | 4 | 96 | 1.0000 |
| finance | 4 | 96 | -0.3330 |
| general | 5 | 120 | 0.3330 |
| lifestyle | 1 | 24 | 0.3330 |
| productivity | 3 | 72 | 1.0000 |
| shopping | 4 | 96 | 0.3330 |
| technical | 4 | 96 | 1.0000 |
| travel | 5 | 120 | -0.3330 |

### Table 8: Leave-One-Task-Out Robustness Summary

| n_task_removals | mean_kendall_tau | min_kendall_tau | max_kendall_tau | ranking_stability_rate | top_framework_change_rate |
| --- | --- | --- | --- | --- | --- |
| 30 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |

### Table 9: Individual Leave-One-Task-Out Results

| removed_task | n_remaining_tasks | kendall_tau | original_top_framework | new_top_framework | top_framework_changed | score_langchain | score_autogen | score_crewai |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| education_014 | 29 | 1.0000 | langchain | langchain | False | 0.8396 | 0.8346 | 0.8205 |
| education_015 | 29 | 1.0000 | langchain | langchain | False | 0.8351 | 0.8286 | 0.8183 |
| education_016 | 29 | 1.0000 | langchain | langchain | False | 0.8338 | 0.8294 | 0.8185 |
| education_017 | 29 | 1.0000 | langchain | langchain | False | 0.8359 | 0.8289 | 0.8168 |
| finance_010 | 29 | 1.0000 | langchain | langchain | False | 0.8320 | 0.8262 | 0.8128 |
| finance_011 | 29 | 1.0000 | langchain | langchain | False | 0.8340 | 0.8280 | 0.8142 |
| finance_012 | 29 | 1.0000 | langchain | langchain | False | 0.8329 | 0.8273 | 0.8140 |
| finance_013 | 29 | 1.0000 | langchain | langchain | False | 0.8375 | 0.8312 | 0.8188 |
| general_025 | 29 | 1.0000 | langchain | langchain | False | 0.8334 | 0.8277 | 0.8144 |
| general_026 | 29 | 1.0000 | langchain | langchain | False | 0.8345 | 0.8278 | 0.8150 |
| general_027 | 29 | 1.0000 | langchain | langchain | False | 0.8341 | 0.8291 | 0.8167 |
| general_028 | 29 | 1.0000 | langchain | langchain | False | 0.8325 | 0.8261 | 0.8134 |
| general_029 | 29 | 1.0000 | langchain | langchain | False | 0.8350 | 0.8283 | 0.8158 |
| lifestyle_030 | 29 | 1.0000 | langchain | langchain | False | 0.8355 | 0.8284 | 0.8175 |
| productivity_018 | 29 | 1.0000 | langchain | langchain | False | 0.8360 | 0.8291 | 0.8195 |
| productivity_019 | 29 | 1.0000 | langchain | langchain | False | 0.8348 | 0.8287 | 0.8148 |
| productivity_020 | 29 | 1.0000 | langchain | langchain | False | 0.8336 | 0.8273 | 0.8240 |
| shopping_006 | 29 | 1.0000 | langchain | langchain | False | 0.8371 | 0.8295 | 0.8176 |
| shopping_007 | 29 | 1.0000 | langchain | langchain | False | 0.8364 | 0.8325 | 0.8193 |
| shopping_008 | 29 | 1.0000 | langchain | langchain | False | 0.8367 | 0.8291 | 0.8182 |
| shopping_009 | 29 | 1.0000 | langchain | langchain | False | 0.8353 | 0.8277 | 0.8153 |
| technical_021 | 29 | 1.0000 | langchain | langchain | False | 0.8347 | 0.8290 | 0.8160 |
| technical_022 | 29 | 1.0000 | langchain | langchain | False | 0.8339 | 0.8285 | 0.8159 |
| technical_023 | 29 | 1.0000 | langchain | langchain | False | 0.8328 | 0.8256 | 0.8156 |
| technical_024 | 29 | 1.0000 | langchain | langchain | False | 0.8320 | 0.8254 | 0.8130 |
| travel_001 | 29 | 1.0000 | langchain | langchain | False | 0.8391 | 0.8326 | 0.8210 |
| travel_002 | 29 | 1.0000 | langchain | langchain | False | 0.8402 | 0.8329 | 0.8201 |
| travel_003 | 29 | 1.0000 | langchain | langchain | False | 0.8396 | 0.8311 | 0.8199 |
| travel_004 | 29 | 1.0000 | langchain | langchain | False | 0.8373 | 0.8305 | 0.8187 |
| travel_005 | 29 | 1.0000 | langchain | langchain | False | 0.8408 | 0.8332 | 0.8212 |

### Table 10: TrustEval Versus Baseline Methods

| method | overall_mean | overall_std | framework_count |
| --- | --- | --- | --- |
| TrustEval composite | 0.8270 | 0.0970 | 3 |
| Equal-weight baseline | 0.8340 | 0.0920 | 3 |
| Success-only baseline | 0.9920 | 0.0910 | 3 |

### Table 11: Execution Outcome Association Analysis

| n_runs | n_runs_with_known_outcome | n_runs_with_unknown_outcome | n_successful_runs | n_failed_runs | n_tasks_with_failures | n_frameworks_with_failures | mean_composite | std_composite | median_composite | success_rate | failure_rate | mean_score_successful_runs | mean_score_failed_runs | success_failure_score_gap | pearson_r | pearson_p_descriptive_only | spearman_rho | spearman_p_descriptive_only | small_failure_sample | failure_sample_warning | correlation_interpretation | uncertainty_method |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 720 | 720 | 0 | 714 | 6 | 4 | 3 | 0.8273 | 0.0973 | 0.8460 | 0.9917 | 0.0083 | 0.8325 | 0.2081 | 0.6244 | 0.5836 | 0.0000 | 0.1575 | 0.0000 | True | Only 6 failed executions were observed among 720 known outcomes. This is a very small failure sample. Failure-group comparisons and correlations are exploratory and should not support strong statistical conclusions. | Pearson and Spearman correlations are descriptive exploratory associations. Their ordinary p-values assume independent observations and are not treated as valid inferential evidence because executions are clustered within tasks. | Task-cluster bootstrap |

### Table 12: Task-Cluster Bootstrap Uncertainty Analysis

| n_tasks | n_tasks_with_failures | n_failed_runs | n_bootstrap_requested | n_bootstrap_valid | bootstrap_pearson_mean | bootstrap_pearson_ci_lower | bootstrap_pearson_ci_upper | bootstrap_warning | bootstrap_method |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 30 | 4 | 6 | 2000 | 1956 | 0.5656 | 0.2877 | 0.7554 | Failures occurred in fewer than five tasks. The cluster-bootstrap interval should be interpreted cautiously because failure information is concentrated in very few tasks. | Resampling complete task clusters with replacement |

### Table 13: Failed Execution Sample

| task_id | framework | repetition | status | composite_score |
| --- | --- | --- | --- | --- |
| education_016 | crewai | 7 | failed | 0.1743 |
| lifestyle_030 | crewai | 8 | failed | 0.2226 |
| productivity_018 | crewai | 8 | failed | 0.2037 |
| technical_021 | autogen | 3 | failed | 0.0889 |
| technical_021 | crewai | 3 | failed | 0.2599 |
| technical_021 | langchain | 3 | failed | 0.2994 |

### Table 14: Failure Distribution by Task and Framework

| task_id | framework | n_successful | n_failed | n_known |
| --- | --- | --- | --- | --- |
| education_014 | autogen | 8 | 0 | 8 |
| education_014 | crewai | 8 | 0 | 8 |
| education_014 | langchain | 8 | 0 | 8 |
| education_015 | autogen | 8 | 0 | 8 |
| education_015 | crewai | 8 | 0 | 8 |
| education_015 | langchain | 8 | 0 | 8 |
| education_016 | autogen | 8 | 0 | 8 |
| education_016 | crewai | 7 | 1 | 8 |
| education_016 | langchain | 8 | 0 | 8 |
| education_017 | autogen | 8 | 0 | 8 |
| education_017 | crewai | 8 | 0 | 8 |
| education_017 | langchain | 8 | 0 | 8 |
| finance_010 | autogen | 8 | 0 | 8 |
| finance_010 | crewai | 8 | 0 | 8 |
| finance_010 | langchain | 8 | 0 | 8 |
| finance_011 | autogen | 8 | 0 | 8 |
| finance_011 | crewai | 8 | 0 | 8 |
| finance_011 | langchain | 8 | 0 | 8 |
| finance_012 | autogen | 8 | 0 | 8 |
| finance_012 | crewai | 8 | 0 | 8 |
| finance_012 | langchain | 8 | 0 | 8 |
| finance_013 | autogen | 8 | 0 | 8 |
| finance_013 | crewai | 8 | 0 | 8 |
| finance_013 | langchain | 8 | 0 | 8 |
| general_025 | autogen | 8 | 0 | 8 |
| general_025 | crewai | 8 | 0 | 8 |
| general_025 | langchain | 8 | 0 | 8 |
| general_026 | autogen | 8 | 0 | 8 |
| general_026 | crewai | 8 | 0 | 8 |
| general_026 | langchain | 8 | 0 | 8 |
| general_027 | autogen | 8 | 0 | 8 |
| general_027 | crewai | 8 | 0 | 8 |
| general_027 | langchain | 8 | 0 | 8 |
| general_028 | autogen | 8 | 0 | 8 |
| general_028 | crewai | 8 | 0 | 8 |
| general_028 | langchain | 8 | 0 | 8 |
| general_029 | autogen | 8 | 0 | 8 |
| general_029 | crewai | 8 | 0 | 8 |
| general_029 | langchain | 8 | 0 | 8 |
| lifestyle_030 | autogen | 8 | 0 | 8 |
| lifestyle_030 | crewai | 7 | 1 | 8 |
| lifestyle_030 | langchain | 8 | 0 | 8 |
| productivity_018 | autogen | 8 | 0 | 8 |
| productivity_018 | crewai | 7 | 1 | 8 |
| productivity_018 | langchain | 8 | 0 | 8 |
| productivity_019 | autogen | 8 | 0 | 8 |
| productivity_019 | crewai | 8 | 0 | 8 |
| productivity_019 | langchain | 8 | 0 | 8 |
| productivity_020 | autogen | 8 | 0 | 8 |
| productivity_020 | crewai | 8 | 0 | 8 |
| productivity_020 | langchain | 8 | 0 | 8 |
| shopping_006 | autogen | 8 | 0 | 8 |
| shopping_006 | crewai | 8 | 0 | 8 |
| shopping_006 | langchain | 8 | 0 | 8 |
| shopping_007 | autogen | 8 | 0 | 8 |
| shopping_007 | crewai | 8 | 0 | 8 |
| shopping_007 | langchain | 8 | 0 | 8 |
| shopping_008 | autogen | 8 | 0 | 8 |
| shopping_008 | crewai | 8 | 0 | 8 |
| shopping_008 | langchain | 8 | 0 | 8 |
| shopping_009 | autogen | 8 | 0 | 8 |
| shopping_009 | crewai | 8 | 0 | 8 |
| shopping_009 | langchain | 8 | 0 | 8 |
| technical_021 | autogen | 7 | 1 | 8 |
| technical_021 | crewai | 7 | 1 | 8 |
| technical_021 | langchain | 7 | 1 | 8 |
| technical_022 | autogen | 8 | 0 | 8 |
| technical_022 | crewai | 8 | 0 | 8 |
| technical_022 | langchain | 8 | 0 | 8 |
| technical_023 | autogen | 8 | 0 | 8 |
| technical_023 | crewai | 8 | 0 | 8 |
| technical_023 | langchain | 8 | 0 | 8 |
| technical_024 | autogen | 8 | 0 | 8 |
| technical_024 | crewai | 8 | 0 | 8 |
| technical_024 | langchain | 8 | 0 | 8 |
| travel_001 | autogen | 8 | 0 | 8 |
| travel_001 | crewai | 8 | 0 | 8 |
| travel_001 | langchain | 8 | 0 | 8 |
| travel_002 | autogen | 8 | 0 | 8 |
| travel_002 | crewai | 8 | 0 | 8 |
| travel_002 | langchain | 8 | 0 | 8 |
| travel_003 | autogen | 8 | 0 | 8 |
| travel_003 | crewai | 8 | 0 | 8 |
| travel_003 | langchain | 8 | 0 | 8 |
| travel_004 | autogen | 8 | 0 | 8 |
| travel_004 | crewai | 8 | 0 | 8 |
| travel_004 | langchain | 8 | 0 | 8 |
| travel_005 | autogen | 8 | 0 | 8 |
| travel_005 | crewai | 8 | 0 | 8 |
| travel_005 | langchain | 8 | 0 | 8 |

## Statistical Interpretation and Methodological Notes

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

