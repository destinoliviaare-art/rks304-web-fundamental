import json
from abc import ABC, abstractmethod
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


class BaseReportExporter(ABC):
    """Abstraksi: antarmuka untuk semua jenis exporter laporan."""

    def __init__(self, scanner, filename):
        # Enkapsulasi: data pemindai dan nama berkas dibuat private
        self.__scanner = scanner
        self.__filename = filename

    @property
    def scanner(self):
        return self.__scanner

    @property
    def filename(self):
        return self.__filename

    @staticmethod
    def _estimate_service(port):
        if port in (80, 443):
            return "HTTP/HTTPS"
        if port == 22:
            return "SSH"
        if port == 21:
            return "FTP"
        return "Lainnya/Custom"

    @abstractmethod
    def export(self):
        """Wajib diimplementasikan subclass."""
        pass


class PDFReportExporter(BaseReportExporter):
    def export(self):
        sc = self.scanner
        doc = SimpleDocTemplate(self.filename, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1a365d'),
            spaceAfter=12,
            alignment=1
        )
        normal_style = styles['Normal']

        story.append(Paragraph("Laporan Hasil Pemindaian Port (Port Scanner)", title_style))
        story.append(Spacer(1, 12))

        summary_data = [
            [Paragraph("<b>Target Host:</b>", normal_style), Paragraph(sc.host, normal_style)],
            [Paragraph("<b>Target IP:</b>", normal_style), Paragraph(sc.target_ip, normal_style)],
            [Paragraph("<b>Rentang Port:</b>", normal_style), Paragraph(f"{sc.start_port} - {sc.end_port}", normal_style)],
            [Paragraph("<b>Waktu Eksekusi:</b>", normal_style), Paragraph(str(datetime.now()), normal_style)],
        ]

        summary_table = Table(summary_data, colWidths=[120, 380])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f7fafc')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e0')),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 15))

        story.append(Paragraph("<b>Daftar Port Terbuka</b>", styles['Heading2']))
        story.append(Spacer(1, 6))

        if sc.open_ports:
            data = [["Port", "Status", "Layanan Umum (Estimasi)"]]
            for p in sc.open_ports:
                data.append([str(p), "TERBUKA", self._estimate_service(p)])

            p_table = Table(data, colWidths=[100, 150, 250])
            p_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2b6cb0')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ffffff')),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
                ('PADDING', (0, 0), (-1, -1), 6),
            ]))
            story.append(p_table)
        else:
            story.append(Paragraph("Tidak ada port terbuka yang ditemukan pada rentang tersebut.", normal_style))

        doc.build(story)
        print(f"[+] Laporan berhasil dieksport ke PDF: {self.filename}")


class JSONReportExporter(BaseReportExporter):
    def export(self):
        sc = self.scanner
        data = {
            "target_host": sc.host,
            "target_ip": sc.target_ip,
            "port_range": {
                "start": sc.start_port,
                "end": sc.end_port
            },
            "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_open_ports": len(sc.open_ports),
            "open_ports": [
                {
                    "port": p,
                    "status": "OPEN",
                    "estimated_service": self._estimate_service(p)
                }
                for p in sc.open_ports
            ]
        }

        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"[+] Laporan berhasil dieksport ke JSON: {self.filename}")