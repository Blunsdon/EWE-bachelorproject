import datetime
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import pytest
from website.models import *
import time
import requests
import json


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


@pytest.mark.django_db(transaction=True)
class CreateEditDeleteUserTestCase(unittest.TestCase):
    """
    class for testing
    -"Create user" landing page
    -"Create user" functionality
    -"Edit other users" functionality
    -"Delete users" functionality
    Methods
    -------
    """

    def setUp(self):
        """
        This function sets up the driver
        :return:
        """
        self.driver = webdriver.Chrome()

    def test_create_user_lp(self):
        """
        This test test's the functionality of create user landing page
        :return:
        """
        selenium = self.driver

        # Choose start Url
        selenium.get("http://127.0.0.1:8000/")
        # Find create_user id
        submit = selenium.find_element_by_id('create_user')
        # Submit form
        submit.click()
        # Test assert Expected URL results
        result_url = 'http://127.0.0.1:8000/create_user/'
        # Check result
        self.assertEqual(result_url, selenium.current_url)

    @pytest.mark.run(order=1)
    def test_create_user(self):
        """
        This function tests the creation of a user by
        login to the new user that is created
        """
        selenium = self.driver
        # Choose start Url
        selenium.get("http://127.0.0.1:8000/create_user/")
        # Get create user code from database
        c = CreateUserCode(code='1')
        c.save()
        cuc = CreateUserCode.objects.get(id=1)
        # Find elements
        create_user_code = selenium.find_element_by_id('CreateUserCode')
        user_email = selenium.find_element_by_id('id_email')
        user_name = selenium.find_element_by_id('id_name')
        phone_number = selenium.find_element_by_id('id_phoneNumber')
        company = selenium.find_element_by_id('id_company')
        user_password = selenium.find_element_by_id('id_password1')
        user_password2 = selenium.find_element_by_id('id_password2')
        # Create the test user
        submit = selenium.find_element_by_id('sign_up')
        # Populate elements form
        create_user_code.send_keys(cuc.code)
        user_email.send_keys('test@test.com')
        user_name.send_keys('test')
        phone_number.send_keys('69854732')
        company.send_keys('test')
        user_password.send_keys('testbruger')
        user_password2.send_keys('testbruger')
        # Submit form
        submit.send_keys(Keys.RETURN)

        # Find elements
        user_email2 = selenium.find_element_by_id('id_username')
        user_password2 = selenium.find_element_by_id('id_password')
        submit2 = selenium.find_element_by_id('login')
        # Populate elements
        user_email2.send_keys('test@test.com')
        user_password2.send_keys('testbruger')

        # Login with new user
        submit2.send_keys(Keys.RETURN)

        # Expected results
        result_url = 'http://127.0.0.1:8000/field_user_home/'

        # Check result
        self.assertEqual(result_url, selenium.current_url)

    @pytest.mark.run(order=4)
    def test_edit_other_user(self):
        """
        This function tests the edit functionality of other user from office user type
        """
        selenium = self.driver
        # Choose start Url
        selenium.get("http://127.0.0.1:8000/accounts/login/")

        # Find elements
        user_email = selenium.find_element_by_id('id_username')
        user_password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_id('login')
        # Populate elements
        user_email.send_keys('office@office.com')
        user_password.send_keys('office')
        # Login with office user
        submit.send_keys(Keys.RETURN)
        # Expected results
        result_url = 'http://127.0.0.1:8000/office_user_home/'
        # Check result
        self.assertEqual(result_url, selenium.current_url)

        # Find elements
        submit_edit_user = selenium.find_element_by_id('edit_user')
        # Go to edit user
        submit_edit_user.click()
        # Expected results
        result_url = 'http://127.0.0.1:8000/office_user_home/office_edit_user/'
        # Check result
        self.assertEqual(result_url, selenium.current_url)

        # Select in dropdown
        select = Select(selenium.find_element_by_name('users_list'))
        select.select_by_visible_text('test')
        button = selenium.find_element_by_xpath("/html/body/fieldset/form[2]/input[2]")
        button.click()

        # Edit user
        user_name = selenium.find_element_by_id('name')
        user_company = selenium.find_element_by_id('company')
        user_phonenumber = selenium.find_element_by_id('phoneNumber')
        user_email_edit = selenium.find_element_by_id('email')
        accept_edits = selenium.find_element_by_id('accept_edits')
        # Clear values
        selenium.find_element_by_id('name').clear()
        selenium.find_element_by_id('company').clear()
        selenium.find_element_by_id('phoneNumber').clear()
        selenium.find_element_by_id('email').clear()
        # Populate elements
        user_name.send_keys('selenium2')
        user_company.send_keys('selenium')
        user_phonenumber.send_keys('4242424242')
        user_email_edit.send_keys('selenium2@selenium.com')
        accept_edits.send_keys(Keys.RETURN)
        # Expected results
        result_url = 'http://127.0.0.1:8000/office_user_home/office_edit_user/'
        # Check result
        self.assertEqual(result_url, selenium.current_url)

    @pytest.mark.run(order=6)
    def test_delete_other_user(self):
        """
        This function tests the delete functionality of other user from office user type
        """
        selenium = self.driver
        # Choose start Url
        selenium.get("http://127.0.0.1:8000/accounts/login/")

        # Find elements
        user_email = selenium.find_element_by_id('id_username')
        user_password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_id('login')
        # Populate elements
        user_email.send_keys('office@office.com')
        user_password.send_keys('office')
        # Login with office user
        submit.send_keys(Keys.RETURN)
        # Expected results
        result_url = 'http://127.0.0.1:8000/office_user_home/'
        # Check result
        self.assertEqual(result_url, selenium.current_url)

        # Find elements
        submit_edit_user = selenium.find_element_by_id('edit_user')
        # Go to edit user
        submit_edit_user.click()
        # Expected results
        result_url = 'http://127.0.0.1:8000/office_user_home/office_edit_user/'
        # Check result
        self.assertEqual(result_url, selenium.current_url)

        # Select in dropdown
        select = Select(selenium.find_element_by_name('users_list'))
        select.select_by_visible_text('selenium2')
        button = selenium.find_element_by_xpath("/html/body/fieldset/form[2]/input[2]")
        button.click()

        # Delete user
        delete_user = selenium.find_element_by_name('delete_user')
        delete_user.click()

        # Expected results
        result_url = 'http://127.0.0.1:8000/office_user_home/office_edit_user/'
        # Check result
        self.assertEqual(result_url, selenium.current_url)

    def tearDown(self):
        """
        This function "cleans up" selenium by closing the driver
        :return:
        """
        self.driver.close()


