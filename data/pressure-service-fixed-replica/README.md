# Pressure-service with fixed replicas

Four randomized blocks cover replica counts from one to four, for 16 runs.
`telemetry-20s.csv` is the original `b1_sr_canonical_20s.csv` under a
descriptive filename. It contains 768 windows. To reproduce the primary
steady-state selection, filter `steady_primary == 1` (400 windows). The
remaining rows retain baseline or transition context.

One row is a 20-second window. Use `run_name, bin_start_s` as the row key
and `plan_index` to identify the planned run.

| Column(s) | Meaning |
| --- | --- |
| `run_name`, `plan_index`, `block`, `replicas` | Run name, plan ID, randomized block, and fixed replica count. |
| `bin_start_s`, `bin_end_s`, `bin_mid_s` | Window start, end, and midpoint in seconds from load start. |
| `level_index`, `is_baseline`, `seconds_into_level`, `steady_primary` | Workload level, baseline flag, elapsed seconds in the level, and primary-analysis selection flag. |
| `target_rps`, `target_rps_per_replica`, `actual_rps`, `actual_rps_per_replica` | Offered and measured request rates for the Deployment or per replica. |
| `request_count`, `failure_rate`, `slo_violation` | Requests in the window, failure fraction, and recorded latency SLO flag. |
| `latency_p50_s`, `latency_p95_s`, `latency_p99_s`, `latency_mean_s`, `latency_max_s` | Client latency summaries in seconds. |
| `resource_snapshot_s`, `resource_staleness_s` | Time of the matched resource observation and its staleness, in seconds. |
| `cpu_quota_mean`, `cpu_quota_max` | Mean and maximum per-Pod CPU use divided by quota, as ratios. |
| `psi_mean`, `psi_max` | Mean and maximum across Pod CPU PSI fractions before EMA. |
| `psi_ema_max_hl40` | Maximum across Pod CPU PSI after per-Pod EMA with a 40-second half-life. |
| `throttle_mean`, `throttle_max` | Mean and maximum across Pod throttled-period fractions. |
| `pod_request_rps_total_1m` | Total Pod request rate over the one-minute observation window. |
| `pod_request_rps_cv_1m`, `pod_request_share_max_1m` | Coefficient of variation of Pod request rates and largest Pod share over one minute. |
| `desired_replicas`, `ready_replicas` | Deployment replica counts at the resource observation. |
