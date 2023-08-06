import pytest


@pytest.fixture(scope="session")
def hub(hub):
    for dyne in {{cookiecutter.dyne_list}}:
        hub.pop.sub.add(dyne_name=dyne)

    hub.pop.config.load(
        {{cookiecutter.dyne_list}},
        cli="{{cookiecutter.clean_name}}",
        parse_cli=False,
    )

    yield hub
