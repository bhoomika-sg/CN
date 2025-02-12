import socket

server_address = ('server_address', 12345)

# Creating a UDP client socket
client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    while True:

        query = input("Enter domain name to query (or 'exit' to quit): ")
        if query.lower() == "exit":
            print("Exiting client.")
            break


        client_sock.sendto(query.encode(), server_address)

        client_sock.settimeout(5)  # Set timeout
        try:
            response, _ = client_sock.recvfrom(512)
            print(f"Response: {response.decode()}")
        except socket.timeout:
            print("No response from server. Please try again.")
finally:
    client_sock.close()
