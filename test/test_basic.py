import os
import unittest

from user_record_app import create_app, db

app = create_app("config.TestConfig")
BASE_URL = "http://127.0.0.1:5000"




class BasicTests(unittest.TestCase):
    """
    This class contains tests to test the core functionality of the application
    such as tests for adding a new user, display filtered data, and serializing
    and displaying data in different formats.
    """

    def setUp(self):
        """
        Sets up a test application to run tests on.
        Writes out database to user_record_app/test/test.db
        """
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["DEBUG"] = False

        db_path = os.path.join(os.path.dirname(__file__), "test.db")
        db_uri = "sqlite:///{}".format(db_path)
        app.config["SQLALCHEMY_DATABASE_URI"] = db_uri

        self.app = app.test_client()
        with app.app_context():
            db.create_all()

        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        """
        Tears down the database.
        """
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_invalid_page(self):
        """
        Tests if it errors when trying to access invalid page.
        """
        response = self.app.get("/INVALID")
        self.assertEqual(response.status_code, 404)

    def test_main_page(self):
        """
        Tests if the home page opens.
        """
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        """
        Tests if you can successfully create a user.
        """
        user_dict = {
            "city": "city",
            "first_name": "first_name",
            "last_name": "last_name",
            "phone_number": "phone_number",
            "province": "province",
            "street": "street"
        }
        response = self.app.post("{}/api/v1/users/create_user".format(BASE_URL), json=user_dict)

        self.assertEqual(response.status_code, 200)


    def test_display_text(self):
        """
        Tests if you can successfully display data in an text output format.
        """
        response = self.app.get("{}/api/v1/users/filter/text".format(BASE_URL))
        self.assertEqual(response.status_code, 200)

    def test_display_html(self):
        """
        Tests if you can successfully display data in an html output format.
        """
        response = self.app.get("{}/api/v1/users/filter/html".format(BASE_URL))
        self.assertEqual(response.status_code, 200)

    def test_invalid_display_format(self):
        """
        Tests if it errors give an invalid output format.
        """
        response = self.app.get("{}/api/v1/users/filter/INVALID_DISPLAY_TYPE".format(BASE_URL))
        self.assertEqual(response.status_code, 500)

    def test_display_all(self):
        """
        Tests if it can successfully display all data in the database.
        """
        response = self.app.get("{}/api/v1/users/all/text".format(BASE_URL))
        self.assertEqual(response.status_code, 200)

    def test_serialize_valid_format(self):
        """
        Tests if it can serialize data to json.
        """
        response = self.app.get("{}/api/v1/users/all/serialize/json".format(BASE_URL))
        self.assertEqual(response.status_code, 200)

    def test_serialize_invalid_format(self):
        """
        Tests if serializing fails when given an invalid output format.
        """
        response = self.app.get("{}/api/v1/users/all/serialize/invalid_format".format(BASE_URL))
        self.assertEqual(response.status_code, 500)

if __name__ == "__main__":
    unittest.main()
