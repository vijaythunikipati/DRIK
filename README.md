# DRIK Port Scanner

DRIK is a simple Python-based port scanner used to find open ports on a target system.  
It is designed for learning networking and basic cybersecurity concepts.

---

## Features

- Scans TCP ports to find open ports
- Multi-threaded scanning for better speed
- Supports IP address and hostname input
- Multiple scan types:
  - Quick Scan (1–1000 ports)
  - Full Scan (1–65535 ports)
  - Custom port range
- Detects common services (HTTP, SSH, etc.)
- Shows scan progress
- Saves results to a file (drik_results.txt)
- Displays total scan time
- Handles errors properly

---

## Requirements

python3
- Install required module:
  
  pip3 install pyfiglet

---

## How to Run

python3 portscanner.py

Then enter:
- Target IP or hostname
- Select scan type

---

## Example Output

[TCP] 22 OPEN (ssh)  
[TCP] 80 OPEN (http)  
[TCP] 443 OPEN (https)

---

## Output File

Scan results are saved in:
drik_results.txt

---

## Note

This tool is for learning purposes only.  
Do not scan systems without permission.

---

## Author

Vijaykanth Thunikipati
