import sqlite3
import unittest
import logging
from web_manipulation import WebManipulationModule
from file_operations import FileOperationsModule

class MemoryStorage:
    def __init__(self, db_file='interactions.db'):
        """
        Initialize the MemoryStorage with a SQLite database.

        Args:
            db_file (str): The SQLite database file path.

        """
        try:
            self.conn = sqlite3.connect(db_file)
            self.create_table()
        except sqlite3.Error as e:
            self.handle_error(e)

    def create_table(self):
        """
        Create the 'interactions' table in the database if it doesn't exist.

        """
        try:
            c = self.conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS interactions
                         (timestamp TEXT, user_input TEXT, response TEXT)''')
            self.conn.commit()
        except sqlite3.Error as e:
            self.handle_error(e)

    def store_interaction(self, timestamp, user_input, response):
        """
        Store an interaction in the database.

        Args:
            timestamp (str): The timestamp of the interaction.
            user_input (str): The user's input.
            response (str): The system's response.

        """
        try:
            c = self.conn.cursor()
            c.execute("INSERT INTO interactions VALUES (?,?,?)", (timestamp, user_input, response))
            self.conn.commit()
        except sqlite3.Error as e:
            self.handle_error(e)

    def retrieve_interaction(self, timestamp):
        """
        Retrieve an interaction based on its timestamp.

        Args:
            timestamp (str): The timestamp of the interaction to retrieve.

        Returns:
            tuple or None: The retrieved interaction as a tuple (timestamp, user_input, response), or None if not found.

        """
        try:
            c = self.conn.cursor()
            c.execute("SELECT * FROM interactions WHERE timestamp=?", (timestamp,))
            return c.fetchone()
        except sqlite3.Error as e:
            self.handle_error(e)
            return None

    def delete_interaction(self, timestamp):
        """
        Delete an interaction based on its timestamp.

        Args:
            timestamp (str): The timestamp of the interaction to delete.

        """
        try:
            c = self.conn.cursor()
            c.execute("DELETE FROM interactions WHERE timestamp=?", (timestamp,))
            self.conn.commit()
        except sqlite3.Error as e:
            self.handle_error(e)

    def retrieve_recent_interactions(self, num_interactions):
        """
        Retrieve the most recent interactions.

        Args:
            num_interactions (int): The number of recent interactions to retrieve.

        Returns:
            list: A list of tuples representing recent interactions.

        """
        try:
            c = self.conn.cursor()
            c.execute("SELECT * FROM interactions ORDER BY timestamp DESC LIMIT ?", (num_interactions,))
            return c.fetchall()
        except sqlite3.Error as e:
            self.handle_error(e)
            return []

    def analyze_interactions(self):
        """
        Analyze interactions by counting occurrences of user inputs.

        Returns:
            list: A list of tuples containing user inputs and their occurrence counts.

        """
        try:
            c = self.conn.cursor()
            c.execute("SELECT user_input, COUNT(*) FROM interactions GROUP BY user_input ORDER BY COUNT(*) DESC")
            return c.fetchall()
        except sqlite3.Error as e:
            self.handle_error(e)
            return []

    def handle_error(self, error):
        """
        Handle errors gracefully and log them.

        Args:
            error (str): Error message.

        """
        logging.error(f"An error occurred: {error}")

class TestMemoryHandling(unittest.TestCase):
    def test_store_interaction(self):
        memory = MemoryStorage(':memory:')  # Use in-memory database for testing
        timestamp = '2023-11-05 13:30:00'
        user_input = 'Hello, Alt!'
        response = 'Hi there!'
        memory.store_interaction(timestamp, user_input, response)
        retrieved_interaction = memory.retrieve_interaction(timestamp)
        self.assertEqual(retrieved_interaction, (timestamp, user_input, response))

    def test_delete_interaction(self):
        memory = MemoryStorage(':memory:')
        timestamp = '2023-11-05 13:30:00'
        user_input = 'Hello, Alt!'
        response = 'Hi there!'
        memory.store_interaction(timestamp, user_input, response)
        memory.delete_interaction(timestamp)
        retrieved_interaction = memory.retrieve_interaction(timestamp)
        self.assertIsNone(retrieved_interaction)

if __name__ == '__main__':
    unittest.main()
