import socket
import threading
import logging

# Configuration
TARGET = "scanme.nmap.org"  # Change to the target IP or domain
PORT_RANGE = (1, 1024)  # Change the port range if needed
NUM_THREADS = 50  # Adjust based on performance
LOG_FILE = "port_scan_results.txt"

# Configure logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

def scan_port(port):
    """Attempts to connect to a given port and logs if it's open."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)  # Set timeout for connection attempt
        if s.connect_ex((TARGET, port)) == 0:
            message = f"[+] Port {port} is open"
            print(message)
            logging.info(message)

def start_scan():
    """Starts the port scanning using threading."""
    print(f"[*] Scanning {TARGET} from port {PORT_RANGE[0]} to {PORT_RANGE[1]}")
    threads = []
    
    for port in range(PORT_RANGE[0], PORT_RANGE[1] + 1):
        thread = threading.Thread(target=scan_port, args=(port,))
        threads.append(thread)
        thread.start()
        
        if len(threads) >= NUM_THREADS:
            for t in threads:
                t.join()
            threads = []

    for t in threads:
        t.join()

    print("[*] Scan complete. Results saved to", LOG_FILE)

if __name__ == "__main__":
    start_scan()
