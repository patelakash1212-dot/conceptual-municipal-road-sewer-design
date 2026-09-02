from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from PIL import Image
from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source" / "Project.pdf"
OUTPUT = ROOT / "docs" / "Municipal_Road_and_Sewer_Design_Portfolio.pdf"
ASSETS = ROOT / "assets"
QA = ROOT / "qa-preview"
PAGE_W, PAGE_H = landscape((11 * inch, 17 * inch))
NAVY = colors.HexColor("#17324D")
TEAL = colors.HexColor("#21A6A1")
INK = colors.HexColor("#1D2B34")
LIGHT = colors.HexColor("#D7E2E8")


def find_pdftoppm() -> str:
    found = shutil.which("pdftoppm")
    if found:
        return found
    bundled = Path.home() / ".cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin/pdftoppm.exe"
    if bundled.exists():
        return str(bundled)
    raise RuntimeError("pdftoppm was not found. Install Poppler or add pdftoppm to PATH.")


def fit_image(path: Path, x: float, y: float, w: float, h: float):
    with Image.open(path) as image:
        iw, ih = image.size
    scale = min(w / iw, h / ih)
    rw, rh = iw * scale, ih * scale
    return x + (w - rw) / 2, y + (h - rh) / 2, rw, rh


def footer(pdf: canvas.Canvas, page_no: int):
    pdf.setStrokeColor(LIGHT)
    pdf.line(38, 27, PAGE_W - 38, 27)
    pdf.setFont("Helvetica", 7.5)
    pdf.setFillColor(colors.HexColor("#577083"))
    pdf.drawString(38, 15, "CONCEPTUAL PORTFOLIO PROJECT - NOT FOR CONSTRUCTION")
    pdf.drawRightString(PAGE_W - 38, 15, f"PORTFOLIO | {page_no:02d}")


def header(pdf: canvas.Canvas, kicker: str, title: str, page_no: int):
    pdf.setFillColor(NAVY)
    pdf.rect(0, PAGE_H - 66, PAGE_W, 66, fill=1, stroke=0)
    pdf.setFillColor(TEAL)
    pdf.rect(0, PAGE_H - 66, 10, 66, fill=1, stroke=0)
    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 8)
    pdf.drawString(34, PAGE_H - 24, kicker.upper())
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(34, PAGE_H - 48, title)
    footer(pdf, page_no)


def draw_wrapped(pdf: canvas.Canvas, text: str, x: float, y: float, width: float, size: float = 11):
    words, line, lines = text.split(), "", []
    for word in words:
        trial = f"{line} {word}".strip()
        if pdf.stringWidth(trial, "Helvetica", size) <= width:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    for item in lines:
        pdf.drawString(x, y, item)
        y -= size * 1.45
    return y


def cover(pdf: canvas.Canvas, image_path: Path):
    pdf.setFillColor(NAVY)
    pdf.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    pdf.setFillColor(TEAL)
    pdf.rect(0, 0, 18, PAGE_H, fill=1, stroke=0)
    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(58, PAGE_H - 54, "CIVIL 3D DESIGN PORTFOLIO")
    pdf.setFont("Helvetica-Bold", 31)
    pdf.drawString(58, PAGE_H - 119, "Municipal Road")
    pdf.drawString(58, PAGE_H - 157, "and Sewer Design")
    pdf.setFont("Helvetica", 12)
    pdf.setFillColor(colors.HexColor("#A9C8D9"))
    pdf.drawString(60, PAGE_H - 187, "Conceptual plan and profile drawing package")
    card_x, card_y, card_w, card_h = 475, 60, PAGE_W - 515, PAGE_H - 110
    pdf.setFillColor(colors.white)
    pdf.roundRect(card_x, card_y, card_w, card_h, 10, fill=1, stroke=0)
    x, y, w, h = fit_image(image_path, card_x + 10, card_y + 10, card_w - 20, card_h - 20)
    pdf.drawImage(ImageReader(str(image_path)), x, y, w, h, preserveAspectRatio=True, mask="auto")
    pdf.setFillColor(colors.HexColor("#244B68"))
    pdf.roundRect(58, 272, 370, 252, 12, fill=1, stroke=0)
    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(82, 490, "CORE CAPABILITIES")
    bullets = [
        "Road corridor and intersection coordination",
        "Storm and sanitary plan/profile production",
        "Conceptual GIS/LiDAR-based existing-condition modelling",
    ]
    y = 447
    for item in bullets:
        pdf.setFillColor(TEAL)
        pdf.circle(86, y, 4, fill=1, stroke=0)
        pdf.setFillColor(colors.white)
        pdf.setFont("Helvetica-Bold", 11)
        draw_wrapped(pdf, item, 104, y - 4, 292, 11)
        y -= 67
    pdf.setFont("Helvetica-Bold", 9)
    pdf.setFillColor(colors.HexColor("#A9C8D9"))
    pdf.drawString(58, 96, "CONCEPTUAL PORTFOLIO PROJECT - NOT FOR CONSTRUCTION")
    pdf.showPage()


