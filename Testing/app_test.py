import unittest
from app import app, db
from sqlalchemy import text

class TestDatabaseConnection(unittest.TestCase):
    def setUp(self):
        # Set up the application context
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        # Tear down the application context
        self.app_context.pop()

    def test_database_connection(self):
        # Test if we can successfully query the database
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM backgrounds LIMIT 1")).fetchall()
            self.assertIsInstance(result, list)  # Ensure the result is a list
            print(f"Result: {result}")  # Debug: Print the fetched result

    def test_query_first_five_rows(self):
        # Test querying the first 5 rows from a table (e.g., 'classes')
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM classes LIMIT 5")).fetchall()
            self.assertIsInstance(result, list)  # Ensure the result is a list
            self.assertTrue(len(result) <= 5)  # Check that the length is 5 or less
            print(f"First 5 rows from 'classes': {result}")  # Debug: Print the fetched result

    def test_query_nonexistent_table(self):
        # Test querying a non-existent table
        with db.engine.connect() as connection:
            with self.assertRaises(Exception) as context:
                connection.execute(text("SELECT * FROM nonexistent_table LIMIT 1")).fetchall()
            print(f"Error caught as expected: {context.exception}")  # Debug: Print the exception

    def test_query_monsters_table(self):
        # Test querying the 'monsters' table to check if it returns data
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM monsters LIMIT 5")).fetchall()
            self.assertIsInstance(result, list)  # Ensure the result is a list
            self.assertTrue(len(result) <= 5)  # Check that the length is 5 or less
            print(f"First 5 rows from 'monsters': {result}")  # Debug: Print the fetched result

# Entry point for running the tests
if __name__ == '__main__':
    unittest.main()
