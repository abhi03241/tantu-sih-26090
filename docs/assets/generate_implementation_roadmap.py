"""Build the one-page ShilpVani implementation roadmap artifacts.

Requires ``pip install qrcode reportlab``. The PDF is vector-based; the PNG
is rendered from the final PDF with Poppler at 200 DPI.
"""

from pathlib import Path

import qrcode
from reportlab.lib.colors import Color, HexColor, white
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


OUT = Path(__file__).parent
PDF = OUT / "ShilpVani_Implementation_Roadmap.pdf"
QR = OUT / "shilpvani_qr.png"
URL = "https://shilpvani.vercel.app/"
PAGE_W, PAGE_H = landscape(A4)

NAVY = HexColor("#0D1628")
PANEL = HexColor("#131F35")
MUTED = HexColor("#AAB7CC")
LIGHT = HexColor("#EAF0FA")
ORANGE = HexColor("#F28705")
INDIGO = HexColor("#7277FF")
GREEN = HexColor("#1DC798")
ROSE = HexColor("#F04372")
GOLD = HexColor("#F5BD3C")


def alpha(hex_color, opacity):
    return Color(hex_color.red, hex_color.green, hex_color.blue, alpha=opacity)


def text(c, value, x, y, size, color=white, font="Helvetica", align="left"):
    c.setFont(font, size)
    c.setFillColor(color)
    if align == "center":
        c.drawCentredString(x, y, value)
    elif align == "right":
        c.drawRightString(x, y, value)
    else:
        c.drawString(x, y, value)


def pill(c, label, x, y, color, size=6.6):
    width = stringWidth(label, "Helvetica-Bold", size) + 12
    c.setFillColor(alpha(color, 0.16))
    c.setStrokeColor(alpha(color, 0.65))
    c.roundRect(x, y, width, 13, 6.5, fill=1, stroke=1)
    text(c, label, x + 6, y + 3.7, size, color, "Helvetica-Bold")
    return width


def bullet(c, value, x, y, accent, size=7.05):
    c.setFillColor(accent)
    c.circle(x + 2, y + 2.7, 1.55, fill=1, stroke=0)
    text(c, value, x + 8, y, size, LIGHT)


def draw_logo(c, x, y):
    """A compact vector mark based on ShilpVani's loom / voice motif."""
    c.setFillColor(ORANGE)
    c.setStrokeColor(ORANGE)
    c.roundRect(x, y, 30, 30, 8, fill=1, stroke=0)
    c.setStrokeColor(white)
    c.setLineWidth(1.4)
    c.ellipse(x + 6, y + 10, x + 24, y + 20, fill=0, stroke=1)
    c.setFillColor(GOLD)
    c.circle(x + 15, y + 15, 3.1, fill=1, stroke=0)
    c.setStrokeColor(HexColor("#FFF4DE"))
    c.setLineWidth(0.8)
    path = c.beginPath()
    path.moveTo(x + 9, y + 15)
    path.curveTo(x + 13, y + 8, x + 17, y + 22, x + 21, y + 15)
    c.drawPath(path, fill=0, stroke=1)


def stage_card(c, x, y, w, h, phase, label, title, accent, sections, journey=None):
    c.setFillColor(PANEL)
    c.setStrokeColor(alpha(accent, 0.75))
    c.setLineWidth(0.8)
    c.roundRect(x, y, w, h, 10, fill=1, stroke=1)
    c.setFillColor(alpha(accent, 0.18))
    c.roundRect(x, y + h - 54, w, 54, 10, fill=1, stroke=0)
    c.rect(x, y + h - 54, w, 10, fill=1, stroke=0)
    c.setFillColor(accent)
    c.roundRect(x, y + h - 54, 3.6, 54, 2, fill=1, stroke=0)

    text(c, phase, x + 11, y + h - 14, 6.7, accent, "Helvetica-Bold")
    pill(c, label, x + 11, y + h - 31, accent)
    text(c, title, x + 11, y + h - 47, 11.2, white, "Helvetica-Bold")

    row_y = y + h - 72
    for heading, rows in sections:
        text(c, heading.upper(), x + 11, row_y, 5.9, accent, "Helvetica-Bold")
        row_y -= 10
        for row in rows:
            bullet(c, row, x + 12, row_y, accent)
            row_y -= 13.5
        row_y -= 3
    if journey:
        c.setStrokeColor(alpha(accent, 0.32))
        c.setLineWidth(0.45)
        c.line(x + 11, y + 31, x + w - 11, y + 31)
        text(c, "CORE JOURNEY", x + 11, y + 21, 5.5, accent, "Helvetica-Bold")
        text(c, journey, x + 11, y + 10, 5.5, LIGHT, "Helvetica-Bold")


