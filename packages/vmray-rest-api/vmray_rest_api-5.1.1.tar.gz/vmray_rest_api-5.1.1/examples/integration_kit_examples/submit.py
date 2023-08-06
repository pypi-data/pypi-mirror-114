#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from pathlib import Path

from vmray.integration_kit import VMRaySubmissionKit


def main():
    parser = argparse.ArgumentParser(description="Example to submit a sample to VMRay Platform.")
    parser.add_argument("-s", "--server", required=True, type=str, help="VMRay Platform server address.")
    parser.add_argument("-k", "--api_key", required=True, type=str, help="VMRay Platform API key.")
    parser.add_argument(
        "-f", "--sample_file", required=True, type=Path, help="A sample file to submit to VMRay Platform."
    )
    args = parser.parse_args()

    kit = VMRaySubmissionKit(args.server, args.api_key, False)
    results = kit.submit_file(args.sample_file)

    for result in results:
        print(f"Submission is {result.verdict}")
        _ = result.get_artifacts()
        _ = result.get_reports()
        _ = result.get_vtis()


if __name__ == "__main__":
    main()
