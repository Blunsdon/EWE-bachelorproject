import unittest

import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from website.models import CreateUserCode


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


class EditUserTestCase(unittest.TestCase):
    """
    class for testing "Edit user" redirects, insertions and saving

    Methods
    -------

    """

    def setUp(self):
        """
        This function sets up the driver

        :return:
        """
        self.driver = webdriver.Chrome()

    def test_choose_user(self):
        """
        This test test's the editing of existing users functionality

        :return:
        """
        selenium = self.driver

        # Choose start Url
        selenium.get("http://127.0.0.1:8000/")

        # login:
        ## Find elements
        user_email = selenium.find_element_by_id('id_username')
        user_password = selenium.find_element_by_id('id_password')

        submit = selenium.find_element_by_id('login')

        ## Populate elements form
        user_email.send_keys('office@office.com')
        user_password.send_keys('office')

        ## Submit form
        submit.send_keys(Keys.RETURN)

        # Direct to "Edit user"
        ## Find element by text
        button = selenium.find_element_by_xpath("//*[contains(text(), 'Edit user')]")

        ## Click button
        button.click()

        ## Test assert
        ### Expected URL results
        result_url = 'http://127.0.0.1:8000/office_user_home/office_edit_user/'

        ### Check result
        self.assertEqual(result_url, selenium.current_url)


    def tearDown(self):
        """
        This function "cleans up" selenium by closing the driver

        :return:
        """
        self.driver.close()


@pytest.mark.django_db(True)
class CreateUserTestCase(unittest.TestCase):
    """
    class for testing "Create user" redirects, insertions and saving

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

    def test_create_user(self):
        """
        This function tests the creation of a user by
        login to the new user that is created
        """
        selenium = self.driver
        # Choose start Url
        selenium.get("http://127.0.0.1:8000/create_user/")
        # Get create user code from database
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


    def tearDown(self):
        """
        This function "cleans up" selenium by closing the driver

        :return:
        """
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
