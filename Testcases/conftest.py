import os
import logging
import time
from ElliPageObjects.login_page import ElliLoginPage
# from Utilities.set_mock_location import set_mock_location_android, set_mock_location_ios
import pytest

from appium import webdriver
from appium.webdriver.appium_service import AppiumService
from appium.options.common import AppiumOptions
from Utilities.read_properties import  read_config_data
# from Utilities.screenshots import Screen_shots
from Utilities.common_util import CURRENT_DIR , CONFIG_PATH
from ElliPageObjects.login_page import ElliLoginPage
# from Utilities.set_mock_location import set_mock_location_android, set_mock_location_ios
# from pytest_metadata.plugin import metadata_key

@pytest.fixture(autouse=True, scope='session')
def logger_setup(request):
    logger_name = "root"
    root_logger = logging.getLogger(logger_name)
    root_logger.setLevel(logging.INFO)
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(name)s : %(message)s',
                                  datefmt='%m/%d/%Y %I:%M:%S %p')
    # Adding console handler for displaying logs in the console
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    root_logger.addHandler(consoleHandler)
    fileHandler = None
    log_folder = os.path.join(CURRENT_DIR, '..')
    try:
        log_file = os.path.join(log_folder, 'test_logs.log')
        fileHandler = logging.FileHandler(log_file, mode='w')
        fileHandler.setFormatter(formatter)
        root_logger.addHandler(fileHandler)
    except Exception as e:
        logger.info("Error creating log folder or file")
    # Suppressing urllib3 logs to avoid clutter
    urllib3_logger = logging.getLogger('urllib3')
    urllib3_logger.setLevel(logging.ERROR)
    consoleHandler.setLevel(logging.ERROR)
    # Clean up log handlers to avoid duplicate log entries
    yield
    root_logger.removeHandler(consoleHandler)
    if fileHandler:
        root_logger.removeHandler(fileHandler)
        fileHandler.close()

@pytest.fixture()
def get_browserstack_cap(session_capabilities):
    return session_capabilities
@pytest.fixture()
def appium_driver_setup(request, pytestconfig):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    use_browserstack = pytestconfig.getoption("use_browserstack")
    android_config = read_config_data(CONFIG_PATH, 'Mobile_Local_Android')
    ios_config = read_config_data(CONFIG_PATH, 'Mobile_Local_iOS')
    appium_service = AppiumService()
    #Browserstack execution - Android
    if use_browserstack:
        remoteURL = read_config_data(CONFIG_PATH, 'browserstack')["remote_url"]
        logger.info("Initializing Appium driver with : %s", remoteURL)
        caps = request.getfixturevalue("get_browserstack_cap")
        driver = webdriver.Remote(remoteURL, caps)
    # Local execution - Android
    else:
        appium_service.start()
        # if pytestconfig.option.markexpr == 'ios':
        #     cap = {
        #         "platformName": ios_config['platform_name'],
        #         "appium:deviceName": ios_config['device_name'],
        #         "appium:automationName": "XCUITest",
        #         "appium:appPackage": ios_config['app_package'],
        #         "appium:platformVersion": ios_config['platform_version'],
        #         "appium:app": ios_config['app_path'],
        #         "appium:autoAcceptAlerts": True,
        #         "newCommandTimeout": 100,
        #         'appium:settings[acceptAlertButtonSelector]': "**/XCUIElementTypeButton[`label CONTAINS[c] 'Allow Once'`]"
        #     }
        # else:

        cap = {
            "deviceName": android_config['device_name'],
            "platformName": android_config['platform_name'],
            "automationName": android_config['automation_name'],
            "appActivity": android_config['app_activity'],
            "appPackage": android_config['app_package'],
            "platformVersion": android_config['platform_version'],
            "app": android_config['app_path'],
            "newCommandTimeout": 100 * 2,
            "autoGrantPermissions": "true"
        }
        options = AppiumOptions().load_capabilities(caps=cap)
        localURL = "http://127.0.0.1:4723"
        logger.info("Initializing Appium driver with : %s", localURL)
        driver = webdriver.Remote(localURL, options=options)
        driver.implicitly_wait(200)
        # if pytestconfig.option.markexpr == 'ios':
        #     set_mock_location_ios(driver, 36.1627, -86.7816)
        # else:
        set_mock_location_android(36.1627, -86.7816)
    try:
        yield driver
    finally:
        logger.info("~~~~~~~~~~Relaunch App from Finally~~~~~~~~~~~~~")
        try:
            package_id = None
            if pytestconfig.option.markexpr == 'ios':
                package_id = ios_config['app_package']
            else:
                package_id = android_config['app_package']
            logger.info("~~~~~~~~~~~~Logged Out from Finally~~~~~~~~~~~~~")
        finally:
            driver.quit()
            appium_service.stop()
def pytest_addoption(parser):
    parser.addoption(
        "--use-browserstack", action="store_true", help="Run tests on BrowserStack"
    )
    parser.addoption(
        "--platform", action="store", default="android", help="Platform to run tests on: android or ios"
    )


# @pytest.hookimpl(wrapper=True)
# def pytest_runtest_makereport(item):
#     pytest_html = item.config.pluginmanager.getplugin('html')
#     outcome = yield
#     report = outcome.get_result()
#     extra = getattr(report, 'extra', [])
#     if report.when == 'call' or report.when == "setup":
#         xfail = hasattr(report, 'wasxfail')
#         if (report.skipped and xfail) or (report.failed and not xfail):
#             file_name = item.nodeid.split("::")[-2]
#             test_name = item.nodeid.split("::")[-1]
#             driver = item.funcargs.get('appium_driver_setup')  # Get the driver from the fixture
#             if driver:
#                 screenshots = Screen_shots()
#                 screenshot_path = screenshots.take_screenshot(driver, file_name, test_name)
#                 relative_screenshot_path = os.path.relpath(screenshot_path, start='Reports')
#                 if file_name:
#                     html = '<div><img src="%s" alt="screenshot" style="width:200px;height:300px;" ' \
#                            'onclick="window.open(this.src)" align="right"/></div>' % relative_screenshot_path
#                     extra.append(pytest_html.extras.html(html))
#                     report.extras = extra
# def pytest_configure(config):
#     config.stash[metadata_key]["Platform"] = config.option.markexpr.upper()