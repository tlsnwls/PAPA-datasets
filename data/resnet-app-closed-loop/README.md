# ResNet-app closed-loop evaluation

The final closed-loop evaluation comprises 48 runs: four randomized blocks,
three 1,800-second workloads (Step, Ramp, and Trace), and four policies.
The scaling target is the Inference Deployment. The PAPA policy forecasts
Deployment PSI 60 seconds ahead. The client latency SLO is p95 at or below
800 milliseconds in a 60-second window. Unavailable windows are identified
separately in the analysis tables.

| File | Rows and purpose |
| --- | --- |
| `run-plan.csv` | 48 planned conditions, with workload schedule names. |
| `run-metrics.csv` | 48 selected runs with performance, capacity, and scaling outcomes. |
| `controller-trajectories.csv` | 4,320 aligned 20-second observations of controller signals and replicas. Fields unavailable for a policy remain blank. |
| `slo-windows.csv` | 1,440 latency analysis windows. |
| `scale-events.csv` | 306 observed replica transitions. |
| `attempts.csv` | 50 attempts: 48 selected runs and two excluded attempts. Operational smoke checks are not included. |
| `paired-comparisons.csv` | 60 within-block comparisons across policies and workloads. |
| `workloads/` | Three workload schedules. In `run-plan.csv`, resolve `schedule_file` inside this directory. |

The primary source is the final campaign's `analysis/` output and the
frozen workload schedules in `experiment-contract/`. Join run tables by
`plan_index`; join paired results by `block, workload, comparison`.
Attempt records are keyed by `plan_index, attempt`. Offsets are in seconds
relative to workload onset. The export omits free-text errors and
unnecessary absolute timestamps, and preserves latency units.

| Column(s) | Meaning |
| --- | --- |
| `plan_index`, `block`, `order_in_block` | Planned run key, randomized block, and position within block. |
| `workload`, `workload_mode`, `schedule_file` | Workload ID, interpolation mode, and schedule filename. |
| `policy`, `policy_name` | Policy ID and display name. |
| `attempt`, `selected`, `technical_valid`, `review_required` | Attempt identifier, analysis inclusion flag, technical validity, and review flag. |
| `performance_failure`, `slo_violation_fraction`, `slo_violation_windows` | Run performance failure flag and fraction/count of SLO-violating latency windows. |
| `p95_ms`, `p99_ms` | Client latency percentiles in milliseconds. In `slo-windows.csv`, `p95_ms` is per window. |
| `failure_rate`, `dropped_fraction` | Request failure fraction and dropped iterations as a fraction of planned arrivals. |
| `actual_rps`, `started_rps`, `successful_rps` | Measured, started, and successful requests per second. |
| `planned_arrivals`, `dropped_iterations`, `requests_started`, `requests_completed` | Load generator counts for the run. |
| `unavailable_window_fraction`, `service_degradation_fraction` | Fractions of unavailable windows and windows classified as degraded by the analyzer. |
| `ready_replica_minutes`, `desired_replica_minutes`, `cpu_minutes` | Integrated Ready replicas, desired replicas, and actual CPU usage over load. CPU minutes are core-minutes. |
| `max_ready_replicas`, `scale_up_count`, `scale_down_count`, `oscillation_count`, `restart_max` | Peak Ready count, increase and decrease counts, direction reversals, and maximum reported restarts. |
| `predictive_lead_seconds`, `proactive_scale_up_count`, `first_scale_up_proactive` | Analyzer's predictive lead in seconds, count of forecast-only scale-ups, and whether the first scale-up was forecast-only. |
| `first_scale_up_offset_seconds`, `first_effective_capacity_offset_seconds` | Seconds from load start to first scale-up and first effective capacity increase, where observed. |
| `offset_seconds`, `sample_valid` | Seconds from load start and sample validity flag in controller traces. |
| `current_psi`, `predicted_psi`, `cpu_utilization`, `throttle` | Current Deployment PSI, forecast Deployment PSI, CPU utilization ratio, and throttling ratio. |
| `desired`, `ready`, `action`, `reason`, `actuation_applied` | Observed replica counts, controller action, reason code, and whether the action was applied. |
| `index`, `start_offset_seconds`, `request_count`, `valid_response_count`, `slo_violated`, `unavailable` | Window index, start time, request and valid response counts, SLO violation and availability flags. |
| `from`, `to` | Replica count before and after a scale event. |
| `target_rps`, `source_target_rps` | ResNet offered requests per second and, for Trace, the rate in the source schedule before mapping. |
| `comparison`, `first`, `second` | Label and ordered policies for a paired comparison. |
| `delta_*` | Analyzer's paired differences (first minus second), in the units of the named metric. |
| `papa_predictive_lead_seconds`, `ready_replica_minutes_change_fraction`, `slo_improvement_pp` | PAPA lead time in seconds, relative Ready replica-minute change, and SLO improvement in percentage points. |
