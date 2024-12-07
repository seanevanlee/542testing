import time  # for manual delays
import logging
from selenium_files.pages.login_page import LoginPage

#logger setup
logger = logging.getLogger(__name__)

# Constant for sleep time
SLEEP_TIME = 1.5 # can be adjusted as needed for demo/performance

def test_valid_login(driver):
    # Login credentials
    username = "admin"
    password = "password"

    # Initialize LoginPage
    login_page = LoginPage(driver)

    # Navigate to the login page
    driver.get("http://localhost:8015/web/login")

    # Perform login with delays to visualize steps
    # time.sleep(SLEEP_TIME)  # Wait and enter username
    login_page.enter_username(username)

    # time.sleep(SLEEP_TIME)  # Wait and enter password
    login_page.enter_password(password)

    # time.sleep(SLEEP_TIME)  # Wait and click login button
    login_page.click_login()

    time.sleep(SLEEP_TIME)  # Wait to observe landing page loading

    # Verify login success
    assert login_page.is_user_avatar_visible(), "User avatar not visible. Login may have failed."

    #Success log
    logger.info("Login successful - user avatar is visible.")
