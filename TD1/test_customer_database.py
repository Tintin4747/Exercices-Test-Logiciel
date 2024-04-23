from sqlite3 import IntegrityError, Connection

import pytest

from customer_database import Customer

TEST_ID = 1


@pytest.fixture(scope="function")  # Scope de la fixture, par default function
def customer_without_table():
    """
    Connection to in memory database using the Customer class

       :return: An instantiated Customer class
    """
    customer = Customer()  # Avant le test, c'est le setup
    yield customer  # Un yield évite de sortir de la fonction
    customer.con.close()  # Après le test, le teardown


@pytest.fixture(scope="function")
def customer_with_table(customer_without_table):
    """
    Connection to in memory database using the Customer class returned the table
    has been created.

       :param customer_without_table: The customer_without_table fixture
       :return: An instantiated Customer class
    """
    customer_without_table.create_table()
    return customer_without_table


@pytest.fixture(scope="function")
def init_one_customer(customer_with_table):
    customer_with_table.insert(TEST_ID, "christophe@in-france.fr")
    return customer_with_table


def test_instantiation(customer_without_table):
    """
    Test the instance of the Customer has an attribute instance of a
    sqlite3.Connection.

       :param customer_without_table: Fixture of a virgin connection
    """
    assert isinstance(customer_without_table.con, Connection)


def test_customer_table_creation(customer_without_table):
    """
    Test the customer_without_table database, the CREATE instruction and SQL validity of the
    definition of the table.

       :param customer_without_table: Fixture of a virgin connection
    """
    try:
        customer_without_table.create_table()
    except Exception as e:
        pytest.fail("The table creation failed: %s" % e)


def test_add_customer(customer_with_table):
    """
    Test the customer_with_table database, the INSERT instruction and SQL validity of the
    definition of the table.

       :param customer_with_table: Fixture of a newly created empty table.
    """
    try:
        customer_with_table.insert(TEST_ID, "christophe@in-france.fr")
    except Exception as e:
        pytest.fail("The customer insertion failed: %s" % e)


def test_customer_uniqueness(init_one_customer):
    """
    Test the same customer ID cannot be added twice therefore they are unique.

      :param init_one_customer: Fixture of a newly created empty table.
    """
    customer_id = 1
    email = "christophe@in-france.fr"
    with pytest.raises(IntegrityError):
        init_one_customer.insert(customer_id, email)


def test_customer_id_cannot_be_null(customer_with_table):
    """
    Test the customer id cannot be NULL.

       :param customer_with_table: Fixture of a newly created empty table.
    """
    with pytest.raises(IntegrityError):
        customer_with_table.insert(None, "christophe@in-france.fr")


def test_customer_email_cannot_be_null(customer_with_table):
    """
    Test the customer email cannot be NULL.

       :param customer_with_table: Fixture of a newly created empty table.
    """
    with pytest.raises(IntegrityError):
        customer_with_table.insert(TEST_ID, None)


def test_update_customer(customer_with_table):
    """
    Test the customer_with_table database, the UPDATE instruction and SQL validity
    of the definition of the table

    :param customer_with_table:
    :return:
    """
    try:
        customer_with_table.update(TEST_ID, "dlp92128@gmail.com")
    except Exception as e:
        pytest.fail("The customer update failed: %s" % e)


def test_update_customer_success(init_one_customer):
    """
    Check if the update of the customer succeed

    :param init_one_customer:
    :return:
    """
    rowcount = init_one_customer.con.total_changes
    assert rowcount == 1, "The customer has not been initialized"
    init_one_customer.update(TEST_ID, "abcd")
    rowcount = init_one_customer.con.total_changes
    assert rowcount == 2, "The customer has not been updated"


def test_update_customer_id_not_exists(init_one_customer):
    """
    Test if the id of the user not exists in database

    :param init_one_customer:
    :return:
    """
    init_one_customer.update(48, "abc")
    rowcount = init_one_customer.con.total_changes
    assert rowcount == 1, "%s customers have been updated but id not exists in database" % rowcount


def test_customer_update_id_cannot_be_null(init_one_customer):
    """
    Check if customer id cannot be null in update

    :param init_one_customer:
    :return:
    """
    init_one_customer.update(None, "dlp92128@gmail.com")
    rowcount = init_one_customer.con.total_changes
    assert rowcount == 1, "A customer have been updated but id is null"


def test_customer_update_mail_not_null(init_one_customer):
    """
    Check if customer mail cannot be null in update

    :param init_one_customer:
    :return:
    """
    with pytest.raises(IntegrityError):
        init_one_customer.update(TEST_ID, None)
