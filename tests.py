import unittest
# from unittest import TestCase
import doctest
import server
# from server import app
import mappingfunctions


def load_tests(loader, tests, ignore):
    """Includes doctests and file-based doctests.

    Note: function name, 'load_tests', is required.
    """

    tests.addTests(doctest.DocTestSuite(server))
    tests.addTests(doctest.DocFileSuite("tests.txt"))
    return tests


class MyAppUnitTestCase(unittest.TestCase):
    """Unit tests: discrete code testing."""

    def setUp(self):
        print "(setUp ran)"
        self.client = server.app.test_client()
        server.app.config['TESTING'] = True
        server.app.config['DEBUG'] = False

        origin = (37.7887, -122.4116)

    def tearDown(self):
        # Don't need to define this method.
        print "(tearDown ran)"

    def test_format_origin(self):
        pass

        # response = mappingfunctions.format_origin(
        # self.assert

    def test_find_appx_dist(self):

        response = mappingfunctions.find_appx_dist(5, 'walking')
        self.assertEqual(response, 0.3)

        response = mappingfunctions.find_appx_dist(15, 'cycling')
        self.assertEqual(response, 3)

        response = mappingfunctions.find_appx_dist(20, 'walking')
        self.assertIsNotNone(response)

        response = mappingfunctions.find_appx_dist(20, 'cycling')
        self.assertEqual(response, 4)


    def test_find_close_parks(self):
        pass

    def test_add_routing_time(self):
        pass

    def test_format_routing_time(self):
        pass
        # response = mappingfunctions.format_routing_time(1.3)
        # self.assertEqual(response, 1.5)
       
        # response = mappingfunctions.format_routing_time(3.0)
        # self.assertEqual(response, 3.0)

        # response = mappingfunctions.format_routing_time(4.1)
        # self.assertEqual(response, 4.0)

## THIS IS THE SAME AS WHA'S BELOW: FlaskTestBasic
# class MyAppIntegrationTestCase(unittest.TestCase):
#     """Integration tests: testing Flask server."""

#     def setUp(self):
#         print "(setUp ran)"
#         self.client = server.app.test_client()
#         server.app.config['TESTING'] = True
#         server.app.config['DEBUG'] = False

#     def tearDown(self):
#         # Don't need to define this method.
#         print "(tearDown ran)"

#     def test_homepage(self):
#         result = self.client.get('/')
#         self.assertEqual(result.status_code, 200)
#         self.assertIn('Search SFparks', result.data)

#     # def test_about_page(self):
#     #     test_client = server.app.test_client()
#     #     result = test_client.post('/about')
#     #     self.assertIn('Flask', result.data)

#     def test_query(self):
#         test_client = server.app.test_client()
#         result = test_client.post('/query?origin=555+Market+St&time=5&routing=walking')
#         self.assertIn('100 Pine Street', result.data)

class FlaskTestsBasic(unittest.TestCase):
    """Flask tests."""

    def setUp(self):
        """Run before every Flask test."""


        app.config['TESTING'] = True # Show Flask errors that happen during tests
        self.client = app.test_client() # Get the Flask test client

    def test_homepage(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertIn('<h1>HELLO</h1>', result.data)
    
    def test_login(self):
        
        result = self.client.post("/login")
        self.assertEqual(result.status_code, 200)
        self.assertIn("<h3>Sign in</h3>", result.data)


class FlaskTestsDatabase(TestCase):
    """Flask tests that use the database."""
    
    #Create fake db in model and use that here
    #In model.py, connect_to_db need to set additional parameter
    #Use this to test queries from the db in server.py

    def setUp(self):
        """Run before every test."""
        
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Run at the end of every test."""

        db.session.close()
        db.drop_all()


    def test_parks(self):
        """Test park features."""

        result = self.client.get('/current-location.json')
        self.assertIn('', result.data)

    TODO: Change
    def test_departments_list(self):
        """Test departments page."""

        result = self.client.get("/departments")
        self.assertIn("Legal", result.data)


    TODO: Change
    def test_departments_details(self):
        """Test departments page."""

        result = self.client.get("/department/fin")
        self.assertIn("Phone: 555-1000", result.data)


    def test_login(self):
        """Test login page."""

        result = self.client.post("/login", 
                                  data={"user_id": "cvlong@gmail.com",
                                        "password": "123"},
                                  follow_redirects=True)
        self.assertIn("You're logged in", result.data)


class FlaskTestsLoggedIn(unittest.TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        server.app.config['TESTING'] = True
        server.app.config['SECRET_KEY'] = 'key'
        self.client = server.app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1


    def test_homepage(self):
        """Test login page."""

        result = self.client.get("/")
        self.assertIn("Sign out", result.data)
        self.assertNotIn("Sign in", result.data)

    def test_query_page(self):
        """Test query page."""

        data = "/query?origin=555+Market+St&time=5&routing=walking"

        result = self.client.get(data)
        self.assertIn("geojson_origin", result.data)
        self.assertIn("My Favorites", result.data)


if __name__ == '__main__':
    unittest.main()
