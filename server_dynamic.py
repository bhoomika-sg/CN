import socket
import logging
import signal
import sys
import threading
import re

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def resolve_domain(domain_name):

    try:
        ip_address = socket.gethostbyname(domain_name)
        return ip_address
    except socket.gaierror:
        return "Domain not found"


def is_valid_domain(domain_name):
    pattern = r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.[A-Za-z]{2,6}$"
    return re.match(pattern, domain_name)


def handle_client(data, client_address, sock):

    try:
        domain_name = data.decode().strip()
        logging.info(f"Received query for: {domain_name} from {client_address}")

        if not is_valid_domain(domain_name):
            response = "Invalid domain name"
            logging.warning(f"Invalid query from {client_address}: {domain_name}")
        else:
            response = resolve_domain(domain_name)

        sock.sendto(response.encode(), client_address)
        logging.info(f"Sent response: {response} to {client_address}")

    except Exception as e:
        logging.error(f"An error occurred while handling {client_address}: {e}")



server_ip = "0.0.0.0"
port = 12345


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((server_ip, port))


def shutdown_server(signal, frame):
    logging.info("Shutting down server...")
    sock.close()
    sys.exit(0)


signal.signal(signal.SIGINT, shutdown_server)
logging.info(f"DNS server running on {server_ip}:{port}...")

while True:
    try:
        data, client_address = sock.recvfrom(512)
        logging.info(f"Received data from {client_address}")

        client_thread = threading.Thread(target=handle_client, args=(data, client_address, sock))
        client_thread.daemon = True
        client_thread.start()

    except Exception as e:
        logging.error(f"Error in main loop: {e}")
