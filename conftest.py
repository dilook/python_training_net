import json
import os

import pytest

from fixture.application import Application

fixture = None
target = None


def load_config(file):
    global target
    if target is None:
        file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(file) as config_file:
            target = json.load(config_file)
    return target


@pytest.fixture(scope="session")
def config(request):
    return load_config(request.config.getoption("--target"))


@pytest.fixture
def app(request, config):
    global fixture
    browser = request.config.getoption("--browser")
    web_admin = config["webadmin"]
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, base_url=config["web"]["base_url"])
    fixture.session.ensure_login(username=web_admin["username"], password=web_admin["password"])
    return fixture


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()

    request.addfinalizer(fin)
    return fixture


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--target", action="store", default="target.json")
