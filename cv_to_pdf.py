import os
import sys
import re
from fpdf import FPDF
from fpdf.enums import XPos, YPos

# ── Paths — update these for each new CV ───────────────────────────────
MD_FILE   = r"C:\Users\ADMIN\Desktop\Claude Code\.claude\commands\cv-builder\output\cv-NguyenThanhMai-2026-05-09.md"
PDF_FILE  = r"C:\Users\ADMIN\Desktop\Claude Code\.claude\commands\cv-builder\output\cv-NguyenThanhMai-2026-05-09.pdf"
# ───────────────────────────────────────────────────────────────────────

# Allow overriding paths via CLI: python cv_to_pdf.py input.md output.pdf
if len(sys.argv) == 3:
    MD_FILE  = sys.argv[1]
    PDF_FILE = sys.argv[2]
elif len(sys.argv) == 2:
    MD_FILE  = sys.argv[1]
    PDF_FILE = os.path.splitext(MD_FILE)[0] + ".pdf"

FONT_DIR  = r"C:\Windows\Fonts"

NAVY  = (0,   51,  102)
BLACK = (26,  26,  26)
GRAY  = (90,  90,  90)
WHITE = (255, 255, 255)
LGRAY = (200, 200, 200)

PHOTO_W   = 33   # mm — width of photo box
PHOTO_H   = 40   # mm — height of photo box
PHOTO_GAP = 6    # mm — gap between photo and text

NX, NY = XPos.LMARGIN, YPos.NEXT


class CV(FPDF):
    def header(self): pass
    def footer(self): pass

    def setup_fonts(self):
        self.add_font("Arial",  "",   f"{FONT_DIR}\\arial.ttf")
        self.add_font("Arial",  "B",  f"{FONT_DIR}\\arialbd.ttf")
        self.add_font("Arial",  "I",  f"{FONT_DIR}\\ariali.ttf")
        self.add_font("Arial",  "BI", f"{FONT_DIR}\\arialbi.ttf")

    def c(self, rgb):
        self.set_text_color(*rgb)

    def usable_w(self):
        return self.w - self.l_margin - self.r_margin

    def hline(self, color=LGRAY, thick=False):
        self.set_draw_color(*color)
        self.set_line_width(0.5 if thick else 0.2)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(2)

    def draw_photo_placeholder(self, x, y, w, h):
        """Draw a dashed placeholder box when no photo file is found."""
        self.set_draw_color(*LGRAY)
        self.set_line_width(0.3)
        self.set_dash_pattern(dash=2, gap=2)
        self.rect(x, y, w, h)
        self.set_dash_pattern()
        self.set_font("Arial", "I", 7.5)
        self.c(GRAY)
        self.set_xy(x, y + h/2 - 3)
        self.cell(w, 5, "Photo", align="C")

    # ── Heading helpers ────────────────────────────────────────────────

    def h1(self, text, col_w=0):
        w = col_w if col_w else self.usable_w()
        self.set_font("Arial", "B", 20)
        self.c(NAVY)
        self.cell(w, 10, text.upper(), new_x=NX, new_y=NY)
        self.ln(1)

    def h2(self, text):
        self.ln(3)
        self.set_font("Arial", "B", 10)
        self.c(NAVY)
        self.cell(self.usable_w(), 6, text.upper(), new_x=NX, new_y=NY)
        self.hline(NAVY, thick=True)

    def h3(self, text):
        self.set_font("Arial", "B", 10)
        self.c(BLACK)
        self.cell(self.usable_w(), 6, text, new_x=NX, new_y=NY)

    def italic(self, text):
        self.set_font("Arial", "I", 9)
        self.c(GRAY)
        self.cell(self.usable_w(), 5, text, new_x=NX, new_y=NY)

    def body(self, text, col_w=0):
        self.set_x(self.l_margin)
        self.set_font("Arial", "", 9.5)
        self.c(BLACK)
        self.multi_cell(col_w if col_w else self.usable_w(), 5, text)

    def bullet(self, text, col_w=0):
        effective = col_w if col_w else self.usable_w()
        self.set_font("Arial", "", 9.5)
        self.c(BLACK)
        y = self.get_y()
        self.set_xy(self.l_margin, y)
        self.cell(4, 5, "•")
        self.set_xy(self.l_margin + 4, y)
        self.multi_cell(effective - 4, 5, text)

    def subline(self, text, col_w=0):
        self.set_x(self.l_margin)
        self.set_font("Arial", "", 9)
        self.c(GRAY)
        self.multi_cell(col_w if col_w else self.usable_w(), 5, text)

    def render_table(self, rows):
        col_w = self.usable_w() / max(len(r) for r in rows)
        self.set_fill_color(*NAVY)
        self.set_text_color(*WHITE)
        self.set_font("Arial", "B", 9)
        for cell in rows[0]:
            self.cell(col_w, 6, cell, fill=True)
        self.ln()
        for row in rows[1:]:
            self.set_text_color(*BLACK)
            self.set_font("Arial", "", 9)
            for cell in row:
                self.cell(col_w, 5.5, cell)
            self.ln()
        self.ln(2)


