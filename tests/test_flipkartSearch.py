import pytest
import allure
import logging
import os
from pages_flipkart.home.page_home import PageHome
from pages_flipkart.screen_details.page_screen_details import ScreenDetails

log = logging.getLogger('flipkartSearch.test_source')

@pytest.mark.usefixtures('homePage_fixture')
@pytest.mark.flipkartSearch
@allure.feature('Flipkart Search')
class TestFlipkartSearch():

    title_val = None
    item_price = None

    #used to get the values from the assigned fixture
    @pytest.fixture(autouse=True)
    def home(self, homePage_fixture):
        self.driver_session = self.driver
        self.input_data = self.input_data
        self.url_val = self.url
        self.search_val = self.search_param
        self.home_page = PageHome(self.driver)
        #self.srchResults_page = SearchResults(self.driver)
        self.scrDetails_page = ScreenDetails(self.driver)

    def test_invoke_flipkart(self):
        _ = 'Invoking the flipkart URL'
        log.info(_)
        with allure.step(_):
            url = self.home_page.invoke_url(self.url_val)
            # print(os.environ.get("flip_username"))
            # print(os.environ.get("flip_password"))
            assert url, "Flipkart - Landing page NOT loaded properly"

    def test_signIn_user_credentials(self):
        #Flipkart UserName/Email Address and Password in Environment variables for security reasons
        _ = 'Enter Email Address and Password to SignIn'
        log.info(_)
        with allure.step(_):
            userName_value = self.home_page.signIn_validate_credentials(self.input_data["ASSERT_NAME"])
            assert userName_value, "User NOT signed in with the credentials"

    def test_enter_value_search(self):
        _ = 'Running tests for entering search values and search'
        log.info(_)
        with allure.step(_):
            breadcrumb_val = self.home_page.enter_value_search(self.input_data["SEARCH_PARAMETER"].lower())
            assert breadcrumb_val, self.input_data["SEARCH_PARAMETER"] + " -- value NOT present in the Search results bread crumb"

    def test_select_items_search_results(self):
        #global bookTitle_val
        _ = 'Running test for selecting the value in search results'
        log.info(_)
        with allure.step(_):
            # "results for" breadcrumb text in the page after displaying the search results
            TestFlipkartSearch.title_val = self.home_page.select_random_item_search_results("results for")
            print("Title value is :: " + TestFlipkartSearch.title_val)
            self.home_page.click_item_search_results(TestFlipkartSearch.title_val)
            assert TestFlipkartSearch.title_val, "Purchase Item value NOT Selected"

    def test_verify_select_items_navigate_cart(self):
        _ = 'Running test to verify the title and get price of selected item'
        log.info(_)
        with allure.step(_):
            self.item_price = self.scrDetails_page.get_pdp_item_title_cost()
            assert self.item_price, "Item price NOT populated"

        _ = "Add item to basket and navigate to cart"
        log.info(_)
        with allure.step(_):
            self.scrDetails_page.add_navigate_cart()




