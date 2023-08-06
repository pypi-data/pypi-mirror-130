"""Time between archival is expected in the range of secs/mins.

<p>This check is an evaluation of the median inter-archival time.
For most processes this is expected to be in the range of seconds to minutes.
<p class="scoring-explanation">The median archival time is mapped to a score as follows: <1s => 0,
<10s => 0.1, <1m => 0.2, <2m => 0.3, <5m => 0.5, <15m=>0.8 and 1 otherwise.</p>
<div class="ts-check-impact">
<p>
</p>
</div>
"""

from datetime import timedelta

import pandas as pd
import numpy as np

import timeseer

_CHECK_NAME = "Time between archival"

META: dict = {
    "checks": [{"name": _CHECK_NAME, "kpi": "Accuracy", "type": "smell"}],
    "conditions": [
        {
            "min_series": 1,
            "min_weeks": 1,
            "min_data_points": 300,
        }
    ],
    "signature": "univariate",
}


def _median_diff_times(df: pd.DataFrame) -> float:
    meas_times = df.index.to_series()
    diff_times = meas_times - meas_times.shift()
    diff_times.dropna()
    diff_times = diff_times[1:].apply(timedelta.total_seconds)
    return np.median(diff_times)


# pylint: disable=too-many-return-statements
def _run_archival_score(
    df: pd.DataFrame,
) -> float:
    median_archival = _median_diff_times(df)
    if median_archival <= 1:
        return 0
    if median_archival <= 10:
        return 0.1
    if median_archival <= 60:
        return 0.2
    if median_archival <= 120:
        return 0.3
    if median_archival <= 300:
        return 0.5
    if median_archival <= 9000:
        return 0.8
    return 1


# pylint: disable=missing-function-docstring
def run(
    analysis_input: timeseer.AnalysisInput,
) -> timeseer.AnalysisResult:
    if len(analysis_input.data) == 0:
        return timeseer.AnalysisResult()

    archival_score = _run_archival_score(analysis_input.data)
    check = timeseer.CheckResult(_CHECK_NAME, float(archival_score))
    return timeseer.AnalysisResult([check])
