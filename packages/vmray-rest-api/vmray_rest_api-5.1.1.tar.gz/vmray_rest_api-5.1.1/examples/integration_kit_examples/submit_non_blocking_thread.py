#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

import threading
import time
import sys

from pathlib import Path
from queue import Empty, Queue

from vmray.integration_kit import VMRaySubmissionKit


class Submitter(threading.Thread):
    def __init__(self, server, api_key, sample_queue, submission_id_queue):
        super().__init__()

        self.kit = VMRaySubmissionKit(server, api_key, False)
        self.sample_queue = sample_queue
        self.submission_id_queue = submission_id_queue

    def run(self):
        while True:
            sample = self.sample_queue.get()
            print(f"submitting sample: {sample}...")
            submissions = self.kit.submit_file(sample, blocking=False)
            for submission in submissions:
                print(f"sample `{sample}` has submission_id {submission.submission_id}")
                submission_id = submission.serialize()
                self.submission_id_queue.put(submission_id)


class Processor(threading.Thread):
    def __init__(self, server, api_key, submission_id_queue):
        super().__init__()

        self.kit = VMRaySubmissionKit(server, api_key, False)
        self.submission_id_queue = submission_id_queue

    def run(self):
        in_work = []
        while True:
            try:
                submission_id = self.submission_id_queue.get(timeout=5)
                in_work.append(submission_id)
            except Empty:
                pass

            for id_ in reversed(in_work):
                print(f"checking if submission {id_} is finished...")
                submission = self.kit.deserialize(id_)
                if submission.is_finished():
                    print(f"Submission {id_} is finished. Verdict: {submission.verdict}")
                    in_work.remove(id_)


def main():
    parser = argparse.ArgumentParser(description="Non-Blocking example to submit multiple samples to VMRay Platform.")
    parser.add_argument("-s", "--server", required=True, type=str, help="VMRay Platform server address.")
    parser.add_argument("-k", "--api_key", required=True, type=str, help="VMRay Platform API key.")
    parser.add_argument(
        "-d",
        "--sample_directory",
        required=True,
        type=Path,
        help="A directory with samples to submit to VMRay Platform."
    )
    args = parser.parse_args()

    if not args.sample_directory.is_dir():
        sys.exit(f"`{args.sample_directory}` is not a direcory.")

    sample_queue = Queue()
    submission_id_queue = Queue()

    submitter = Submitter(args.server, args.api_key, sample_queue, submission_id_queue)
    submitter.start()

    processor = Processor(args.server, args.api_key, submission_id_queue)
    processor.start()

    for sample in args.sample_directory.iterdir():
        sample_queue.put(sample)

    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
