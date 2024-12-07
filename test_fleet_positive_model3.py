from time import sleep

from selenium_files.pages.fleet_page import FleetPage
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
    # Create and save after entering Tesla Model 3 data
    fleet_page = FleetPage(driver)
    fleet_page.navigate_to_fleet_module()
    fleet_page.create_new_vehicle()
    fleet_page.enter_vehicle_model("Model 3")
    fleet_page.enter_license_plate("CPSC542")
    fleet_page.select_tag("Sedan")
    fleet_page.select_driver("Azure Interior")
    fleet_page.fill_tax_info("9999", "42000")
    fleet_page.save_vehicle()
    fleet_page.is_vehicle_saved()

    # Dictionary of data used
    info_dict = {
        "model": "Model 3",
        "license_plate": "CPSC542",
        "tag": "Sedan",
        "driver": "Azure Interior",
        "horsepower_taxation": "9,999",
        "purchase_value": "42,000"
    }

    # Ensure data on page matches data in dict
    fleet_page.verify_saved_inputs(info_dict)

    #Success log
    logger.info("Successfully saved a new car to fleet.")