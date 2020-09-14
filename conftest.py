import json
import os
import tempfile

import ftputil
import jinja2
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
        fixture = Application(browser=browser, config=config)
    # fixture.session.ensure_login(username=web_admin["username"], password=web_admin["password"])
    return fixture


def install_server_configuration(host, username, password, file):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config/config_inc.php.bak"):
            remote.remove("config/config_inc.php.bak")
        if remote.path.isfile("config/config_inc.php"):
            remote.rename("config/config_inc.php", "config/config_inc.php.bak")
        remote.upload(file.name, "config/config_inc.php")


def restore_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config/config_inc.php.bak"):
            if remote.path.isfile("config/config_inc.php"):
                remote.remove("config/config_inc.php")
            remote.rename("config/config_inc.php.bak", "config/config_inc.php")


@pytest.fixture(scope="session", autouse=True)
def configure_server(request, config):
    ftp_config = config["ftp"]

    config_file = get_mantis_config_file(config)
    install_server_configuration(ftp_config["host"], ftp_config["username"], ftp_config["password"], config_file)

    def fin():
        restore_server_configuration(ftp_config["host"], ftp_config["username"], ftp_config["password"])

    request.addfinalizer(fin)


def get_mantis_config_file(config):
    ftp_config = config["ftp"]["config_inc"]
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        template_file = os.path.join(os.path.dirname(__file__), "resources", "config_inc.php")
        with open(template_file) as template_file:
            template = jinja2.Template(template_file.read())
        bind = {"g_db_password": ftp_config["g_db_password"],
                "g_crypto_master_salt": ftp_config["g_crypto_master_salt"],
                "smtp_port": config["mail"]["port"]
                }
        out = template.render(bind)
        tf.write(out.encode())
    return tf


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
