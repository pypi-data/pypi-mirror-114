# Changelog

## [Unreleased][]

[Unreleased]: https://github.com/chaostoolkit-incubator/chaostoolkit-reliably/compare/0.2.1...HEAD

## [0.2.1][]

[0.2.1]: https://github.com/chaostoolkit-incubator/chaostoolkit-reliably/compare/0.2.0...0.2.1

### Changed

- Updated `get_objective_results_by_labels` to have a default `limit` of `1`
- Add `slo_is_met` as a probe to encompass the `get_objective_results_by_labels` probe and `all_objective_results_ok` tolerance


## [0.2.0][]

[0.2.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-reliably/compare/0.1.2...0.2.0

### Changed

- Fix issue where secrets were not correctly extracted from Experiment config [#1][1]
- Refactor to use new Reliably Entity Server rather than previous API
  - One probe available: `get_objective_results_by_labels`
    - For a given Objectives labels, get the Objective Results
  - One tolerance available: `all_objective_results_ok`
    - For a list of Objective Results, determine if they were all OK
- Allow for user to provide `org` as a secret/get it from `currentOrg` in their Reliably config

[1]: https://github.com/chaostoolkit-incubator/chaostoolkit-reliably/issues/1

## [0.1.2][]

[0.1.2]: https://github.com/chaostoolkit-incubator/chaostoolkit-reliably/compare/0.1.1...0.1.2

### Changed

- Use the most recent SLO report only

## [0.1.1][]

[0.1.1]: https://github.com/chaostoolkit-incubator/chaostoolkit-reliably/compare/0.1.0...0.1.1

### Changed

- Add `install_requires` so that dependencies are properly installed via pip

## [0.1.0][]

[0.1.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-reliably/tree/0.1.0

### Added

-   Initial release
