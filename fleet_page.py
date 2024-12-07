from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from time import sleep

class FleetPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        # Locators
        self.menu_dropdown_locator = (By.CSS_SELECTOR, "button[title='Home Menu']")
        self.menu_fleet_locator = (By.CSS_SELECTOR, "a[data-menu-xmlid='fleet.menu_root']")
        self.vehicle_create_button_locator = (By.CSS_SELECTOR, "button[title='Create record']")

        self.save_button_locator = (By.CSS_SELECTOR, "button[title='Save record']")
        self.error_message_locator = (By.CLASS_NAME, "o_notification_manager")

    def navigate_to_fleet_module(self):
        """
        Open dropdown and navigate to Fleet module
        """
        # Open the Home Menu dropdown
        menu_dropdown = self.wait.until(EC.element_to_be_clickable(self.menu_dropdown_locator))
        menu_dropdown.click()

        # Click on the Fleet module
        fleet_menu = self.wait.until(EC.element_to_be_clickable(self.menu_fleet_locator))
        fleet_menu.click()

    def create_new_vehicle(self):
        """
        Clicks 'Create' button
        """
        # Click the "Create" button
        create_button = self.wait.until(EC.element_to_be_clickable(self.vehicle_create_button_locator))
        create_button.click()

    def enter_vehicle_model(self, vehicle_model):
        """
        Clicks 'Create' button

        Args:
            vehicle_name (str): The name of the vehicle to input
        """
        # Click on the parent div to activate the input field
        parent_div = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "div.o_field_widget.o_field_many2one.o_quick_editable.o_required_modifier"))
        )
        parent_div.click()  # Activate input field

        #Enter vehicle name
        self.driver.switch_to.active_element.send_keys(vehicle_model)

        # Wait for  dropdown to populate
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul.ui-autocomplete")))  # Adjust selector if needed

        # Wait for suggestion to appear
        self.wait.until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, "li.ui-menu-item"), "Tesla Motors/Model 3"
            )
        )

        # Simulate Enter key to select option
        self.driver.switch_to.active_element.send_keys(Keys.ENTER)

    def enter_license_plate(self, license_plate):
        """
        Enters license plate number

        Args:
            license_plate (str): The license plate to input.
        """
        # Locate the License Plate input field
        license_plate_input = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='license_plate']"))
        )

        # Clear the field before entering data
        license_plate_input.clear()

        # Enter the license plate text
        license_plate_input.send_keys(license_plate)

    def select_tag(self, tag_name):
        """
        Enters tag name into the Tags dropdown and selects it

        Args:
            tag_name (str): The name of the tag to select (ex: 'Sedan').
        """
        # Click on Tags dropdown
        tags_dropdown = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.o_field_widget.o_field_many2manytags"))
        )
        tags_dropdown.click()

        # Enter tag name into the input field
        active_input = self.driver.switch_to.active_element
        active_input.send_keys(tag_name)

        # Wait for desired tag to appear
        dropdown_items = self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.ui-menu-item"))
        )

        # Look for desired tag name in dropdown items
        for item in dropdown_items:
            if tag_name in item.text:
                item.click()  # Click matching item
                return

        # Raise error if no match found
        raise ValueError(f"Tag '{tag_name}' not found in the dropdown.")

    def select_driver(self, driver_name):
        """
        Select a driver from the Driver dropdown

        Args:
            driver_name (str): The name of the driver to select (ex: Deco Addict).
        """
        # Click on Driver dropdown to activate input field
        driver_dropdown = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[name='driver_id']"))
        )
        driver_dropdown.click()

        # Enter driver name into active input field
        active_input = self.driver.switch_to.active_element
        active_input.send_keys(driver_name)

    def fill_tax_info(self, horsepower_taxation, purchase_value):
        """
        Fill out Horsepower Taxation Purchase Value fields

        Args:
            horsepower_taxation (str or int): The value for Horsepower Taxation.
            purchase_value (str or int): The value for Purchase Value.
        """
        # Locate Horsepower Taxation input field and enter the value
        horsepower_input = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[name='horsepower_tax'] input"))
        )
        horsepower_input.click()  # Ensure the field is focused
        horsepower_input.clear()  # Clear any existing value
        horsepower_input.send_keys(horsepower_taxation)

        # Locate Purchase Value input field and enter the value
        purchase_value_input = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[name='net_car_value'] input"))
        )
        purchase_value_input.click()  # Ensure the field is focused
        purchase_value_input.clear()  # Clear any existing value
        purchase_value_input.send_keys(purchase_value)

    def save_vehicle(self):
        """
         Clicks 'Save' button
        """
        # Click the "Save" button
        save_button = self.wait.until(EC.element_to_be_clickable(self.save_button_locator))
        save_button.click()

    def is_vehicle_saved(self):
        """
        Verify if vehicle is saved successfully

        Returns:
            bool: True if the vehicle is saved successfully, False otherwise.
        """
        try:
            # Check if the "Save" button is no longer visible
            save_button_invisible = self.wait.until_not(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button[title='Save']"))
            )

            # Check if the "Edit" button is now visible
            edit_button_visible = self.wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "button[title='Edit']"))
            )

            # Return True if both conditions are met
            return save_button_invisible and edit_button_visible
        except Exception as e:
            print(f"Error verifying vehicle save status: {e}")
            return False

    def verify_saved_inputs(self, expected_values):
        """
        Verify all the inputs were saved properly

        Args:
            expected_values (dict): A dictionary of expected field values.
                Example:
                {
                    "model": "Tesla Model S",
                    "license_plate": "ABC-123",
                    "tag": "Sedan",
                    "driver": "Deco Addict",
                    "horsepower_taxation": "150",
                    "purchase_value": "30000"
                }

        Returns:
            bool: True if all fields include the expected values, False otherwise.
        """
        try:
            # Verify Model
            model_value = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div a[name='model_id'] span"))
            ).text
            assert expected_values[
                       "model"] in model_value, f"Model mismatch: {model_value} does not include {expected_values['model']}"

            # Verify License Plate
            license_plate_value = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div h2 span[name='license_plate']"))
            ).text
            assert expected_values[
                       "license_plate"] in license_plate_value, f"License Plate mismatch: {license_plate_value} does not include {expected_values['license_plate']}"

            # Verify Tag
            tag_value = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div a span span.o_tag_badge_text"))
            ).text
            assert expected_values[
                       "tag"] in tag_value, f"Tag mismatch: {tag_value} does not include {expected_values['tag']}"

            # Verify Driver
            driver_value = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[name='driver_id'] span"))
            ).text
            assert expected_values[
                       "driver"] in driver_value, f"Driver mismatch: {driver_value} does not include {expected_values['driver']}"

            # Verify Horsepower Taxation
            horsepower_tax_elements = self.driver.find_elements(
                By.CSS_SELECTOR, "div table:nth-child(1) tbody tr:nth-child(2) td:nth-child(2) span"
            )
            if not horsepower_tax_elements:
                raise ValueError("No elements found for Horsepower Taxation")
            horsepower_tax_value = horsepower_tax_elements[0].text
            assert expected_values[
                       "horsepower_taxation"] in horsepower_tax_value, f"Horsepower Taxation mismatch: {horsepower_tax_value} does not include {expected_values['horsepower_taxation']}"

            purchase_value_elements = self.driver.find_elements(
                By.CSS_SELECTOR, "div table:nth-child(1) tbody tr:nth-child(3) td:nth-child(2) span"
            )
            if not purchase_value_elements:
                raise ValueError("No elements found for Purchase Value")
            purchase_value = purchase_value_elements[0].text
            assert expected_values[
                       "purchase_value"] in purchase_value, f"Purchase Value mismatch: {purchase_value} does not include {expected_values['purchase_value']}"

            # If all fields match, return True
            return True

        except AssertionError as e:
            print(f"Verification failed: {e}")
            return False

    def verify_error_message(self):
        """
        Verify expected error message is displayed after an invalid save attempt

        Returns:
            bool: True if the expected error message is displayed, False otherwise.
        """

        # Hard-coded (expected text)
        validation_message = "Invalid fields"
        expected_field = "Model"
        try:
            # Wait for the error message to appear
            error_message = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".o_notification_title"))
            ).text

            # Locate / verify validation message
            error_message = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.o_notification_title"))
            ).text
            assert validation_message in error_message, f"Validation message mismatch: {error_message} does not include '{validation_message}'"

            # Locate / verify required field in notification content
            field_message = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.o_notification_content ul > li"))
            ).text
            assert expected_field in field_message, f"Required field mismatch: {field_message} does not include '{expected_field}'"

            #Visualize model
            sleep(1)

            # If both validations pass, return True
            return True

        except AssertionError as e:
            print(f"Verification failed: {e}")
            return False
        except Exception as e:
            print(f"An error occurred while verifying the validation error: {e}")
            return False