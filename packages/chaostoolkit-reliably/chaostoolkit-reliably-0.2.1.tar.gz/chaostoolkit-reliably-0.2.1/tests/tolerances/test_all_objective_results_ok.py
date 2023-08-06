from unittest.mock import patch

from chaosreliably.slo.tolerances import all_objective_results_ok


def test_all_objective_results_ok_when_results_all_ok(objective_results_all_ok):
    all_ok = all_objective_results_ok(objective_results_all_ok)
    assert all_ok


def test_all_objective_results_ok_when_results_not_all_ok(objective_results):
    all_ok = all_objective_results_ok(objective_results)
    assert not all_ok


@patch("chaosreliably.slo.tolerances.logger")
def test_all_objective_results_ok_doesnt_log_table_when_results_all_ok(
    mocked_logger, objective_results_all_ok
):
    _ = all_objective_results_ok(objective_results_all_ok)
    mocked_logger.info.assert_called_once_with("All Objective Results were OK.")


@patch("chaosreliably.slo.tolerances.logger")
def test_all_objective_results_ok_logs_table_when_all_results_not_ok(
    mocked_logger, objective_results, not_ok_table
):
    _ = all_objective_results_ok(objective_results)
    mocked_logger.critical.assert_called_once_with(
        (
            "The following Objective Results were not OK:\n\n"
            "Objective Results are sorted by latest at the top:\n"
            f"{not_ok_table}"
        )
    )
