from pathlib import Path
import shutil, subprocess
from PIL import Image, ImageEnhance
from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source" / "Project.pdf"
OUTPUT = ROOT / "docs" / "Municipal_Road_and_Sewer_Design_Portfolio.pdf"
ASSETS, QA = ROOT / "assets", ROOT / "qa-preview"
W, H = landscape((11 * inch, 17 * inch))
PAPER, WHITE = colors.HexColor("#F6F7F5"), colors.white
INK, SLATE = colors.HexColor("#202B33"), colors.HexColor("#596A73")
BLUE, GREEN = colors.HexColor("#1F5D78"), colors.HexColor("#527861")
PALE_B, PALE_G, LINE = colors.HexColor("#E9F0F3"), colors.HexColor("#EDF2EE"), colors.HexColor("#C8D1D5")

def pdftoppm():
    found = shutil.which("pdftoppm")
    bundled = Path.home()/".cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin/pdftoppm.exe"
    if found: return found
    if bundled.exists(): return str(bundled)
    raise RuntimeError("pdftoppm was not found. Install Poppler or add it to PATH.")

def fit(path, x, y, w, h):
    with Image.open(path) as im: iw, ih = im.size
    s = min(w/iw, h/ih); rw, rh = iw*s, ih*s
    return x+(w-rw)/2, y+(h-rh)/2, rw, rh

def wrap(pdf, text, x, y, width, font="Helvetica", size=10, leading=None):
    leading = leading or size*1.4; lines=[]; line=""
    for word in text.split():
        trial=(line+" "+word).strip()
        if pdf.stringWidth(trial,font,size)<=width: line=trial
        else: lines.append(line); line=word
    if line: lines.append(line)
    pdf.setFont(font,size)
    for line in lines: pdf.drawString(x,y,line); y-=leading
    return y

def base(pdf):
    pdf.setFillColor(PAPER); pdf.rect(0,0,W,H,fill=1,stroke=0)

def folio(pdf,n,label="PORTFOLIO"):
    pdf.setStrokeColor(LINE); pdf.setLineWidth(.6); pdf.line(30,24,W-30,24)
    pdf.setFillColor(SLATE); pdf.setFont("Helvetica",6.8)
    pdf.drawString(30,12,"CONCEPTUAL PORTFOLIO PROJECT - NOT FOR CONSTRUCTION")
    pdf.drawRightString(W-30,12,f"{label}  /  {n:02d}")

def header(pdf,kicker,title,n):
    base(pdf); pdf.setFillColor(INK); pdf.setFont("Helvetica-Bold",7.2); pdf.drawString(32,H-27,kicker.upper())
    pdf.setFont("Helvetica-Bold",17); pdf.drawString(32,H-49,title)
    pdf.setStrokeColor(BLUE); pdf.setLineWidth(2.2); pdf.line(32,H-61,W-32,H-61); folio(pdf,n)

def cover(pdf,image,sheets):
    base(pdf); ix,iy,iw,ih=28,45,796,H-74
    pdf.setFillColor(WHITE); pdf.setStrokeColor(LINE); pdf.roundRect(ix,iy,iw,ih,5,fill=1,stroke=1)
    x,y,w,h=fit(image,ix+9,iy+9,iw-18,ih-18); pdf.drawImage(ImageReader(str(image)),x,y,w,h,mask="auto")
    px=852; pdf.setFillColor(INK); pdf.roundRect(px,45,W-px-28,H-74,5,fill=1,stroke=0)
    pdf.setFillColor(GREEN); pdf.rect(px,H-74,72,4,fill=1,stroke=0)
    pdf.setFillColor(colors.HexColor("#B8C7CE")); pdf.setFont("Helvetica-Bold",7.5); pdf.drawString(px+28,H-103,"CIVIL 3D DESIGN PORTFOLIO")
    pdf.setFillColor(WHITE); pdf.setFont("Helvetica-Bold",27); pdf.drawString(px+28,H-151,"Municipal Road"); pdf.drawString(px+28,H-185,"and Sewer Design")
    pdf.setFillColor(colors.HexColor("#CBD5DA")); wrap(pdf,"Conceptual plan and profile drawing package",px+28,H-218,W-px-82,size=10.5)
    pdf.setStrokeColor(colors.HexColor("#53656F")); pdf.line(px+28,H-258,W-56,H-258)
    pdf.setFillColor(colors.HexColor("#B8C7CE")); pdf.setFont("Helvetica-Bold",7.2); pdf.drawString(px+28,H-284,"SELECTED CAPABILITIES")
    y=H-322
    for item in ["Road corridor and intersection coordination","Storm and sanitary plan/profile production","Conceptual GIS/LiDAR existing-condition modelling"]:
        pdf.setFillColor(GREEN); pdf.rect(px+29,y-2,4,19,fill=1,stroke=0)
        pdf.setFillColor(WHITE); y=wrap(pdf,item,px+47,y+10,W-px-100,"Helvetica-Bold",10,14)-27
    pdf.setFillColor(colors.HexColor("#B8C7CE")); pdf.setFont("Helvetica",7.5); pdf.drawString(px+28,94,f"{sheets} PLAN/PROFILE EXHIBITS")
    pdf.drawString(px+28,78,"ROAD  /  STORM  /  SANITARY")
    pdf.setFillColor(WHITE); pdf.setFont("Helvetica-Bold",7.2); pdf.drawString(px+28,61,"CONCEPTUAL - NOT FOR CONSTRUCTION"); pdf.showPage()

