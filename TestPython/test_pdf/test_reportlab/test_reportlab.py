__author__ = 'R.Azh'
from reportlab.pdfgen import canvas

c = canvas.Canvas('hello.pdf')                  #can be an absolute path or a relative path
c.drawString(100, 750, "Welcome to Reportlab")
c.save()

print('################## change font ######################')
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# add a font that supports farsi
# copy Bahij-Nazanin-Regular.ttf into /usr/local/lib/python3.4/dist-packages/reportlab/fonts folder
pdfmetrics.registerFont(TTFont('Persian', 'Bahij-Nazanin-Regular.ttf'))

c = canvas.Canvas('font.pdf')
c.setFont('Persian', 14)
c.drawString(100, 750, u"خوش آمدید".encode('utf-8'))
c.save()

print('################## print farsi ######################')
from bidi.algorithm import get_display
from rtl import reshaper

c = canvas.Canvas('farsi.pdf')
c.setFont('Persian', 14)
reshaped_text = reshaper.reshape(u"خوش آمدید")    # for reshaping and concating words
bidi_text = get_display(reshaped_text)            # for right to left
# c.drawString(100, 750, bidi_text)
from hazm import *
normalizer = Normalizer()
text = 'شاید هنوز اندروید نوقا برای تمام گوشی‌های اندرویدی عرضه نشده باشد، ولی اگر صاحب یکی از گوشی‌های نکسوس یا پیکسل باشید احتمالا تا الان زمان نسبتا زیادی را با آخرین نسخه‌ی اندروید سپری کرده‌اید. اگر در کار با اندروید نوقا دچار مشکل شده‌اید، با دیجی‌کالا مگ همراه باشید تا با هم برخی از رایج‌ترین مشکلات گزارش شده و راه حل آن‌ها را بررسی کنیم. البته از بسیاری از این روش‌ها در سایر نسخه‌های اندروید هم می‌توانید استفاده کنید. اندروید برخلاف iOS روی گستره‌ی وسیعی از گوشی‌ها با پوسته‌ها و اپلیکیشن‌های اضافی متنوع نصب می‌شود. بنابراین تجویز یک نسخه‌ی مشترک برای حل مشکلات آن کار چندان ساده‌ای نیست. با این حال برخی روش‌های عمومی وجود دارد که بهتر است پیش از هر چیز آن‌ها را بیازمایید.'
txt = normalizer.normalize(text)
reshaped_text = reshaper.reshape(txt)
bidi_text = get_display(reshaped_text)
c.drawString(100, 750, bidi_text)
c.save()

print('################## change paper size ######################')
from reportlab.lib.pagesizes import letter

c = canvas.Canvas('page_size.pdf', pagesize=letter)
width, height = letter
# that you can use  width and height for calculations to decide when to add a page break or help define margins.
c.drawString(100, 750, "Welcome to Reportlab")
c.save()


print('################## create a form ######################')

c = canvas.Canvas('form.pdf', pagesize=letter)
c.setLineWidth(.3)
c.setFont('Helvetica', 12)

c.drawString(30, 750, 'Official Communique')
c.drawString(30, 735, 'Of ACME Industries')
c.drawString(500, 750, "12/12/2010")
c.line(480, 747, 580, 747)

c.drawString(275, 725, 'Amount Owed:')
c.drawString(500, 725, '$1,000.00')
c.line(378, 723, 580, 723)

c.drawString(30, 703, 'RECEIVED BY:')
c.line(120, 700, 580, 700)
c.drawString(120, 703, "JOHN DOE")

c.save()

print('################## create flowable ######################')

import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

doc = SimpleDocTemplate("form_letter.pdf", pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72,
                        bottomMargin=18)
Story = []
logo = 'python_logo.png'
mag_name = 'pythonista'
issue_name = 12
sub_price = '99.00'
limited_date = '03/05/2010'
free_gift = 'tin foil hat'

formatted_time = time.ctime()
full_name = "Mike Driscoll"
address_parts = ["411 State St.", "Marshalltown, IA 50158"]

img = Image(logo, 2*inch, 2*inch)
Story.append(img)

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
p_text = '<font size=12>%s</font>' % formatted_time

Story.append(Paragraph(p_text, styles['Normal']))
Story.append(Spacer(1, 12))

p_text = '<font size=12>%s</font>' % full_name
Story.append(Paragraph(p_text, styles["Normal"]))

Story.append(Paragraph(p_text, styles["Normal"]))
for part in address_parts:
    p_text = '<font size=12>%s</font>' % part.strip()
    Story.append(Paragraph(p_text, styles["Normal"]))

Story.append(Spacer(1, 12))
p_text = '<font size=12>Dear %s:</font>' % full_name.split()[0].strip()
Story.append(Paragraph(p_text, styles["Normal"]))
Story.append(Spacer(1, 12))

p_text = '<font size=12>We would like to welcome you to our subscriber base for %s Magazine! \
        You will receive %s issues at the excellent introductory price of $%s. Please respond by\
        %s to start receiving your subscription and get the following free gift: %s.</font>' % (mag_name,
                                                                                                issue_name,
                                                                                                sub_price,
                                                                                                limited_date,
                                                                                                free_gift)
Story.append(Paragraph(p_text, styles["Justify"]))
Story.append(Spacer(1, 12))


p_text = '<font size=12>Thank you very much and we look forward to serving you.</font>'
Story.append(Paragraph(p_text, styles["Justify"]))
Story.append(Spacer(1, 12))
p_text = '<font size=12>Sincerely,</font>'
Story.append(Paragraph(p_text, styles["Normal"]))
Story.append(Spacer(1, 48))
p_text = '<font size=12>Ima Sucker</font>'
Story.append(Paragraph(p_text, styles["Normal"]))
Story.append(Spacer(1, 12))
doc.build(Story)



