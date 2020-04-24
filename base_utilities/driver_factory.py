"""
It creates a webdriver instance based on browser configurations

"""

from selenium import webdriver
import os

class DriverFactory():

    def __init__(self, browser):
        """
        Inits WebDriverFactory class
        """
        self.browser = browser


    def getDriverInstance(self, url=None):
        """
       Get Driver Instance based on the browser configuration

        Returns:
            'Driver Instance'
        """
        #baseURL = "https://www.amazon.com"
        if self.browser == "iexplorer":
            # Set ie driver
            driver = webdriver.Ie()
        elif self.browser == "firefox":
            driver = webdriver.Firefox(executable_path='..\\executables\\geckodriver.exe')
        elif self.browser == "chrome":
            # Set chrome driver
            chromeDriverLocation = "..\\executables\\chromedriver.exe"
            os.environ["webdriver.chrome.driver"] = chromeDriverLocation
            driver = webdriver.Chrome(chromeDriverLocation)
        else:
            #driver = webdriver.Firefox(executable_path='..\\executables\\geckodriver.exe')
            pass
        # Setting Driver Implicit Time out for An Element
        driver.implicitly_wait(5)
        # Maximize the window
        driver.maximize_window()
        return driver