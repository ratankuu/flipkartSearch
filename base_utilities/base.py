"""
This class needs to be inherited by all the page classes
"""
from .selenium_utils import SeleniumUtils
from traceback import print_stack


class BasePage(SeleniumUtils):

    def __init__(self, driver):
        """
        Inits BasePage class
        """
        super(BasePage, self).__init__(driver)
        self.driver = driver

    def verifyPageTitle(self, titleToVerify):
        """
        Verify the page Title
        Note : Not used in any of the tests
        """
        try:
            actualTitle = self.getTitle()
            assert actualTitle == titleToVerify, "Home page title does NOT match"
            #return self.util.verifyTextContains(actualTitle, titleToVerify)
            #return True
        except:
            self.log.error("Failed to get page title")
            print_stack()
            return False