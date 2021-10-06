import datetime
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import pytest
import pytz
import time #for test testing purpose


class LoginTestCase(unittest.TestCase):
    """
    class for testing login redirects

    Methods
    -------
    setUp(self):
    test_login_field(self):
    test_login_office(self):
    test_login_admin(self):
    tearDown(self):
    """

    def setUp(self):
        """
        This function sets up the driver

        :return:
        """
        self.driver = webdriver.Chrome()

    def test_login_field(self):
        """
        This function asserts the redirect for field user login

        :return:
        """
        selenium = self.driver

        # Choose Url
        selenium.get("http://127.0.0.1:8000/")

        # Find elements
        user_email = selenium.find_element_by_id('id_username')
        user_password = selenium.find_element_by_id('id_password')

        submit = selenium.find_element_by_id('login')

        # Populate elements form
        user_email.send_keys('field@field.com')
        user_password.send_keys('field')

        # Submit form
        submit.send_keys(Keys.RETURN)

        # Expected results
        result_url = 'http://127.0.0.1:8000/field_user_home/'

        # Check result
        self.assertEqual(result_url, selenium.current_url)

    def test_login_office(self):
        """
        This function asserts the redirect for office user login

        :return:
        """
        selenium = self.driver

        # Choose Url
        selenium.get("http://127.0.0.1:8000/")

        # Find elements
        user_email = selenium.find_element_by_id('id_username')
        user_password = selenium.find_element_by_id('id_password')

        submit = selenium.find_element_by_id('login')

        # Populate elements form
        user_email.send_keys('office@office.com')
        user_password.send_keys('office')

        # Submit form
        submit.send_keys(Keys.RETURN)

        # Expected results
        result_url = 'http://127.0.0.1:8000/office_user_home/'

        # Check result
        self.assertEqual(result_url, selenium.current_url)

    def test_login_admin(self):
        """
        This function asserts the redirect for admin user login

        :return:
        """
        selenium = self.driver

        # Choose Url
        selenium.get("http://127.0.0.1:8000/")

        # Find elements
        user_email = selenium.find_element_by_id('id_username')
        user_password = selenium.find_element_by_id('id_password')

        submit = selenium.find_element_by_id('login')

        # Populate elements form
        user_email.send_keys('admin@admin.com')
        user_password.send_keys('admin')

        # Submit form
        submit.send_keys(Keys.RETURN)

        # Expected results
        result_url = 'http://127.0.0.1:8000/admin/'

        # Check result
        self.assertEqual(result_url, selenium.current_url)

    def tearDown(self):
        """
        This function "cleans up" selenium by closing the driver

        :return:
        """
        self.driver.close()


