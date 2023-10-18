import socket
import time
import threading

def main():
    target_password = "a234"  # Password to find (you can set it here)
    num_workers = 2  # Number of worker threads


    stop_event = threading.Event()  # Event to signal workers to stop searching
    result_event = threading.Event()  # Event to signal password found

    server_stop_event = threading.Event()  # Event to signal the server to stop

    results = []
    worker_sockets = []

    # Create a socket server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("127.0.0.1", 12345)  # Replace with your server IP and port
    server_socket.bind(server_address)
    server_socket.listen(num_workers)

    character_sets = [
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ]
    start_time = time.time()
    threads = []
    # Send the data to the worker threads
    for _ in range(num_workers):
        worker_socket, _ = server_socket.accept()
        worker_sockets.append(worker_socket)

    for i, (worker_socket, character_set) in enumerate(zip(worker_sockets, character_sets)):
        print(f"Worker {i + 1} is testing password with character set: {character_set}")

        # Send data to the worker
        data = f"{target_password},{character_set}"
        worker_socket.send(data.encode('utf-8'))

        thread = threading.Thread(target=worker_thread, args=(worker_socket, results, stop_event, result_event, server_socket, worker_sockets, server_stop_event))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    found = result_event.is_set()

    server_socket.close()

    end_time = time.time()
    elapsed_time = end_time - start_time

    if found:
        print(f"Password found: {target_password}")
        # When password is found, signal all workers to stop searching
        stop_event.set()
        server_stop_event.set()
    else:
        print("Password not found.")

    print(f"Time elapsed: {elapsed_time} seconds")

def worker_thread(worker_socket, results, stop_event, result_event, server_socket, worker_sockets, server_stop_event):
    try:
        while not stop_event.is_set():
            data = worker_socket.recv(1024)  # Adjust the buffer size as needed

            if not data:
                print("No data received from the server.")
                return

            data_str = data.decode('utf-8')
            result = data_str

            results.append(result)

            if result == "Password found":
                stop_event.set()
                result_event.set()
                server_stop_event.set()
                for i in worker_sockets:
                    i.close()
                break
    except:print('Password has been')

if __name__ == "__main__":
    main()
