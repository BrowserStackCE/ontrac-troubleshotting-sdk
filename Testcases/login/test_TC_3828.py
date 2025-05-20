import logging
from ElliPageObjects.login_page import ElliLoginPage
import pytest
from Utilities.read_properties import read_json_file
from Utilities.common_util import LOGIN_PATH


class Test_TC_3828:
    login_data = read_json_file(LOGIN_PATH)

    @pytest.mark.android
    @pytest.mark.ios
    @pytest.mark.no_driver_1
    @pytest.mark.xdist_group("train_driver1")
    #no driver required so running on real_driver thread
    def test_Login_TC_3828_Launch_elli_application(self, appium_driver_setup):
        logging.getLogger("root").info("Starting test_login_list_options")
        elli_login_page = ElliLoginPage(appium_driver_setup)
        elli_login_page.perform_initial_actions()
        elli_login_page.fill_and_submit_form(self.login_data["sequence_url"], self.login_data["events_url"])
        logging.getLogger("root").info("Changing to stages Successfully")
        elli_login_page.assert_driver_id_and_password_field()
        elli_login_page.assert_and_select_terms_and_conditions()
        elli_login_page.click_and_print_context()
        logging.getLogger("root").info("Ending test_launch_elli_application")


# import logging
# import pytest

# # Minimal placeholder Page Object
# class ElliLoginPage:
#     def __init__(self, driver):
#         self.driver = driver

#     def wait_for_app_launch(self):
#         self.driver.implicitly_wait(10)

#     def is_login_field_visible(self):
#         try:
#             return self.driver.find_element("id", "login_field").is_displayed()
#         except:
#             return False

# class Test_TC_3828:

#     @pytest.mark.android
#     @pytest.mark.ios
#     @pytest.mark.no_driver_1
#     @pytest.mark.xdist_group("train_driver1")
#     def test_Login_TC_3828_Launch_elli_application(self, appium_driver_setup):
#         logging.getLogger("root").info("Starting test_Login_TC_3828_Launch_elli_application")
        
#         elli_login_page = ElliLoginPage(appium_driver_setup)
#         elli_login_page.wait_for_app_launch()
        
#         assert elli_login_page.is_login_field_visible(), "Login field not visible after launch"

#         logging.getLogger("root").info("App launched and login field verified successfully")


