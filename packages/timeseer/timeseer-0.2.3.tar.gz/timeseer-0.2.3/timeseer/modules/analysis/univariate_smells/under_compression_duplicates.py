"""There should be no consecutively recorded repeated values.

<p>This check is a simple check for undercompression. If there are repeated
consecutive values recorded closer together than the maximum allowed time frame
by the compression settings, this could indicate that the exception setting is too strict.</p>
<p class="scoring-explanation">The score for this check is a simple boolean (True / False).</p>
<div class="ts-check-impact">
<p>
Badly compressed data, specifically overcompression,
can lead to critical events such as upsets, safety issues and downtime.
</p>
</div>
"""

import pandas as pd

import timeseer

from timeseer import DataType

_CHECK_NAME = "No repeated values"

META: dict = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "kpi": "Consistency",
            "type": "smell",
            "data_type": "bool",
        }
    ],
    "conditions": [
        {
            "min_series": 1,
            "min_weeks": 1,
            "min_data_points": 300,
            "data_type": [
                DataType.FLOAT32,
                DataType.FLOAT64,
                DataType.DICTIONARY,
                DataType.CATEGORICAL,
            ],
        }
    ],
    "signature": "univariate",
}


def _are_consecutive_duplicates_present(df: pd.DataFrame) -> int:
    return int(any(df["value"].diff() == 0))


# pylint: disable=missing-function-docstring
def run(
    analysis_input: timeseer.AnalysisInput,
) -> timeseer.AnalysisResult:
    if len(analysis_input.data) == 0:
        return timeseer.AnalysisResult()

    check = timeseer.CheckResult(
        _CHECK_NAME,
        float(_are_consecutive_duplicates_present(analysis_input.data)),
    )
    return timeseer.AnalysisResult(check_results=[check])
