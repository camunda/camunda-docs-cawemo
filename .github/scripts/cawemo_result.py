#!/usr/bin/env python3
"""Require every independent gate; skipped/cancelled is never real success."""

import argparse
import json
import os
import sys


def destination_result(phase, dry_run, results):
    if phase not in ("stage", "live") or dry_run not in ("true", "false"):
        raise ValueError("Invalid result request")
    expected = {
        "validate": "success", "publish": "success",
        "pre-product": "skipped", "pre-global": "skipped",
        "post-product": "skipped", "post-global": "skipped",
    }
    if dry_run == "false":
        expected.update({"post-product": "success", "post-global": "success"})
        if phase == "live":
            expected.update({"pre-product": "success", "pre-global": "success"})
    return results == expected


def aggregate(results):
    return isinstance(results, dict) and bool(results) and all(value == "success" for value in results.values())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("destination", "aggregate"))
    args = parser.parse_args()
    results = json.loads(os.environ["RESULTS"])
    if args.mode == "destination":
        phase, dry = os.environ["PHASE"], os.environ["DRY_RUN"]
        passed = destination_result(phase, dry, results)
        note = ("DRY RUN ONLY: no remote mutation; real product/global gates intentionally skipped, NOT smoke passed."
                if dry == "true" else "Real publication requires every product/global gate. A failed transfer/post-gate may mean partial mutation.")
    else:
        passed = aggregate(results)
        note = "Every selected destination is required; inspect individual summaries for partial success. No automatic rollback."
    message = f"Cawemo {args.mode}: {'SUCCESS' if passed else 'FAILED'}; {json.dumps(results, sort_keys=True)}. {note}"
    print(message)
    with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as output:
        output.write(message + "\n")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
