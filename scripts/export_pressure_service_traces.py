#!/usr/bin/env python3
"""Add the final pressure-service traces to the PAPA dataset repository."""
import argparse
import csv
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory

TABLES = {
    "controller.csv": ("controller-trajectories.csv", (
        "tick", "actuation_enabled", "sample_valid", "decision_eligible",
        "telemetry_complete", "telemetry_coverage", "desired", "current", "ready",
        "available", "cpu_mean", "psi_ema_max_hl40", "throttle_mean",
        "history_input_source", "history_steps_available", "predicted_future_psi_h20",
        "threshold", "up_signal", "down_signal", "inflight", "readiness_degraded",
        "action", "action_target",
    )),
    "service_20s.csv": ("service-windows.csv", (
        "bin_index", "bin_start_s", "bin_end_s", "bin_mid_s", "minute_index",
        "target_rps", "request_count", "actual_rps", "latency_p50_s", "latency_p95_s",
        "latency_p99_s", "latency_mean_s", "latency_max_s", "failure_rate",
        "failure_samples", "slo_violation",
    )),
    "replica_monitor.csv": ("replica-trajectories.csv", (
        "desired", "current", "ready", "available", "updated",
        "hpa_current_utilization", "hpa_desired",
    )),
}
CATALOG = ("plan_index", "block", "policy", "threshold", "phase", "load_seconds")


def index_runs(traces, expected):
    selected = {}
    for manifest in traces.glob("*/run_manifest.txt"):
        directory = manifest.parent
        if not (directory / "_SUCCESS").is_file():
            continue
        fields = dict(line.split("=", 1) for line in manifest.read_text().splitlines()
                      if "=" in line)
        index = int(fields["plan_index"])
        if index in selected or index not in expected:
            raise ValueError(f"Duplicate or unexpected successful plan_index={index}")
        for key in ("block", "policy", "threshold"):
            if fields[key] != expected[index][key]:
                raise ValueError(f"plan_index={index}: {key} differs from run-metrics.csv")
        selected[index] = (directory, fields)
    if set(selected) != set(expected):
        raise ValueError(f"Missing successful plan indexes: {sorted(set(expected) - set(selected))}")
    return selected


def write_tables(selected, output):
    counts = {}
    with (output / "run-catalog.csv").open("w", newline="") as dst:
        writer = csv.DictWriter(dst, CATALOG, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(fields for _, fields in selected.values())
    for source, (target, fields) in TABLES.items():
        has_epoch = source != "service_20s.csv"
        header = ("plan_index",) + (("offset_seconds",) if has_epoch else ()) + fields
        counts[target] = 0
        with (output / target).open("w", newline="") as dst:
            writer = csv.DictWriter(dst, header)
            writer.writeheader()
            for index, (directory, meta) in selected.items():
                if source == "controller.csv" and meta["policy"] == "cpu_hpa":
                    continue
                with (directory / source).open(newline="") as src:
                    rows = csv.DictReader(src)
                    required = set(fields) | ({"epoch"} if has_epoch else set())
                    if not required <= set(rows.fieldnames or ()):
                        raise ValueError(f"plan_index={index} {source}: missing columns "
                                         f"{sorted(required - set(rows.fieldnames or ()))}")
                    for row in rows:
                        record = {name: row[name] for name in fields}
                        record["plan_index"] = index
                        if has_epoch:
                            record["offset_seconds"] = str(Decimal(row["epoch"]) -
                                                           Decimal(meta["k6_start_epoch"]))
                        writer.writerow(record)
                        counts[target] += 1
    return counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--traces", required=True, type=Path,
                        help="directory containing the 32 successful run subdirectories")
    args = parser.parse_args()
    output = Path(__file__).resolve().parents[1] / "data/pressure-service-closed-loop"
    with (output / "run-metrics.csv").open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    expected = {int(row["plan_index"]): row for row in rows}
    if len(rows) != 32 or len(expected) != 32 or any(
            row["technical_valid"].lower() != "true" for row in rows):
        parser.error("run-metrics.csv must contain the 32 unique technically valid runs")
    selected = index_runs(args.traces, expected)
    selected = dict(sorted(selected.items()))
    with TemporaryDirectory(dir=output) as temp:
        staging = Path(temp)
        counts = write_tables(selected, staging)
        for file in staging.iterdir():
            file.replace(output / file.name)
    print(f"Exported {len(selected)} successful runs to {output}")
    for name, count in counts.items():
        print(f"  {name}: {count:,} rows")


if __name__ == "__main__":
    main()
