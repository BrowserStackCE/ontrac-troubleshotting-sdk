import os
import time
from functools import reduce
from operator import getitem
import requests
from requests_ntlm import HttpNtlmAuth
import json
import random
import string
import logging
from datetime import datetime, timedelta
from appium.webdriver.webdriver import WebDriver
import pytz
from Utilities.read_properties import read_json_file, read_config_data


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(CURRENT_DIR, '..', 'Configurations', 'config.ini')
PUSH_ORDER_SMDY_PATH = os.path.join(CURRENT_DIR, '..', 'Data', 'push_order_SMDY.json')
CONTRACTOR_LIST_PATH = os.path.join(CURRENT_DIR, '..', 'Data', 'contractor_list.json')
ADDRESS_LIST_PATH = os.path.join(CURRENT_DIR, '..', 'Data', 'address_list.json')
API_URL_PATH = os.path.join(CURRENT_DIR, '..', 'Data', 'api_url_endpoint.json')
CREATE_RECEIVED_EVENT_RCVD_PATH = os.path.join(CURRENT_DIR, '..', 'Data', 'create_received_event_RCVD.json')
CREATE_OASS_EVENT_PATH = os.path.join(CURRENT_DIR, '..', 'Data', 'create_OASS_event.json')
DRIVER_ASSIGNMENT_PATH = os.path.join(CURRENT_DIR, '..', 'Data', 'driver_assignment.json')
LOGIN_PATH = os.path.join(CURRENT_DIR, '..', 'Data', 'login.json')
MAIN_MAP_SCREEN_PATH = os.path.join(CURRENT_DIR, '..', 'Data', 'main_map_screen.json')
NAVIGATION_SCREEN_PATH = os.path.join(CURRENT_DIR, '..', 'Data', 'navigation_screen.json')
MENU_PATH = os.path.join(CURRENT_DIR, '..', 'Data', 'menu.json')
CREATE_ROUTE_DATA_PATH = os.path.join(CURRENT_DIR, '..', 'Data', 'create_route_data.json')
SERVICE_PATH = os.path.join(CURRENT_DIR, '..', 'Data', 'service.json')
CREATE_ROUTE_PATH = os.path.join(CURRENT_DIR, '..', 'Data', 'create_route.json')
MANIFEST_SCREEN = os.path.join(CURRENT_DIR, '..', 'Data', 'manifest_screen.json')
FINAL_REVIEW_PATH = os.path.join(CURRENT_DIR, '..', 'Data', 'final_review_screen.json')
SCAN_LOAD_SCREEN = os.path.join(CURRENT_DIR, '..', 'Data', 'scan_load_screen.json')
REGRESSION_SPRINT_12 = os.path.join(CURRENT_DIR, '..', 'Data', 'regression_sprint_12.json')
SERVICE_DATA = os.path.join(CURRENT_DIR, '..', 'Data', 'service.json')
DEVELOPMENT_ANDROID=os.path.join(CURRENT_DIR,'..','Data','development_android_34688.json')
PUSH_ORDER_PU=os.path.join(CURRENT_DIR,'..','Data','push_order_PU.json')
CREATE_DASS_EVENT=os.path.join(CURRENT_DIR,'..','Data','create_DASS_event.json')

ios_config = read_config_data(CONFIG_PATH, 'Mobile_Local_iOS')


def toggle_airplane_mode(appium_driver: WebDriver, enable: bool):
    try:
        if appium_driver.capabilities['platformName'].lower() == 'android':
            mode = 1 if enable else 0
            appium_driver.execute_script("mobile: shell", {
                'command': 'settings',
                'args': ['put',
                         'global', 'airplane_mode_on', str(mode)]
            })
        else:
            logging.getLogger("root").warning("Airplane mode toggle is only supported on Android.")
    except Exception as e:
        logging.getLogger("root").error(f"Error setting network conditions: {e}")


def toggle_wifi_mode(appium_driver: WebDriver, enable: bool):
    try:
        if appium_driver.capabilities['platformName'].lower() == 'android':
            wifi_command = 'enable' if (not enable) else 'disable'
            appium_driver.execute_script("mobile: shell", {
                'command': 'svc',
                'args': ['wifi', wifi_command]
            })
            logging.info(f"WiFi {'enabled' if not enable else 'disabled'} successfully.")
        else:
            logging.getLogger("root").warning("WiFi mode toggle is only supported on Android.")
    except Exception as e:
        logging.getLogger("root").error(f"Error setting network conditions: {e}")


def toggle_mobile_data_mode(appium_driver: WebDriver, enable: bool):
    try:
        if appium_driver.capabilities['platformName'].lower() == 'android':
            mobile_data_command = 'enable' if (not enable) else 'disable'
            appium_driver.execute_script("mobile: shell", {
                'command': 'svc',
                'args': ['data', mobile_data_command]
            })
            logging.info(f"Mobile data {'enabled' if not enable else 'disabled'} successfully.")
        else:
            logging.getLogger("root").warning("Mobile data mode toggle is only supported on Android.")
    except Exception as e:
        logging.getLogger("root").error(f"Error setting network conditions: {e}")