class LogsTestCase(unittest.TestCase):
    """
    class for testing logs

    NOTE
    ------
    All logs Logss table will be deleted!

    Methods
    -------
    setUp(self):
    test_create_log(self):
    test_facility_log(self):
    test_user_log(self):
    test_delete_log(self):
    tearDown(self):
    """

    dateTime_stamp = ""

    def setUp(self):
        """
        This function sets up the driver

        :return:
        """
        self.driver = webdriver.Chrome()

    @pytest.mark.run(order=1)
    def test_create_log(self):
        """
        This test creates a log through the admin user site

        :return:
        """
        selenium = self.driver

        # Choose start URL
        selenium.get("http://127.0.0.1:8000/")

        # ----------------------------------------------------------------------------------------------------------- #
        # Login
        ## Find elements
        user_email = selenium.find_element_by_id('id_username')
        user_password = selenium.find_element_by_id('id_password')

        submit = selenium.find_element_by_id('login')

        ## Populate elements form
        user_email.send_keys('admin@admin.com')
        user_password.send_keys('admin')

        ## Submit form
        submit.send_keys(Keys.RETURN)

        # ----------------------------------------------------------------------------------------------------------- #
        # Direct to "Logss"
        ## Find "logs" link and click
        button = selenium.find_element_by_xpath("//*[contains(text(), 'Logss')]")
        button.click()

        ## Find "ADD LOGS" link and click
        button = selenium.find_element_by_xpath("//*[contains(text(), 'Add logs')]")
        button.click()

        ## Find "Today" and "Now" and click"
        button1 = selenium.find_element_by_xpath("//*[contains(text(), 'Today')]")
        button2 = selenium.find_element_by_xpath("//*[contains(text(), 'Now')]")
        button1.click()
        button2.click()

        ## Find elements
        company_name = selenium.find_element_by_id('id_companyName')
        user_name = selenium.find_element_by_id('id_userName')
        user_email = selenium.find_element_by_id('id_userEmail')
        facility_name = selenium.find_element_by_id('id_facilityName')
        facility_location = selenium.find_element_by_id('id_facilityLocation')

        submit = selenium.find_element_by_name('_save')

        ## Populate elements form
        company_name.send_keys('Selenium company')
        user_name.send_keys('Selenium')
        user_email.send_keys('selenium@selenium.com')
        facility_name.send_keys('Selenium facility')
        facility_location.send_keys('Selenium road')

        ## Submit form
        submit.send_keys(Keys.RETURN)

        dt_stamp = datetime.datetime.now()
        self.dateTime_stamp = dt_stamp.strftime("%b. %#d, %Y, %#I:%#M")

        # ----------------------------------------------------------------------------------------------------------- #
        # Assert log object
        ### Check result
        self.assertTrue('Logs object', selenium.page_source)

    @pytest.mark.run(order=2)
    def test_facility_log(self):
        """
        This test checks the facility log view function

        :return:
        """

        selenium = self.driver

        # Choose start URL
        selenium.get("http://127.0.0.1:8000/")

        # ----------------------------------------------------------------------------------------------------------- #
        # Login
        ## Find elements
        user_email = selenium.find_element_by_id('id_username')
        user_password = selenium.find_element_by_id('id_password')

        submit = selenium.find_element_by_id('login')

        ## Populate elements form
        user_email.send_keys('office@office.com')
        user_password.send_keys('office')

        ## Submit form
        submit.send_keys(Keys.RETURN)

        # ----------------------------------------------------------------------------------------------------------- #
        # Direct to "View facility logs"
        ## Find link and click
        button = selenium.find_element_by_xpath("//*[contains(text(), 'View facility logs')]")
        button.click()

        # ----------------------------------------------------------------------------------------------------------- #
        # fill out "log filter" page
        ## Find select location option
        select = Select(selenium.find_element_by_name('fac_loc_list'))
        select.select_by_visible_text('Selenium road')
        ## Click filter
        button = selenium.find_element_by_xpath("/html/body/fieldset/form[1]/input[2]")
        button.submit()

        ## Find select location option
        select = Select(selenium.find_element_by_name('facilities_list'))
        select.select_by_visible_text('Selenium facility')
        ## Click view facility
        button = selenium.find_element_by_xpath("/html/body/fieldset/form[2]/input[2]")
        button.submit()

        # ----------------------------------------------------------------------------------------------------------- #
        # extract table values
        time.sleep(1)
        table_company = selenium.find_element_by_xpath("/html/body/fieldset/table/tbody/tr[2]/td[1]").text
        table_person = selenium.find_element_by_xpath("/html/body/fieldset/table/tbody/tr[2]/td[2]").text
        table_email = selenium.find_element_by_xpath("/html/body/fieldset/table/tbody/tr[2]/td[3]").text
        table_dateTime = selenium.find_element_by_xpath("/html/body/fieldset/table/tbody/tr[2]/td[4]").text

        # ----------------------------------------------------------------------------------------------------------- #
        # Asserts
        ## company
        self.assertEqual(table_company, 'Selenium company')
        ## person
        self.assertEqual(table_person, 'Selenium')
        ## email
        self.assertEqual(table_email, 'selenium@selenium.com')
        ## dateTime
        self.assertTrue(self.dateTime_stamp in table_dateTime)

    @pytest.mark.run(order=3)
    def test_user_log(self):
        """
                This test checks the user log view function

                :return:
                """

        selenium = self.driver

        # Choose start URL
        selenium.get("http://127.0.0.1:8000/")

        # ----------------------------------------------------------------------------------------------------------- #
        # Login
        ## Find elements
        user_email = selenium.find_element_by_id('id_username')
        user_password = selenium.find_element_by_id('id_password')

        submit = selenium.find_element_by_id('login')

        ## Populate elements form
        user_email.send_keys('office@office.com')
        user_password.send_keys('office')

        ## Submit form
        submit.send_keys(Keys.RETURN)

        # ----------------------------------------------------------------------------------------------------------- #
        # Direct to "View user logs"
        ## Find link and click
        button = selenium.find_element_by_xpath("//*[contains(text(), 'View user logs')]")
        button.click()

        # ----------------------------------------------------------------------------------------------------------- #
        # fill out "log filter" page
        ## Find select company option
        select = Select(selenium.find_element_by_name('company_list'))
        select.select_by_visible_text('Selenium company')
        ## Click filter
        button = selenium.find_element_by_xpath("/html/body/fieldset/form[1]/input[2]")
        button.submit()

        ## Find select user option
        select = Select(selenium.find_element_by_name('user_list'))
        select.select_by_visible_text('Selenium')
        ## Click choose user
        button = selenium.find_element_by_xpath("/html/body/fieldset/form[2]/input[2]")
        button.click()

        selenium.implicitly_wait(2)

        ## Find select facility option
        select = Select(selenium.find_element_by_name('facility_list'))
        select.select_by_visible_text('Selenium facility')
        ## Click choose facility
        button = selenium.find_element_by_xpath("/html/body/fieldset/form[3]/input[2]")
        button.submit()

        # ----------------------------------------------------------------------------------------------------------- #
        # extract table values
        time.sleep(1)
        table_facility = selenium.find_element_by_xpath("/html/body/fieldset/table/tbody/tr[2]/td[1]").text
        table_dateTime = selenium.find_element_by_xpath("/html/body/fieldset/table/tbody/tr[2]/td[2]").text

        # ----------------------------------------------------------------------------------------------------------- #
        # Asserts
        ## facility
        self.assertEqual(table_facility, 'Selenium facility')
        ## dateTime
        self.assertTrue(self.dateTime_stamp in table_dateTime)

    @pytest.mark.run(order=4)
    def test_delete_log(self):
        """
        This test deletes the log through the admin user site

        :return:
        """
        selenium = self.driver

        # Choose start URL
        selenium.get("http://127.0.0.1:8000/")

        # ----------------------------------------------------------------------------------------------------------- #
        # Login
        ## Find elements
        user_email = selenium.find_element_by_id('id_username')
        user_password = selenium.find_element_by_id('id_password')

        submit = selenium.find_element_by_id('login')

        ## Populate elements form
        user_email.send_keys('admin@admin.com')
        user_password.send_keys('admin')

        ## Submit form
        submit.send_keys(Keys.RETURN)

        # ----------------------------------------------------------------------------------------------------------- #
        # Direct to "Logss"
        ## Find "logs" link and click
        button = selenium.find_element_by_xpath("//*[contains(text(), 'Logss')]")
        button.click()

        ## Find "checkbox" link and click
        checkbox = selenium.find_element_by_id('action-toggle')
        checkbox.click()

        ## Find select option
        select = Select(selenium.find_element_by_name('action'))
        select.select_by_visible_text('Delete selected logss')

        ## Press "GO"
        button = selenium.find_element_by_xpath("//*[contains(text(), 'Go')]")
        button.click()

        ## Press "Yes"
        button = selenium.find_element_by_xpath("/html/body/div/div[3]/div/div[1]/form/div/input[4]")
        button.submit()

        # ----------------------------------------------------------------------------------------------------------- #
        # Assert log object
        self.assertTrue('Logss object' not in selenium.page_source)

    def tearDown(self):
        """
        This function "cleans up" selenium by closing the driver

        :return:
        """
        self.driver.close()


