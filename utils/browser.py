import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver


class ElementActions:
    def __init__(self, element: WebElement):
        self.element = element

    def click(self):
        if not self.element.is_displayed():
            raise RuntimeError("Element is not displayed.")
        if not self.element.is_enabled():
            raise RuntimeError("Element is not enabled.")
        self.element.click()

    def send_keys(self, keys):
        if not self.element.is_displayed():
            raise RuntimeError("Element is not displayed.")
        if not self.element.is_enabled():
            raise RuntimeError("Element is not enabled.")
        self.element.send_keys(keys)

    def get_text(self):
        if not self.element.is_displayed():
            raise RuntimeError("Element is not displayed.")
        return self.element.text.strip()

    def get_attribute(self, name):
        if not self.element.is_displayed():
            raise RuntimeError("Element is not displayed.")
        return self.element.get_attribute(name).strip() if self.element.get_attribute(name) else None

    def find_element(self, by, value):
        if not self.element.is_displayed():
            raise RuntimeError("Element is not displayed.")
        found_element = self.element.find_element(by, value)
        if not found_element:
            raise RuntimeError(f"Element not found: {by}={value}")
        return ElementActions(found_element)

class BrowserFirefox:
    def __init__(self, binary_path=None, options=None, headless=True):
        self.__started = False
        self.binary_path = binary_path
        self.options = options or FirefoxOptions()
        if headless:
            self.options.add_argument("--headless")
        self.driver = None

    def start(self):
        if self.__started:
            raise RuntimeError("Browser is already running.")
        self.__started = True
        self.options.binary_location = self.binary_path
        self.driver = webdriver.Firefox(options=self.options)
        self.__started = True

    def stop(self):
        if not self.__started:
            return
        if self.driver:
            self.driver.quit()
            self.driver = None


    def get_url(self, url, timeout=10):
        if not self.__started:
            raise RuntimeError("Browser is not started.")
        self.driver.get(url)
        is_url = WebDriverWait(self.driver, timeout).until(lambda d: d.current_url == url)
        while not is_url and timeout > 0:
            time.sleep(0.1)
            timeout -= 0.1


    def find_elements(self, by, value, timeout=10):
        if not self.__started:
            raise RuntimeError("Browser is not started.")
        elements_found = WebDriverWait(self.driver, timeout).until(
            lambda d: d.find_elements(by, value)
        )
        while not elements_found and timeout > 0:
            time.sleep(0.1)
            timeout -= 0.1
        if not elements_found:
            raise RuntimeError(f"Element not found: {by}={value}")
        return [ElementActions(x) for x in elements_found]

    def find_element(self, by, value, timeout=10):
        return self.find_elements(by, value, timeout=timeout)[0]



    def wait_for_url(self, url = None, regex = None, timeout=10):
        if not self.__started:
            raise RuntimeError("Browser is not started.")
        if not url and not regex:
            raise ValueError("Either url or regex must be provided.")

        if regex is None:
            found = WebDriverWait(self.driver, timeout).until(lambda d: url in d.current_url)
        else:
            found = WebDriverWait(self.driver, timeout).until(lambda d: re.search(regex, d.current_url) is not None)

        while not found and timeout > 0:
            time.sleep(0.1)
            timeout -= 0.1
            if regex is None:
                found = WebDriverWait(self.driver, timeout).until(lambda d: url in d.current_url)
            else:
                found = WebDriverWait(self.driver, timeout).until(lambda d: re.search(regex, d.current_url) is not None)

    def wait_for_element(self, by, value, timeout=10):
        if not self.__started:
            raise RuntimeError("Browser is not started.")
        elements_found = WebDriverWait(self.driver, timeout).until(
            lambda d: d.find_elements(by, value)
        )
        while not elements_found and timeout > 0:
            time.sleep(0.1)
            timeout -= 0.1
        if not elements_found:
            raise RuntimeError(f"Element not found: {by}={value}")

    def get_cookies(self):
        if not self.__started:
            raise RuntimeError("Browser is not started.")
        return self.driver.get_cookies()

def get_2fa_options(browser: BrowserFirefox) -> list[tuple[str, ElementActions]]:
    """
    Get the available 2FA options.

    :param browser: The browser instance.
    :return: A list of available 2FA options.
    """
    # Get the 2FA options
    elements = browser.find_elements(By.CSS_SELECTOR, "div.radio")
    values = []
    for element in elements:
        label = element.find_element(By.TAG_NAME, "label")
        values.append((label.get_text(), label))
    return values

if __name__ == "__main__":
    options = FirefoxOptions()
    options.add_argument("--headless")
    browser = BrowserFirefox(binary_path=r"C:\Users\Floch\Downloads\geckodriver\geckodriver.exe", options=options)
    browser.start()
    browser.get_url("https://atoz-login.amazon.work/")
    browser.stop()