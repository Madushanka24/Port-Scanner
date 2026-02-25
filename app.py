from flask import Flask, render_template, request
import socket
import threading
import csv
import os

app = Flask(__name__)
RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    if request.method == "POST":
        target = request.form["target"]
        start = int(request.form["start"])
        end = int(request.form["end"])
        scan_type = request.form["scan_type"]
        export_type = request.form["export_type"]

        open_ports = []

        def scan_tcp(port):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            try:
                if s.connect_ex((target, port)) == 0:
                    try:
                        service = socket.getservbyport(port)
                    except:
                        service = "Unknown"
                    try:
                        s.send(b"\n")
                        banner = s.recv(1024).decode().strip()
                    except:
                        banner = "No banner"
                    open_ports.append(f"{port},TCP,{service},{banner}")
            except:
                pass
            finally:
                s.close()

        def scan_udp(port):
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(1)
            try:
                s.sendto(b"\n", (target, port))
                data, _ = s.recvfrom(1024)
                service = "Unknown"
                banner = data.decode().strip()
                open_ports.append(f"{port},UDP,{service},{banner}")
            except socket.timeout:
                # UDP often doesn't respond
                pass
            except:
                pass
            finally:
                s.close()

        threads = []
        for port in range(start, end + 1):
            if scan_type == "TCP":
                t = threading.Thread(target=scan_tcp, args=(port,))
            else:
                t = threading.Thread(target=scan_udp, args=(port,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        if open_ports:
            result = "\n".join(open_ports)
        else:
            result = "No open ports found."

        # Export results
        if export_type != "None" and open_ports:
            filename = f"{RESULTS_DIR}/scan_{target}_{scan_type}.{export_type.lower()}"
            if export_type == "TXT":
                with open(filename, "w") as f:
                    f.write("\n".join(open_ports))
            elif export_type == "CSV":
                with open(filename, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Port","Protocol","Service","Banner"])
                    for line in open_ports:
                        writer.writerow(line.split(","))
            result += f"\n\nResults exported to {filename}"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)