from time import sleep

from selenium_files.pages.hospital_page import HospitalPage
from selenium_files.pages.login_page import LoginPage
import logging
#logger setup
logger = logging.getLogger(__name__)

def test_create_vehicle_positive(driver):
    """
    Test creating a new vehicle in the Fleet module (positive scenario).
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
    # Create and save after entering patient data
    hospital_page = HospitalPage(driver)
    hospital_page.navigate_to_hospital_module()
    hospital_page.create_new_patient()
    hospital_page.enter_patient_name("Cal Newport")
    hospital_page.select_gender("Female")
    hospital_page.select_responsible("Azure Interior")
    hospital_page.enter_description("This is a new Patient, Cal")
    hospital_page.enter_age("32")
    hospital_page.save_patient()
    hospital_page.is_patient_saved()

    # Dictionary of data used
    info_dict = {
        "name": "Cal Newport",
        "gender": "Female",
        "responsible": "Azure Interior",
        "description": "This is a new Patient, Cal",
        "age": "32",
    }

    # Ensure data on page matches data in dict
    hospital_page.verify_saved_inputs(info_dict)

    #Success log
    logger.info("Successfully created and saved patient.")