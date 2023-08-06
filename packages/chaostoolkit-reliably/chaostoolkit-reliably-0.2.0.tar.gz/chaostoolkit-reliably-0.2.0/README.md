# Chaos Toolkit extension for Reliably

![Build](https://github.com/chaostoolkit-incubator/chaostoolkit-reliably/workflows/Build/badge.svg)

[Reliably][reliably] support for the [Chaos Toolkit][chaostoolkit].

[reliably]: https://reliably.com
[chaostoolkit]: http://chaostoolkit.org/

## Install

To be used from your experiment, this package must be installed in the Python
environment where [chaostoolkit][] already lives.

[chaostoolkit]: https://github.com/chaostoolkit/chaostoolkit

```
$ pip install chaostoolkit-reliably
```

## Authentication

To use this package, you must create have registered with Reliably services
through their [CLI][configreliably].

[configreliably]: https://reliably.com/docs/getting-started/login/

You have two ways to pass on the credentials information.

The first one by specifying the path to the Reliably's configuration file,
which defaults to `$HOME/.config/reliably/config.yaml`. The simplest way to
achieve this is by running `$ reliably login` as this will generate the
appropriate file.

```json
{
    "configuration": {
        "reliably_config_path": "~/.config/reliably/config.yaml"
    }
}
```

Because we use the default path, you may omit this configuration's entry
altogether unless you need a specific different path.

The second one is by setting some environment variables as secrets. This is
for specific use case and usually not required.

* `RELIABLY_TOKEN`: the token to authenticate against Reliably's API
* `RELIABLY_ORG`: the Reliably organisation to use
* `RELIABLY_HOST:`: the hostname to connect to, default to `reliably.com`

```json
{
    "secrets": {
        "reliably": {
            "token": {
                "type": "env",
                "key": "RELIABLY_TOKEN"
            },
            "org": {
                "type": "env",
                "key": "RELIABLY_ORG"
            },
            "host": {
                "type": "env",
                "key": "RELIABLY_HOST",
                "default": "reliably.com"
            }
        }
    }
}
```

## Usage

### As Steady Steate Hypothesis

You can use Reliably's SLO as a mechanism to determine if your system has
deviated during a Chaos Toolkit experiment. Here is a simple example:

```json
"steady-state-hypothesis": {
    "title": "We do not consume all of our error budgets during the experiment",
    "probes": [
        {
            "name": "Our 'Must be good' SLO results must be OK",
            "type": "probe",
            "provider": {
                "type": "python",
                "module": "chaosreliably.slo.probes",
                "func": "get_objective_results_by_labels",
                "arguments": {
                    "labels": {"name": "must-be-good", "service": "must-be-good-service"},
                    "limit": 5
                }
            },
            "tolerance": {
                "type": "probe",
                "name": "Check all SLO results are ok",
                "provider": {
                    "type": "python",
                    "module": "chaosreliably.slo.tolerances",
                    "func": "all_objective_results_ok",
                    "arguments": {}
                }
            }
        }
    ]
}
```

This above example will get the last 5 Objective Results for our `Must be good` SLO and determine if they were all okay or whether we've spent our [error budget](https://sre.google/workbook/error-budget-policy/#:~:text=Error%20budgets%20are%20the%20tool,with%20the%20pace%20of%20innovation.&text=The%20error%20budget%20forms%20a,has%20a%200.1%25%20error%20budget.)
they are allowed.


### As Safeguards

Safeguards, provided by the
[Chaos Toolkit addons extension](https://github.com/chaostoolkit/chaostoolkit-addons)
gives you a nice way to interrupt an experiment as soon as error budgets have
been consumed. This is orthogonal to the steady-state hypothesis as it is a
mechanism to protect your system from being harmed too harshly by an experiment.

```json
"controls": [
    {
        "name": "safeguard",
        "provider": {
            "type": "python",
            "module": "chaosaddons.controls.safeguards",
            "arguments": {
                "probes": [
                    {
                        "name": "we-do-not-have-enough-error-budget-left-to-carry-on",
                        "type": "probe",
                        "frequency": 5,
                        "provider": {
                            "type": "python",
                            "module": "chaosreliably.slo.probes",
                            "func": "get_objective_results_by_labels",
                            "arguments": {
                                "labels": {"name": "must-be-good", "service": "must-be-good-service"},
                                "limit": 5
                            }
                        },
                        "tolerance": {
                            "type": "probe",
                            "name": "Check all SLO results are ok",
                            "provider": {
                                "type": "python",
                                "module": "chaosreliably.slo.tolerances",
                                "func": "all_objective_results_ok",
                                "arguments": {}
                            }
                        }
                    }
                ]
            }
        }
    }
]
```

As you can notice it is the same construct as for the steady-state, it's merely
used with a different purpose. Here these probes will be executed every 5s
during the experiment (this frequence is for demo purposes, you would usually only run it
once every minute or less).

## Contribute

If you wish to contribute more functions to this package, you are more than
welcome to do so. Please, fork this project, make your changes following the
usual [PEP 8][pep8] code style, sprinkling with tests and submit a PR for
review.

[pep8]: https://pycodestyle.readthedocs.io/en/latest/

### Develop

If you wish to develop on this project, make sure to install the development
dependencies. But first, [create a virtual environment][venv] and then install
those dependencies.

[venv]: http://chaostoolkit.org/reference/usage/install/#create-a-virtual-environment

```console
$ pip install -r requirements-dev.txt -r requirements.txt 
```

Then, point your environment to this directory:

```console
$ python setup.py develop
```

Now, you can edit the files and they will be automatically be seen by your
environment, even when running from the `chaos` command locally.

### Test

To run the tests for the project execute the following:

```
$ pytest
```

### Linting & Formatting

A `Makefile` is provided to abstract away the linting and formatting commands.

To lint the project, run:

```bash
$ make lint
```

To format the project, run:

```bash
$ make format
```
