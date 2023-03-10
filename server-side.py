import socket
import database
import json

BUFFER_SIZE = 1024

def create_server_socket(server_ip: str, server_port: int) -> socket.socket:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (server_ip, server_port)
    server_socket.bind(server_address)
    server_socket.listen(1)
    return server_socket
                
def connect_to_client(server_socket: socket.socket) -> socket.socket:
    print('Waiting for a connection')
    client_socket, client_address = server_socket.accept()
    print(f'Connection from {client_address}')
    return client_socket, client_address

def receive_data_from_client(client_socket: socket.socket, client_address: str) -> json:
    print("waiting for data from the client")
    client_socket.settimeout(30.0)
    data = client_socket.recv(BUFFER_SIZE)
    data = json.loads(data.decode())
    print(f'Received "{data}" from {client_address} OPENED')
    return data

def first_choice(session, data: json) -> tuple:
    print("Client choose to add a country")
    name = data["name"]
    population = data["population"]
    ethnicity = data["ethnicity"]
    founding_year = data["founding_year"]
    in_war = data["in_war"]
    bool_response = database.add_value_to_db(session, name, population, ethnicity, founding_year, in_war)
    message = "Added value to db" if bool_response else "Value was already in db"
    return bool_response, message

def second_choice(session, data: json) -> tuple:
    print("Client choose to get all countries")
    countries = [x.to_dict() for x in list(database.get_all_countries(session))]
    bool_response = True if len(countries) > 0 else False
    message = "Countries matched - "
    for country in countries:
        message += str(country)
        message += " "
    return bool_response, message

def third_choice(session, data: json) -> tuple:
    print("Client choose to get a specific country")
    country = list(database.get_country_by_name(session,data["name"]))
    bool_response = True if len(country) > 0 else False
    message = f"Country matched - {country[0].to_dict()}"
    return bool_response, message

def fourth_choice(session, data: json) -> tuple:
    print("Client choose to get all countries by a specific ethnicity")
    countries = [x.to_dict() for x in list(database.get_countries_by_ethnicity(session, data["ethnicity"]))]
    bool_response = True if len(countries) > 0 else False
    message = "Countries matched - "
    for country in countries:
        message += str(country)
        message += " "
    return bool_response, message

def fifth_choice(session, data: json) -> tuple:
    print("Client choose to get all countries by a specific war status")
    countries = [x.to_dict() for x in list(database.get_counties_by_war_status(session, data["war_status"]))]
    bool_response = True if len(countries) > 0 else False
    message = "Countries matched - "
    for country in countries:
        message += str(country)
        message += " "
    return bool_response, message

def sixth_choice(session, data: json) -> tuple:
    print("Client choose to get all countries with population over number")
    countries = [x.to_dict() for x in list(database.get_counties_with_population_over_number(session, int(data["number"])))]
    bool_response = True if len(countries) > 0 else False
    message = "Countries matched - "
    for country in countries:
        message += str(country)
        message += " "
    return bool_response, message

def seventh_choice(session, data: json) -> tuple:
    print("Client choose to get all countries that founded after year")
    countries = [x.to_dict() for x in list(database.get_countries_founded_after_year(session, data["year"]))]
    bool_response = True if len(countries) > 0 else False
    message = "Countries matched - "
    for country in countries:
        message += str(country)
        message += " "
    return bool_response, message

def eighth_choice(session, data: json) -> tuple:
    print("Client choose to change a country's name")
    bool_response = database.change_country_name(session, data["old_name"], data["new_name"])
    message = "Changed value" if bool_response else "Couldn't change value"
    return bool_response, message

def ninth_choice(session, data: json) -> tuple:
    print("Client choose to change a country's war status")
    bool_response = database.change_country_war_status(session, data["name"], data["new_war_status"])
    message = "Changed value" if bool_response else "Couldn't change value"
    return bool_response, message

def tenth_choice(session, data: json) -> tuple:
    print("Client choose to change a country's population")
    bool_response = database.change_country_population(session, data["name"], data["new_population"])
    message = "Changed value" if bool_response else "Couldn't change value"
    return bool_response, message

def main():
    server_socket = create_server_socket("localhost", 1234)
    while True:
        client_socket, client_address = connect_to_client(server_socket)
        while True:
            try:
                data = receive_data_from_client(client_socket, client_address)
                choice = data["choice"]
                session = database.get_session()

                if (choice == 1):
                    bool_response, message = first_choice(session, data)

                elif (choice == 2):
                    bool_response, message = second_choice(session, data)

                elif (choice == 3):
                    bool_response, message = third_choice(session, data)

                elif (choice == 4):
                    bool_response, message = fourth_choice(session, data)

                elif (choice == 5):
                    bool_response, message = fifth_choice(session, data)

                elif (choice == 6):
                    bool_response, message = sixth_choice(session, data)

                elif (choice == 7):
                    bool_response, message = seventh_choice(session, data)

                elif (choice == 8):
                    bool_response, message = eighth_choice(session, data)

                elif (choice == 9):
                    bool_response, message = ninth_choice(session, data)

                elif (choice == 10):
                    bool_response, message = tenth_choice(session, data)
                else:
                    client_socket.close()
                    print(f'Connection from {client_address} CLOSED')
                    break

                response = json.dumps({'status': 200 if bool_response else 404, "message": message})
                client_socket.sendall(response.encode())
                print(f'Sent "{response}" to {client_address}')
            
            except Exception as e:
                client_socket.close()
                print(f'Connection from {client_address} CLOSED')
                break

if __name__ == "__main__":
    main()
