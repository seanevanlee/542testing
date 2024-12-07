from time import sleep

from selenium_files.pages.hospital_page import HospitalPage
from selenium_files.pages.login_page import LoginPage
import logging
#logger setup
logger = logging.getLogger(__name__)

def test_create_vehicle_positive(driver):
    """
    Test validation after saving a new patient in the Hospital module without data (negative scenario).
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

    # Navigate to Hospital module
    # Click create button to navigate to patient creation
    hospital_page = HospitalPage(driver)
    hospital_page.navigate_to_hospital_module()
    hospital_page.create_new_patient()

    #Click save without filling in data + verify error message
    hospital_page.save_patient()
    hospital_page.verify_error_message()

    #Success log
    logger.info("Successfully validated empty patient name error message.")