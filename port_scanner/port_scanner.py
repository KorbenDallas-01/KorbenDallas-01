import socket
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime


def scan_port(target, port, timeout):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)

            result = sock.connect_ex((target, port))

            if result == 0:
                try:
                    service = socket.getservbyport(port, "tcp")
                except OSError:
                    service = "unknown"

                return port, service

    except socket.error:
        pass

    return None


def main():
    parser = argparse.ArgumentParser(description="Simple multi-threaded port scanner")
    parser.add_argument("target", help="Target host, for example 127.0.0.1")
    parser.add_argument("--start", type=int, default=1, help="Start port")
    parser.add_argument("--end", type=int, default=1024, help="End port")
    parser.add_argument("--timeout", type=float, default=1.0, help="Timeout in seconds")
    parser.add_argument("--threads", type=int, default=100, help="Number of threads")

    args = parser.parse_args()

    print(f"Target: {args.target}")
    print(f"Ports: {args.start}-{args.end}")
    print(f"Threads: {args.threads}")
    print(f"Start time: {datetime.now()}")
    print("-" * 60)

    open_ports = []

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = []

        for port in range(args.start, args.end + 1):
            futures.append(
                executor.submit(scan_port, args.target, port, args.timeout)
            )

        for future in as_completed(futures):
            result = future.result()

            if result:
                port, service = result
                open_ports.append((port, service))
                print(f"[OPEN] Port {port} | Service: {service}")

    print("-" * 60)
    print("Scan finished")

    if open_ports:
        open_ports.sort()

        print(f"Open ports found: {len(open_ports)}")

        for port, service in open_ports:
            print(f"{port}/tcp - {service}")
    else:
        print("No open ports found")


if __name__ == "__main__":
    main()
