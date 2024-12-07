from time import sleep

from selenium_files.pages.fleet_page import FleetPage
from selenium_files.pages.login_page import LoginPage
import logging
#logger setup
logger = logging.getLogger(__name__)

def test_create_vehicle_positive(driver):
    """
    Test validation after saving a new vehicle in the Fleet module without data (negative scenario).
    """
    # Test credentials
    username = "admin"
    password = "password"

    # Login to Odoo
    login_page = LoginPage(driver)
    driver.get("http://localhost:8015/web/login")
    login_page.enter_username(username)
    login_page.enter_password(password)
    login_page.click_login()

    # Navigate to Fleet module
    # Create
    fleet_page = FleetPage(driver)
    fleet_page.navigate_to_fleet_module()
    fleet_page.create_new_vehicle()

    #Click save without filling in data + verify error message
    fleet_page.save_vehicle()
    fleet_page.verify_error_message()

    #Success log
    logger.info("Successfully validated empty car model error message.")