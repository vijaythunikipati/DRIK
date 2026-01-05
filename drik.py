import pyfiglet
import socket
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

# ---------------- BANNER ----------------
banner = pyfiglet.figlet_format("DRIK")
for line in banner.split("\n"):
    print(line)
    time.sleep(0.03)

# ---------------- INPUT ----------------
target_input = input("\nEnter IP address or hostname to scan: ")

try:
    target = socket.gethostbyname(target_input)
except socket.gaierror:
    print("Hostname could not be resolved")
    exit()

print("-" * 60)
print("Target          :", target)
print("Scan started at :", datetime.now())
print("-" * 60)

# ---------------- GLOBALS ----------------
TOTAL_TCP_PORTS = 65535
scanned_ports = 0
lock = Lock()

open_tcp = []
closed_tcp = []
filtered_tcp = []

# ---------------- TCP SCAN ----------------
def tcp_scan(port):
    global scanned_ports

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)

    try:
        result = s.connect_ex((target, port))

        if result == 0:
            state = "OPEN"
            open_tcp.append(port)
        elif result == 111 or result == 10061:
            state = "CLOSED"
            closed_tcp.append(port)
        else:
            state = "FILTERED"
            filtered_tcp.append(port)

    except:
        state = "FILTERED"
        filtered_tcp.append(port)

    finally:
        s.close()

        with lock:
            scanned_ports += 1
            if scanned_ports % 1000 == 0 or scanned_ports == TOTAL_TCP_PORTS:
                percent = (scanned_ports / TOTAL_TCP_PORTS) * 100
                print(f"\rProgress: {scanned_ports}/{TOTAL_TCP_PORTS} ({percent:.1f}%)", end="")

    return port, state

# ---------------- UDP SCAN (COMMON PORTS) ----------------
def udp_scan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(1)

    try:
        s.sendto(b"\x00", (target, port))
        s.recvfrom(1024)
        print(f"\n[UDP] {port:<5} OPEN")
    except socket.timeout:
        print(f"\n[UDP] {port:<5} OPEN|FILTERED")
    except:
        pass
    finally:
        s.close()

# ---------------- EXECUTION ----------------
try:
    print("\n[+] Starting FULL TCP Scan (1–65535)\n")

    with ThreadPoolExecutor(max_workers=200) as executor:
        futures = [executor.submit(tcp_scan, port) for port in range(1, 65536)]
        for _ in as_completed(futures):
            pass

    print("\n\n[+] TCP Scan Results")
    print("-" * 60)
    for p in open_tcp:
        print(f"[TCP] {p:<5} OPEN")

    print("\n[+] Starting UDP Scan (Common Ports)\n")
    udp_ports = [53, 67, 68, 69, 123, 161, 500, 514]
    with ThreadPoolExecutor(max_workers=30) as executor:
        executor.map(udp_scan, udp_ports)

except KeyboardInterrupt:
    print("\nScan stopped by user")
    exit()

# ---------------- SUMMARY ----------------
print("\n" + "-" * 60)
print("Scan finished at :", datetime.now())
print("OPEN TCP ports   :", len(open_tcp))
print("CLOSED TCP ports :", len(closed_tcp))
print("FILTERED TCP     :", len(filtered_tcp))
print("-" * 60)

