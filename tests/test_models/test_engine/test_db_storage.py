#!/usr/bin/python3
import os
import unittest
from models.state import State
from models.engine.db_storage import DBStorage
from sqlalchemy.orm import sessionmaker

storage = DBStorage()
storage.reload()
Session = sessionmaker(bind=storage._DBStorage__engine)
session = Session()

@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DB Storage test')
class TestDBStorage(unittest.TestCase):
    """Tests for the DBStorage engine"""

    @classmethod
    def setUpClass(cls):
        """Setting up the test environment"""
        cls.session = session

    @classmethod
    def tearDownClass(cls):
        """Tearing down the test environment"""
        cls.session.close()

    def setUp(self):
        """Begin a new session for each test"""
        self.session.begin()

    def tearDown(self):
        """Roll back the session after each test"""
        self.session.rollback()

    def test_add_and_commit(self):
        """Testing adding and committing objects to Database"""
        initial_count = self.session.query(State).count()
        new_state = State(name="Texas")
        self.session.add(new_state)
        self.session.commit()
        self.assertEqual(self.session.query(State).count(), initial_count + 1)
        self.session.delete(new_state)
        self.session.commit()

    def test_delete_state(self):
        """Testing deleting a State from the Database"""
        initial_count = self.session.query(State).count()

        new_state = State(name="California")
        self.session.add(new_state)
        self.session.commit()

        self.assertEqual(self.session.query(State).count(), initial_count + 1)

        # Deletes then verifies removal
        self.session.delete(new_state)
        self.session.commit()
        self.assertEqual(self.session.query(State).count(), initial_count)

    def test_get_state(self):
        """Testing retrieving a State from the Database"""
        new_state = State(name="Nevada")
        self.session.add(new_state)
        self.session.commit()

        # Retrieves and verifies retrieval
        retrieved_state = self.session.query(State).get(new_state.id)
        self.assertEqual(retrieved_state.id, new_state.id)
        self.assertEqual(retrieved_state.name, "Nevada")

        # Cleanup
        self.session.delete(new_state)
        self.session.commit()

if __name__ == "__main__":
    unittest.main()