import unittest

import pytest
from py import test
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from website.models import *
from selenium.webdriver.support.ui import Select


class LoginTestCase(unittest.TestCase):
    """
    class for testing login redirects

    Methods
    -------
    setUp(self):
        This function sets up the driver

    test_login_field(self):
        This function asserts the redirect for field user login

    test_login_office(self):
        This function asserts the redirect for office user login

    test_login_admin(self):
        This function asserts the redirect for admin user login

    tearDown(self):
        This function "cleans up" selenium by closing the driver
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
        # Create the selenium user
        submit = selenium.find_element_by_id('sign_up')
        # Populate elements form
        create_user_code.send_keys(cuc.code)
        user_email.send_keys('selenium@selenium.com')
        user_name.send_keys('selenium')
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
        user_email2.send_keys('selenium@selenium.com')
        user_password2.send_keys('testbruger')

        # Login with new user
        submit2.send_keys(Keys.RETURN)

        # Expected results
        result_url = 'http://127.0.0.1:8000/field_user_home/'

        # Check result
        self.assertEqual(result_url, selenium.current_url)

    @pytest.mark.run(order=2)
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
        select.select_by_visible_text('selenium')
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

    @pytest.mark.run(order=3)
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

    @pytest.mark.run(order=1)
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

    def tearDown(self):
        """
        This function "cleans up" selenium by closing the driver

        :return:
        """
        self.driver.close()


class OfficePersonalInfoAndAccessTestCase(unittest.TestCase):
    """
    Must have to work:
    - a user named "test" with email "test@test.com"
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


if __name__ == "__main__":
    unittest.main()
