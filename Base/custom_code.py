import os
import time
from datetime import datetime
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.pointer_input import PointerInput
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
import os
import logging
from datetime import datetime



class Custom_code:

    def __init__(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(20)

    @property
    def platform(self):
        return 'android' if self.driver.capabilities['platformName'].lower() == 'android' else 'ios'

    def get_by_type(self, locator_type):
        locator_type = locator_type.lower()

        if locator_type == "id":
            return By.ID
        elif locator_type == "xpath":
            return By.XPATH
        elif locator_type == "name":
            return By.NAME
        elif locator_type == "link":
            return By.LINK_TEXT
        elif locator_type == "css":
            return By.CSS_SELECTOR
        elif locator_type == "class":
            return By.CLASS_NAME
        elif locator_type == "partial link":
            return By.PARTIAL_LINK_TEXT
        elif locator_type == "tag":
            return By.TAG_NAME
        else:
            return False

    def get_element(self, locator):
        element = None
        locator_type = locator[0]
        locator_value = locator[1]
        by_type = self.get_by_type(locator_type)
        try:
            element = self.driver.find_element(by_type, locator_value)
            return element
        except Exception as e:
            # try:
            #     # actions = ActionChains(self.driver)
            #     # touch_input = PointerInput(interaction.POINTER_TOUCH, "touch")
            #     # actions.w3c_actions.devices.append(touch_input)
            #     # start_time = time.time()
            #     timeout = 2
            #     while timeout>0:
            #         # elapsed_time = time.time() - start_time
            #         try:
            #             self.scroll_fixed_steps(steps=2)
            #             self.driver.find_element(by_type, locator_value)
            #             logging.info("Element found.")
            #             return element
            #         except NoSuchElementException:
            #             logging.info("scrolling down to find element")
            #             timeout -= 1
            # except Exception as e:
            logging.getLogger("root").info(f"Exception in get_element: {str(e)} after trying")
            assert False

    def get_element_present_status(self, locator):
        element = None
        try:
            locator_type = locator[0]
            locator_value = locator[1]
            by_type = self.get_by_type(locator_type)
            element = self.driver.find_element(by_type, locator_value)
            return element
        except Exception as e:
            logging.getLogger("root").info(f"Exception in get_element: {str(e)}")
            return False

    def click_on_element(self, locator):
        try:
            element = self.get_element(locator)
            element.click()
        except Exception as e:
            logging.getLogger("root").error(f"Failed to click on element with locator {locator}: {str(e)}")

    def clear_field(self, locator):
        try:
            element = self.get_element(locator)
            element.clear()
        except Exception as e:
            logging.getLogger("root").error(f"Failed to clear field with locator {locator}: {str(e)}")

    def send_keys_action_chains(self, locator, data):
        try:
            element = self.get_element(locator)
            element.click()
            action_chain = ActionChains(self.driver)
            data_rev = data[::-1]
            for letter in data_rev:
                action_chain.send_keys(letter).perform()
                action_chain.send_keys(Keys.LEFT).perform()
        except Exception as e:
            logging.getLogger("root").error(f"Failed to send keys '{data}' to element with locator {locator}: {str(e)}")

    def send_keys_to(self, locator, data):
        try:
            element = self.get_element(locator)
            element.send_keys(data)
        except Exception as e:
            logging.getLogger("root").error(f"Failed to send keys '{data}' to element with locator {locator}: {str(e)}")

    def isElementPresent(self, locator):
        try:
            element = self.get_element(locator)
            if element is not None:
                return True
            else:
                logging.getLogger("root").info(f"Element not present with locator: {locator}")
                return AssertionError
        except Exception as e:
            message = f"Element not found with locator: '{locator}'\n"
            message += f"Exception details: {str(e)}"
            logging.getLogger("root").error(f"Exception checking element presence with locator {locator}: {str(e)}")
            raise AssertionError(message) from e



    def ElementPresent_and_click(self, locator):
        try:
            element = self.get_element(locator)
            if element is not None:
                # element.click()
                actions = ActionChains(self.driver)
                actions.move_to_element(element)
                actions.click()
                actions.perform()
                return True
            else:
                logging.getLogger("root").info(f"Element not found for clicking with locator: {locator}")
                return False
        except Exception as e:
            logging.getLogger("root").error(f"Failed to click on element with locator {locator}")
            return False

    def take_screenshot(self, testcase_name="", module_name=""):
        try:
            test_name = testcase_name.replace(" ", "_")
            test_name = test_name.replace(" ", "_")
            date = datetime.now().strftime("%I:%M%p on %B %d, %Y")
            date = date.replace('', "_")
            date = date.replace(':', "_")
            date = date.replace(',', '')
            date = "_DATE_" + date

            fileDir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.dirname(fileDir) + "\\Screenshots\\" + module_name + "\\" + testcase_name + date + '.png'

            self.driver.save_screenshot(file_path)
            logging.getLogger("root").info(f"Screenshot saved: {file_path}")
        except Exception as e:
            logging.getLogger("root").error(f"Failed to take screenshot: {str(e)}")

    def select_values_from_drop_down_textContent(self, dropDownOptionsList, value):
        try:
            element_find = "N"
            for element in dropDownOptionsList:
                time.sleep(3)
                if element.get_attribute('textContent') == value:
                    element.click()
                    element_find = "y"
                    break
            if element_find == "N":
                logging.getLogger("root").warning(f"Cannot select value from dropdown: {value}")
        except Exception as e:
            logging.getLogger("root").error(f"Failed to select value from dropdown: {str(e)}")

    def select_values_from_drop_down_index(self, dropDownOptionsList, value):
        try:
            element_find = "N"
            for element in dropDownOptionsList:
                if element.get_attribute('data-offset-index') == value:
                    element.click()
                    element_find = "y"
                    break
            if element_find == "N":
                logging.getLogger("root").warning(f"Cannot select value from dropdown by index: {value}")
        except Exception as e:
            logging.getLogger("root").error(f"Failed to select value from dropdown by index: {str(e)}")

    def wait_for_element_clickable(self, locator, timeOut=10):
        try:
            WebDriverWait(self.driver, timeOut).until(EC.element_to_be_clickable((self.get_by_type(locator[0]), locator[1])))
        except Exception as e:
            logging.getLogger("root").error(f"Timed out waiting for element to be clickable: {str(e)}")

    def wait_for_element_not_clickable(self, locator, timeOut=10):
        try:
            WebDriverWait(self.driver, timeOut).until_not(EC.element_to_be_clickable((self.get_by_type(locator[0]), locator[1])))
        except Exception as e:
            logging.getLogger("root").error(f"Timed out waiting for element to not be clickable: {str(e)}")

    def context_click(self, locator):
        try:
            action = ActionChains(self.driver)
            action.context_click(self.get_element(locator)).perform()
            logging.getLogger("root").info(f"Performed context click on element with locator: {locator}")
        except Exception as e:
            logging.getLogger("root").error(f"Failed to perform context click on element with locator {locator}: {str(e)}")

    def get_elements(self, locator):
        elements = None
        try:
            locator_type = locator[0]
            locator_value = locator[1]
            by_type = self.get_by_type(locator_type)
            elements = self.driver.find_elements(by_type, locator_value)
            logging.getLogger("root").info(f"Found {len(elements)} elements with locator: {locator}")
            return elements
        except Exception as e:
            logging.getLogger("root").error(f"Failed to find elements with locator {locator}: {str(e)}")
            return None

    def page_refresh_and_wait(self, timeOut=5):
        try:
            self.driver.refresh()
            time.sleep(timeOut)
        except Exception as e:
            logging.getLogger("root").error(f"Failed to refresh page: {str(e)}")

    def select_values_from_drop_down_with_JS(self, dropDownOptionsList, value, timeOut=10):
        try:
            element_find = "N"
            for element in dropDownOptionsList:
                if element.text == value:
                    WebDriverWait(self.driver, timeOut).until(EC.element_to_be_clickable(element))
                    self.driver.execute_script("arguments[0].click();", element)
                    element_find = "y"
                    break
            if element_find == "N":
                logging.getLogger("root").warning(f"Cannot select value from dropdown with JS: {value}")
        except Exception as e:
            logging.getLogger("root").error(f"Failed to select value from dropdown with JS: {str(e)}")

    def select_values_from_drop_down_textContent_JS(self, dropDownOptionsList, value, timeOut=10):
        try:
            element_find = "N"
            for element in dropDownOptionsList:
                if element.get_attribute('textContent') == value:
                    self.driver.execute_script("arguments[0].click();", element)
                    element_find = "y"
                    break
            if element_find == "N":
                logging.getLogger("root").warning(f"Cannot select value from dropdown with JS using textContent: {value}")
        except Exception as e:
            logging.getLogger("root").error(f"Failed to select value from dropdown with JS using textContent: {str(e)}")

    def sleep1(self):
        time.sleep(1)

    def sleep2(self):
        time.sleep(2)

    def sleep3(self):
        time.sleep(3)

    def sleep5(self):
        time.sleep(5)

    def imp_wait_20(self):
        self.driver.implicitly_wait(20)

    def imp_wait_20_and_then_sleep1(self):
        self.driver.implicitly_wait(20)
        time.sleep(1)

    def imp_wait_20_and_then_sleep2(self):
        self.driver.implicitly_wait(20)
        time.sleep(2)

    def imp_wait_8_and_then_sleep2(self):
        self.driver.implicitly_wait(8)
        time.sleep(2)

    def imp_wait_5_and_then_sleep2(self):
        self.driver.implicitly_wait(5)
        time.sleep(2)

    def scroll_fixed_steps(self, steps=1):
        try:
            scrollable_ui = f'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollForward({steps})'
            self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, scrollable_ui)
        except NoSuchElementException:
            logging.getLogger("root").info(f"Not scrolled {steps} steps.")

    def screenshot(self, testcase_name="", module_name=""):
        try:
            test_name = testcase_name.replace(" ", "_")
            date = datetime.now().strftime("%I_%M%p_%B_%d_%Y").replace(':', "_")
            fileDir = os.path.dirname(os.path.abspath(__file__))
            screenshots_root_dir = os.path.join(os.path.dirname(fileDir), "Screenshots")
            file_path = os.path.join(screenshots_root_dir, module_name,
                                     f"{test_name}_DATE_{date}.png")

            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            if self.driver.save_screenshot(file_path):
                logging.info(f" Screenshot saved at: {file_path}")
            else:
                logging.info(" Screenshot failed to save!")
                return None, None
            return file_path, screenshots_root_dir
        except Exception as e:
            logging.getLogger("root").error(f"Error taking screenshot: {e}")
            return None, None

    def get_current_window_size(self):
        return self.driver.get_window_size()

    def wait_untill_element_visible(self,element_to_be_visible,max_wait):
        for i in range(max_wait):
            if self.get_element_present_status(element_to_be_visible):
                break
            elif i == max_wait-1:
                assert False , 'max pool wait exceeded'
            else:
                time.sleep(1)

    def wait_untill_element_invisible(self,element_to_be_invisible,max_wait):
        for i in range(max_wait):
            if not self.get_element_present_status(element_to_be_invisible):
                break
            elif i == max_wait-1:
                assert False , 'max pool wait exceeded'
            else:
                time.sleep(1)

    def initialization_issue(self):
        try:
            time.sleep(10)
            if self.get_element_present_status((AppiumBy.XPATH, "//android.widget.TextView[@text='Initializing']")):
                self.driver.back()
            time.sleep(3)
        except Exception as e:
            logging.info(f"Back is not working: {e}")