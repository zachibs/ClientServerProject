import socket
import json
from config import *
from clients.dhcp_client import start_dhcp_client
from clients.dns_client import query_dns_server_for_ip
BUFFER_SIZE = 1024


def connect_to_server(server_ip: str, server_port: int) -> socket.socket:
    """
    Connects to a server using a TCP socket.

    Args:
        server_ip (str): The IP address of the server to connect to.
        server_port (int): The port of the server to connect to.

    Returns:
        socket.socket: The socket object used to communicate with the server if the connection was successful. Otherwise, returns None.
    """
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP socket
        server_address = (server_ip, server_port) # Tuple containing the IP address and port of the server
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        client_socket.bind(("", APP_SERVER_SRC_PORT))
        client_socket.connect(server_address) # Connect to the server
    except Exception as e:
        print("Failed to connect to server")
        return None

    return client_socket


def print_menu() -> None:
    """
    Prints the menu of options.
    """
    print("Menu of options:\n 1.Add a country\n 2.Get all countries\n 3.Get a specific country\n \
4.Get all countries by a specific ethnicity\n 5.Get all countries by a specific war status\n \
6.get all countries with population over number\n 7.Get all countries that founded after year\n \
8.Change a country's name\n 9.Change a country's war status\n 10.Change a country's population\n 11. Delete a country by its name\n 12-inf. exit menu")


def get_user_choice() -> int:
    """
    Gets the user's choice.

    Returns:
        int: The user's choice.
    """
    choice = int(input("please choose your option: ")) # Get the user's choice
    return choice


def create_new_entry() -> json:
    """
    Prompts the user for a new country's information and returns it as a JSON-formatted request.

    Returns:
        json: The request containing the new country's information.
    """
    # Get the country's information
    name = input("Please enter the country's name: ")
    population = int(input("Please enter the country's population: "))
    ethnicity = input("Please enter the country's ethnicity: ")
    founding_year = int(input("Please enter the country's founding_year: "))
    in_war_prompt = input("Please enter the country's war status (True or False): ")
    in_war = True if (in_war_prompt == "True") else False
    
    # Create a JSON string containing the country's information
    request = json.dumps({"choice": 1, "name": name, "population": population,
                        "ethnicity":ethnicity, "founding_year": founding_year,
                        "in_war": in_war})
    return request


def get_all_countries() -> json:
    """
    Returns a JSON-formatted request to get all countries.

    Returns:
        json: The request to get all countries.
    """
    # Create a JSON string with the choice to get all countries
    request = json.dumps({"choice": 2})
    return request


def get_country_by_name() -> json:
    """
    Prompts the user for a country's name and returns it as a JSON-formatted request to search for the country.

    Returns:
        json: The request to search for the country by name.
    """
    name = input("Please enter the country's name: ") # Get the name of the country to search for
    request = json.dumps({"choice": 3, "name": name}) # Create a JSON string with the choice to search for a country by name and the name of the country
    return request


def get_country_by_ethnicity() -> json:
    """
    Prompt user for ethnicity and return a JSON-formatted request to search for countries by ethnicity.

    Returns:
    JSON-formatted request with the choice to search for countries by ethnicity and the ethnicity to search for.
    """
    ethnicity = input("Please enter the country's ethnicity: ")
    request = json.dumps({"choice": 4, "ethnicity": ethnicity}) 
    return request


def get_country_by_war_status() -> json:
    """
    Prompt user for war status and return a JSON-formatted request to search for countries by war status.

    Returns:
    JSON-formatted request with the choice to search for countries by war status and the war status to search for.
    """
    in_war_prompt = input("Please enter the country's war status (True or False): ")
    if in_war_prompt == "True":
        in_war = True
    elif in_war_prompt == "False":
        in_war = False
    else:
        in_war = in_war_prompt
    request = json.dumps({"choice": 5, "war_status": in_war})
    return request

