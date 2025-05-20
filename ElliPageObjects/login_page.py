import os
import time
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.wait import WebDriverWait
from Base.custom_code import Custom_code
import logging
import subprocess
import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Base.custom_code import Custom_code
from selenium.webdriver import Keys, ActionChains
import re

class ElliLoginPage(Custom_code):
    locators = {
        'android': {
            'app_name_and_version_label':(AppiumBy.XPATH,'//android.widget.TextView[@resource-id="comid/tvVersionName"]'),
            'app_build_number_label':(AppiumBy.XPATH,'//android.widget.TextView[@resource-id="/tvBuildNumber"]'),
            'terms_and_privacy_label':(AppiumBy.XPATH,'//android.widget.TextView[@text="Terms, Privacy & FAQ"]'),
            'download_system_logs':(AppiumBy.XPATH,'//android.widget.TextView[@text="Download System Logs"]'),
            'login_page_title_label':(AppiumBy.XPATH,'//android.widget.TextView[@resource-id="tvTitle"]')
            }
    }


    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def click_on_ok_btn_ios(self):
        try:
            if self.get_element(self.locators[self.platform]['ok_btn']):
                self.ElementPresent_and_click(self.locators[self.platform]['ok_btn'])
        except Exception as e:
            logging.getLogger("root").info(f"Exception in get_element: {str(e)}")

    def click_on_skip_element(self):
        assert self.get_element_present_status(self.locators[self.platform]['Skip_btn']), "Failed to find Skip button after App launched"
        self.ElementPresent_and_click(self.locators[self.platform]['Skip_btn'])