def footer_team(c):
    teams = [
        ("Abhishek Shukla", "Tech Lead + Backend + Integration"),
        ("Maanyta", "AI/NLP + Voice + Multilingual Intelligence"),
        ("Raj", "Computer Vision + Image Enhancement"),
        ("Pratishtha", "Frontend / Mobile UI"),
        ("Sanskriti", "Dynamic Pricing + B2B Marketplace"),
        ("Parth", "Database + Testing + QA / Integration Support"),
    ]
    start_x, start_y = 25, 104
    for index, (name, role) in enumerate(teams):
        col, row = index % 2, index // 2
        x = start_x + col * 330
        y = start_y - row * 15
        text(c, name, x, y, 6.25, white, "Helvetica-Bold")
        text(c, role, x, y - 7, 5.45, MUTED)


def build():
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=4,
    )
    qr.add_data(URL)
    qr.make(fit=True)
    qr.make_image(fill_color="#0D1628", back_color="white").save(QR)

    c = canvas.Canvas(str(PDF), pagesize=(PAGE_W, PAGE_H), pageCompression=1)
    c.setTitle("ShilpVani - Implementation Roadmap | SIH 2026")
    c.setSubject("SIH 2026 Problem Statement 26090 - Heritage & Culture")
    c.setAuthor("Team ShilpVani")

    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(alpha(ORANGE, 0.14))
    c.circle(-20, PAGE_H + 20, 180, fill=1, stroke=0)
    c.setFillColor(alpha(INDIGO, 0.12))
    c.circle(PAGE_W + 30, -15, 170, fill=1, stroke=0)
    c.setFillColor(ORANGE)
    c.rect(0, PAGE_H - 4, PAGE_W * 0.27, 4, fill=1, stroke=0)
    c.setFillColor(INDIGO)
    c.rect(PAGE_W * 0.27, PAGE_H - 4, PAGE_W * 0.45, 4, fill=1, stroke=0)
    c.setFillColor(GREEN)
    c.rect(PAGE_W * 0.72, PAGE_H - 4, PAGE_W * 0.17, 4, fill=1, stroke=0)
    c.setFillColor(ROSE)
    c.rect(PAGE_W * 0.89, PAGE_H - 4, PAGE_W * 0.11, 4, fill=1, stroke=0)

    draw_logo(c, 25, 537)
    text(c, "ShilpVani", 63, 554, 18, HexColor("#FFAA37"), "Helvetica-Bold")
    text(c, "AI Market Linkage for Marginalized Artisans", 63, 542, 7.5, MUTED)
    text(c, "SHILPVANI - IMPLEMENTATION ROADMAP", PAGE_W / 2, 555, 15.2, white, "Helvetica-Bold", "center")
    text(c, "From SIH Prototype > Pilot > Scale > Artisan Commerce Ecosystem", PAGE_W / 2, 543, 7.25, MUTED, align="center")
    c.setStrokeColor(alpha(ORANGE, 0.9))
    c.roundRect(670, 549, 145, 21, 10.5, fill=0, stroke=1)
    text(c, "SMART INDIA HACKATHON 2026", 742.5, 556, 7.4, HexColor("#FFA226"), "Helvetica-Bold", "center")
    text(c, "Problem Statement 26090 | Heritage & Culture", 815, 541, 6.7, MUTED, align="right")
    c.setStrokeColor(alpha(LIGHT, 0.18))
    c.line(25, 527, PAGE_W - 25, 527)

    stage_x = [25, 229, 433, 637]
    accents = [ORANGE, INDIGO, GREEN, ROSE]
    for index, x in enumerate(stage_x):
        c.setFillColor(accents[index])
        c.circle(x, 511, 4.2, fill=1, stroke=0)
        if index < 3:
            c.setStrokeColor(alpha(accents[index], 0.78))
            c.setLineWidth(1.5)
            c.line(x + 5, 511, stage_x[index + 1] - 5, 511)
            c.setFillColor(accents[index])
            c.saveState()
            c.translate(stage_x[index + 1] - 5, 511)
            path = c.beginPath()
            path.moveTo(-4, 3)
            path.lineTo(2, 0)
            path.lineTo(-4, -3)
            path.close()
            c.drawPath(path, fill=1, stroke=0)
            c.restoreState()
    c.setFillColor(ROSE)
    c.circle(815, 511, 4.2, fill=1, stroke=0)

    y, card_w, card_h = 191, 179, 304
    stage_card(c, stage_x[0], y, card_w, card_h, "PHASE 01", "CURRENT PROTOTYPE", "SIH Working Prototype", ORANGE,
               [("Current build", ["Artisan voice / image input", "Vision image enhancement", "Multilingual NLP catalogue", "AI-assisted pricing", "Validation & state management", "B2B marketplace", "Bulk orders", "7-language interface", "Automated regression tests"])],
               "Craft > Voice > AI > Catalogue > Price > Buyer > Bulk Order")
    stage_card(c, stage_x[1], y, card_w, card_h, "PHASE 02", "NEXT IMPLEMENTATION", "Pilot Deployment", INDIGO,
               [("Deployment", ["Vercel frontend deployment", "Render FastAPI backend", "Persistent database / storage"]),
                ("Operations", ["Production authentication", "Monitoring & error logging"]),
                ("Validation", ["Real-artisan pilot validation"])])
    stage_card(c, stage_x[2], y, card_w, card_h, "PHASE 03", "INTELLIGENCE & SCALE", "Intelligence & Scale", GREEN,
               [("AI intelligence", ["Regional market-price datasets", "Improved multilingual speech / NLP", "More Indic languages", "Async AI processing"]),
                ("Platform scale", ["Background workers", "Caching", "Scalable database", "Object storage", "Analytics"])])
    stage_card(c, stage_x[3], y, card_w, card_h, "PHASE 04", "FUTURE SCALE", "Ecosystem Expansion", ROSE,
               [("Commerce", ["ONDC / digital commerce integration", "Government / institutional buyers", "Retail & wholesale partnerships", "Logistics integration", "Payments"]),
                ("Community", ["Community onboarding", "Production-grade security"])])

    c.setStrokeColor(alpha(LIGHT, 0.18))
    c.line(25, 174, PAGE_W - 25, 174)
    text(c, '"Start simple > Validate with artisans > Productionize > Scale the ecosystem"', 25, 155, 11, HexColor("#FFA226"), "Helvetica-Bold")
    text(c, "ShilpVani is designed modularly, allowing each AI and commerce layer to evolve independently without rebuilding the entire platform.", 25, 141, 6.7, MUTED)
    text(c, "TEAM", 25, 112, 6.3, HexColor("#FFA226"), "Helvetica-Bold")
    footer_team(c)

    c.setFillColor(white)
    c.roundRect(730, 57, 84, 84, 5, fill=1, stroke=0)
    c.drawImage(str(QR), 735, 62, width=74, height=74, mask="auto")
    text(c, "LIVE PROJECT", 772, 145, 5.2, MUTED, "Helvetica-Bold", "center")
    text(c, URL, 772, 48, 5.15, HexColor("#FFA226"), "Helvetica-Bold", "center")

    c.showPage()
    c.save()


if __name__ == "__main__":
    build()
