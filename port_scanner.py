import socket

# Ask user for target
target = input("Enter target IP address: ")

# Ask for port range
start = int(input("Start port: "))
end = int(input("End port: "))

print(f"\nScanning {target} from port {start} to {end}...\n")

# Loop through port range
for port in range(start, end + 1):

    # Create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Set timeout (in seconds)
    s.settimeout(0.5)

    # Try connecting
    result = s.connect_ex((target, port))

    if result == 0:
        print(f"Port {port} is OPEN")

    # Close connection
    s.close()

print("\nScan complete.")