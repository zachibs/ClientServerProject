import socket
import json
from sqlalchemy.orm import session

import sys
sys.path.append('.')
print(sys.path)
import database as database
from config import *

BUFFER_SIZE = 1024

def create_server_socket(server_ip: str, server_port: int) -> socket.socket:
    """Creates a server socket with a specified IP address and port number.

    Args:
        server_ip (str): IP address for the server socket.
        server_port (int): Port number for the server socket.

    Returns:
        socket.socket: The server socket that has been created and bound to the specified IP address and port number.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (server_ip, server_port)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(server_address)
    server_socket.listen(10)
    return server_socket


def connect_to_client(server_socket: socket.socket) -> tuple:
    """Waits for and accepts a client connection, returning a socket and client address tuple.

    Args:
        server_socket (socket.socket): The server socket to accept connections from.

    Returns:
        tuple: A tuple consisting of the client socket and the client address.
    """
    print('Waiting for a connection')
    client_socket, client_address = server_socket.accept()
    print(f'Connection from {client_address}')
    return client_socket, client_address


def receive_data_from_client(client_socket: socket.socket, client_address: str) -> json:
    """Receives and decodes data from the client and returns it as a JSON object.

    Args:
        client_socket (socket.socket): The socket used for communication with the client.
        client_address (str): The address of the client.

    Returns:
        json: The data received from the client, decoded as a JSON object.
    """
    print("Waiting for data from the client")
    client_socket.settimeout(60.0)
    data = client_socket.recv(BUFFER_SIZE)
    data = json.loads(data.decode())
    print(f'Received "{data}" from {client_address} OPENED')
    return data


def add_country_to_db(session: session.Session, data: json) -> tuple:
    """Adds a new country to the database, returning a tuple of a boolean indicating success and a message.

    Args:
        session: The database session to use.
        data (json): The data to be added to the database.

    Returns:
        tuple: A tuple consisting of a boolean indicating whether the operation was successful and a message.
    """
    print("Client choose to add a country")
    name = data["name"]
    population = data["population"]
    ethnicity = data["ethnicity"]
    founding_year = data["founding_year"]
    in_war = data["in_war"]
    bool_response = database.add_value_to_db(session, name, population, ethnicity, founding_year, in_war)
    message = "Added value to db" if bool_response else "Value was already in db"
    return bool_response, message


def get_all_countries_from_db(session: session.Session, data: json) -> tuple:
    """Retrieves all countries from the database and returns them as a tuple of a boolean indicating success and a message.

    Args:
        session: The database session to use.
        data (json): Additional data, not used in this function.

    Returns:
        tuple: A tuple consisting of a boolean indicating whether the operation was successful and a message.
    """
    print("Client choose to get all countries")
    countries = database.get_all_countries(session)

    if countries == None:
        return False, "No countries found"

    countries = [x.to_dict() for x in list(countries)]
    bool_response = True if len(countries) > 0 else False
    message = ""
    for country in countries:
        message += str(country)
        message += " "
    return bool_response, message


def get_country_by_name_from_db(session: session.Session, data: json) -> tuple:
    """
    Retrieves a specific country from the database by name and returns it as a tuple of a boolean indicating success and a message.

    Parameters:
    session (object): SQLAlchemy session object
    data (json): JSON data containing country name

    Returns:
    tuple: Tuple of a boolean indicating success and a message
    """
    print("Client choose to get a specific country")
    country = database.get_country_by_name(session,data["name"])
    if country == None:
        message = "Country not Found"
    else:
        message = country.to_dict()
    bool_response = True if country != None else False
    return bool_response, message


def get_country_by_ethnicity_from_db(session: session.Session, data: json) -> tuple:
    """
    Retrieves all countries from the database that match a specified ethnicity and returns them as a tuple of a boolean indicating success and a message.

    Parameters:
    session (object): SQLAlchemy session object
    data (json): JSON data containing ethnicity

    Returns:
    tuple: Tuple of a boolean indicating success and a message
    """
    print("Client choose to get all countries by a specific ethnicity")
    countries = database.get_countries_by_ethnicity(session, data["ethnicity"])
    if countries == None:
        return False, "No countries found"
    countries = [x.to_dict() for x in list(countries)]
    bool_response = True if len(countries) > 0 else False
    message = ""
    for country in countries:
        message += str(country)
        message += " "
    return bool_response, message


def get_all_countries_by_war_status_from_db(session: session.Session, data: json) -> tuple:
    """
    Retrieves all countries with a specific war status from the database and returns them as a tuple of a boolean indicating success and a message.

    Parameters:
    session (object): SQLAlchemy session object
    data (json): JSON data containing war status

    Returns:
    tuple: Tuple of a boolean indicating success and a message
    """
    print("Client choose to get all countries by a specific war status")
    countries = database.get_counties_by_war_status(session, data["war_status"])
    if countries == None:
        return False, "No countries found"
    countries = [x.to_dict() for x in list(countries)]
    bool_response = True if len(countries) > 0 else False

    message = ""
    for country in countries:
        message += str(country)
        message += " "

    return bool_response, message


def get_all_countries_over_population_from_db(session: session.Session, data: json) -> tuple:
    """
    Retrieves all countries with a population greater than a specified number from the database and returns them as a tuple of a boolean indicating success and a message.

    Parameters:
    session (object): SQLAlchemy session object
    data (json): JSON data containing population number

    Returns:
    tuple: Tuple of a boolean indicating success and a message
    """
    print("Client choose to get all countries with population over number")
    countries = database.get_counties_with_population_over_number(session, int(data["number"]))
    if countries == None:
        return False, "No countries found"
    countries = [x.to_dict() for x in list()]

    bool_response = True if len(countries) > 0 else False

    message = ""
    for country in countries:
        message += str(country)
        message += " "

    return bool_response, message


# Function to get all countries founded after specified year
def get_all_countries_founded_after_year_from_db(session: session.Session, data: json) -> tuple:
    """
    Get all countries founded after the specified year from the database.

    Args:
        session: A SQLAlchemy session object.
        data (json): A dictionary containing the following keys: 
            - year (int): The year to filter countries.

    Returns:
        A tuple containing a boolean value and a message string.
        The boolean value indicates whether any countries were found.
        The message string contains the list of matched countries.
    """
    print("Client choose to get all countries that founded after year")

    # Get list of countries founded after specified year from database and convert to dict
    countries = database.get_countries_founded_after_year(session, data["year"])
    if countries == None:
        return False, "No countries found"
    countries = [x.to_dict() for x in list(countries)]

    # Check if any countries matched
    bool_response = True if len(countries) > 0 else False

    # Build message string with matched countries
    message = ""
    for country in countries:
        message += str(country)
        message += " "

    return bool_response, message


# Function to change a country's name in the database
def change_a_contry_name_in_db(session: session.Session, data: json) -> tuple:
    """
    Change a country's name in the database.

    Args:
        session: A SQLAlchemy session object.
        data (json): A dictionary containing the following keys: 
            - old_name (str): The old name of the country.
            - new_name (str): The new name of the country.

    Returns:
        A tuple containing a boolean value and a message string.
        The boolean value indicates whether the change was successful or not.
        The message string contains a status message.
    """
    print("Client choose to change a country's name")

    # Call function in database module to change country's name
    bool_response = database.change_country_name(session, data["old_name"], data["new_name"])

    # Build message string based on whether change was successful or not
    message = "Changed value" if bool_response else "Couldn't change value"

    return bool_response, message


# Function to change a country's war status in the database
def change_a_country_war_status_in_db(session: session.Session, data: json) -> tuple:
    """
    Change a country's war status in the database.

    Args:
        session: A SQLAlchemy session object.
        data (json): A dictionary containing the following keys: 
            - name (str): The name of the country.
            - new_war_status (bool): The new war status of the country.

    Returns:
        A tuple containing a boolean value and a message string.
        The boolean value indicates whether the change was successful or not.
        The message string contains a status message.
    """
    print("Client choose to change a country's war status")

    # Call function in database module to change country's war status
    bool_response = database.change_country_war_status(session, data["name"], data["new_war_status"])

    # Build message string based on whether change was successful or not
    message = "Changed value" if bool_response else "Couldn't change value"

    return bool_response, message


# Function to change a country's population count in the database
def change_a_country_population_count_in_db(session: session.Session, data: json) -> tuple:
    """
    Function to change a country's population count in the database.

    Args:
        session: The session object to connect to the database.
        data (dict): The data containing the name of the country to update and its new population count.

    Returns:
        A tuple containing a boolean value indicating whether the population count was changed successfully
        and a message string indicating whether the change was successful or not.
    """
    print("Client choose to change a country's population")
    bool_response = database.change_country_population(session, data["name"], data["new_population"])
    message = "Changed value" if bool_response else "Couldn't change value"
    return bool_response, message


# Function to change a country's population count in the database
def delete_country_by_name(session: session.Session, data: json) -> tuple:
    """
    Function to delete a country from the database.

    Args:
        session: The session object to connect to the database.
        data (dict): The data containing the name of the country to delete.

    Returns:
        A tuple containing a boolean value indicating whether the population count was changed successfully
        and a message string indicating whether the change was successful or not.
    """
    print("Client choose to delete a country")
    bool_response = database.delete_country(session, data["name"])
    message = "deleted country" if bool_response else "Couldn't find country"
    return bool_response, message

def main():
    print("Starting APP server...")
    server_socket = create_server_socket(APP_SERVER_IP, APP_SERVER_DST_PORT)
    while True:
        client_socket, client_address = connect_to_client(server_socket)
        while True:
            try:
                data = receive_data_from_client(client_socket, client_address)
                choice = data["choice"]
                session = database.get_session()

                if (choice == 1):
                    bool_response, message = add_country_to_db(session, data)

                elif (choice == 2):
                    bool_response, message = get_all_countries_from_db(session, data)

                elif (choice == 3):
                    bool_response, message = get_country_by_name_from_db(session, data)

                elif (choice == 4):
                    bool_response, message = get_country_by_ethnicity_from_db(session, data)

                elif (choice == 5):
                    bool_response, message = get_all_countries_by_war_status_from_db(session, data)

                elif (choice == 6):
                    bool_response, message = get_all_countries_over_population_from_db(session, data)

                elif (choice == 7):
                    bool_response, message = get_all_countries_founded_after_year_from_db(session, data)

                elif (choice == 8):
                    bool_response, message = change_a_contry_name_in_db(session, data)

                elif (choice == 9):
                    bool_response, message = change_a_country_war_status_in_db(session, data)

                elif (choice == 10):
                    bool_response, message = change_a_country_population_count_in_db(session, data)

                elif (choice == 11):
                    bool_response, message = delete_country_by_name(session, data)

                else:
                    client_socket.close()
                    print(f'Connection from {client_address} CLOSED')
                    break

                response = json.dumps({'status': 200 if bool_response else 404, "message": message})
                client_socket.sendall(response.encode())
                print(f'Sent response to {client_address}')
            
            except Exception as e:
                client_socket.close()
                print(f'Connection from {client_address} CLOSED')
                break

if __name__ == "__main__":
    main()
