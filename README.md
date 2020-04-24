# flipkartSearch
1. Framework used -> Selenium Webdriver + Python + Pytest + allure reports framework
2. input_data_yaml/input_data.yaml -> to update the required inputs
3. Updates required to execute:
  FlipKart Username & Password stored in environment variables as "flip_username" and "flip_password".
  Please change the UserName in input_data.yaml used for assertion purpose.
4. executables/ -> chrome driver & gecko driver exe's to use by the scripts for browser compatibility
5. Log files would be created in log/ directory
6. Test Suite is "TestFlipkartSearch" and flow starts from tests/test_flipkartSearch.py
7. Flow:
  Invoke Flipkart URL
  Sign in with the credentials
  Search using the "Search Parameter Value" -> input_data.yaml
  Select any of the items in the search results and get the ITEM NAME
  Click the item and get the PRICE of the item
  Click ADD TO BASKET / ADD TO CART buttons
Note : Due to the pandemic, the results are not consistent and most of the times the buttons are disabled/not found and hence could not
proceed with the next steps.
8. Pycharm Run configurations in "Additional Arguments":
	-v -m flipkartSearch --browser firefox --alluredir <location of allure_report directory in local>
Note : Without --browser option -> Chrome browser would be invoked
9. Generate allure reports:
"allure.bat" is required in local. Navigate to path in command line and execute:
allure serve <location of allure_report directory in local>