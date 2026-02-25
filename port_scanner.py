import socket

# Ask user for target
target = input("Enter target IP address: ")

print(f"\nScanning {target}...\n")

# Loop through ports
for port in range(1, 1025):

    # Create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Set timeout
    s.settimeout(0.5)

    # Try connecting
    result = s.connect_ex((target, port))

    if result == 0:
        print(f"Port {port} is OPEN")

    s.close()