def overview(pdf: canvas.Canvas):
    header(pdf, "Project narrative", "Design approach and responsibilities", 2)
    pdf.setFillColor(colors.HexColor("#EEF4F7"))
    pdf.roundRect(38, PAGE_H - 205, PAGE_W - 76, 107, 10, fill=1, stroke=0)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica", 11)
    draw_wrapped(pdf, "This independent conceptual exercise demonstrates a coordinated municipal road, storm sewer and sanitary sewer drawing package. The focus is Civil 3D modelling, plan/profile coordination and drawing production—not construction authorization or final engineering certification.", 58, PAGE_H - 127, PAGE_W - 116, 11)
    columns = [
        ("MODEL DEVELOPMENT", ["Existing-ground surface", "Road alignment and profile", "Corridor and intersection tie-ins", "Storm and sanitary networks"]),
        ("DRAWING PRODUCTION", ["Plan and profile views", "Pipe and structure annotation", "Profile data bands", "View frames and match lines"]),
        ("QUALITY REVIEW", ["Network/profile consistency", "Pipe slopes and inverts", "Structure placement", "Colour plot readability"]),
    ]
    for x, (title, items) in zip((38, 317, 596), columns):
        pdf.setFillColor(colors.white)
        pdf.setStrokeColor(LIGHT)
        pdf.roundRect(x, 157, 247, 318, 9, fill=1, stroke=1)
        pdf.setFillColor(colors.HexColor("#2878B5"))
        pdf.rect(x, 435, 247, 40, fill=1, stroke=0)
        pdf.setFillColor(colors.white)
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(x + 18, 450, title)
        y = 400
        for item in items:
            pdf.setFillColor(TEAL)
            pdf.circle(x + 22, y + 3, 3, fill=1, stroke=0)
            pdf.setFillColor(INK)
            pdf.setFont("Helvetica", 10)
            draw_wrapped(pdf, item, x + 36, y + 7, 185, 10)
            y -= 55
    pdf.showPage()


def drawing_page(pdf: canvas.Canvas, image_path: Path, index: int, total: int):
    header(pdf, "Drawing exhibit", f"Plan and profile sheet {index} of {total}", index + 2)
    x, y, w, h = 34, 40, PAGE_W - 68, PAGE_H - 122
    pdf.setFillColor(colors.white)
    pdf.setStrokeColor(LIGHT)
    pdf.roundRect(x, y, w, h, 6, fill=1, stroke=1)
    ix, iy, iw, ih = fit_image(image_path, x + 7, y + 7, w - 14, h - 14)
    pdf.drawImage(ImageReader(str(image_path)), ix, iy, iw, ih, preserveAspectRatio=True, mask="auto")
    pdf.showPage()


