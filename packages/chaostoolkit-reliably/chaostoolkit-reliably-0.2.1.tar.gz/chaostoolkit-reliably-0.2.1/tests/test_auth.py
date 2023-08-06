from tempfile import NamedTemporaryFile

import pytest
import yaml
from chaoslib.exceptions import ActivityFailed

from chaosreliably import get_auth_info


def test_using_config_file():
    with NamedTemporaryFile(mode="w") as f:
        yaml.safe_dump(
            {
                "auths": {"api.reliably.com": {"token": "12345", "username": "jane"}},
                "currentOrg": {"name": "test-org"},
            },
            f,
            indent=2,
            default_flow_style=False,
        )
        f.seek(0)

        auth_info = get_auth_info({"reliably_config_path": f.name})
        assert auth_info["token"] == "12345"
        assert auth_info["host"] == "api.reliably.com"
        assert auth_info["org"] == "test-org"


def test_using_config_file_but_override_token_and_host():
    with NamedTemporaryFile(mode="w") as f:
        yaml.safe_dump(
            {
                "auths": {"reliably.com": {"token": "12345", "username": "jane"}},
                "currentOrg": {"name": "test-org"},
            },
            f,
            indent=2,
            default_flow_style=False,
        )
        f.seek(0)

        auth_info = get_auth_info(
            {"reliably_config_path": f.name},
            {"token": "78890", "host": "api.reliably.dev", "org": "overriden-org"},
        )
        assert auth_info["token"] == "78890"
        assert auth_info["host"] == "api.reliably.dev"
        assert auth_info["org"] == "overriden-org"


def test_using_secret_only():
    auth_info = get_auth_info(
        None, {"token": "78890", "host": "reliably.dev", "org": "secret-org"}
    )
    assert auth_info["token"] == "78890"
    assert auth_info["host"] == "reliably.dev"
    assert auth_info["org"] == "secret-org"


def test_missing_token_from_secrets():
    with pytest.raises(ActivityFailed):
        get_auth_info(
            {
                "reliably_config_path": "",
            },
            {"reliably": {"host": "reliably.dev", "org": "an-org"}},
        )


def test_missing_host_from_secrets():
    with pytest.raises(ActivityFailed):
        get_auth_info(
            {
                "reliably_config_path": "",
            },
            {"reliably": {"token": "78890", "org": "an-org"}},
        )


def test_missing_org_from_secrets():
    with pytest.raises(ActivityFailed):
        get_auth_info(
            {
                "reliably_config_path": "",
            },
            {"reliably": {"token": "78890", "host": "reliably.dev"}},
        )
