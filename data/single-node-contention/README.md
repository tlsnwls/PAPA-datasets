# Single-node contention

A two-by-two experiment crosses CPU quota with noisy-neighbor CPU contention.
Five randomized blocks cover all four conditions with one target replica. The
source is the final single-node experiment, using the 20 per-run `dataset.csv`
files and their manifests. The export includes all sampled rows, including
warm-up and recovery observations. It does not select only plateau windows.

- `telemetry.csv`: one row per observation, keyed by `run_id, offset_seconds`.
  The offset is the recorded timestamp minus the per-run load start.
- `runs.csv`: one row per run. Original run identifiers were shortened to
  block, execution position, and condition, e.g. `b01-p1-q0c0`.
- `q0c0` means quota off and contention off; `q1c0`, `q0c1`, and `q1c1`
  set the corresponding switches. Quota-off CPU limits can be blank.

| Column(s) | Meaning |
| --- | --- |
| `run_id`, `block_id`, `condition` | Run key, randomized block, and condition code. |
| `quota_on`, `contention_on` | Binary condition switches. |
| `offset_seconds` | Seconds from load start. Negative values precede the load. |
| `target_rps`, `actual_rps`, `successful_rps`, `failed_rps` | Scheduled, measured, successful, and failed requests per second. |
| `dropped_iterations_rps`, `overload_503_rps` | Dropped k6 iterations per second and HTTP 503 responses per second. |
| `throughput_shortfall` | Recorded shortfall relative to offered load, as a fraction. |
| `latency_p95`, `latency_p99` | Client latency percentiles in seconds. |
| `fail_rate` | Recorded request failure fraction. |
| `cpu_cores`, `cpu_limit_cores`, `usage_fraction_of_limit` | Target CPU use and limit in cores, and use divided by the limit. |
| `cpu_psi`, `cpu_psi_full`, `node_cpu_psi` | Target CPU PSI, target CPU full PSI, and node CPU PSI. These are rate-derived stall fractions, not cumulative counters. |
| `throttle_ratio`, `throttled_seconds_rate` | Fraction of CPU periods throttled and throttled seconds per second. |
| `mem_mb`, `mem_psi`, `mem_psi_full` | Target memory in MB and target memory PSI fractions. |
| `metrics_complete` | Collector flag for observations considered complete. |
| `resource_window`, `k6_window` | Source rate or aggregation windows (in `runs.csv`). |
| `rows`, `complete_rows` | Total and complete observation counts (in `runs.csv`). |

The export does not impute missing values or overwrite throttling values
already recorded in the source. Apply any quota-off structural-zero rule
explicitly when reproducing a specific analysis.
