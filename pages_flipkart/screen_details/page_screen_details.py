from selenium.webdriver.common.by import By
from base_utilities.base import BasePage
import logging
import time
from utilities.utils import Utils


class ScreenDetails(BasePage):

    log = logging.getLogger('flipkartSearch.pdp')
    com_utils = Utils()

    _purchase_item_pdp_title = (By.XPATH, "//h1/span[starts-with(@class,'_')]")
    pdp_item_cost = (By.XPATH, "(//div[contains(text(),'₹')])[1]")
    _add_to_basket = (By.XPATH, "//div[@class='row']/button[contains(text(),'ADD TO BASKET')]")
    _add_to_cart = (By.XPATH, "//ul/li/button")
    _cart_icon = (By.XPATH, "//a/span[contains(text(),'Cart')]")

    def get_pdp_item_title_cost(self):
        """
        To return the cost of the item from PDP
        """
        purchase_item_pdp_cost = self.getText(self.pdp_item_cost, info="Item Price value")
        print("PDP cost value :: " + str(purchase_item_pdp_cost))
        return purchase_item_pdp_cost

    def add_navigate_cart(self):
        """
        Add to basket and Navigate to cart
        """
        basket_elem = self.getElement(self._add_to_basket, elementName="Add to Basket button")
        if basket_elem is None:
            # cart_elem = self.getElement(self._add_to_cart, elementName="Add to Cart button")
            # self.javascript_execute("arguments[0].scrollIntoView();", cart_elem)
            self.elementClick(self._add_to_cart, elementName="Add to Cart button")
            time.sleep(2)
        else:
            # self.javascript_execute("arguments[0].scrollIntoView();", basket_elem)
            self.elementClick(self._add_to_basket, elementName="Add to Basket button")
            time.sleep(2)

        # self.elementClick(self._add_to_basket, elementName="Add to Basket button")
        # time.sleep(2)
        # self.elementClick(self._add_to_cart, elementName="Add to Cart button")
        # time.sleep(2)
        self.elementClick(self._cart_icon, elementName="Cart icon")
        time.sleep(2)



