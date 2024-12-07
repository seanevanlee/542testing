from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        # Locators
        self.username_locator = (By.ID, "login")
        self.password_locator = (By.ID, "password")
        self.login_button_locator = (By.XPATH, "//button[@type='submit']")
        self.user_avatar_locator = (By.CSS_SELECTOR, "img.o_user_avatar[alt='User']")

    def enter_username(self, username):
        username_field = self.wait.until(EC.presence_of_element_located(self.username_locator))
        username_field.send_keys(username)

    def enter_password(self, password):
        password_field = self.wait.until(EC.presence_of_element_located(self.password_locator))
        password_field.send_keys(password)

    def click_login(self):
        login_button = self.wait.until(EC.element_to_be_clickable(self.login_button_locator))
        login_button.click()

    def is_user_avatar_visible(self):
        user_avatar = self.wait.until(EC.presence_of_element_located(self.user_avatar_locator))
        return user_avatar.is_displayed()