def overview(pdf):
    header(pdf,"Project overview","From existing information to coordinated sheets",2)
    pdf.setFillColor(INK); pdf.setFont("Helvetica-Bold",21); pdf.drawString(46,H-112,"A concise municipal design-production exercise")
    pdf.setFillColor(SLATE); wrap(pdf,"This independent conceptual project demonstrates how public terrain and mapping information can be organized into a coordinated Civil 3D road and sewer drawing package. The emphasis is modelling discipline, plan/profile communication and sheet quality.",46,H-143,W-92,size=10.5,leading=15)
    stages=[("01","Existing context","GIS and LiDAR-derived terrain organized as a conceptual existing-ground model."),("02","Road model","Alignment, profile, corridor and intersection transition coordination."),("03","Municipal services","Storm and sanitary pipes, structures, profiles, labels and bands."),("04","Drawing package","View frames, match lines, colour plan/profile sheets and publication checks.")]
    for i,(num,title,body) in enumerate(stages):
        x=46+i*286; pdf.setFillColor(WHITE); pdf.setStrokeColor(LINE); pdf.roundRect(x,305,271,248,5,fill=1,stroke=1)
        pdf.setFillColor(PALE_B if i%2==0 else PALE_G); pdf.rect(x,493,271,60,fill=1,stroke=0)
        pdf.setFillColor(BLUE if i%2==0 else GREEN); pdf.setFont("Helvetica-Bold",20); pdf.drawString(x+18,513,num)
        pdf.setFillColor(INK); pdf.setFont("Helvetica-Bold",12); pdf.drawString(x+18,459,title)
        pdf.setFillColor(SLATE); wrap(pdf,body,x+18,430,235,size=9.5,leading=14)
    pdf.setFillColor(INK); pdf.roundRect(46,72,W-92,184,5,fill=1,stroke=0)
    pdf.setFillColor(WHITE); pdf.setFont("Helvetica-Bold",12); pdf.drawString(68,225,"Professional boundary")
    pdf.setFillColor(colors.HexColor("#D4DDE1")); wrap(pdf,"This portfolio demonstrates software, coordination and drawing-production skills. Existing conditions are based on public information and require survey, records review, field verification and engineering review before real-world use. The work is not approved, sealed, tendered or construction-ready.",68,199,W-136,size=9.5,leading=14)
    pdf.setFillColor(GREEN); pdf.rect(68,106,210,3,fill=1,stroke=0); pdf.setFillColor(WHITE); pdf.setFont("Helvetica-Bold",8); pdf.drawString(68,87,"CONCEPTUAL PORTFOLIO PROJECT - NOT FOR CONSTRUCTION"); pdf.showPage()

def drawing(pdf,image,index,total):
    base(pdf); pdf.setFillColor(INK); pdf.setFont("Helvetica-Bold",7.2); pdf.drawString(30,H-24,"MUNICIPAL ROAD AND SEWER DESIGN")
    pdf.setFillColor(SLATE); pdf.setFont("Helvetica",7.2); pdf.drawRightString(W-30,H-24,f"PLAN / PROFILE EXHIBIT  {index:02d} OF {total:02d}")
    pdf.setStrokeColor(BLUE); pdf.setLineWidth(1.8); pdf.line(30,H-34,W-30,H-34)
    fx,fy,fw,fh=24,31,W-48,H-76; pdf.setFillColor(WHITE); pdf.setStrokeColor(LINE); pdf.roundRect(fx,fy,fw,fh,3,fill=1,stroke=1)
    x,y,w,h=fit(image,fx+5,fy+5,fw-10,fh-10); pdf.drawImage(ImageReader(str(image)),x,y,w,h,mask="auto"); folio(pdf,index+2,"DRAWING EXHIBIT"); pdf.showPage()

