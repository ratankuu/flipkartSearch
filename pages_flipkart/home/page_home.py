from selenium.webdriver.common.by import By
from base_utilities.base import BasePage
from utilities.utils import Utils
import os
import random
import time

class PageHome(BasePage):

    com_utils = Utils()
    email_value = os.environ.get("flip_username")
    password_value = os.environ.get("flip_password")

    _signIn_user_name = (By.XPATH, "(//input[@type='text'])[last()]")
    _signIn_password = (By.CSS_SELECTOR, "input[type='password']")
    _signIn_login = (By.XPATH, "(//button[@type='submit'])[last()]")
    _signIn_userName_val= '//div[contains(text(),"{0}")]'
    username_elem = None
    _search_results_index_path = None
    _signIn_searchBox = (By.CSS_SELECTOR, "input[type='text'][name='q']")
    _search_icon = (By.CSS_SELECTOR, "button[type='submit']")
    _results_breadcrumb = "//div[@class='bhgxx2']//following::span[contains(text(),'{}')]"
    _search_results_index = "(//div[contains(@class,'bhgxx2 col-12-12')]/div/child::div[@data-id])[{}]//following::a"
    _purchase_item_pdp_title = "//h1/span[contains(text(), '{}')]"

    def invoke_url(self, url):
        """
        Get amazon url and wait for the page to load
        """
        self.open(url)
        pageLoaded = self.page_loaded()
        return pageLoaded

    def signIn_enter_emailaddress(self):
        self.clearTextVals(self._signIn_user_name, "Email/Mobile Number field")
        self.sendKeys(self.email_value, self._signIn_user_name, "Email/Mobile Number text field")

    def signIn_enter_password(self):
        self.clearTextVals(self._signIn_password, "Password field")
        self.sendKeys(self.password_value, self._signIn_password, "Password text field")

    def signIn_click_login(self, userName_val):
        self.elementClick(self._signIn_login, elementName="Login button")
        self._signIn_userName_assert = self.com_utils.addTextValXpath(userName_val, self._signIn_userName_val)
        self.username_elem = self.waitForElement(self._signIn_userName_assert, elementName="User Name text")

    def signIn_validate_credentials(self, userName_val):
        self.signIn_enter_emailaddress()
        self.signIn_enter_password()
        self.signIn_click_login(userName_val)
        return self.username_elem

    def enter_value_search(self, searchValue):
        """
        Enter values based on searchValue parameter
        """
        self.sendKeys(searchValue, self._signIn_searchBox, elementName="Search box")
        self.elementClick(self._search_icon, elementName="Search icon")
        _search_results_breadcrumb = self.com_utils.addTextValXpath(searchValue, self._results_breadcrumb)
        self.waitForElement(_search_results_breadcrumb, elementName="Breadcrumb text")
        breadcrumb_searchVal = self.isElementPresent(locator=_search_results_breadcrumb)
        return breadcrumb_searchVal

    def select_random_item_search_results(self, searchLabel):
        """
        Select any random item from the search results
        """
        _search_results_breadcrumb = self.com_utils.addTextValXpath(searchLabel, self._results_breadcrumb)
        results_text = self.getText(_search_results_breadcrumb, info="Getting results count in page")
        #print("Breadcrumb for search results :: " + results_count)
        results_index = results_text.split(" ")
        #print("Results index :: " + str(results_index))
        results_start_index = results_index[1]
        #print("Results start index :: " + str(results_start_index))
        results_end_index = results_index[3]
        #print("Results End index :: " + str(results_end_index))
        random_index = random.randint(int(results_start_index) + 1, int(results_end_index) - 1)
        #print("Selecting the item in index :: " + str(random_index))
        self._search_results_index_path = self.com_utils.addTextValXpath(random_index, self._search_results_index)
        purchase_item_title = self.getText(self._search_results_index_path, info="Purchase Item Title")
        if purchase_item_title.endswith("..."):
            purchase_item_title = purchase_item_title.replace("...", "", 1)
        return purchase_item_title

    def click_item_search_results(self, purchase_item_title):
        self.elementClick(self._search_results_index_path, elementName="Purchase Item")
        time.sleep(3)
        # purchase_item_pdp_title = self.com_utils.addTextValXpath(purchase_item_title, self._purchase_item_pdp_title)
        # self.waitForElement(purchase_item_pdp_title, elementName="PDP - Purchase Item Title")

