import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="function")
def driver():
    # WebDriver setup
    service = Service("/Users/keshav/Documents/chromeStuff/chromedriver")
    options = Options()
    options.binary_location = "/Users/keshav/Documents/chromeStuff/chromeTesting.app/Contents/MacOS/chromeTesting"
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()

    # WebDriver instance for test
    yield driver

    # Cleanup after the test
    driver.quit()