def closing(pdf,n):
    header(pdf,"Portfolio summary","Capabilities demonstrated",n)
    pdf.setFillColor(INK); pdf.setFont("Helvetica-Bold",21); pdf.drawString(46,H-115,"A coordinated Civil 3D production workflow")
    pdf.setFillColor(SLATE); pdf.setFont("Helvetica",10.5); pdf.drawString(46,H-143,"The project connects model development, municipal servicing and drawing communication.")
    items=[("Surface and alignment","Existing-ground organization, alignment controls and profile-based coordination."),("Road corridor","Corridor geometry and intersection lane-width transition development."),("Pipe networks","Storm and sanitary pipes, structures, styles, labels and profile display."),("Sheet production","Profile bands, view frames, match lines and colour portfolio publishing.")]
    y=533
    for i,(title,body) in enumerate(items,1):
        pdf.setFillColor(PALE_B if i%2 else PALE_G); pdf.roundRect(46,y-77,W-92,69,4,fill=1,stroke=0)
        pdf.setFillColor(BLUE if i%2 else GREEN); pdf.rect(46,y-77,6,69,fill=1,stroke=0); pdf.setFont("Helvetica-Bold",13); pdf.drawString(74,y-37,f"{i:02d}")
        pdf.setFillColor(INK); pdf.setFont("Helvetica-Bold",11); pdf.drawString(122,y-30,title); pdf.setFillColor(SLATE); pdf.setFont("Helvetica",9.5); pdf.drawString(122,y-49,body); y-=87
    pdf.setFillColor(INK); pdf.roundRect(46,65,W-92,98,4,fill=1,stroke=0); pdf.setFillColor(WHITE); pdf.setFont("Helvetica-Bold",10); pdf.drawString(68,132,"USE OF THIS PORTFOLIO")
    pdf.setFillColor(colors.HexColor("#D4DDE1")); wrap(pdf,"Prepared as an employment portfolio to demonstrate Civil 3D modelling and municipal drawing-production skills. It is not an issued design, permit submission, tender package, record drawing or construction document.",68,109,W-136,size=9,leading=13); pdf.showPage()

def main():
    if not SOURCE.exists(): raise FileNotFoundError(f"Replace this missing file: {SOURCE}")
    count=len(PdfReader(str(SOURCE)).pages)
    if not 1<=count<=30: raise RuntimeError(f"Expected 1 to 30 drawing sheets; found {count}.")
    tool=pdftoppm(); work=ROOT/".build"
    if work.exists(): shutil.rmtree(work)
    work.mkdir(); OUTPUT.parent.mkdir(exist_ok=True); ASSETS.mkdir(exist_ok=True)
    if QA.exists(): shutil.rmtree(QA)
    QA.mkdir()
    subprocess.run([tool,"-png","-r","190",str(SOURCE),str(work/"sheet")],check=True)
    images=sorted(work.glob("sheet-*.png"))
    if len(images)!=count: raise RuntimeError(f"Rendered {len(images)} pages from {count} sheets.")
    for path in images:
        with Image.open(path) as im:
            out=ImageEnhance.Contrast(im.convert("RGB")).enhance(1.035); out=ImageEnhance.Sharpness(out).enhance(1.12); out.save(path,optimize=True)
    src=images[1] if len(images)>1 else images[0]
    with Image.open(src) as im:
        ww,hh=im.size; crop=im.crop((int(ww*.015),int(hh*.015),int(ww*.79),int(hh*.985))); crop.save(ASSETS/"plan-profile-sample.png",optimize=True); cover_image=work/"cover-plan-profile.png"; crop.save(cover_image,optimize=True)
    pdf=canvas.Canvas(str(OUTPUT),pagesize=(W,H),pageCompression=1); pdf.setTitle("Municipal Road and Sewer Design Portfolio"); pdf.setAuthor("Civil 3D Portfolio")
    cover(pdf,cover_image,count); overview(pdf)
    for i,image in enumerate(images,1): drawing(pdf,image,i,count)
    closing(pdf,count+3); pdf.save()
    subprocess.run([tool,"-f","1","-singlefile","-png","-r","150",str(OUTPUT),str(ASSETS/"portfolio-cover")],check=True)
    subprocess.run([tool,"-png","-r","125",str(OUTPUT),str(QA/"portfolio")],check=True)
    print(f"Built {OUTPUT} from {count} sheet(s).")

if __name__=="__main__": main()
