import socket
import time
import uuid


# Get the website IP to access from the user
destination_ip = input("Enter the website IP you want to access: ")

# Create a socket for communication with the proxy server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the proxy server
proxy_ip = "127.0.0.1"
proxy_port = 5023
try:
    client_socket.connect((proxy_ip, proxy_port))
except ConnectionRefusedError:
    print("Error: Unable to connect to proxy server at", proxy_ip, ":", proxy_port)
    client_socket.close()
    exit()

# Send the request to the proxy server
request = "GET http://" + destination_ip + " HTTP/1.1\r\nHost: " + destination_ip + "\r\nConnection: close\r\n\r\n"
start_time = time.time()
client_socket.send(request.encode())
print("Request sent to proxy server at", time.ctime(start_time))

# Receive the reply from the proxy server
try:
    response = client_socket.recv(4096)
except ConnectionResetError:
    print("Error: Connection to proxy server was reset.")
    client_socket.close()
    exit()
end_time = time.time()
print("Response received from proxy server at", time.ctime(end_time))

# Display the reply to the user
print("\nResponse:")
print(response.decode())

# Calculate and display the total round-trip time
round_trip_time = end_time - start_time
print("\nTotal round-trip time:", round_trip_time, "seconds")

def get_mac_address():
    mac = hex(uuid.getnode()).replace('0x', '').upper()
    return ':'.join(mac[i:i + 2] for i in range(0, 11, 2))

# Display the MAC address of the client's physical machine
mac_address = get_mac_address()
print("\nMAC address:", mac_address)

# Close the socket
client_socket.close()
