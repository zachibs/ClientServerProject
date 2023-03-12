import socket
import json
from config import *
from dhcpclient import start_dhcp_client
from dnsclient import query_dns_server_for_ip
BUFFER_SIZE = 1024

# Function to connect to the server
def connect_to_server(server_ip: str, server_port: int) -> socket.socket:
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP socket
        server_address = (server_ip, server_port) # Tuple containing the IP address and port of the server
        client_socket.connect(server_address) # Connect to the server
    except Exception as e:
        print("Failed to connect to server")
        return None

    return client_socket

# Function to print the menu of options
def print_menu() -> None:
    print("Menu of options:\n 1.Add a country\n 2.Get all countries\n 3.Get a specific country\n \
4.Get all countries by a specific ethnicity\n 5.Get all countries by a specific war status\n \
6.get all countries with population over number\n 7.Get all countries that founded after year\n \
8.Change a country's name\n 9.Change a country's war status\n 10.Change a country's population")

# Function to get the user's choice
def get_user_choice() -> int:
    choice = int(input("please choose your option: ")) # Get the user's choice
    return choice

# Function to create a new entry
def create_new_entry() -> json:
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

# Function to get all countries
def get_all_countries() -> json:
    # Create a JSON string with the choice to get all countries
    request = json.dumps({"choice": 2})
    return request

# Function to get a specific country by name
def get_country_by_name() -> json:
    name = input("Please enter the country's name: ") # Get the name of the country to search for
    request = json.dumps({"choice": 3, "name": name}) # Create a JSON string with the choice to search for a country by name and the name of the country
    return request

# Function to get all countries with a specific ethnicity
def get_country_by_ethnicity() -> json:
    ethnicity = input("Please enter the country's ethnicity: ") # Get the ethnicity to search for
    request = json.dumps({"choice": 4, "ethnicity": ethnicity}) # Create a JSON string with the choice to search for countries by ethnicity and the ethnicity to search for
    return request

# Function to get all countries with a specific war status
def get_country_by_war_status() -> json:
    in_war_prompt = input("Please enter the country's war status (True or False): ")
    in_war = True if in_war_prompt == "True" else False
    request = json.dumps({"choice": 5, "war_status": in_war})
    return request
# Define function to prompt user to enter population number and return a JSON-formatted request
def get_countries_over_population_number() -> json:
    number = int(input("Please enter the country's population: "))
    request = json.dumps({"choice": 6, "number": number})
    return request

# Define function to prompt user to enter founding year and return a JSON-formatted request
def get_countries_founded_after_year() -> json:
    year = int(input("Please enter the country's founding_year: "))
    request = json.dumps({"choice": 7, "year": year})
    return request

# Define function to prompt user to enter the name of the country they want to change, the new name, and return a JSON-formatted request
def change_country_name() -> json:
    name = input("Please enter the country's name whom you want to change: ")
    new_name = input("Please enter the country's new name: ")
    request = json.dumps({"choice":8, "old_name":name, "new_name":new_name})
    return request

# Define function to prompt user to enter the name of the country they want to change the war status of, and the new war status, and return a JSON-formatted request
def change_country_war_status() -> json:
    name = input("Please enter the country's name whom you want to change the war status: ")
    in_war_prompt = input("Please enter the country's new war status (True or False): ")
    new_war_status = True if in_war_prompt == "True" else False
    request = json.dumps({"choice":9, "name":name, "new_war_status":new_war_status})
    return request

# Define function to prompt user to enter the name of the country they want to change the population count of, the new population count, and return a JSON-formatted request
def change_country_population() -> json:
    name = input("Please enter the country's name whom you want the population count: ")
    new_population = int(input("Please enter the country's new population: "))
    request = json.dumps({"choice":10, "name":name, "new_population":new_population})
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
            else:
                break

            # Send request to server
            client_socket.sendall(request.encode())
            
            # Set timeout and receive data from server
            client_socket.settimeout(3.0)
            data = client_socket.recv(BUFFER_SIZE)
            data = json.loads(data.decode())
            print(data)

        except Exception as e:
            client_socket.close()
            break

    client_socket.close()

if __name__ == "__main__":
    main()