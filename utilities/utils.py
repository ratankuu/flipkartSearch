"""
@package utilities

Util class implementation
Commonly used Python utilities in this class

"""

import time
import traceback
import logging
from selenium.webdriver.common.by import By

class Utils(object):
    log = logging.getLogger('flipkartSearch.python_utils')

    def addTextValXpath(self, addLinkVal, val1, val2='None'):
        """
        Used to generate dynamic xpath values
        """
        if val2 is not None:
            val3 = val1.format(addLinkVal, val2)
        else:
            val3 = val1.format(addLinkVal)
        ADD_VAL = (By.XPATH, val3)
        return ADD_VAL

    def verifyTextMatch(self, actualText, expectedText):
        """
        Verify text match
        """
        self.log.info("Actual Text From Application Web UI --> :: " + actualText)
        self.log.info("Expected Text From Application Web UI --> :: " + expectedText)
        if expectedText.lower() in actualText.lower():
            self.log.info("### VERIFICATION MATCHED !!!")
            return True
        else:
            self.log.info("### VERIFICATION DOES NOT MATCH !!!")
            return False