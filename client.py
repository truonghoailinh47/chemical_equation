#!/usr/bin/env python3

import socket

def send_equation(reactants, products, server_ip='127.0.0.1', port=65432):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port))

    # Prepare the data to send (reactants and products as comma-separated strings)
    data = ",".join(reactants) + "|" + ",".join(products)
    print("Sending data:", data)
    client_socket.sendall(data.encode())

    # Receive the balanced equation from the server
    balanced_equation = client_socket.recv(1024).decode()
    print("Balanced Equation:", balanced_equation)

    client_socket.close()

if __name__ == "__main__":
    reactants = ["H2", "O2"]
    products = ["H2O"]
    send_equation(reactants, products)
