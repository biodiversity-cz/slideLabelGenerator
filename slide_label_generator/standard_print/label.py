from reportlab.platypus.flowables import Flowable
from reportlab.lib.units import mm
import qrcode
from io import BytesIO
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

class Label(Flowable):
    def __init__(self, text_lines, width, height, padding=2*mm):
        super().__init__()
        self.id = text_lines['id']
        self.pid = text_lines['pid']
        self.taxon = text_lines['taxon']
        self.line_1 = text_lines.get('line_1')
        self.line_2 = text_lines.get('line_2')
        self.line_3 = text_lines.get('line_3')
        self.width = width
        self.height = height
        self.padding = padding
        self.font = 'DejaVuSans'
        self.font_italic = 'DejaVuSans-Oblique'
        pdfmetrics.registerFont(TTFont(self.font,  "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
        pdfmetrics.registerFont(TTFont(self.font_italic,  "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf"))

    def draw(self):

        c = self.canv
        x0, y0 = 1, 1

        # Okraj štítku
        c.rect(x0, y0, self.width, self.height)

        # Rozdělení prostoru: pravá část = ID, prostřední = PID, levá 2/3 = QR
        id_band_width = 4 * mm
        taxon_band_width = 4 * mm
        qr_width = self.width - id_band_width - taxon_band_width

        # Levý okraj QR části
        qr_x = x0 + self.padding
        qr_y = y0 + self.padding
        qr_size = min(qr_width - 2*self.padding, self.height - 2*self.padding)


        # Volitelné řádky nad QR
        c.setFont(self.font, 6)
        line_height = 2 * mm
        lines = [self.line_1, self.line_2, self.line_3]
        lines = [l for l in lines if l]  # jen neNone
        text_start_y = qr_y + qr_size + 1 * mm  # začátek nad QR
        text_center_x = qr_x + qr_size / 2
        for line in reversed(lines):  # vykreslíme odshora dolů
            c.drawCentredString(text_center_x, text_start_y, line)
            text_start_y += line_height

         # QR kód bez bílého rámečku
        qr = qrcode.QRCode(
            version=1,  # velikost QR
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=0  # <--- tady nastavíš "border" na 0
        )
        qr.add_data("https://example.com")
        qr.make(fit=True)

        qr = qr.make_image(fill_color="black", back_color="white")
        qr_io = BytesIO()
        qr.save(qr_io, format="PNG")
        qr_io.seek(0)

        qr_reader = ImageReader(qr_io)

        c.drawImage(
            qr_reader,
            qr_x,
            qr_y,
            width=qr_size,
            height=qr_size,
            preserveAspectRatio=True,
            mask='auto'
        )

        # 2️⃣ Svislá čára mezi QR a PID částí
        taxon_line_x = x0 + qr_width
        c.line(taxon_line_x, y0, taxon_line_x, y0 + self.height)

        # 3️⃣ Svislý text taxon
        c.saveState()
        c.translate(taxon_line_x + taxon_band_width/2, y0 + self.height/2)
        c.rotate(-90)
        c.setFont(self.font_italic, 7)
        text_width = c.stringWidth(self.taxon, self.font, 8)
        c.drawCentredString(0, -1 * mm, self.taxon)
        c.restoreState()

        # 4️⃣ Svislá čára mezi PID a ID částí
        id_line_x = taxon_line_x + taxon_band_width
        c.line(id_line_x, y0, id_line_x, y0 + self.height)

        # 5️⃣ Svislý text ID
        c.saveState()
        c.translate(id_line_x + id_band_width/2, y0 + self.height/2)
        c.rotate(-90)
        c.setFont(self.font, 9)
        c.drawCentredString(0, -1 * mm, self.id)
        c.restoreState()
