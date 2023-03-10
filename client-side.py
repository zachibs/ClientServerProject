import socket
import json

BUFFER_SIZE = 1024

def connect_to_server(server_ip: str, server_port: int) -> socket.socket:
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (server_ip, server_port)
        client_socket.connect(server_address)
    except Exception as e:
        print("Failed to connect to server")
        return None

    return client_socket

def print_menu() -> None:
    print("Menu of options:\n 1.Add a country\n 2.Get all countries\n 3.Get a specific country\n \
4.Get all countries by a specific ethnicity\n 5.Get all countries by a specific war status\n \
6.get all countries with population over number\n 7.Get all countries that founded after year\n \
8.Change a country's name\n 9.Change a country's war status\n 10.Change a country's population")
    
def get_user_choice() -> int:
    choice = int(input("please choose your option: "))
    return choice

def create_new_entry() -> json:
    name = input("Please enter the country's name: ")
    population = int(input("Please enter the country's population: "))
    ethnicity = input("Please enter the country's ethnicity: ")
    founding_year = int(input("Please enter the country's founding_year: "))
    in_war_prompt = input("Please enter the country's war status (True or False): ")
    in_war = True if (in_war_prompt == "True") else False
    request = json.dumps({"choice": 1, "name": name, "population": population,
                        "ethnicity":ethnicity, "founding_year": founding_year,
                        "in_war": in_war})
    return request

def get_all_countries() -> json:
    request = json.dumps({"choice": 2})
    return request

def get_country_by_name() -> json:
    name = input("Please enter the country's name: ")
    request = json.dumps({"choice": 3, "name": name})
    return request

def get_country_by_ethnicity() -> json:
    ethnicity = input("Please enter the country's ethnicity: ")
    request = json.dumps({"choice": 4, "ethnicity": ethnicity})
    return request

def get_country_by_war_status() -> json:
    in_war_prompt = input("Please enter the country's war status (True or False): ")
    in_war = True if in_war_prompt == "True" else False
    request = json.dumps({"choice": 5, "war_status": in_war})
    return request

def get_countries_over_population_number() -> json:
    number = int(input("Please enter the country's population: "))
    request = json.dumps({"choice": 6, "number": number})
    return request

def get_countries_founded_after_year() -> json:
    year = int(input("Please enter the country's founding_year: "))
    request = json.dumps({"choice": 7, "year": year})
    return request

def change_country_name() -> json:
    name = input("Please enter the country's name whom you want to change: ")
    new_name = input("Please enter the country's new name: ")
    request = json.dumps({"choice":8, "old_name":name, "new_name":new_name})
    return request

def change_country_war_status() -> json:
    name = input("Please enter the country's name whom you want to change the war status: ")
    in_war_prompt = input("Please enter the country's new war status (True or False): ")
    new_war_status = True if in_war_prompt == "True" else False
    request = json.dumps({"choice":9, "name":name, "new_war_status":new_war_status})
    return request

def change_country_population() -> json:
    name = input("Please enter the country's name whom you want the population count: ")
    new_population = int(input("Please enter the country's new population: "))
    request = json.dumps({"choice":10, "name":name, "new_population":new_population})
    return request

def main():
    client_socket = connect_to_server("localhost", 1234)

    if client_socket == None:
        return
    
    print("Welcome to the client side !")
    
    while True:
        print_menu()
        try:
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

            client_socket.sendall(request.encode())
            
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