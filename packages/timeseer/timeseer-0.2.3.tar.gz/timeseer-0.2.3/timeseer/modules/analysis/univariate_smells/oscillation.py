"""Identify periods in series where there is a dominant oscillation frequency.

<p>For most sensors the presence of oscillations is an indication of an underlying problem.
This could be, for instance, due to problems with a controller (either directly or upstream).</p>
<p>Image here</p>
<p class="scoring-explanation">The score of this check is calculated based on the sum of time of all
the event-frames containing oscillations. E.g. assume a total period being analyzed of 1 year and
2 event-frames of 1 month and 2 months respectively with oscillations.
The score of this check will then be 75% = 1 - 3 / 12. Which means that in 75% of
time no oscillation is detected.</p>
<div class="ts-check-impact">
<p>
Oscillations typically lead to higher variability in the product quality and more stress on the control
system.
Any type of anomaly detection based on normal behavior of the phyiscal sensor can act as a guide for
prioritization of callibration / maintenance.
</p>
</div>
"""

import logging

from typing import List

import numpy as np
import pandas as pd

from scipy import signal, stats
from scipy.signal import butter

import timeseer

from timeseer import DataType
from timeseer.analysis.utils import (
    event_frames_from_dataframe,
    merge_intervals_and_open_event_frames,
    process_open_intervals,
    calculate_local_score,
)
from timeseer.metadata import fields

_CHECK_NAME = "Oscillation"

META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "kpi": "Validity",
            "type": "smell",
            "event_frames": ["Oscillation"],
            "weight": 1,
        }
    ],
    "conditions": [
        {
            "min_series": 1,
            "min_weeks": 1,
            "min_data_points": 300,
            "data_type": [DataType.FLOAT32, DataType.FLOAT64],
        }
    ],
    "signature": "univariate",
}

logger = logging.getLogger(__name__)


def _close_open_event_frames(open_event_frames, analysis_start):
    for item in open_event_frames:
        item.end_date = analysis_start
    return open_event_frames


def _get_last_analyzed_point(df, window_size):
    if len(df) < window_size:
        return df.index[0]
    return df.index[-window_size]


def _is_anomaly(upper, arr):
    a_upper = np.any(arr > upper)
    return a_upper


# def _get_upper(Zxx, strictness):
#    q1, q3 = np.nanquantile(np.array(np.abs(Zxx), dtype=float), [0.25, 0.75], axis=0)
#    iqr = q3 - q1
#    return np.maximum(q3 + strictness * iqr, [0.13] * Zxx.shape[1])  # Magic number 0.13 is peak by accident


def _get_upper(fourier_transform, strictness):
    ampl = np.array(np.abs(fourier_transform), dtype=float)
    median = np.median(ampl, axis=0)
    mad = stats.median_abs_deviation(ampl, axis=0)
    return median + mad * strictness


def _get_intervals(df, anomalies):
    anomalies = pd.Series(data=anomalies, index=df.index).fillna(False)
    anomaly_grp = (anomalies != anomalies.shift().bfill()).cumsum()
    intervals = (
        df.assign(anomaly_grp=anomaly_grp)[anomalies]
        .reset_index()
        .groupby(["anomaly_grp"])
        .agg(start_date=("ts", "first"), end_date=("ts", "last"))
    )
    intervals["type"] = _CHECK_NAME
    return intervals


def _handle_open_intervals(df, intervals):
    intervals["open"] = intervals["end_date"] == df.index[-1]
    return intervals


def _clean_dataframe(df: pd.DataFrame):
    return df[~df.index.duplicated(keep="first")].dropna().sort_index()


def _detrend(resampled):
    butter_b, butter_a = butter(5, [0.01, 0.004], "bandpass")
    return signal.filtfilt(butter_b, butter_a, resampled)


