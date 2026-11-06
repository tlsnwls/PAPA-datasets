# Pressure-service closed-loop evaluation

Four randomized blocks cover eight conditions each. CPU-HPA and CPU-Reactive
use an 80% CPU target. PSI-Reactive and PAPA use PSI thresholds 0.15, 0.20, and
0.25. Each run applies a common 3,600-second workload. The primary latency
SLO is client p95 at or below 0.800 seconds per 20-second window.

[`run-metrics.csv`](run-metrics.csv) contains one summary row for each of
the 32 technically valid pressure-service closed-loop runs. `experiment-settings.json` captures the
relevant protocol values from the frozen experiment specification.

The following files contain traces from the 32 successful runs. They were
generated from the original run directories using
[`scripts/export_pressure_service_traces.py`](../../scripts/export_pressure_service_traces.py).

| File | Granularity |
| --- | --- |
| `run-catalog.csv` | One row per successful run. |
| `controller-trajectories.csv` | One row per controller tick, for the 28 runs of the three custom policies. CPU-HPA has no custom controller trace. |
| `service-windows.csv` | One row per 20-second client window, with the scheduled rate (`target_rps`). |
| `replica-trajectories.csv` | One row per replica monitor observation. |

Join using `plan_index`. Controller and replica times are relative to the
recorded k6 start (`offset_seconds`); client window bounds (`bin_start_s`,
`bin_end_s`) use the workload time axis. Negative offsets precede load start.
Use the workload interval for resource-cost comparisons. The export retains
measurement values and omits free-text errors, Pod identities, and local paths.

| Column(s) | Meaning |
| --- | --- |
| `plan_index`, `block`, `policy`, `threshold` (run tables) | Planned run key, randomized block, policy ID, and threshold label. `cpu_matched` denotes CPU-Reactive. Labels: `cpu80` = 80%; `low`, `nominal`, `high` = 0.15, 0.20, 0.25 PSI. |
| `phase`, `load_seconds` | Primary (`F1`) or sensitivity (`F2`) phase and load duration in seconds. |
| `slo_violation_fraction`, `slo_violation_seconds` | Fraction of all analyzed windows with p95 above 0.800 s, and that fraction multiplied by load duration. |
| `latency_p95_bin_median_s`, `latency_p95_bin_q95_s`, `latency_p99_max_s` | Median and 95th percentile of window p95s, and maximum window p99, in seconds. |
| `http_failure_rate_weighted`, `request_count_bins` | Request-weighted HTTP failure fraction and summed request count across bins. |
| `dropped_iterations` | k6 iterations not started. |
| `ready_replica_minutes`, `desired_replica_minutes` | Time integral of replica counts over load, in replica-minutes. |
| `max_ready_replicas`, `scale_up_count`, `scale_down_count` | Maximum observed Ready count and counts of replica increases and decreases. |
| `ready_r1_minutes` through `ready_r4_minutes` | Minutes spent at each observed Ready replica count. |
| `replica_monitor_max_gap_s`, `technical_valid` | Maximum monitor observation gap in seconds and technical validity flag. |
| `offset_seconds`, `tick` | Observation offset from k6 start in seconds and controller tick index. |
| `actuation_enabled`, `sample_valid`, `decision_eligible`, `telemetry_complete`, `telemetry_coverage` | Actuation, sample validity, decision eligibility, telemetry completeness, and measured coverage fraction. |
| `desired`, `current`, `ready`, `available`, `updated` | Deployment replica counts at observation time. |
| `cpu_mean`, `psi_ema_max_hl40`, `throttle_mean` | Mean Pod CPU use divided by 0.3 cores, maximum Pod PSI after 40-second-half-life EMA, and mean throttling fraction. |
| `history_input_source`, `history_steps_available`, `predicted_future_psi_h20` | Predictor input status, history length in ticks, and forecast of Deployment PSI 20 seconds ahead. |
| `threshold` (controller trajectory), `up_signal`, `down_signal` | Numeric threshold for the active policy and its scale-up and scale-down signal flags. CPU threshold is a ratio. |
| `inflight`, `readiness_degraded`, `action`, `action_target` | Transition and readiness flags, recorded action, and target replicas. |
| `hpa_current_utilization`, `hpa_desired` | HPA-reported CPU utilization in percent and desired replicas. |
| `bin_index`, `bin_start_s`, `bin_end_s`, `bin_mid_s`, `minute_index` | Window index, bounds and midpoint in seconds, and workload minute index. |
| `target_rps`, `request_count`, `actual_rps` | Scheduled rate, requests observed, and observed rate in the window. Rates are requests per second. |
| `latency_p50_s`, `latency_p95_s`, `latency_p99_s`, `latency_mean_s`, `latency_max_s` | Client latency summaries in seconds. |
| `failure_rate`, `failure_samples`, `slo_violation` | HTTP failure fraction, sample count used for that fraction, and recorded latency SLO flag. |
