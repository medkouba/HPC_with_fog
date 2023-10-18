# Password Cracking Server

This is a simple multi-threaded server and client implementation for password cracking. The server distributes password-cracking tasks to multiple worker threads, and the workers attempt to find a specific target password using character sets.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Configuration](#configuration)


## Prerequisites

- Python 3.x (server and worker)
- A working network connection between the server and worker(s)

## Usage

1. Clone the repository to your local machine:

    ```sh
    git clone https://github.com/yourusername/password-cracking-server.git
    cd password-cracking-server
    ```

2. Modify the `server.py` and `worker.py` to set your target password and configure character sets if needed.

3. Run the server:

    ```sh
    python server.py
    ```

4. Run the worker(s) on other machines or terminals:

    ```sh
    python worker.py
    ```

5. Wait for the server to distribute tasks to the workers. When a worker finds the password, the server will terminate all workers gracefully.

## Configuration

- `server.py`: Modify the `target_password` and character sets as needed.
- `worker.py`: Modify the `server_ip` and `server_port` to match the server's IP and port.

You can customize the character sets and other parameters in both files to fit your specific use case.
