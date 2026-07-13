import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, PageBreak
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib.units import cm
from reportlab.lib import colors

styles = getSampleStyleSheet()

styles.add(ParagraphStyle(name='DaDaJustify', alignment=TA_JUSTIFY, fontSize=10.5, leading=15, spaceAfter=6))
styles.add(ParagraphStyle(name='DaDaH2', alignment=TA_LEFT, fontSize=13, leading=16, spaceAfter=6, spaceBefore=14, fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name='DaDaH3', alignment=TA_LEFT, fontSize=11, leading=14, spaceAfter=4, spaceBefore=10, fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name='DaDaCenter', alignment=TA_CENTER, fontSize=10, leading=13, spaceAfter=4, textColor=colors.HexColor("#444444")))
styles.add(ParagraphStyle(name='DaDaBullet', alignment=TA_LEFT, fontSize=10.5, leading=15, spaceAfter=4, leftIndent=18, bulletIndent=6))

def build_story(title, subtitle, content_blocks):
    story = []
    story.append(Spacer(1, 2 * cm))
    cover_title_style = ParagraphStyle(name="CoverTitle", fontSize=22, leading=28, alignment=TA_CENTER, fontName="Helvetica-Bold", textColor=colors.HexColor("#1A1A2E"))
    story.append(Paragraph("Da&Da Solutions", cover_title_style))
    story.append(Spacer(1, 0.4 * cm))
    story.append(HRFlowable(width="80%", thickness=2, color=colors.HexColor("#7C3AED")))
    story.append(Spacer(1, 0.6 * cm))
    doc_title_style = ParagraphStyle(name="DocTitle", fontSize=18, leading=24, alignment=TA_CENTER, fontName="Helvetica-Bold", textColor=colors.HexColor("#2D2D2D"))
    story.append(Paragraph(title, doc_title_style))
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph(subtitle, styles["DaDaCenter"]))
    story.append(Spacer(1, 1.5 * cm))
    story.append(HRFlowable(width="60%", thickness=1, color=colors.HexColor("#AAAAAA")))
    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph("Documento Interno — Confidencial", styles["DaDaCenter"]))
    story.append(Paragraph("Version 3.1  |  Ano 2026  |  Departamento de Ingenieria", styles["DaDaCenter"]))
    story.append(PageBreak())
    for block in content_blocks:
        if block.strip() == ">>>BREAK":
            story.append(PageBreak())
        elif block.strip() == "---":
            story.append(Spacer(1, 6))
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CCCCCC")))
            story.append(Spacer(1, 6))
        elif block.startswith("###"):
            story.append(Paragraph(block[3:].strip(), styles["DaDaH3"]))
        elif block.startswith("##"):
            story.append(Paragraph(block[2:].strip(), styles["DaDaH2"]))
        elif block.startswith("-"):
            story.append(Paragraph("  - " + block[1:].strip(), styles["DaDaBullet"]))
        else:
            story.append(Paragraph(block.strip(), styles["DaDaJustify"]))
    return story

def create_pdf(filename, title, subtitle, content_blocks):
    filepath = os.path.join("docs", filename)
    doc = SimpleDocTemplate(filepath, pagesize=A4, rightMargin=2.2*cm, leftMargin=2.2*cm, topMargin=2.2*cm, bottomMargin=2*cm)
    story = build_story(title, subtitle, content_blocks)
    doc.build(story)
    print(f"  OK  {filename}")

print("Script loaded OK")
