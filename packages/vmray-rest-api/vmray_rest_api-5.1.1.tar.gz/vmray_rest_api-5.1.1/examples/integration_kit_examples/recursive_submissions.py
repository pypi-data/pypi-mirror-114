#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from typing import Iterator
from pathlib import Path

from vmray.integration_kit import VMRaySubmissionKit, SubmissionResult


def iter_recursive_submissions(kit: VMRaySubmissionKit, sample_id: int) -> Iterator[SubmissionResult]:
    child_submissions = kit.get_submissions_from_sample_id(sample_id)

    for submission in child_submissions:
        for child_sample_id in submission.child_sample_ids:
            yield from iter_recursive_submissions(kit, child_sample_id)
        yield submission


def main():
    parser = argparse.ArgumentParser(description="Example how to get recursive submission results.")
    parser.add_argument("-s", "--server", required=True, type=str, help="VMRay Platform server address.")
    parser.add_argument("-k", "--api_key", required=True, type=str, help="VMRay Platform API key.")
    parser.add_argument(
        "-f", "--sample_file", required=True, type=Path, help="A sample file to submit to VMRay Platform."
    )
    args = parser.parse_args()

    kit = VMRaySubmissionKit(args.server, args.api_key, False)
    results = kit.submit_file(args.sample_file)

    for result in results:
        if not result.child_sample_ids:
            print(f"Submission {result.submission_id} has no child samples")
            continue

        for child_sample_id in result.child_sample_ids:
            for submission in iter_recursive_submissions(kit, child_sample_id):
                print(f"Submission ({submission.submission_id}) is {submission.verdict}")


if __name__ == "__main__":
    main()
