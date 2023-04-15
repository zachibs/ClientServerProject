from src.servers.app_server import *
from db.database import *
import unittest


class appTestClass(unittest.TestCase):
    session = None

    def setUp(self):
        global session
        session = get_session()

    def tearDown(self):
        global session
        session.rollback()
        session.close()

    def test_add_country(self):
        data = {"name": "unitTestCountry", "population": 123456,
                "ethnicity":"test", "founding_year": 2023,
                "in_war": False}
        add_country_to_db(session, data)
        country = (get_country_by_name_from_db(session, {"name":"unitTestCountry"}))[1]
        self.assertEqual(country['name'],"unitTestCountry")
        self.assertEqual(country['population'],123456)
        self.assertEqual(country['ethnicity'],"test")
        self.assertEqual(country['founding_year'],2023)
        self.assertEqual(country['in_war'],False)

    def test_delete_country(self):
        data = {"name": "unitTestCountry", "population": 123456,
                "ethnicity":"test", "founding_year": 2023,
                "in_war": False}
        add_country_to_db(session, data)
        response = (delete_country_by_name(session, {"name":"unitTestCountry"}))[0]
        self.assertEqual(response,True)


if __name__ == '__main__':
    unittest.main()