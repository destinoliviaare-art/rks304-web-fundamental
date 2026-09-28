import socket
import sys

from scanner import TCPPortScanner
from report import PDFReportExporter, JSONReportExporter


def main():
    print("=== APLIKASI PORT SCANNER & EXPORTER (OOP) ===")
    target = input("Masukkan IP atau Domain target (contoh: 127.0.0.1): ").strip()

    try:
        start = int(input("Masukkan port awal (contoh: 1): "))
        end = int(input("Masukkan port akhir (contoh: 1024): "))
    except ValueError:
        print("[!] Masukkan angka port yang valid.")
        sys.exit(1)

    scanner = TCPPortScanner(target, start, end, timeout=0.4)

    try:
        scanner.resolve_host()
    except socket.gaierror:
        print("\n[!] Host tidak dapat diselesaikan. Periksa kembali nama/IP target.")
        sys.exit(1)

    scanner.scan()

    safe_target = target.replace('.', '_')
    exporters = [
        PDFReportExporter(scanner, f"scan_report_{safe_target}.pdf"),
        JSONReportExporter(scanner, f"scan_report_{safe_target}.json"),
    ]

    # Polimorfisme: export() dipanggil seragam, hasilnya beda per class
    for exporter in exporters:
        exporter.export()


if __name__ == "__main__":
    main()