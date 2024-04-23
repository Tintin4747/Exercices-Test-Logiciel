import sqlite3


# noinspection SqlNoDataSourceInspection
class Customer:
    """
    Customer class containing all the method to interact with the customer table
    """

    def __init__(self, path=":memory:") -> None:
        """
        Connect to in memory database by default, or to a database file if
        specified.
        """
        self.con = sqlite3.connect(path)

    def create_table(self) -> None:
        """
        Create the customer table if not exists
        """
        self.con.execute("""
            CREATE TABLE IF NOT EXISTS customer (
                id INT PRIMARY KEY NOT NULL,
                email TEXT NOT NULL
            )
            """)

    def insert(self, customer_id: int, email: str) -> None:
        """
        Insert a new customer in the table.

           :param customer_id: The customer id as an int
           :param email: The customer email as a string
        """
        self.con.execute("""
            INSERT INTO customer (
                id,
                email
            ) VALUES (
                ?, ?
            )""", (customer_id, email))
        self.con.commit()

    def update(self, customer_id: int, email: str) -> None:
        """
        Update a customer in the table.

           :param customer_id: The customer id as an int
           :param email: The customer email as a string
        """
        self.con.execute("""
            UPDATE customer
            SET email = ?
            WHERE id = ?
            """, (email, customer_id))
        self.con.commit()