def _run_oscillation_check(
    analysis_input, mas, open_event_frames, strictness=10
):  # pylint: disable=too-many-locals
    # Set params for window size
    w_size = 1024
    overlap_size = 512

    # Clean up the data
    df = _clean_dataframe(analysis_input.data)

    analysis_start = df.index[0]
    if analysis_input.analysis_start is not None:
        analysis_start = analysis_input.analysis_start

    # Resample at median archival rate
    old_index = df.index
    frequency = max(1, round(mas))
    new_index = pd.date_range(
        old_index.min(), old_index.max(), freq=str(frequency) + "S"
    )
    resampled = (
        df.reindex(old_index.union(new_index)).interpolate("linear").reindex(new_index)
    )
    resampled.index = resampled.index.set_names("ts")
    if len(resampled) < w_size:
        closed_event_frames = _close_open_event_frames(
            open_event_frames, analysis_start
        )
        return 0, closed_event_frames, None
    resampled = resampled.iloc[0 : (len(resampled) // w_size) * w_size]

    filtered = _detrend(resampled.values.flatten())
    # Perform short-term fourier transform (windows of size w_s )
    _, _, fourier_transform = signal.stft(
        stats.zscore(filtered),
        fs=1,
        window="hann",
        nperseg=w_size,
        noverlap=overlap_size,
        boundary=None,
    )
    # Find iqr upper boundary in the spectrum of each window
    upper = _get_upper(fourier_transform, strictness)
    # Detect anomalies in zone without low frequencies (=no offset)
    window_anomalies = [
        _is_anomaly(upper[index], column[10:])
        for index, column in enumerate(
            np.array(np.abs(fourier_transform), dtype=float).T
        )
    ]

    # Transform anomalies in windows to anomalies in resampled
    idx = [
        [np.arange(index * overlap_size, index * overlap_size + w_size)]
        for index, window in enumerate(window_anomalies)
        if window
    ]

    if len(idx) == 0:
        closed_event_frames = _close_open_event_frames(
            open_event_frames, analysis_start
        )
        return 0, closed_event_frames, _get_last_analyzed_point(resampled, w_size)

    anomalies = np.array([False] * len(resampled))
    anomalies[np.array(idx).flatten()] = True
    intervals = _get_intervals(resampled, anomalies)
    intervals = _handle_open_intervals(resampled, intervals)
    intervals = merge_intervals_and_open_event_frames(
        analysis_start, intervals, open_event_frames
    )

    percentage = calculate_local_score(resampled, analysis_start, intervals, mas)

    frames = event_frames_from_dataframe(process_open_intervals(intervals))

    last_analyzed_point = _get_last_analyzed_point(resampled, w_size)

    return percentage, list(frames), last_analyzed_point


def _get_interpolation_type(analysis_input: timeseer.AnalysisInput) -> str:
    interpolation_type = analysis_input.metadata.get_field(fields.InterpolationType)
    if interpolation_type is not None and interpolation_type == "STEPPED":
        return "pad"
    return "linear"


def _is_relevant_open_event_frame(event_frame):
    return (
        event_frame.end_date is None
        and event_frame.type in META["checks"][0]["event_frames"]
    )


def _get_open_event_frames(
    analysis_input: timeseer.AnalysisInput,
) -> List[timeseer.EventFrame]:
    return [
        frame
        for frame in analysis_input.event_frames
        if _is_relevant_open_event_frame(frame)
    ]


def _is_valid_input(analysis_input: timeseer.AnalysisInput):
    return len(_clean_dataframe(analysis_input.data)) > 0


# pylint: disable=missing-function-docstring,unreachable
def run(
    analysis_input: timeseer.AnalysisInput,
) -> timeseer.AnalysisResult:
    return timeseer.AnalysisResult()

    if not _is_valid_input(analysis_input):
        return timeseer.AnalysisResult()

    median_archival_step = [
        statistic.result
        for statistic in analysis_input.statistics
        if statistic.name == "Archival time median"
    ]
    if median_archival_step is None or len(median_archival_step) == 0:
        return timeseer.AnalysisResult()

    interpolation_type = _get_interpolation_type(analysis_input)
    if interpolation_type == "pad":
        return timeseer.AnalysisResult()

    open_event_frames = _get_open_event_frames(analysis_input)

    pct_oscillation, frames, last_analyzed_point = _run_oscillation_check(
        analysis_input, float(median_archival_step[0]), open_event_frames
    )

    if pct_oscillation is None:
        return timeseer.AnalysisResult()

    check = timeseer.CheckResult(_CHECK_NAME, float(pct_oscillation))
    return timeseer.AnalysisResult(
        [check], frames, last_analyzed_point=last_analyzed_point
    )
