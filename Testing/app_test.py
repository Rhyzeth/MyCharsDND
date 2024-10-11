import unittest
from flask import Flask
from app import app, db

class TestDatabaseConnection(unittest.TestCase):

    def setUp(self):
        # Set up the test client for Flask
        self.app = app
        self.client = self.app.test_client()

        # Ensure the app is in testing mode
        self.app.config['TESTING'] = True

        # Make sure to use a different database for testing if possible
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_dnd_database.db'

        # Create tables in the test database
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        # Drop all tables after each test to clean up the test database
        with self.app.app_context():
            db.drop_all()

    def test_database_connection(self):
        # Test if the connection and querying of the database works
        with self.app.app_context():
            try:
                # Query any table, e.g., backgrounds
                result = db.engine.execute("SELECT * FROM backgrounds LIMIT 1").fetchall()
                self.assertIsNotNone(result)  # Assert that some result is returned
                print("Database connected and table queried successfully!")
            except Exception as e:
                self.fail(f"Database query failed: {e}")

if __name__ == '__main__':
    unittest.main()