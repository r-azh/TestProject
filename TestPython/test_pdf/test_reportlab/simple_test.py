from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from bidi.algorithm import get_display
from rtl import reshaper
import textwrap

pdfmetrics.registerFont(TTFont('Persian', 'Bahij-Nazanin-Regular.ttf'))
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT, fontName='Persian', fontSize=10))


def get_farsi_text(text):
    if reshaper.has_arabic_letters(text):
        words = text.split()
        reshaped_words = []
        for word in words:
            if reshaper.has_arabic_letters(word):
                # for reshaping and concating words
                reshaped_text = reshaper.reshape(word)
                # for right to left
                bidi_text = get_display(reshaped_text)
                reshaped_words.append(bidi_text)
            else:
                reshaped_words.append(word)
        reshaped_words.reverse()
        return ' '.join(reshaped_words)
    return text


def get_farsi_bulleted_text(text, wrap_length=None):
    farsi_text = get_farsi_text(text)
    if wrap_length:
        line_list = textwrap.wrap(farsi_text, wrap_length)
        line_list.reverse()
        line_list[0] = '{} &#x02022;'.format(line_list[0])
        farsi_text = '<br/>'.join(line_list)
        return '<font>%s</font>' % farsi_text
    return '<font>%s &#x02022;</font>' % farsi_text


doc = SimpleDocTemplate("farsi_wrap.pdf", pagesize=letter,    rightMargin=72, leftMargin=72, topMargin=72,
                        bottomMargin=18)
Story = []

text = 'شاید هنوز اندروید نوقا برای تمام گوشی‌های اندرویدی عرضه نشده باشد، ولی اگر صاحب یکی از گوشی‌های نکسوس یا پیک' \
       'سل باشید احتمالا تا الان زمان نسبتا زیادی را با آخرین نسخه‌ی اندروید سپری کرده‌اید. اگر در کار با اندروید نوقا' \
       ' دچار مشکل شده‌اید، با دیجی‌کالا مگ همراه باشید تا با هم برخی از رایج‌ترین مشکلات گزارش شده و راه حل آن‌ها را' \
       ' بررسی کنیم. البته از بسیاری از این روش‌ها در سایر نسخه‌های اندروید هم می‌توانید استفاده کنید. اندروید برخلاف iOS ' \
       'روی گستره‌ی وسیعی از گوشی‌ها با پوسته‌ها و اپلیکیشن‌های اضافی متنوع نصب می‌شود. بنابراین تجویز یک نسخه‌ی مشترک برا' \
       'ی حل مشکلات آن کار چندان ساده‌ای نیست. با این حال برخی روش‌های عمومی وجود دارد که بهتر است پیش از هر چیز آن‌ها را' \
       ' بیازمایید.'
tw = get_farsi_bulleted_text(text, wrap_length=120)
p = Paragraph(tw, styles['Right'])
Story.append(p)
doc.build(Story)
