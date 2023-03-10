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


def add_value(session, data):
    session = database.get_session()
    name = data["name"]
    population = data["population"]
    ethnicity = data["ethnicity"]
    founding_year = data["founding_year"]
    in_war = data["in_war"]
    return database.add_value_to_db(session, name, population, ethnicity, founding_year, in_war)
                

if __name__ == "__main__":
    server_socket = create_server_socket("localhost", 1234)
    while True:
        print('Waiting for a connection')
        client_socket, client_address = server_socket.accept()
        print(f'Connection from {client_address}')
        
        while True:
            try:
                # Receiving
                print("waiting for data from the client")
                client_socket.settimeout(10.0)
                data = client_socket.recv(BUFFER_SIZE)
                data = json.loads(data.decode())
                print(f'Received "{data}" from {client_address} OPENED')
                choice = data["choice"]
                session = database.get_session()

                if (choice == 1):
                    print("Client choose to add a country")
                    bool_response = add_value(session, data)
                    message = "Added value to db" if bool_response else "Value was already in db"

                elif (choice == 2):
                    print("Client choose to get all countries")
                    countries = [x.to_dict() for x in list(database.get_all_countries(session))]
                    bool_response = True if len(countries) > 0 else False
                    message = "Countries matched - "
                    for country in countries:
                        message += str(country)
                        message += " "

                elif (choice == 3):
                    print("Client choose to get a specific country")
                    country = list(database.get_country_by_name(session,data["name"]))
                    bool_response = True if len(country) > 0 else False
                    message = f"Country matched - {country[0].to_dict()}"

                elif (choice == 4):
                    print("Client choose to get all countries by a specific ethnicity")
                    countries = [x.to_dict() for x in list(database.get_countries_by_ethnicity(session, data["ethnicity"]))]
                    bool_response = True if len(countries) > 0 else False
                    message = "Countries matched - "
                    for country in countries:
                        message += str(country)
                        message += " "

                elif (choice == 5):
                    print("Client choose to get all countries by a specific war status")
                    countries = [x.to_dict() for x in list(database.get_counties_by_war_status(session, data["war_status"]))]
                    bool_response = True if len(countries) > 0 else False
                    message = "Countries matched - "
                    for country in countries:
                        message += str(country)
                        message += " "

                elif (choice == 6):
                    print("Client choose to get all countries with population over number")
                    countries = [x.to_dict() for x in list(database.get_counties_with_population_over_number(session, data["number"]))]
                    bool_response = True if len(countries) > 0 else False
                    message = "Countries matched - "
                    for country in countries:
                        message += str(country)
                        message += " "

                elif (choice == 7):
                    print("Client choose to get all countries that founded after year")
                    countries = [x.to_dict() for x in list(database.get_counties_with_population_over_number(session, data["year"]))]
                    bool_response = True if len(countries) > 0 else False
                    message = "Countries matched - "
                    for country in countries:
                        message += str(country)
                        message += " "

                elif (choice == 8):
                    print("Client choose to change a country's name")
                    bool_response = database.change_country_name(session, data["old_name"], data["new_name"])
                    message = "Changed value" if bool_response else "Couldn't change value"

                elif (choice == 9):
                    print("Client choose to change a country's war status")
                    bool_response = database.change_country_war_status(session, data["name"], data["new_in_war"])
                    message = "Changed value" if bool_response else "Couldn't change value"

                elif (choice == 10):
                    print("Client choose to change a country's population")
                    bool_response = database.change_country_war_status(session, data["name"], data["new_population"])
                    message = "Changed value" if bool_response else "Couldn't change value"
                else:
                    client_socket.close()
                    print(f'Connection from {client_address} CLOSED')
                    break

                # Response
                response = json.dumps({'status': bool_response, "message": message})
                client_socket.sendall(response.encode())
                print(f'Sent "{response}" to {client_address}')
            
            except Exception as e:
                client_socket.close()
                print(f'Connection from {client_address} CLOSED')
                break
