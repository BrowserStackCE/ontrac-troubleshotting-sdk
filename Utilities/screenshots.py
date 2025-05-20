import datetime
import os
from logging import Logger
import time
import pytest


class Screen_shots:

    def take_screenshot(self, driver, file_name, test_name):
        os.makedirs('Reports/screenshots', exist_ok=True)
        filename = f'Reports/screenshots/{file_name}_{test_name}.png'
        driver.save_screenshot(filename)
        return filename
