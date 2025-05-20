import json
import configparser
import logging

from appium.webdriver.webdriver import WebDriver


def read_config_data(file_path, section):
    config = configparser.ConfigParser()
    config.read(file_path)
    if section in config:
        return dict(config[section])
    else:
        raise ValueError(f"Section '{section}' not found in the config file.")


def read_platforms(file_path, platform):
    config = configparser.ConfigParser()
    config.read(file_path)
    platforms = []
    for section in config.sections():
        if platform == 'Android' and section.startswith('Android'):
            android = {
                'deviceName': config[section]['device_name'],
                'osVersion': config[section]['os_version'],
                'platformName': config[section]['platform_name']
            }
            platforms.append(android)
        if platform == 'ios' and section.startswith('ios'):
            ios = {
                'deviceName': config[section]['device_name'],
                'osVersion': config[section]['os_version'],
                'platformName': config[section]['platform_name']
            }
            platforms.append(ios)

    return platforms


def read_json_file(file_path):
    with open(file_path, "r", encoding='utf-8') as file:
        data = json.load(file)
    return data


def toggle_airplane_mode(appium_driver: WebDriver, enable: bool):
    try:
        if appium_driver.capabilities['platformName'].lower() == 'android':
            mode = 1 if enable else 0
            # Set airplane mode
            appium_driver.execute_script("mobile: shell", {
                'command': 'settings',
                'args': ['put', 'global', 'airplane_mode_on', str(mode)]
            })

            # Broadcast the change
            appium_driver.execute_script("mobile: shell", {
                'command': 'am',
                'args': ['broadcast', '-a', 'android.intent.action.AIRPLANE_MODE', '--ez', 'state', str(enable).lower()]
            })

            logging.getLogger("root").info(f"Airplane mode {'enabled' if enable else 'disabled'} successfully.")
        else:
            logging.getLogger("root").warning("Airplane mode toggle is only supported on Android.")
    except Exception as e:
        logging.getLogger("root").error(f"Error setting network conditions: {e}")