class EditFacilityAccessTestCase(unittest.TestCase):
    """
    class for testing
    -"Edit facility access" landing page
    -"Give access" landing page
    -"Remove access" landing page
    -"Give access" functionality
    -"Remove access" functionality
    Methods
    -------
    """

    def setUp(self):
        """
        This function sets up the driver
        :return:
        """
        self.driver = webdriver.Chrome()

    def test_edit_facility_lp(self):
        """
        This test test's the
        - facility access landing page
        - Give access landing page
        - Remove access landing page
        :return:
        """
        selenium = self.driver
        # Choose start Url
        selenium.get("http://127.0.0.1:8000/accounts/login/")
        # Find elements
        user_email = selenium.find_element_by_id('id_username')
        user_password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_id('login')
        # Populate elements
        user_email.send_keys('office@office.com')
        user_password.send_keys('office')
        # Login with office user
        submit.send_keys(Keys.RETURN)
        # Expected results
        result_url = 'http://127.0.0.1:8000/office_user_home/'
        # Check result
        self.assertEqual(result_url, selenium.current_url)
        # Go to facility access page
        edit_facility_access = selenium.find_element_by_xpath("/html/body/button[4]")
        edit_facility_access.click()
        # Expected results
        result_url = 'http://127.0.0.1:8000/office_user_home/facility_access/'
        # Check result
        self.assertEqual(result_url, selenium.current_url)
        # Go to Give access page
        give_facility_access = selenium.find_element_by_xpath("/html/body/button[1]")
        give_facility_access.click()
        # Expected results
        result_url = 'http://127.0.0.1:8000/office_user_home/facility_access/facility_access_give_filter/'
        # Check result
        self.assertEqual(result_url, selenium.current_url)
        # Go back to facility access page
        back = selenium.find_element_by_xpath("/html/body/fieldset/button")
        back.click()
        # Expected results
        result_url = 'http://127.0.0.1:8000/office_user_home/facility_access/'
        # Check result
        self.assertEqual(result_url, selenium.current_url)
        # Go to remove access page
        remove_facility_access = selenium.find_element_by_xpath("/html/body/button[2]")
        remove_facility_access.click()
        # Expected results
        result_url = 'http://127.0.0.1:8000/office_user_home/facility_access/facility_access_remove/'
        # Check result
        self.assertEqual(result_url, selenium.current_url)

    @pytest.mark.run(order=2)
    def test_give_access(self):
        """
        This test test's the
        - Give access functionality from office user type
        :return:
        """
        selenium = self.driver
        # Choose start Url
        selenium.get("http://127.0.0.1:8000/accounts/login/")
        # Find elements
        user_email = selenium.find_element_by_id('id_username')
        user_password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_id('login')
        # Populate elements
        user_email.send_keys('office@office.com')
        user_password.send_keys('office')
        # Login with office user
        submit.send_keys(Keys.RETURN)
        # Expected results
        result_url = 'http://127.0.0.1:8000/office_user_home/'
        # Check result
        self.assertEqual(result_url, selenium.current_url)

        # Direct to "Add facility"
        button = selenium.find_element_by_xpath("//*[contains(text(), 'Add/Edit/Remove facility')]")
        button.click()
        ## Find link and click
        button = selenium.find_element_by_xpath("//*[contains(text(), 'Add facility')]")
        button.click()
        ## Find elements
        name = selenium.find_element_by_id('name')
        adress = selenium.find_element_by_id('location')
        owner = selenium.find_element_by_id('owner')
        key = selenium.find_element_by_id('key')
        submit = selenium.find_element_by_xpath("/html/body/fieldset/form/table/tbody/tr[5]/td/button")
        ## Populate elements form
        name.send_keys('test fac1')
        adress.send_keys('Selenium road')
        owner.send_keys('Selenium')
        key.send_keys('1234')
        ## Submit form
        submit.send_keys(Keys.RETURN)
        # Assert
        self.assertEqual('http://127.0.0.1:8000/office_user_home/facility/', selenium.current_url)
        back_from_add = selenium.find_element_by_xpath("/html/body/fieldset/button[4]")
        back_from_add.click()

        # Go to facility access page
        edit_facility_access = selenium.find_element_by_xpath("/html/body/button[4]")
        edit_facility_access.click()
        # Expected results
        result_url = 'http://127.0.0.1:8000/office_user_home/facility_access/'
        # Check result
        self.assertEqual(result_url, selenium.current_url)
        # Go to Give access page
        give_facility_access = selenium.find_element_by_xpath("/html/body/button[1]")
        give_facility_access.click()
        # Expected results
        result_url = 'http://127.0.0.1:8000/office_user_home/facility_access/facility_access_give_filter/'
        # Check result
        self.assertEqual(result_url, selenium.current_url)

        # find a facility to get access from from a dropdown
        select = Select(selenium.find_element_by_name('names_list'))
        select.select_by_visible_text('test fac1')
        button = selenium.find_element_by_xpath("/html/body/fieldset/form[2]/input[2]")
        button.click()
        # find a user to give access too from a dropdown
        select_user = Select(selenium.find_element_by_name('user'))
        select_user.select_by_visible_text('test (test@test.com)')
        # Get start date and end date
        start_date = selenium.find_element_by_name('timer_start')
        end_date = selenium.find_element_by_name('timer')
        # Clear values
        selenium.find_element_by_name('timer_start').clear()
        selenium.find_element_by_name('timer').clear()
        # Populate elements
        start_date.send_keys('15.12.2021')
        end_date.send_keys('18.12.2021')
        # Give access to "test fac1" to the user "test"
        give_access = selenium.find_element_by_xpath("/html/body/fieldset/form/table/tbody/tr[6]/td/button")
        give_access.send_keys(Keys.RETURN)
        # Expected results
        result_url = 'http://127.0.0.1:8000/office_user_home/facility_access/'
        # Check result
        self.assertEqual(result_url, selenium.current_url)

    @pytest.mark.run(order=3)
    def test_remove_access(self):
        """
        This test test's the
        - Remove access functionality from office user type
        :return:
        """
        selenium = self.driver
        # Choose start Url
        selenium.get("http://127.0.0.1:8000/accounts/login/")
        # Find elements
        user_email = selenium.find_element_by_id('id_username')
        user_password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_id('login')
        # Populate elements
        user_email.send_keys('office@office.com')
        user_password.send_keys('office')
        # Login with office user
        submit.send_keys(Keys.RETURN)
        # Expected results
        result_url = 'http://127.0.0.1:8000/office_user_home/'
        # Check result
        self.assertEqual(result_url, selenium.current_url)
        # Go to facility access page
        edit_facility_access = selenium.find_element_by_xpath("/html/body/button[4]")
        edit_facility_access.click()
        # Expected results
        result_url = 'http://127.0.0.1:8000/office_user_home/facility_access/'
        # Check result
        self.assertEqual(result_url, selenium.current_url)
        # Go to Remove access page
        remove_facility_access = selenium.find_element_by_xpath("/html/body/button[2]")
        remove_facility_access.click()
        # Expected results
        result_url = 'http://127.0.0.1:8000/office_user_home/facility_access/facility_access_remove/'
        # Check result
        self.assertEqual(result_url, selenium.current_url)
        # find a facility to remove access from from a dropdown
        select = Select(selenium.find_element_by_name('facility'))
        select.select_by_visible_text('test fac1')
        button = selenium.find_element_by_xpath("/html/body/fieldset/form/input[2]")
        button.click()
        # find a user to give access too from a dropdown
        select_user = Select(selenium.find_element_by_name('user'))
        select_user.select_by_visible_text('test (test@test.com)')
        # Give access to "test fac1" to the user "test"
        give_access = selenium.find_element_by_xpath("/html/body/fieldset/form/input[2]")
        give_access.send_keys(Keys.RETURN)
        # Expected results
        result_url = 'http://127.0.0.1:8000/office_user_home/facility_access/facility_access_remove/'
        # Check result
        self.assertEqual(result_url, selenium.current_url)
        back = selenium.find_element_by_xpath("/html/body/fieldset/button")
        back.click()
        # Expected results
        result_url = 'http://127.0.0.1:8000/office_user_home/facility_access/'
        # Check result
        self.assertEqual(result_url, selenium.current_url)

        # Go back to home page for office user
        back_from_facility_access = selenium.find_element_by_xpath("/html/body/button[3]")
        back_from_facility_access.click()
        # Direct to "Remove facility"
        button = selenium.find_element_by_xpath("//*[contains(text(), 'Add/Edit/Remove facility')]")
        button.click()
        ## Find link and click
        button = selenium.find_element_by_xpath("//*[contains(text(), 'Remove facility')]")
        button.click()
        # find test fac1 facility
        select = Select(selenium.find_element_by_name('names_list'))
        select.select_by_visible_text('test fac1')
        ## Click filter
        button = selenium.find_element_by_xpath("/html/body/fieldset/form[2]/input[2]")
        button.submit()
        # Remove facility
        fac_name = selenium.find_element_by_xpath("/html/body/fieldset/form/table/tbody/tr[1]/td[2]").text
        self.assertEqual(fac_name, 'test fac1')
        ## Find "Remove facility" link and click
        button = selenium.find_element_by_xpath("/html/body/fieldset/form/table/tbody/tr[5]/td/button")
        button.submit()
        self.assertEqual('http://127.0.0.1:8000/office_user_home/facility/facility_remove_filter/',
                         selenium.current_url)

    def tearDown(self):
        """
        This function "cleans up" selenium by closing the driver
        :return:
        """
        self.driver.close()