def closing(pdf: canvas.Canvas, page_no: int):
    header(pdf, "Portfolio summary", "Demonstrated Civil 3D capabilities", page_no)
    items = [
        ("Surface and alignment", "Existing-ground organization and alignment-based plan/profile production."),
        ("Road corridor", "Corridor geometry and intersection lane-width transition coordination."),
        ("Pipe networks", "Storm and sanitary pipes, structures, profiles, styles and annotation."),
        ("Sheet production", "View frames, match lines, data bands and colour sheet-set publishing."),
    ]
    y = PAGE_H - 126
    for number, (title, body) in enumerate(items, 1):
        pdf.setFillColor(colors.HexColor("#EEF4F7"))
        pdf.roundRect(46, y - 82, PAGE_W - 92, 70, 8, fill=1, stroke=0)
        pdf.setFillColor(TEAL)
        pdf.circle(76, y - 47, 18, fill=1, stroke=0)
        pdf.setFillColor(colors.white)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawCentredString(76, y - 51, str(number))
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawString(110, y - 36, title)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica", 9.5)
        pdf.drawString(110, y - 56, body)
        y -= 92
    pdf.setFillColor(NAVY)
    pdf.roundRect(46, 76, PAGE_W - 92, 88, 9, fill=1, stroke=0)
    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(68, 132, "PROFESSIONAL USE LIMITATION")
    pdf.setFont("Helvetica", 9)
    draw_wrapped(pdf, "This is a skills demonstration—not an issued design, tender document, permit submission, record drawing or construction document. It has not been independently reviewed or sealed.", 68, 112, PAGE_W - 136, 9)
    pdf.showPage()


def validate_source() -> int:
    if not SOURCE.exists():
        raise FileNotFoundError(f"Replace this missing file: {SOURCE}")
    reader = PdfReader(str(SOURCE))
    count = len(reader.pages)
    if count < 1 or count > 30:
        raise RuntimeError(f"Expected 1 to 30 drawing sheets; found {count}.")
    bad_pages = []
    for number, page in enumerate(reader.pages, 1):
        if "???" in (page.extract_text() or ""):
            bad_pages.append(str(number))
    if bad_pages:
        raise RuntimeError("Unresolved '???' text found on source sheet page(s): " + ", ".join(bad_pages))
    return count


def main():
    count = validate_source()
    pdftoppm = find_pdftoppm()
    work = ROOT / ".build"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    if QA.exists():
        shutil.rmtree(QA)
    QA.mkdir(parents=True)
    subprocess.run([pdftoppm, "-png", "-r", "170", str(SOURCE), str(work / "sheet")], check=True)
    images = sorted(work.glob("sheet-*.png"))
    if len(images) != count:
        raise RuntimeError(f"Rendered {len(images)} images from {count} PDF pages.")
    sample_source = images[1] if len(images) > 1 else images[0]
    with Image.open(sample_source) as image:
        width, height = image.size
        crop = image.crop((int(width * .02), int(height * .02), int(width * .82), int(height * .97)))
        crop.save(ASSETS / "plan-profile-sample.png", optimize=True)
        crop.save(work / "cover-plan-profile.png", optimize=True)
    pdf = canvas.Canvas(str(OUTPUT), pagesize=(PAGE_W, PAGE_H), pageCompression=1)
    pdf.setTitle("Municipal Road and Sewer Design Portfolio")
    pdf.setAuthor("Civil 3D Portfolio")
    cover(pdf, work / "cover-plan-profile.png")
    overview(pdf)
    for index, image_path in enumerate(images, 1):
        drawing_page(pdf, image_path, index, count)
    closing(pdf, count + 3)
    pdf.save()
    subprocess.run([pdftoppm, "-f", "1", "-singlefile", "-png", "-r", "150", str(OUTPUT), str(ASSETS / "portfolio-cover")], check=True)
    subprocess.run([pdftoppm, "-png", "-r", "110", str(OUTPUT), str(QA / "portfolio")], check=True)
    print(f"Built {OUTPUT} from {count} sheet(s).")
    print(f"Review the rendered pages in {QA} before publishing.")


if __name__ == "__main__":
    main()
