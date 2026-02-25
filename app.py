from flask import Flask, render_template, request
import socket
import threading
import csv
import os

app = Flask(__name__)
RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

# Common ports to protocol mapping for better detection
PROTOCOLS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3389: "RDP",
}

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    if request.method == "POST":
        targets_input = request.form["targets"]
        start = int(request.form["start"])
        end = int(request.form["end"])
        scan_type = request.form["scan_type"]
        export_type = request.form["export_type"]

        targets = [t.strip() for t in targets_input.split(",")]
        all_results = []

        def scan_port(target, port):
            s = None
            try:
                if scan_type == "TCP":
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(1)
                    if s.connect_ex((target, port)) == 0:
                        service = PROTOCOLS.get(port, "Unknown")
                        try:
                            s.send(b"\n")
                            banner = s.recv(1024).decode().strip()
                        except:
                            banner = "No banner"
                        all_results.append(f"{target},{port},TCP,{service},{banner}")
                elif scan_type == "UDP":
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    s.settimeout(1)
                    s.sendto(b"\n", (target, port))
                    try:
                        data, _ = s.recvfrom(1024)
                        banner = data.decode().strip()
                    except:
                        banner = "No banner"
                    service = PROTOCOLS.get(port, "Unknown")
                    all_results.append(f"{target},{port},UDP,{service},{banner}")
            except:
                pass
            finally:
                if s:
                    s.close()

        threads = []
        for target in targets:
            for port in range(start, end + 1):
                t = threading.Thread(target=scan_port, args=(target, port))
                threads.append(t)
                t.start()

        for t in threads:
            t.join()

        if all_results:
            result = all_results 
        else:
            result = ["No open ports found."]

        # Export
        if export_type != "None" and all_results:
            filename = f"{RESULTS_DIR}/scan_results.{export_type.lower()}"
            if export_type == "TXT":
                with open(filename, "w") as f:
                    f.write("\n".join(all_results))
            elif export_type == "CSV":
                with open(filename, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Target","Port","Protocol","Service","Banner"])
                    for line in all_results:
                        writer.writerow(line.split(","))
            result += f"\n\nResults exported to {filename}"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)