class OfficePersonalInfoAndAccessTestCase(unittest.TestCase):
    """
    Must have to work:
    - a facility named "test fac1" in Database
    class for testing
    -"Personal info" landing page for office user
    -"Facility access" landing page for office user
    -"Personal info" functionality
    Methods
    -------
    """

    def setUp(self):
        """
        This function sets up the driver
        :return:
        """
        self.driver = webdriver.Chrome()

    def test_personal_info_lp(self):
        """
        This test test's the
        - Personal info landing page
        :return:
        """
        selenium = self.driver
        # Choose start Url
        selenium.get("http://127.0.0.1:8000/accounts/login/")
        # Find elements
        user_email = selenium.find_element_by_id('id_username')
        user_password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_id('login')
        # Populate elements
        user_email.send_keys('office@office.com')
        user_password.send_keys('office')
        # Login with office user
        submit.send_keys(Keys.RETURN)
        # Expected results
        result_url = 'http://127.0.0.1:8000/office_user_home/'
        # Check result
        self.assertEqual(result_url, selenium.current_url)
        # Go to personal info page
        personal_info = selenium.find_element_by_xpath("/html/body/button[6]")
        personal_info.click()
        # Expected results
        result_url = 'http://127.0.0.1:8000/office_user_home/office_user_info/'
        # Check result
        self.assertEqual(result_url, selenium.current_url)
        # Go back
        personal_info_back = selenium.find_element_by_xpath("/html/body/fieldset/button")
        personal_info_back.click()
        # Expected results
        result_url = 'http://127.0.0.1:8000/office_user_home/'
        # Check result
        self.assertEqual(result_url, selenium.current_url)

    def test_facility_access_lp(self):
        """
        This test test's the
        - Facility access landing page
        :return:
        """
        selenium = self.driver
        # Choose start Url
        selenium.get("http://127.0.0.1:8000/accounts/login/")
        # Find elements
        user_email = selenium.find_element_by_id('id_username')
        user_password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_id('login')
        # Populate elements
        user_email.send_keys('office@office.com')
        user_password.send_keys('office')
        # Login with office user
        submit.send_keys(Keys.RETURN)
        # Expected results
        result_url = 'http://127.0.0.1:8000/office_user_home/'
        # Check result
        self.assertEqual(result_url, selenium.current_url)
        # Go to Facility access page
        facility_access = selenium.find_element_by_xpath("/html/body/button[7]")
        facility_access.click()
        # Expected results
        result_url = 'http://127.0.0.1:8000/office_user_home/office_user_access/'
        # Check result
        self.assertEqual(result_url, selenium.current_url)
        # Go back
        facility_access_back = selenium.find_element_by_xpath("/html/body/button")
        facility_access_back.click()
        # Expected results
        result_url = 'http://127.0.0.1:8000/office_user_home/'
        # Check result
        self.assertEqual(result_url, selenium.current_url)

    def test_edit_personal_info(self):
        """
        This test test's the
        - Give access functionality from office user type
        :return:
        """
        selenium = self.driver
        # Choose start Url
        selenium.get("http://127.0.0.1:8000/accounts/login/")
        # Find elements
        user_email = selenium.find_element_by_id('id_username')
        user_password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_id('login')
        # Populate elements
        user_email.send_keys('office@office.com')
        user_password.send_keys('office')
        # Login with office user
        submit.send_keys(Keys.RETURN)
        # Expected results
        result_url = 'http://127.0.0.1:8000/office_user_home/'
        # Check result
        self.assertEqual(result_url, selenium.current_url)
        # Go to personal info page
        personal_info = selenium.find_element_by_xpath("/html/body/button[6]")
        personal_info.click()
        # Expected results
        result_url = 'http://127.0.0.1:8000/office_user_home/office_user_info/'
        # Check result
        self.assertEqual(result_url, selenium.current_url)

        # Get phone number and email elements
        phonenumber = selenium.find_element_by_name('phoneNumber')
        email = selenium.find_element_by_name('email')
        # Clear values
        selenium.find_element_by_name('phoneNumber').clear()
        selenium.find_element_by_name('email').clear()
        # Populate elements
        phonenumber.send_keys('4242424242')
        email.send_keys('office2@office.com')
        # Edit user with new email and phone number
        give_access = selenium.find_element_by_xpath("/html/body/fieldset/form/table/tbody/tr[4]/td[3]/button")
        give_access.send_keys(Keys.RETURN)
        # Expected results
        result_url = 'http://127.0.0.1:8000/office_user_home/'
        # Check result
        self.assertEqual(result_url, selenium.current_url)

        # Clean office user up
        # Go to personal info page
        personal_info = selenium.find_element_by_xpath("/html/body/button[6]")
        personal_info.click()
        # Expected results
        result_url = 'http://127.0.0.1:8000/office_user_home/office_user_info/'
        # Check result
        self.assertEqual(result_url, selenium.current_url)

        # Get phone number and email elements
        phonenumber = selenium.find_element_by_name('phoneNumber')
        email = selenium.find_element_by_name('email')
        print(phonenumber)
        print(email)
        # Clear values
        selenium.find_element_by_name('phoneNumber').clear()
        selenium.find_element_by_name('email').clear()
        # Populate elements
        phonenumber.send_keys('4242424242')
        email.send_keys('office@office.com')
        # Update user"
        give_access = selenium.find_element_by_xpath("/html/body/fieldset/form/table/tbody/tr[4]/td[3]/button")
        give_access.send_keys(Keys.RETURN)
        # Expected results
        result_url = 'http://127.0.0.1:8000/office_user_home/'
        # Check result
        self.assertEqual(result_url, selenium.current_url)

    def tearDown(self):
        """
        This function "cleans up" selenium by closing the driver
        :return:
        """
        self.driver.close()


