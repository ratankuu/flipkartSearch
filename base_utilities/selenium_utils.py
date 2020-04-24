from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from traceback import print_stack
import logging
import time

class SeleniumUtils(object):
    log = logging.getLogger('flipkartSearch.selenium_utils')

    def __init__(self, driver):
        self.driver = driver

    def open(self, url):
        self.driver.get(url)
        self.driver.set_page_load_timeout(10)

    def page_loaded(self):
        for i in range(10):
            _ = self.driver.execute_script('return document.readyState;')
            if _ == 'complete':
                return True
        return False

    def javascript_execute(self, *script):
        self.driver.execute_script(*script)

    def getAttributeVals(self, locator, val, elementName='None'):
        metaElem1 = self.getElement(locator, elementName=elementName)
        #Get value of the attribute in the locator
        metaElem = metaElem1.get_attribute(val)
        return metaElem

    def select(self, locator, txt, elementName="None"):
        element = self.getElement(locator, elementName=elementName)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        value_options = [values for values in element.find_elements_by_tag_name("option")]

        elem = Select(element)
        for value in value_options:
            books_val = value.get_attribute("value")
            if txt in books_val:
                elem.select_by_value(books_val)
                return True

    def getElement(self, locator, elementName=None):
        element = None
        try:
            element = self.driver.find_element(*locator)
            self.log.info("Element found with locator: " + str(elementName))
        except:
            try:
                elem = self.driver.find_element(*locator)
                actions = ActionChains(self.driver)
                time.sleep(1)
                actions.move_to_element(elem)
            except Exception as e:
                self.log.info("Element not found with locator: " + str(elementName))
        return element

    def getElementList(self, locator):
        """
        Get list of elements
        """
        element = None
        try:
            element = self.driver.find_elements(*locator)
            self.log.info("Element list found with locator: " + str(locator))
        except:
            self.log.info("Element list not found with locator: " + str(locator))
        return element

    def elementClick(self, locator="", element=None, elementName=None):
        """
        Either provide element or locator
        """
        try:
            if locator:  # if locator is not empty
                element = self.getElement(locator, elementName=elementName)
            element.click()
            self.log.info("Clicked on element : " + elementName)
        except:
            self.log.info("Cannot click on the element: " + elementName)
            #print_stack()

    def sendKeys(self, data, locator="", elementName=None):
        """
        Either provide element or locator
        """
        try:
            if locator:  # This means if locator is not empty
                element = self.getElement(locator, elementName=elementName)
            element.send_keys(data)
            self.log.info("Sent data on element with locator: " + elementName)
        except:
            self.log.info("Cannot send data on the element with locator: " + elementName)
            #print_stack()

    def getText(self, locator="", element=None, info=""):
        """
        Get 'Text' on an element
        Either provide element or locator
        """
        try:
            if locator:
                element = self.getElement(locator, elementName=info)
            self.log.debug("Finding text")
            text = element.text
            self.log.debug("After finding element, test size is: " + str(len(text)))
            if len(text) == 0:
                text = element.get_attribute("innerText")
            if len(text) != 0:
                self.log.info("Getting text on element :: " + info)
                #self.log.info("The text is :: '" + text + "'")
                text = text.strip()
        except:
            self.log.error("Failed to get text on element " + info)
            #print_stack()
            text = None
        return text

    def isElementPresent(self, locator="", element=None, elementName=None):
        """
        Either provide element or a locator
        """
        try:
            if locator:  # This means if locator is not empty
                element = self.getElement(locator, elementName=elementName)
            if element is not None:
                self.log.info("Element present with locator: " + str(locator))
                return True
            else:
                self.log.info("Element not present with locator: " + str(locator))
                return False
        except:
            self.log.info("Element not found")
            return False

    def waitForElement(self, locator,
                       timeout=10, pollFrequency=1, elementName=None):
        element = None
        try:
            self.log.info("Waiting for maximum :: " + str(timeout) +
                          " :: seconds for element to be clickable")
            wait = WebDriverWait(self.driver, timeout=timeout,
                                 poll_frequency=pollFrequency,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(EC.element_to_be_clickable((locator)))
            self.log.info("Element appeared on the web page :: " + elementName)
        except:
            self.log.info("Element not appeared on the web page :: " + elementName)
            #print_stack()
        return element

    def clearTextVals(self, locator, elementName='None'):
        elem = self.getElement(locator, elementName=elementName)
        elem.clear()
        self.log.info(elementName + " : values are cleared for editing")
