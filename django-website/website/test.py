import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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



if __name__ == "__main__":
    unittest.main()
