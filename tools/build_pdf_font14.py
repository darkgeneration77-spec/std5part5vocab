from pathlib import Path
import re, json
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

html=Path('index.html').read_text(encoding='utf-8')
m=re.search(r'const THEMES\s*=\s*(\[.*?\]);\s*const ',html,re.S) or re.search(r'const THEMES\s*=\s*(\[.*?\]);\s*\n',html,re.S)
if not m:
    raise SystemExit('THEMES data not found')
themes=json.loads(m.group(1))

pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
font='STSong-Light'
out='Year5_Word_Scoop_Vocabulary.pdf'
doc=SimpleDocTemplate(out,pagesize=A4,leftMargin=26,rightMargin=26,topMargin=24,bottomMargin=26)

title=ParagraphStyle('title',fontName=font,fontSize=24,leading=29,textColor=colors.HexColor('#211B55'),alignment=TA_CENTER,spaceAfter=4)
subtitle=ParagraphStyle('subtitle',fontName=font,fontSize=14,leading=18,textColor=colors.HexColor('#66627D'),alignment=TA_CENTER,spaceAfter=12)
theme_style=ParagraphStyle('theme',fontName=font,fontSize=17,leading=21,textColor=colors.white)
head=ParagraphStyle('head',fontName=font,fontSize=14,leading=18,textColor=colors.HexColor('#4438CA'))
cell=ParagraphStyle('cell',fontName=font,fontSize=14,leading=18,textColor=colors.HexColor('#222238'))
clue=ParagraphStyle('clue',fontName=font,fontSize=14,leading=18,textColor=colors.HexColor('#44445A'))

story=[]
page_w=A4[0]-52
for ti,t in enumerate(themes):
    if ti==0:
        story += [Paragraph('Year 5 Word Scoop',title),Paragraph('Vocabulary Reference - 24 Themes - 192 Words',subtitle)]
    band=Table([[Paragraph(f"Theme {ti+1} - {t['name']}",theme_style)]],colWidths=[page_w])
    band.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#5B4BFF')),('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
    data=[[Paragraph('Word',head),Paragraph('中文',head),Paragraph('English clue',head)]]
    for w in t['words']:
        data.append([Paragraph(w['word'],cell),Paragraph(w['meaning'],cell),Paragraph(w['definition'],clue)])
    tbl=Table(data,colWidths=[125,88,page_w-213],repeatRows=1)
    tbl.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#EFEEFF')),('GRID',(0,0),(-1,-1),0.45,colors.HexColor('#D9D8EA')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#FBFBFF')])]))
    story += [band,Spacer(1,7),tbl]
    if ti != len(themes)-1:
        story.append(PageBreak())

def footer(canvas,doc):
    canvas.saveState();canvas.setFont(font,9);canvas.setFillColor(colors.HexColor('#88849B'))
    canvas.drawString(26,12,'Year 5 Word Scoop - Vocabulary Reference')
    canvas.drawRightString(A4[0]-26,12,f'Page {doc.page}')
    canvas.restoreState()

doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(f'Built {out} with minimum 14 pt vocabulary text and {len(themes)} pages.')