def clean(text):
    text = re.sub(r"!\[.*?\]\([^)]*\)", "", text)           # remove ![img](path)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)   # [text](url) → text
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    return text.strip()


# ── Pre-scan markdown ───────────────────────────────────────────────────

with open(MD_FILE, encoding="utf-8") as f:
    lines = f.readlines()

# Find photo path and first section break
photo_path = None
first_hr = None
for j, line in enumerate(lines):
    m = re.match(r"!\[.*?\]\((.+?)\)", line.strip())
    if m and photo_path is None:
        raw_path = m.group(1)
        if os.path.isabs(raw_path):
            photo_path = raw_path
        else:
            photo_path = os.path.join(os.path.dirname(MD_FILE), raw_path)
    if re.match(r"^-{3,}$", line.strip()) and first_hr is None:
        first_hr = j

has_photo = photo_path and os.path.exists(photo_path)

# ── Build PDF ───────────────────────────────────────────────────────────

pdf = CV()
pdf.set_margins(18, 16, 18)
pdf.setup_fonts()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)

# Column width for header text when photo is present
text_col_w = pdf.usable_w() - PHOTO_W - PHOTO_GAP if has_photo else 0

i = 0
# in_header stays True until the first --- separator.
# If the MD has no --- at all, we still render the photo at the end.
in_header = first_hr is not None

while i < len(lines):
    raw = lines[i].rstrip("\n")
    stripped = raw.strip()

    # Track when we leave the header block
    if re.match(r"^-{3,}$", stripped):
        if in_header:
            # Header done: place photo and sync Y position
            if has_photo:
                photo_x = pdf.w - pdf.r_margin - PHOTO_W
                photo_y = pdf.t_margin
                pdf.image(photo_path, x=photo_x, y=photo_y, w=PHOTO_W, h=PHOTO_H)
                photo_bottom = photo_y + PHOTO_H + 2
                if pdf.get_y() < photo_bottom:
                    pdf.set_y(photo_bottom)
            else:
                # Draw placeholder box so layout is visible
                pdf.draw_photo_placeholder(
                    x=pdf.w - pdf.r_margin - PHOTO_W,
                    y=pdf.t_margin,
                    w=PHOTO_W,
                    h=PHOTO_H,
                )
                photo_bottom = pdf.t_margin + PHOTO_H + 2
                if pdf.get_y() < photo_bottom:
                    pdf.set_y(photo_bottom)
            in_header = False
        i += 1
        continue

    # Skip photo markdown image line
    if re.match(r"^!\[.*?\]\(.+?\)$", stripped):
        i += 1
        continue

    cw = text_col_w if in_header else 0

    # H1
    if stripped.startswith("# ") and not stripped.startswith("## "):
        pdf.h1(clean(stripped[2:]), col_w=cw)
        i += 1; continue

    # H2
    if stripped.startswith("## ") and not stripped.startswith("### "):
        pdf.h2(clean(stripped[3:]))
        i += 1; continue

    # H3
    if stripped.startswith("### "):
        pdf.h3(clean(stripped[4:]))
        i += 1; continue

    # Bullet
    if stripped.startswith("- "):
        pdf.bullet(clean(stripped[2:]), col_w=cw)
        i += 1; continue

    # Italic line
    if re.match(r"^\*[^*].*[^*]\*$", stripped):
        pdf.italic(clean(stripped))
        i += 1; continue

    # Table
    if stripped.startswith("|"):
        rows = []
        while i < len(lines) and lines[i].strip().startswith("|"):
            row_raw = lines[i].strip()
            if re.match(r"^\|[-| :]+\|$", row_raw):
                i += 1; continue
            cells = [clean(c.strip()) for c in row_raw.strip("|").split("|")]
            rows.append(cells)
            i += 1
        if rows:
            pdf.render_table(rows)
        continue

    # Non-empty line
    if stripped:
        if re.match(r"^\*\*", stripped):
            pdf.subline(clean(stripped), col_w=cw)
        else:
            pdf.body(clean(stripped), col_w=cw)
    else:
        pdf.ln(1.5)

    i += 1

pdf.output(PDF_FILE)
print(f"PDF saved: {PDF_FILE}")
