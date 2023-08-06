import json
import time

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, BinaryIO, Dict, Iterator, List, Optional

from packaging.version import Version
from vmray.rest_api import VMRayRESTAPI


class VMRayAPIWrapper(VMRayRESTAPI):
    def __init__(self, server: str, api_key: str, verify_cert: bool = True):
        super().__init__(server, api_key, verify_cert=verify_cert)

    def system_info(self) -> Dict[str, Any]:
        return self.call("GET", "/rest/system_info")

    def get_platform_version(self) -> Version:
        system_info = self.system_info()
        return Version(system_info["version"])

    def get_analyses_by_submission_id(self, submission_id: int) -> List[Dict[str, Any]]:
        return self.call("GET", f"/rest/analysis?analysis_submission_id={submission_id}")

    def get_report(self, analysis_id: int) -> BinaryIO:
        return self.call(
            "GET",
            f"/rest/analysis/{analysis_id}/archive/logs/summary_v2.json",
            raw_data=True
        )

    def get_vtis_by_sample_id(self, sample_id: int) -> Dict[str, Any]:
        return self.call("GET", f"/rest/sample/{sample_id}/vtis")

    def get_sample_info(self, sample_id: int) -> Dict[str, Any]:
        return self.call("GET", f"/rest/sample/{sample_id}")

    def get_artifacts(self, sample_id: int, all_artifacts: bool) -> Dict[str, Any]:
        return self.call("GET", f"/rest/sample/{sample_id}/iocs/all_artifacts/{all_artifacts}")

    def get_submission(self, submission_id: int) -> Dict[str, Any]:
        return self.call("GET", f"/rest/submission/{submission_id}")

    def get_submissions(self, last_submission_id: Optional[int], limit: int = 100) -> List[Dict[str, Any]]:
        params = {"_order": "asc", "_limit": limit}

        if last_submission_id:
            if self.get_platform_version() >= Version("4.0.1"):
                # _last_id parameter was introduced in 4.0 and fixed in 4.0.1
                # greater than
                params["_last_id"] = last_submission_id
            else:
                # greater than or equals
                params["_min_id"] = last_submission_id + 1

        data = self.call("GET", "/rest/submission", params=params)
        return data

    def get_submissions_by_sample_id(self, sample_id: int) -> List[Dict[str, Any]]:
        return self.call("GET", f"/rest/submission?submission_sample_id={sample_id}")

    def submission_finished(self, submission_id: int) -> bool:
        return self.get_submission(submission_id)["submission_finished"]

    def submit(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return self.call("POST", "/rest/sample/submit", params=params)


@dataclass
class SubmissionResult:
    _api: VMRayAPIWrapper
    submission_id: int
    _sample_id: int = field(init=False)
    child_sample_ids: List[int] = field(default_factory=list)
    classifications: List[str] = field(default_factory=list)
    threat_names: List[str] = field(default_factory=list)
    verdict: Optional[str] = None
    verdict_reason: Optional[str] = None

    def __post_init__(self) -> None:
        sub = self._api.get_submission(self.submission_id)
        self._sample_id = sub["submission_sample_id"]

        if sub["submission_finished"]:
            self._update()

    def _update(self) -> None:
        """Update this `SampleResult`. This method is called automatically.

        Exceptions:
            VMRayRESTAPIError: An error occurred while interacting with VMRay Platform.
        """

        sample_info = self._api.get_sample_info(self._sample_id)
        self.child_sample_ids = sample_info.get("sample_child_sample_ids", [])
        self.classifications = sample_info.get("sample_classifications", [])
        self.threat_names = sample_info.get("sample_threat_names", [])
        self.verdict = sample_info.get("sample_verdict")
        self.verdict_reason = sample_info.get("sample_verdict_reason_description")

    def serialize(self) -> int:
        return self.submission_id

    def is_finished(self) -> bool:
        """Checks, if a submission is finished.

        Only use this method when a sample was submitted in non-blocking mode,
        otherwise `SampleResult` is fully initialized.

        Exception:
            VMRayRESTAPIError: An error occurred while interacting with VMRay Platform.
        """

        is_finished = self._api.submission_finished(self.submission_id)
        if is_finished:
            self._update()

        return is_finished

    def get_vtis(self) -> Dict[str, Any]:
        """Get threat indicators for a sample.

        Exceptions:
            KeyError: The VTI result is invalid.
            VMRayRESTAPIError: An error occurred while interacting with VMRay Platform.
        """

        return self._api.get_vtis_by_sample_id(self._sample_id)["threat_indicators"]

    def get_artifacts(self, ioc_only: bool = True) -> Dict[str, Any]:
        """Get all artifacts for a sample.

        Parameters:
            ioc_only : bool
                only return artifacts that are Indicators Of Compromise (IOC)

        Exceptions:
            KeyError: The artifacts result is invalid.
            VMRayRESTAPIError: An error occurred while interacting with VMRay Platform.
        """

        return self._api.get_artifacts(self._sample_id, not ioc_only)["iocs"]

    def get_reports(self) -> List[Dict[str, Any]]:
        """Get all reports for a submission.

        Exceptions:
            KeyError: The analysis result is invalid.
            VMRayRESTAPIError: An error occurred while interacting with VMRay Platform.
        """

        reports = list(self.iter_reports())
        return reports

    def iter_reports(self) -> Iterator[Dict[str, Any]]:
        """Iterator for all reports for a submission.

        Exceptions:
            KeyError: The analysis result is invalid.
            VMRayRESTAPIError: An error occurred while interacting with VMRay Platform.
        """

        analyses = self._api.get_analyses_by_submission_id(self.submission_id)

        for analysis in analyses:
            analysis_id = analysis["analysis_id"]
            report = self._api.get_report(analysis_id)
            yield json.load(report)


class VMRaySubmissionKit:
    """A class to submit files and URLs on VMRay Platform."""

    def __init__(self, server: str, api_key: str, verify_cert: bool = True) -> None:
        """
        Parameters:
            server : str
                URL to the VMRay Platform server
            api_key :str
                API key for VMRay Platform server
            verify_cert : bool
                verify SSL/TLS certificate of VMRay Platform server
        """

        self._api = VMRayAPIWrapper(server, api_key, verify_cert)

    def _wait_for_submissions(self, submissions: List[Dict[str, Any]]) -> None:
        """Wait for submissions to finish."""

        submission_ids = [submission["submission_id"] for submission in submissions]

        while True:
            submissions_finished = []
            for submission_id in submission_ids:
                finished = self._api.submission_finished(submission_id)
                submissions_finished.append(finished)

            if all(finished for finished in submissions_finished):
                break

            time.sleep(5)

    def _submit(self, blocking: bool, params: Dict[str, Any]) -> List[SubmissionResult]:
        """Submit a sample to VMRay Platform and process the result.

        Exceptions:
            ValueError: The submission result is invalid.
        """

        result = self._api.submit(params)

        try:
            submissions = result["submissions"]
            _ = [s["submission_id"] for s in submissions]
        except KeyError as exc:
            raise ValueError("The submission result is invalid") from exc

        if not blocking:
            return [
                SubmissionResult(self._api, s["submission_id"])
                for s in submissions
            ]

        self._wait_for_submissions(submissions)

        results = []
        for submission in submissions:
            sample_result = SubmissionResult(self._api, submission["submission_id"])
            results.append(sample_result)

        return results

    def submit_file(
        self, sample_path: Path, blocking: bool = True, params: Optional[Dict[str, Any]] = None
    ) -> List[SubmissionResult]:
        """Submit a file on VMRay Platform.

        Parameters:
            sample_path : Path
                Path to a file you want to analyze.
            blocking : bool
                Wait for an analysis to finish before returning.
            params : Optional[Dict[str, Any]]
                Key/Value pairs to configure the analysis.
                More documentation can be found in the API docs.

        Exceptions:
            FileNotFoundError: An error indicating that the file couldn't be found.
            ValueError: The submission result is invalid.
            VMRayRESTAPIError: An error occurred while interacting with VMRay Platform.
        """

        if not params:
            params = {}

        with sample_path.open("rb") as fobj:
            params["sample_file"] = fobj
            return self._submit(blocking, params)

    def submit_url(
        self, url: str, blocking: bool = True, params: Optional[Dict[str, Any]] = None
    ) -> List[SubmissionResult]:
        """Submit a URL on VMRay Platform.

        Parameters:
            url : str
                URL to a website you want to analyze.
            blocking : bool
                Wait for an analysis to finish before returning.
            params : Optional[Dict[str, Any]]
                Key/Value pairs to configure the analysis.
                More documentation can be found in the API docs.

        Exceptions:
            ValueError: The submission result is invalid.
            VMRayRESTAPIError: An error occurred while interacting with VMRay Platform.
        """

        if not params:
            params = {}

        params["sample_url"] = url
        return self._submit(blocking, params)

    def iter_submissions(self, last_submission_id: Optional[int], limit: int = 100) -> Iterator[SubmissionResult]:
        """An iterator for finished submissions.

        Retrieves submissions based on `last_submissions_id` where `limit` determines
        how many per iteration.

        Parameters:
            last_submission_id : Optional[int]
                A submission ID to start with.
                The first submission is used if ID is `0` or `None`.
            limit : int
                Number of submissions to fetch for one iteration.

        Exceptions:
            ValueError: The submission result is invalid.
            VMRayRESTAPIError: An error occurred while interacting with VMRay Platform.
        """

        submissions = self._api.get_submissions(last_submission_id, limit)

        for submission in submissions:
            try:
                sample_result = SubmissionResult(self._api, submission["submission_id"])
            except KeyError as exc:
                raise ValueError("The submission result is invalid") from exc

            yield sample_result

    def deserialize(self, submission_id: int) -> SubmissionResult:
        """Deserialize `SubmissionResult` from a value returned by `SubmissionResult.serialize`"""

        return SubmissionResult(self._api, submission_id)

    def get_submissions_from_sample_id(self, sample_id: int) -> List[SubmissionResult]:
        """Get a list of submissions related to a sample ID

        Exceptions:
            ValueError: The submission result is invalid.
            VMRayRESTAPIError: An error occurred while interacting with VMRay Platform.
        """

        submissions = []
        for submission in self._api.get_submissions_by_sample_id(sample_id):
            try:
                submissions.append(SubmissionResult(self._api, submission["submission_id"]))
            except KeyError as exc:
                raise ValueError("The submission result is invalid") from exc

        return submissions
