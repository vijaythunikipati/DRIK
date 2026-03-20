# DRIK Port Scanner

DRIK is a Python-based multi-threaded port scanner used to identify open ports and running services on a target system.  
It supports both TCP and basic UDP scanning and is designed for learning networking and cybersecurity concepts.

---

## Features

- Scans TCP ports to identify open ports
- Basic UDP scanning for common ports
- Multi-threaded scanning for faster performance
- Supports IP address and hostname input
- Multiple scan types:
  - Quick Scan (1–1000 ports)
  - Full Scan (1–65535 ports)
  - Custom port range
- Detects common services (HTTP, SSH, DNS, etc.)
- Displays real-time scan progress
- Saves results to a file (drik_results.txt)
- Shows total scan time
- Animated banner using pyfiglet
- Handles errors and interruptions properly

---

## Requirements

- Python 3
- Install required module:

pip install pyfiglet

---

## How to Run

python3 portscanner.py

Then:
- Enter target IP or hostname
- Select scan type

---

## Example Output

[TCP] 22 OPEN (ssh)  
[TCP] 80 OPEN (http)  
[TCP] 443 OPEN (https)  

[UDP] 53 OPEN (domain)  
[UDP] 123 OPEN|FILTERED (ntp)

---

## Output File

Scan results are saved in:
drik_results.txt

---

## Note

This tool is created for learning and educational purposes only.  
Do not scan systems without permission.

---

## Author

Vijaykanth Thunikipati
