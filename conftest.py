
import pytest
import yaml
import os
import logging
import glob
import sys
from base_utilities.driver_factory import DriverFactory


driver = None
env = None
config_file = None
logger = logging.getLogger('flipkartSearch')
logger.setLevel(logging.INFO)
log_path = "log"
report_path = "allure_report"
log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), log_path)
report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), report_path)
handler = logging.FileHandler(os.path.join(log_path, 'flipkartSearch.log'), mode='w')
handler.setLevel(logging.INFO)

formatter = logging.Formatter('[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s')

handler.setFormatter(formatter)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.addHandler(handler)
files = glob.glob(os.path.join(report_path, '*'))

# To empty allure reports folder
for f in files:
    try:
        os.remove(f)
    except:
        pass

@pytest.fixture(scope='class')
def homePage_fixture(request, browser, env):
    global config_file
    global driver

    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input_data_yaml")
    config_file = os.path.join(config_file, request.config.getoption("--input_data"))

    try:
        with open(config_file, 'r') as yml_data:
            input_data_config = yaml.safe_load(yml_data)
            if "prod" in env.lower():
                input_data = input_data_config["PROD"]
            elif "stage" in env.lower():
                input_data = input_data_config["STAGE"]
            elif "QA" in env.lower():
                input_data = input_data_config["QA"]
            else:
                sys.exit("Environment variable not specified")
            url = input_data["URL"]
            search_value = input_data["SEARCH_PARAMETER"]
    except:
        sys.exit("Failed to load input YAML file:: " + str(config_file))
    display_test_info(browser, url, report_path, env, search_value)

    df = DriverFactory(browser) ## Initialize the driver based on browser
    driver = df.getDriverInstance() ## Get driver instance

    if request.cls is not None:
        request.cls.driver = driver ## To create unique driver session for tests class
        request.cls.input_data = input_data
        request.cls.url = url
        request.cls.search_param = search_value

    def fin():
        logger.info("Executing tear down")
        driver.quit()
    request.addfinalizer(fin) ## Tear down method to close the driver session


def display_test_info(browser, url, report_path, env, search_param):
    logger.info('Test started with the following parameters:')
    logger.info('-' * 30)
    logger.info('\tBrowser = {}'.format(browser))
    logger.info('\tURL = {}'.format(url))
    logger.info('\tSearch Parameter = {}'.format(search_param))
    logger.info('\tEnvironment = {}'.format(env))
    logger.info('\tReport_path = {}'.format(report_path))
    logger.info('-' * 30)


def pytest_addoption(parser):
    parser.addoption("--input_data", help='YAML file with environment parameters', action="store", default="input_data.yaml")
    parser.addoption("--browser", help='Browser to run script on', action="store", default="chrome")
    parser.addoption("--env", help='Name of the environment to run script on', action="store", default="prod")

@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("--browser")

@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")