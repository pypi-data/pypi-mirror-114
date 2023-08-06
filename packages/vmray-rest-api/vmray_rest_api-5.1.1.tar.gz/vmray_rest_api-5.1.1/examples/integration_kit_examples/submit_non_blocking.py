#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import time

from pathlib import Path

from vmray.integration_kit import VMRaySubmissionKit


def main():
    parser = argparse.ArgumentParser(description="Non-Blocking example to submit a sample to VMRay Platform.")
    parser.add_argument("-s", "--server", required=True, type=str, help="VMRay Platform server address.")
    parser.add_argument("-k", "--api_key", required=True, type=str, help="VMRay Platform API key.")
    parser.add_argument(
        "-f", "--sample_file", required=True, type=Path, help="A sample file to submit to VMRay Platform."
    )
    args = parser.parse_args()

    kit = VMRaySubmissionKit(args.server, args.api_key, False)
    submissions = kit.submit_file(args.sample_file, blocking=False)

    while True:
        finished_submissions = []
        for submission in submissions:
            finished_submissions.append(submission.is_finished())

        if all(finished for finished in finished_submissions):
            break

        time.sleep(5)

    for submission in submissions:
        print(f"{args.sample_file} is {submission.verdict}")


if __name__ == "__main__":
    main()
