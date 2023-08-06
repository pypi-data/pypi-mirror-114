#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from vmray.integration_kit import VMRaySubmissionKit


def main():
    parser = argparse.ArgumentParser(description="Example to iterate over finished submissions.")
    parser.add_argument("-s", "--server", required=True, type=str, help="VMRay Platform server address.")
    parser.add_argument("-k", "--api_key", required=True, type=str, help="VMRay Platform API key.")
    parser.add_argument("-l", "--last_submission_id", type=int, default=0, help="A submission ID to start with.")
    args = parser.parse_args()

    kit = VMRaySubmissionKit(args.server, args.api_key, False)

    last_processed_id = None
    for submission in kit.iter_submissions(args.last_submission_id):
        last_processed_id = submission.submission_id

        for report in submission.iter_reports():
            print(report["mitre_attack"])

    if not last_processed_id:
        print("Could not find new submissions.")
        return

    print(f"Start the next iteration with submission ID `{last_processed_id}`.")


if __name__ == "__main__":
    main()
