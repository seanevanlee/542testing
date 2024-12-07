from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from time import sleep

from odoo.release import description


class HospitalPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        # Locators
        self.menu_dropdown_locator = (By.CSS_SELECTOR, "button[title='Home Menu']")
        self.menu_hospital_locator = (By.CSS_SELECTOR, "a[data-menu-xmlid='om_hospital.menu_hospital_root']")
        self.create_patient_button_locator = (By.CSS_SELECTOR, "button[data-original-title='Create record']")
        self.save_button_locator = (By.CSS_SELECTOR, "button[title='Save record']")
        self.patient_name_input_locator = ()

    def navigate_to_hospital_module(self):
        """
        Open dropdown and navigate to Hospital module
        """
        # Open the Home Menu dropdown
        menu_dropdown = self.wait.until(EC.element_to_be_clickable(self.menu_dropdown_locator))
        menu_dropdown.click()

        # Click on the Hospital module
        hospital_menu = self.wait.until(EC.element_to_be_clickable(self.menu_hospital_locator))
        hospital_menu.click()

    def create_new_patient(self):
        """
        Clicks 'Create' button
        """
        sleep(1)
        # Click the "Create" button
        create_button = self.wait.until(EC.element_to_be_clickable(self.create_patient_button_locator))
        create_button.click()


    def enter_patient_name(self, patient_name):
        """
        Enters patient's name

        Args:
            patient_name (str): The name of the patient to input.
        """
        # Locate the License Plate input field
        patient_name_input = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='name']"))
        )

        # Clear the field before entering data
        patient_name_input.clear()

        # Enter the patient name text
        patient_name_input.send_keys(patient_name)

    def select_gender(self, gender_value):
        """
        Select gender from dropdown menu

        Args:
            gender_value (str): The gender to select.
        """
        try:
            # Locate the dropdown by its name attribute
            gender_dropdown = self.wait.until(
                EC.presence_of_element_located((By.NAME, "gender"))
            )

            # Use Selenium's Select class to interact with the dropdown
            select = Select(gender_dropdown)

            # Select by visible text (or change to select by value if needed)
            select.select_by_visible_text(gender_value)

            sleep(1)
        except Exception as e:
            print(f"Error selecting gender: {e}")
            raise

    def select_responsible(self, responsible_name):
        """
        Select a person from the Responsible dropdown

        Args:
            responsible_name (str): The name of the person responsible for patient.
        """
        # Click on Responsible dropdown to activate input field
        driver_dropdown = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[name='responsible_id']"))
        )
        driver_dropdown.click()

        # Enter driver name into active input field
        active_input = self.driver.switch_to.active_element
        active_input.send_keys(responsible_name)

    def enter_description(self, description_text):
        """
        Enter text into description input field

        Args:
            description_text (str): The text to enter into the description field.
        """
        try:
            # Locate the description input textarea
            description_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[name='note']"))
            )

            # Clear any existing text in the input field
            description_input.clear()

            # Enter the provided text
            description_input.send_keys(description_text)

        except Exception as e:
            print(f"Error entering description: {e}")
            raise

    def enter_age(self, age):
        """
        Enter patient's age into age input field

        Args:
            age (str): The age of the patient.
        """
        try:
            # Locate the description input textarea
            age_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='age']"))
            )

            # Clear any existing text in the input field
            age_input.clear()

            # Enter the provided text
            age_input.send_keys(age)

            sleep(2)

        except Exception as e:
            print(f"Error entering description: {e}")
            raise

    def save_patient(self):
        """
         Clicks 'Save' button
        """
        sleep(1)
        # Click the "Save" button
        save_button = self.wait.until(EC.element_to_be_clickable(self.save_button_locator))
        save_button.click()

    def is_patient_saved(self):
        """
        Verify if patient is saved successfully

        Returns:
            bool: True if the patient is saved successfully, False otherwise.
        """
        try:
            sleep(1)
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
            print(f"Error verifying patient save status: {e}")
            return False

    def verify_saved_inputs(self, expected_values):
        """
        Verify all the inputs were saved properly

        Args:
            expected_values (dict): A dictionary of expected field values.
                Example:
                {
                    "name": "First Last",
                    "gender": "Male",
                    "responsible": "Deco Addict",
                    "description": "adding a patient (new)",
                    "age": "55",
                }

        Returns:
            bool: True if all fields include the expected values, False otherwise.
        """
        try:
            # Verify Name
            name_value = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div span[name='name']"))
            ).text
            assert expected_values[
                       "name"] in name_value, f"Name mismatch: {name_value} does not include {expected_values['name']}"

            # Verify Gender
            gender_value = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div span[name='gender']"))
            ).text
            assert expected_values[
                       "gender"] in gender_value, f"License Plate mismatch: {gender_value} does not include {expected_values['gender']}"

            # Verify Responsible
            responsible_value = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[name='responsible_id'] span"))
            ).text
            assert expected_values[
                       "responsible"] in responsible_value, f"Tag mismatch: {responsible_value} does not include {expected_values['responsible']}"

            # Verify Age
            age_value = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div span[name='age']"))
            ).text
            assert expected_values[
                       "age"] in age_value, f"Driver mismatch: {age_value} does not include {expected_values['age']}"

            # Verify Description
            description_value = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div span[name='note']"))
            ).text
            assert expected_values[
                       "description"] in description_value, f"Driver mismatch: {description_value} does not include {expected_values['description']}"

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

        sleep(1)

        # Hard-coded (expected text)
        validation_message = "Invalid fields"
        expected_field = "Name"
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