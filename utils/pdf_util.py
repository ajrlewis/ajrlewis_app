from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def register_fonts():
    font_name_to_file = {
        "CMUTypewriter-Light": "cmunbtl.ttf",
        "CMUTypewriter-LightOblique": "cmunbto.ttf",
        "CMUTypewriter-Regular": "cmuntt.ttf",
        "CMUTypewriter-Italic": "cmunit.ttf",
        "CMUTypewriter-Bold": "cmunrm.ttf",
        "CMUTypewriter-Oblique": "cmunst.ttf",
        "CMUTypewriter-BoldItalic": "cmuntx.ttf",
    }
    for font_name, font_file in font_name_to_file.items():
        font = TTFont(font_name, f"static/fonts/cm-unicode-0.7.0/{font_file}")
        pdfmetrics.registerFont(font)


register_fonts()


class PDF:
    def __init__(self):
        # The canvas should be thought of as a sheet of white paper with points on the sheet identified using Cartesian
        # (X,Y) coordinates which by default have the (0,0) origin point at the lower left corner of the page.
        # Furthermore the first coordinate x goes to the right and the second coordinate y goes up, by default.
        # A simple example program that uses a can

        self._width, self._height = letter

        self._x_margin = 0.05 * self._width
        self._y_margin = 0.05 * self._height

        self._x = self._x_margin
        self._y = self._height - self._y_margin

        self._buffer = BytesIO()
        # self._canvas = canvas.Canvas(self._buffer, pagesize=letter)
        self._canvas = canvas.Canvas("canvas.pdf", pagesize=letter)

        self.the_section = 0
        self.the_subsection = 0

    def within_bottom(self) -> bool:
        return self._y + self._line_height > 0.0

    def set_font(self, name: str = "CMUTypewriter-Regular", size: int = 12):
        self._canvas.setFont(name, size)

    def section(self, name: str):
        self.the_section += 1
        self.the_subsection = 0
        self.set_font("CMUTypewriter-Bold", 12)
        self._canvas.drawString(self._x, self._y, f"{self.the_section}  {name}")
        self.line_break(scale=2.2)

    def subsection(self, name: str):
        self.the_subsection += 1
        self.set_font("CMUTypewriter-Bold", 12)
        self._canvas.drawString(
            self._x, self._y, f"{self.the_section}.{self.the_subsection}  {name}"
        )
        self.line_break(scale=2.2)

    def line_break(self, font_size: int = 12, scale: float = 1.2):
        self._x = self._x_margin
        self._y -= font_size * scale

    def page_break(self):
        self._canvas.showPage()
        self._x = self._left_margin
        self._y = self._height - self._top_margin
        self._add_header()

    def save(self):
        self._canvas.save()

    def to_bytes(self):
        pdf = self._buffer.getvalue()
        self._buffer.close()
        return pdf


def create(title: str = ""):
    pdf = PDF()
    import os
    import reportlab

    pdf.section("Project Details")
    pdf.subsection("Title")
    pdf.save()

    # return pdf.to_bytes()


def main():
    pdf = create()
    # print(f"{pdf = }")
    print(pdf)


if __name__ == "__main__":
    main()
