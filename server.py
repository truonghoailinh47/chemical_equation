#!/usr/bin/env python3

import socket
from balancing import balance_equation

def handle_client(client_socket):
    try:
        # Receive the reactants and products from the client
        data = client_socket.recv(1024).decode()
        reactants, products = data.split('|')
        reactants = reactants.split(',')
        products = products.split(',')

        # Balance the chemical equation
        balanced_equation = balance_equation(reactants, products)

        # Send the balanced equation back to the client
        client_socket.sendall(balanced_equation.encode())
    finally:
        client_socket.close()

def start_server(host='0.0.0.0', port=65432):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server is listening on {host}:{port}...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address} has been established!")
        handle_client(client_socket)

if __name__ == "__main__":
    start_server()