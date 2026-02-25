# Advanced Flask Web Port Scanner

A **web-based network port scanner** built with **Python and Flask**.  
This tool allows you to scan **TCP and UDP ports**, detect **services and banners**, scan **multiple targets**, export results, and view everything in a **beautiful web interface**.

---

## 🌐 Project Overview

This project is a **mini web-based Nmap clone** designed for learning networking, cybersecurity basics, and full-stack development.  

It scans one or multiple target IPs, checks which ports are open, detects common services (HTTP, FTP, SSH, etc.), grabs banners where possible, and displays results in a **color-coded table**.  

Results can also be exported as **TXT** or **CSV**.

---

## 🔥 Features

**Basic Features:**
- Target IP scanning
- Custom port range scanning
- TCP scanning
- UDP scanning

**Advanced Features Added:**
- Multiple targets scanning (comma-separated)
- Service detection (HTTP, FTP, SSH, SMTP, DNS, etc.)
- Banner grabbing for service information
- Multithreading for faster scans
- Export results to TXT or CSV
- Beautiful web interface with Bootstrap and CSS
- Loading spinner / progress feedback
- Color-coded table: green = open, red = closed

---

## 💻 Tech Stack

- **Python 3** – main programming language  
- **Flask** – web framework  
- **Socket module** – TCP/UDP scanning  
- **Threading** – concurrent scanning  
- **CSV/TXT** – export results  
- **HTML + CSS + Bootstrap 5** – professional UI  

---

## ⚡ How It Works

1. User enters:
   - Target IP(s)  
   - Port range  
   - Scan type (TCP/UDP)  
   - Export type (TXT/CSV)

2. Flask app performs multithreaded scanning:
   - Connects to each port
   - Detects open ports and service names
   - Grabs service banners (if available)

3. Results are displayed in a **color-coded table** and optionally exported.

4. 

https://github.com/user-attachments/assets/8497c6d1-08f8-4e35-bd3c-7e194b845933



---

## 📦 Installation & Setup

1. Clone the repository:

```bash
git clone <your-repo-link>
cd Port-Scanner-Flask
