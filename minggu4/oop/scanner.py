import socket
from abc import ABC, abstractmethod
from datetime import datetime


class BaseScanner(ABC):
    """Abstraksi: kontrak yang wajib dipenuhi semua jenis scanner."""

    def __init__(self, host, start_port, end_port):
        # Enkapsulasi: atribut private, diakses lewat property (read-only)
        self.__host = host
        self.__start_port = start_port
        self.__end_port = end_port
        self._open_ports = []  # protected: boleh diakses subclass

    @property
    def host(self):
        return self.__host

    @property
    def start_port(self):
        return self.__start_port

    @property
    def end_port(self):
        return self.__end_port

    @property
    def open_ports(self):
        return list(self._open_ports)

    @abstractmethod
    def scan(self):
        """Wajib diimplementasikan subclass."""
        pass


class TCPPortScanner(BaseScanner):
    """Pewarisan: scanner konkret untuk protokol TCP."""

    def __init__(self, host, start_port, end_port, timeout=0.4):
        super().__init__(host, start_port, end_port)
        self.__timeout = timeout
        self.__target_ip = None

    @property
    def target_ip(self):
        return self.__target_ip

    def resolve_host(self):
        """Menyelesaikan nama host menjadi alamat IP."""
        self.__target_ip = socket.gethostbyname(self.host)
        return self.__target_ip

    def scan(self):
        """Polimorfisme: implementasi scan() khusus TCP."""
        if self.__target_ip is None:
            self.resolve_host()

        self._open_ports = []

        print("-" * 50)
        print(f" Memindai Target IP: {self.__target_ip}")
        print(f" Rentang Port      : {self.start_port} - {self.end_port}")
        print(f" Waktu Mulai       : {str(datetime.now())}")
        print("-" * 50)

        try:
            for port in range(self.start_port, self.end_port + 1):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(self.__timeout)
                result = s.connect_ex((self.__target_ip, port))
                s.close()

                if result == 0:
                    print(f"[+] Port {port} : TERBUKA")
                    self._open_ports.append(port)

        except KeyboardInterrupt:
            print("\n[!] Pemindaian dibatalkan oleh pengguna (Ctrl+C).")

        print("-" * 50)
        print(f" Pemindaian Selesai. Total port terbuka ditemukan: {len(self._open_ports)}")
        print("-" * 50)

        return self.open_ports