def get_countries_over_population_number() -> json:
    """
    Prompt user for population number and return a JSON-formatted request to search for countries with population over the specified number.

    Returns:
    JSON-formatted request with the choice to search for countries with population over a certain number and the population number to search for.
    """
    number = int(input("Please enter the country's population: "))
    request = json.dumps({"choice": 6, "number": number})
    return request


def get_countries_founded_after_year() -> json:
    """
    Prompt user for founding year and return a JSON-formatted request to search for countries founded after the specified year.

    Returns:
    JSON-formatted request with the choice to search for countries founded after a certain year and the year to search for.
    """
    year = int(input("Please enter the country's founding_year: "))
    request = json.dumps({"choice": 7, "year": year})
    return request


def change_country_name() -> json:
    """
    Prompt user for the name of the country they want to change, the new name, and return a JSON-formatted request to change the country's name.

    Returns:
    JSON-formatted request with the choice to change the name of a country, the name of the country to change, and the new name to assign.
    """
    name = input("Please enter the country's name whom you want to change: ")
    new_name = input("Please enter the country's new name: ")
    request = json.dumps({"choice":8, "old_name":name, "new_name":new_name})
    return request


def change_country_war_status() -> json:
    """
    Prompt user for the name of the country they want to change the war status of, the new war status, and return a JSON-formatted request to change the country's war status.

    Returns:
    JSON-formatted request with the choice to change the war status of a country, the name of the country to change the war status of, and the new war status to assign.
    """
    name = input("Please enter the country's name whom you want to change the war status: ")
    in_war_prompt = input("Please enter the country's new war status (True or False): ")
    new_war_status = True if in_war_prompt == "True" else False
    request = json.dumps({"choice":9, "name":name, "new_war_status":new_war_status})
    return request


def change_country_population() -> json:
    """Prompts the user to enter the name of the country they want to change the population count of, 
    the new population count, and returns a JSON-formatted request.

    Returns:
    JSON-formatted request
    """
    name = input("Please enter the country's name whom you want the population count: ")
    new_population = int(input("Please enter the country's new population: "))
    request = json.dumps({"choice":10, "name":name, "new_population":new_population})
    return request

def delete_country_by_name() -> json:
    """Prompts the user to enter the name of the country they want to delete, and returns a JSON-formatted request.

    Returns:
    JSON-formatted request
    """
    name = input("Please enter the country's name whom you want delete: ")
    request = json.dumps({"choice":11, "name":name})
    return request

# Define main function
def main():

    # Get app ip address and dns server ip address:

    new_client_ip_address, dns_server_ip_address = start_dhcp_client()

    app_ip_address = query_dns_server_for_ip(APP_DOMAIN, new_client_ip_address, dns_server_ip_address)

    print(new_client_ip_address, dns_server_ip_address, app_ip_address)

    # Connect to server

    client_socket = connect_to_server(app_ip_address, APP_SERVER_DST_PORT)

    if client_socket == None:
        return
    
    # Print welcome message
    print("Welcome to the client side !")
    
    while True:
        # Print menu options
        print_menu()
        try:
            # Get user choice and call corresponding function to create request
            choice = get_user_choice()
            if (choice == 1):
                request = create_new_entry()
            elif (choice == 2):
                request = get_all_countries()
            elif (choice == 3):
                request = get_country_by_name()
            elif (choice == 4):
                request = get_country_by_ethnicity()
            elif (choice == 5):
                request = get_country_by_war_status()
            elif (choice == 6):
                request = get_countries_over_population_number()
            elif (choice == 7):
                request = get_countries_founded_after_year()
            elif (choice == 8):
                request = change_country_name()
            elif (choice == 9):
                request = change_country_war_status()
            elif (choice == 10):
                request = change_country_population()
            elif (choice == 11):
                request = delete_country_by_name()
            else:
                break

            # Send request to server
            client_socket.sendall(request.encode())
            
            # Set timeout and receive data from server
            client_socket.settimeout(3.0)
            data = client_socket.recv(BUFFER_SIZE)
            data = json.loads(data.decode())
            print(f"\n{data}\n")

        except Exception as e:
            client_socket.close()
            break

    client_socket.close()

if __name__ == "__main__":
    main()