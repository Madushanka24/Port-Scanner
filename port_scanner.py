import socket
import threading

target = input("Enter target IP address: ")
start = int(input("Start port: "))
end = int(input("End port: "))

print(f"\nScanning {target} from port {start} to {end}...\n")

def scan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)

    if s.connect_ex((target, port)) == 0:
        print(f"Port {port} is OPEN")

    s.close()

for port in range(start, end + 1):
    thread = threading.Thread(target=scan, args=(port,))
    thread.start()

print("Scan started...\n")