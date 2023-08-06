from unittest import mock

import pytest


@pytest.fixture(scope="function")
def hub(hub):
    for dyne in {{cookiecutter.dyne_list}}:
        hub.pop.sub.add(dyne_name=dyne)
    yield hub


@pytest.fixture(scope="function")
def mock_hub(hub):
    m_hub = hub.pop.testing.mock_hub()
    m_hub.OPT = mock.MagicMock()
    m_hub.SUBPARSER = mock.MagicMock()
    yield m_hub
