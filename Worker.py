import socket

def main():
    server_ip = "127.0.0.1"  # Replace with the server IP
    server_port = 12345  # Replace with the server port

    worker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        try:
            print("Attempting to connect to the server...")
            worker_socket.connect((server_ip, server_port))
            print("Connected to the server.")
            break
        except ConnectionRefusedError:
            print("Connection to the server failed. Retrying...")

    data = worker_socket.recv(1024)  # Adjust the buffer size as needed

    if not data:
        print("No data received from the server.")
        worker_socket.close()
        return

    data_str = data.decode('utf-8')
    target_password, character_set = data_str.split(',')

    found = False

    for password_attempt in generate_password_combinations(character_set, target_password):
        print(f"Testing combination: {password_attempt}")
        if password_attempt == target_password:
            print(f"Password found: {password_attempt}")
            found = True
            break

    result = "Password found" if found else "Password not found"
    try:
        # Send the result to the server
        worker_socket.send(result.encode('utf-8'))

        # Wait for the server to acknowledge the result
        server_acknowledgment = worker_socket.recv(1024)

        worker_socket.close()
    except:(print('Connection has been terminated by host!'))

def generate_password_combinations(character_set, target_password):
    from itertools import product
    for combination in product(character_set, repeat=len(target_password)):
        yield ''.join(combination)

if __name__ == "__main__":
    main()