class RAPITestCase(unittest.TestCase):

    def setUp(self):
        return None

    @pytest.mark.run(order=3)
    def test_curl_create(self):
        selenium = webdriver.Chrome()

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
        # Direct to "facilities" and create a test facility
        ## Find "Facilitiess" link and click
        button = selenium.find_element_by_xpath("//*[contains(text(), 'Facilitiess')]")
        button.click()

        ## Find "Add facilities" link and click
        button = selenium.find_element_by_xpath("//*[contains(text(), 'Add facilities')]")
        button.click()

        ## Find elements
        Name = selenium.find_element_by_id('id_name')
        Location = selenium.find_element_by_id('id_location')
        Owner = selenium.find_element_by_id('id_owner')
        Key = selenium.find_element_by_id('id_key')

        submit = selenium.find_element_by_name('_save')

        ## Populate elements form
        Name.send_keys('curl test fac')
        Location.send_keys('curl location')
        Owner.send_keys('curl')
        Key.send_keys('curl key')

        ## Submit form
        submit.send_keys(Keys.RETURN)

        # ----------------------------------------------------------------------------------------------------------- #
        # Direct to "join tables" and create a test jointable
        ## Find "Join tables" link and click
        button = selenium.find_element_by_xpath("//*[contains(text(), 'Join tables')]")
        button.click()

        ## Find "Add Join table" link and click
        button = selenium.find_element_by_xpath("//*[contains(text(), 'Add join table')]")
        button.click()

        ## Find elements
        select_fac = Select(selenium.find_element_by_id('id_facility'))
        select_fac.select_by_visible_text('curl test fac')
        select_user = Select(selenium.find_element_by_id('id_user'))
        select_user.select_by_visible_text('field@field.com')

        submit = selenium.find_element_by_name('_save')

        submit.submit()

        selenium.close()

    @pytest.mark.run(order=5)
    def test_RAPI_endpoints(self):
        # ----------------------------------------------------------------------------------------------------------- #
        # Test login endpoint
        ## structure request
        url = 'http://127.0.0.1:8000/api/auth/token/login/'
        payload = '{' \
                  '"email": "field@field.com",' \
                  '"password": "field"' \
                  '}'
        headers = {'Content-Type': 'application/json'}

        ## send request
        r = requests.post(url, data=payload, headers=headers)

        ## extract response payload
        response = r.json()
        token = response['auth_token']

        ## assert token
        self.assertTrue(isinstance(token, str))

        # ----------------------------------------------------------------------------------------------------------- #
        # Test facility list endpoint
        ## structure request
        url = 'http://127.0.0.1:8000/rest_api/key_api/'
        payload = '{\"userEmail\":\"field@field.com\"}'
        string = 'Token ' + str(token)
        headers = {'Content-Type':'application/json',
               'Authorization': 'Token {}'.format(token)}

        ## send request
        r = requests.post(url, data=payload, headers=headers)

        ## extract response payload
        response = r.json()
        list = response['list']

        ## assert response payload
        self.assertEqual(list[0][0], 'curl test fac')
        self.assertEqual(list[0][1], 'curl location')
        self.assertEqual(list[0][2], 'field@field.com')
        self.assertEqual(list[0][3], 'ewe2')
        self.assertEqual(list[0][4], 'field')

        # ----------------------------------------------------------------------------------------------------------- #
        # Test log + key endpoint
        ## structure request
        url = 'http://127.0.0.1:8000/rest_api/log_api/'
        payload = '{"facility":' \
                    '[{"name":"curl test fac"}],' \
                  '"log":' \
                    '[{"userName":"field"' \
                    ',"companyName":"ewe2",' \
                    '"dateTime":"2021-10-10T18:44:22",' \
                    '"userEmail":"field@field.com",' \
                    '"facilityName":"curl test fac",' \
                    '"facilityLocation":"curl location"}]}'
        string = 'Token ' + str(token)
        headers = {'Content-Type':'application/json',
               'Authorization': 'Token {}'.format(token)}

        ## send request
        r = requests.post(url, data=payload, headers=headers)

        ## extract response payload
        response = r.json()

        ## assert response payload
        self.assertEqual(response['status'], 'success')
        self.assertEqual(response['key'], 'curl key')

    @pytest.mark.run(order=6)
    def test_curl_delete(self):
        selenium = webdriver.Chrome()

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
        # Direct to "facilities" and delete all facilities
        ## Find "Facilitiess" link and click
        button = selenium.find_element_by_xpath("//*[contains(text(), 'Facilitiess')]")
        button.click()

        ## Find "checkbox" link and click
        checkbox = selenium.find_element_by_id('action-toggle')
        checkbox.click()

        ## Find select option
        select = Select(selenium.find_element_by_name('action'))
        select.select_by_visible_text('Delete selected facilitiess')

        ## Press "GO"
        button = selenium.find_element_by_xpath("//*[contains(text(), 'Go')]")
        button.click()

        ## Press "Yes"
        button = selenium.find_element_by_xpath("/html/body/div/div[3]/div/div[1]/form/div/input[4]")
        button.submit()

        selenium.close()


    def tearDown(self):
        return None


if __name__ == "__main__":
    unittest.main()
