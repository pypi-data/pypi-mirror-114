import json
import os
from pathlib import Path

from pytest import fixture
from tabulate import tabulate

TEST_DATA_DIR = os.path.join(Path(__file__).parent, "data")


@fixture
def objective_results():
    with open(
        os.path.join(TEST_DATA_DIR, "objective_results_from_api.json"), "r"
    ) as json_in:
        return json.load(json_in)


@fixture
def objective_results_all_ok(objective_results):
    for result in objective_results:
        result["spec"]["objectivePercent"] = 90.00
        result["spec"]["actualPercent"] = 100.00
        result["spec"]["remainingPercent"] = 10.00
    return objective_results


@fixture
def not_ok_table_contents():
    return [
        [
            "2021-07-22 10:51:55.184558 +0000 UTC",
            "2021-07-22 10:51:55.184558 +0000 UTC",
            99.9,
            90,
            -9.900000000000006,
            {
                "category": "Availability",
                "indicator_name": (
                    "exploring-reliability-guide-service-availability-indicator"
                ),
            },
        ],
        [
            "2021-07-22 09:28:32.497773 +0000 UTC",
            "2021-07-22 09:28:32.497773 +0000 UTC",
            99.9,
            90,
            -9.900000000000006,
            {
                "category": "Availability",
                "indicator_name": (
                    "exploring-reliability-guide-service-availability-indicator"
                ),
            },
        ],
        [
            "2021-07-21 13:35:24.4716 +0000 UTC",
            "2021-07-21 13:35:24.4716 +0000 UTC",
            99.9,
            90,
            -9.900000000000006,
            {
                "category": "Availability",
                "indicator_name": (
                    "exploring-reliability-guide-service-availability-indicator"
                ),
            },
        ],
    ]


@fixture
def not_ok_table(not_ok_table_contents):
    headers = [
        "From",
        "To",
        "Objective %",
        "Actual %",
        "Remaining %",
        "Indicator Selector",
    ]
    return tabulate(not_ok_table_contents, headers=headers, tablefmt="github")
