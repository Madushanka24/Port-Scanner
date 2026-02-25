from flask import Flask, render_template, request
import socket
import threading

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    if request.method == "POST":
        target = request.form["target"]
        start = int(request.form["start"])
        end = int(request.form["end"])
        open_ports = []

        def scan(port):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            try:
                if s.connect_ex((target, port)) == 0:
                    try:
                        service = socket.getservbyport(port)
                    except:
                        service = "Unknown"
                    try:
                        s.send(b"\n")  # trigger banner for some services
                        banner = s.recv(1024).decode().strip()
                    except:
                        banner = "No banner"
                    open_ports.append(f"Port {port} OPEN ({service}) | Banner: {banner}")
            except:
                pass
            finally:
                s.close()

        threads = []
        for port in range(start, end + 1):
            t = threading.Thread(target=scan, args=(port,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        if open_ports:
            result = "\n".join(open_ports)
        else:
            result = "No open ports found."

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)