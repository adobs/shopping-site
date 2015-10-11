"""Customers at Hackbright."""


class Customer(object):
    """Ubermelon customer."""

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def __repr__(self):
        return "Customer data: {}, {}, {}, {}".format(self.first_name, self.last_name, self.email, self.password)


def read_customers_from_file(filename):
    """Reads a text file of customer information.  Creates a new object with provided attributes.

    There is a customers dictionary that stores all customer objects.

    """

    customers = {}

    for line in open(filename):
        first_name, last_name, email, password = line.strip().split("|")

        customers[email] = Customer(first_name, last_name, email, password)

    return customers


def get_by_email(email):
    """Takes an email, returns the customer object corresponding to it"""

    return customers[email]


def get_all_customers():

    return customers

customers = read_customers_from_file("customers.txt")
