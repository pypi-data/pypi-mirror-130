"""Multivariate correlation structure without outliers.

<p>This depicts the correlation between all tags in the flow over the time frame of the flow.
Outliers have been removed for this correlation calculation.
Outliers include: all zero measurements and NaNs</p>"""

import pandas as pd

import timeseer

from timeseer import DataType


META: dict = {
    "run": "before",
    "statistics": [
        {"name": "Correlation structure"},
    ],
    "conditions": [
        {
            "min_series": 2,
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
    "signature": "multivariate",
}


def _rename_to_index(data: pd.DataFrame, index: int) -> pd.DataFrame:
    return data.rename({"value": index}, axis=1, copy=False)[index]


def _clean_inputs(inputs):
    concatenated_df = (
        pd.concat(
            [
                _rename_to_index(series.data, index)[
                    ~series.data.index.duplicated(keep="first")
                ]
                for index, series in enumerate(inputs)
            ],
            axis=1,
            sort=False,
        )
        .interpolate("linear")
        .dropna()
    )
    concatenated_df = concatenated_df[(concatenated_df != 0).all(1)]
    return concatenated_df


def _run_multivariate_correlation(inputs):
    clean_df = _clean_inputs(inputs)
    if len(clean_df) < 30:
        return None

    return clean_df.corr()


# pylint: disable=missing-function-docstring
def run(
    analysis_input: timeseer.MultivariateAnalysisInput,
) -> timeseer.AnalysisResult:
    inputs = analysis_input.inputs

    correlation = _run_multivariate_correlation(inputs)
    if correlation is None:
        return timeseer.AnalysisResult()

    correlation_dict = correlation.to_dict("list")
    result = {
        "series": [inputs[index].metadata.series for index in correlation_dict],
        "columns": list(correlation_dict.values()),
    }
    correlation_statistic = timeseer.Statistic(
        META["statistics"][0]["name"], "correlation", result
    )
    return timeseer.AnalysisResult(statistics=[correlation_statistic])
