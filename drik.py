import pyfiglet
import socket
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

# ---------------- BANNER ----------------
banner = pyfiglet.figlet_format("DRIK")
for line in banner.split("\n"):
    print(line)
    time.sleep(0.03)

# ---------------- INPUT ----------------
target_input = input("\nEnter IP address or hostname: ")

try:
    target = socket.gethostbyname(target_input)
except socket.gaierror:
    print("Hostname could not be resolved")
    exit()

# ---------------- SCAN TYPE ----------------
print("\nSelect Scan Type:")
print("1. Quick Scan (1-1000)")
print("2. Full Scan (1-65535)")
print("3. Custom Range")

choice = input("Enter choice (1/2/3): ")

if choice == "1":
    ports = range(1, 1001)
elif choice == "2":
    ports = range(1, 65536)
else:
    start = int(input("Start Port: "))
    end = int(input("End Port: "))
    ports = range(start, end + 1)

TOTAL_PORTS = len(ports)

print("-" * 60)
print("Target          :", target)
print("Scan started at :", datetime.now())
print("-" * 60)

# ---------------- GLOBALS ----------------
open_ports = []
scanned = 0
lock = Lock()

start_time = datetime.now()

# ---------------- TCP SCAN ----------------
def scan_port(port):
    global scanned

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)

    try:
        result = s.connect_ex((target, port))

        if result == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "unknown"

            open_ports.append((port, service))
            print(f"\n[TCP] {port:<5} OPEN ({service})")

    except:
        pass

    finally:
        s.close()

        with lock:
            scanned += 1
            if scanned % 500 == 0 or scanned == TOTAL_PORTS:
                percent = (scanned / TOTAL_PORTS) * 100
                print(f"\rProgress: {scanned}/{TOTAL_PORTS} ({percent:.1f}%)", end="")

# ---------------- RUN SCAN ----------------
try:
    with ThreadPoolExecutor(max_workers=200) as executor:
        executor.map(scan_port, ports)

except KeyboardInterrupt:
    print("\nScan stopped by user")
    exit()

# ---------------- SAVE RESULTS ----------------
with open("drik_results.txt", "w") as f:
    for port, service in open_ports:
        f.write(f"{port} OPEN ({service})\n")

# ---------------- SUMMARY ----------------
end_time = datetime.now()

print("\n" + "-" * 60)
print("Scan finished at :", end_time)
print("Total time       :", end_time - start_time)
print("Open ports       :", len(open_ports))
print("Results saved to : drik_results.txt")
print("-" * 60)