class FacilityAddEditRemoveTestCase(unittest.TestCase):
    """
    Class for testing facility add/edit/remove functionality

    Methods
    -------
    setUp(self):
    test_add_facility(self):
    test_edit_facility(self):
    test_remove_facility(self):
    tearDown(self):
    """

    def setUp(self):
        """
        This function sets up the driver

        :return:
        """
        self.driver = webdriver.Chrome()

    @pytest.mark.run(order=1)
    def test_add_facility(self):
        """
        This test checks the facility add function

        :return:
        """

        selenium = self.driver

        # Choose start URL
        selenium.get("http://127.0.0.1:8000/")

        # ----------------------------------------------------------------------------------------------------------- #
        # Login
        ## Find elements
        user_email = selenium.find_element_by_id('id_username')
        user_password = selenium.find_element_by_id('id_password')

        submit = selenium.find_element_by_id('login')

        ## Populate elements form
        user_email.send_keys('office@office.com')
        user_password.send_keys('office')

        ## Submit form
        submit.send_keys(Keys.RETURN)

        # ----------------------------------------------------------------------------------------------------------- #
        # Direct to "Add facility"
        ## Find link and click
        button = selenium.find_element_by_xpath("//*[contains(text(), 'Add/Edit/Remove facility')]")
        button.click()

        ## Find link and click
        button = selenium.find_element_by_xpath("//*[contains(text(), 'Add facility')]")
        button.click()

        # ----------------------------------------------------------------------------------------------------------- #
        # Fill out page
        ## Find elements
        name = selenium.find_element_by_id('name')
        adress = selenium.find_element_by_id('location')
        owner = selenium.find_element_by_id('owner')
        key = selenium.find_element_by_id('key')

        submit = selenium.find_element_by_xpath("/html/body/fieldset/form/table/tbody/tr[5]/td/button")

        ## Populate elements form
        name.send_keys('Selenium facility')
        adress.send_keys('Selenium road')
        owner.send_keys('Selenium')
        key.send_keys('1234')

        ## Submit form
        submit.send_keys(Keys.RETURN)

        #Assert
        self.assertEqual('http://127.0.0.1:8000/office_user_home/facility/', selenium.current_url)

        # ----------------------------------------------------------------------------------------------------------- #

    @pytest.mark.run(order=2)
    def test_edit_facility(self):
        """
        This test checks the facility edit function

        :return:
        """

        selenium = self.driver

        # Choose start URL
        selenium.get("http://127.0.0.1:8000/")

        # ----------------------------------------------------------------------------------------------------------- #
        # Login
        ## Find elements
        user_email = selenium.find_element_by_id('id_username')
        user_password = selenium.find_element_by_id('id_password')

        submit = selenium.find_element_by_id('login')

        ## Populate elements form
        user_email.send_keys('office@office.com')
        user_password.send_keys('office')

        ## Submit form
        submit.send_keys(Keys.RETURN)

        # ----------------------------------------------------------------------------------------------------------- #
        # Direct to "Edit facility"
        ## Find link and click
        button = selenium.find_element_by_xpath("//*[contains(text(), 'Add/Edit/Remove facility')]")
        button.click()

        ## Find link and click
        button = selenium.find_element_by_xpath("//*[contains(text(), 'Edit facility')]")
        button.click()

        # ----------------------------------------------------------------------------------------------------------- #
        # fill out "facility filter" page
        ## Find select location option
        select = Select(selenium.find_element_by_name('location_list'))
        select.select_by_visible_text('Selenium road')
        ## Click filter
        button = selenium.find_element_by_xpath("/html/body/fieldset/form[1]/input[2]")
        button.submit()

        ## Find select location option
        select = Select(selenium.find_element_by_name('names_list'))
        select.select_by_visible_text('Selenium facility')
        ## Click view facility
        button = selenium.find_element_by_xpath("/html/body/fieldset/form[2]/input[2]")
        button.submit()

        # ----------------------------------------------------------------------------------------------------------- #
        # Fill out page
        ## Find elements
        selenium.find_element_by_id('name').clear()
        name = selenium.find_element_by_id('name')
        selenium.find_element_by_id('location').clear()
        location = selenium.find_element_by_id('location')
        selenium.find_element_by_id('owner').clear()
        owner = selenium.find_element_by_id('owner')

        submit = selenium.find_element_by_xpath("/html/body/fieldset/form/table/tbody/tr[5]/td/button")

        ## Populate elements form
        name.send_keys('Selenium facility 2')
        location.send_keys('Selenium road 2')
        owner.send_keys('Selenium 2')

        ## Submit form
        submit.send_keys(Keys.RETURN)

        # ----------------------------------------------------------------------------------------------------------- #
        # assert

        ## fill out "facility filter" page
        ### Find select location option
        select = Select(selenium.find_element_by_name('location_list'))
        select.select_by_visible_text('Selenium road 2')
        ### Click filter
        button = selenium.find_element_by_xpath("/html/body/fieldset/form[1]/input[2]")
        button.submit()

        ### Find select location option
        select = Select(selenium.find_element_by_name('names_list'))
        select.select_by_visible_text('Selenium facility 2')
        ### Click view facility
        button = selenium.find_element_by_xpath("/html/body/fieldset/form[2]/input[2]")
        button.submit()

        ## extract table values
        time.sleep(1)
        table_name = selenium.find_element_by_id('name')
        table_location = selenium.find_element_by_id('location')
        table_owner = selenium.find_element_by_id('owner')

        ## name
        self.assertEqual(table_name.get_attribute('value'), 'Selenium facility 2')
        ## location
        self.assertEqual(table_location.get_attribute('value'), 'Selenium road 2')
        ## owner
        self.assertEqual(table_owner.get_attribute('value'), 'Selenium 2')

    @pytest.mark.run(order=3)
    def test_remove_facility(self):
        """
        This test checks the facility remove function

        :return:
        """

        selenium = self.driver

        # Choose start URL
        selenium.get("http://127.0.0.1:8000/")

        # ----------------------------------------------------------------------------------------------------------- #
        # Login
        ## Find elements
        user_email = selenium.find_element_by_id('id_username')
        user_password = selenium.find_element_by_id('id_password')

        submit = selenium.find_element_by_id('login')

        ## Populate elements form
        user_email.send_keys('office@office.com')
        user_password.send_keys('office')

        ## Submit form
        submit.send_keys(Keys.RETURN)

        # ----------------------------------------------------------------------------------------------------------- #
        # Direct to "Remove facility"
        ## Find link and click
        button = selenium.find_element_by_xpath("//*[contains(text(), 'Add/Edit/Remove facility')]")
        button.click()

        ## Find link and click
        button = selenium.find_element_by_xpath("//*[contains(text(), 'Remove facility')]")
        button.click()

        # ----------------------------------------------------------------------------------------------------------- #
        # find selenium facility
        ## Find select location option
        select = Select(selenium.find_element_by_name('location_list'))
        select.select_by_visible_text('Selenium road 2')
        ## Click filter
        button = selenium.find_element_by_xpath("/html/body/fieldset/form[1]/input[2]")
        button.submit()

        ## Find select location option
        select = Select(selenium.find_element_by_name('names_list'))
        select.select_by_visible_text('Selenium facility 2')
        ## Click filter
        button = selenium.find_element_by_xpath("/html/body/fieldset/form[2]/input[2]")
        button.submit()

        # ----------------------------------------------------------------------------------------------------------- #
        # Remove facility
        ## Assert correct option chosen
        fac_name = selenium.find_element_by_xpath("/html/body/fieldset/form/table/tbody/tr[1]/td[2]").text
        self.assertEqual(fac_name, 'Selenium facility 2')

        ## Find link and click
        button = selenium.find_element_by_xpath("/html/body/fieldset/form/table/tbody/tr[5]/td/button")
        button.submit()

        self.assertEqual('http://127.0.0.1:8000/office_user_home/facility/facility_remove_filter/', selenium.current_url)

    def tearDown(self):
        """
        This function "cleans up" selenium by closing the driver

        :return:
        """
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
