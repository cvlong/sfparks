import unittest
import doctest
import mappingfunctions
# import server


# def load_tests(loader, tests, ignore):
#     """Includes doctests and file-based doctests.

#     Note: function name, 'load_tests', is required.
#     """

#     tests.addTests(doctest.DocTestSuite(server))
#     tests.addTests(doctest.DocFileSuite("tests.txt"))
#     return tests


class MyAppUnitTestCase(unittest.TestCase):
    """Unit tests: discrete code testing."""

#ADD SETUP/TEARDOWN
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

        response = mappingfunctions.format_origin(
        self.assert

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

    def test_round_num(self):

        response = mappingfunctions.round_num(1.3)
        self.assertEqual(response, 1.5)
       
        response = mappingfunctions.round_num(3.0)
        self.assertEqual(response, 3.0)

        response = mappingfunctions.round_num(4.1)
        self.assertEqual(response, 4.0)


class MyAppIntegrationTestCase(unittest.TestCase):
    """Integration tests: testing Flask server."""

    def setUp(self):
        print "(setUp ran)"
        self.client = server.app.test_client()
        server.app.config['TESTING'] = True
        server.app.config['DEBUG'] = False

    def tearDown(self):
        # Don't need to define this method.
        print "(tearDown ran)"

    def test_homepage(self):
        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Starting location', result.data)

    # # TODO: Change
    # def test_favorite_color_form(self):
    #     test_client = server.app.test_client()
    #     result = test_client.post('/fav_color', data={'color': 'blue'})
    #     self.assertIn('I like blue, too', result.data)


    # TODO: Change
    # def test_adder(self):
    #     result = self.client.get('/add-things?x=-1&y=1')
    #     self.assertEqual(result.data, "99")

    # TODO: Change
    # def test_query(self):
    #     result = self.client.get('/')
    #     self.assertIn('<h1>Test</h1>', result.data)


if __name__ == '__main__':
    unittest.main()
