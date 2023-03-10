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


if __name__ == "__main__":

    client_socket = connect_to_server("localhost", 1234)
        
    if client_socket != None:
        print("Welcome to the client side !")
        while True:
            print("Menu of options:\n 1.Add a country\n 2.Get all countries\n 3.Get a specific country\n \
4.Get all countries by a specific ethnicity\n 5.Get all countries by a specific war status\n \
6.get all countries with population over number\n 7.Get all countries that founded after year\n \
8.Change a country's name\n 9.Change a country's war status\n 10.Change a country's population")
            
            try:
                choice = int(input("please choose your option: "))
                if (choice == 1):
                    name = input("Please enter the country's name: ")
                    population = int(input("Please enter the country's population: "))
                    ethnicity = input("Please enter the country's ethnicity: ")
                    founding_year = int(input("Please enter the country's founding_year: "))
                    in_war_prompt = input("Please enter the country's war status (True or False): ")
                    in_war = True if in_war_prompt == "True" else False
                    request = json.dumps({"choice": choice, "name": name, "population": population,
                                        "ethnicity":ethnicity, "founding_year": founding_year,
                                        "in_war": in_war})
                if (choice == 1):
                    pass
                if (choice == 1):
                    pass
                if (choice == 1):
                    pass
                if (choice == 1):
                    pass
                if (choice == 1):
                    pass
                else:
                    break

                client_socket.sendall(request.encode())
                
                client_socket.settimeout(10.0)
                data = client_socket.recv(BUFFER_SIZE)
                data = json.loads(data.decode())
                print(data)

            except Exception as e:
                client_socket.close()

        client_socket.close()