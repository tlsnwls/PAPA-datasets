# PAPA CPU Pressure Datasets

These datasets link CPU Pressure Stall Information (PSI) to resource usage,
client latency, and, in the closed-loop experiments, autoscaling decisions and
replica readiness. They cover two benchmark applications evaluated on
Kubernetes: pressure-service and ResNet-app.

| Dataset | Design | Start here |
| --- | --- | --- |
| [Single-node contention](data/single-node-contention/README.md) | 5 blocks × 4 CPU quota and contention conditions | `telemetry.csv`: 801 observations from 20 runs |
| [Pressure-service fixed replicas](data/pressure-service-fixed-replica/README.md) | 4 blocks × 4 replica counts | `telemetry-20s.csv`: 768 windows from 16 runs, including 400 steady windows |
| [Pressure-service closed loop](data/pressure-service-closed-loop/README.md) | 4 blocks × 8 policy and threshold conditions | `run-metrics.csv`: 32 technically valid runs; window and controller traces are exported separately |
| [ResNet-app closed loop](data/resnet-app-closed-loop/README.md) | 4 blocks × 3 workloads × 4 policies | `run-metrics.csv`: 48 technically valid runs, with controller trajectories, SLO windows, and workload schedules |

Each dataset README describes its provenance, row granularity, keys, units,
and columns. The experiment folders deliberately keep their native sampling
intervals. Join tables within an experiment by run key before aligning time;
controller ticks and client latency windows do not necessarily occur at the
same cadence.

- PSI in these files is derived from CPU stall telemetry. Pod-level PSI and
  Deployment PSI are distinct. The latter is the maximum of the per-Pod PSI
  values after smoothing, where that aggregation is used.
- Blank and NaN values are missing or not applicable, depending on the column. They
  are not zero. Preserve them when loading the CSVs.
- Closed-loop comparisons use matched blocks as the unit of comparison.
  Repeated windows in a run are not independent experimental replicates.
- Model weights, input image payloads, debug logs, credentials, and full
  cluster snapshots are outside the scope of these datasets.

Related code: [PAPA controller](https://github.com/tlsnwls/PAPA) and
[benchmark applications](https://github.com/tlsnwls/PAPA-Benchmarks).
