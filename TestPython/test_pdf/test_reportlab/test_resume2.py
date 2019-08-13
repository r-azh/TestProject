# -*- coding: utf-8 -*-
import urllib
from urllib.request import urlretrieve
from bson import ObjectId
from pymongo import MongoClient
from bidi.algorithm import get_display
from reportlab.graphics.shapes import Line, Drawing, Rect
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Image, ParagraphAndImage
from rtl import reshaper

__author__ = 'R.Azh'


def get_user_data():
    dbClient = MongoClient('185.4.30.75', 27017)
    # dbClient = MongoClient('localhost', 27017)
    db = dbClient.ipn_db
    user = db.person.find({'_id': ObjectId('560121abcbf62c13d4567f0d')})
    return user[0]


def get_farsi_formatted_text(text):
    return '<font>%s</font>' % get_farsi_text(text)


def get_farsi_text(text):
    words = text.split()
    reshaped_words = []
    for word in words:
        if reshaper.has_arabic_letters(word):
            reshaped_text = reshaper.reshape(word)    # for reshaping and concating words
            bidi_text = get_display(reshaped_text)    # for right to left
            reshaped_words.append(bidi_text)
        else:
            reshaped_words.append(word)
    reshaped_words.reverse()
    # reshaped_text = reshaper.reshape_sentence(text) reshape_it(text)
    return ' '.join(reshaped_words)


def get_farsi_list_item(text):
    return '<li>%s</li>' % get_farsi_text(text)


def get_farsi_formatted_bullet_text(text):
    return '<bullet>&bull;</bullet>%s' % get_farsi_text(text)


def get_jalali_date(isoformat_date):
    import dateutil.parser
    import jalaali

    _date = dateutil.parser.parse(isoformat_date)
    jalai_date = jalaali.Jalaali().to_jalaali(_date.year, _date.month, _date.day)
    return reshaper.replace_digits('{}-{}-{}'.format(jalai_date['jy'], jalai_date['jm'], jalai_date['jd']))


def get_farsi_numbers(text):
    return reshaper.replace_digits(text)


def add_styles():
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_CENTER
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    pdfmetrics.registerFont(TTFont('Persian', 'Bahij-Nazanin-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('Persian-Bold', 'Bahij-Nazanin-Bold.ttf'))
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontName='Persian', fontSize=10))
    styles.add(ParagraphStyle(name='Justify-Bold', alignment=TA_JUSTIFY, fontName='Persian-Bold', fontSize=10))
    styles.add(ParagraphStyle(name='Right-indented', alignment=TA_RIGHT, fontName='Persian', fontSize=10,
                              rightIndent=10, wordWrap='CJK'))
    styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT, fontName='Persian', fontSize=10,
                              rightIndent=10,
                              # firstLineIndent=0,
                              wordWrap='CJK'))
    styles.add(ParagraphStyle(name='Right-Bold', alignment=TA_RIGHT, fontName='Persian-Bold', fontSize=10))
    # styles.add(ParagraphStyle(name='Right-Bold-Titr', alignment=TA_RIGHT, fontName='Persian-Bold', fontSize=12,
    #                           backColor=colors.lavender, borderPadding=5, borderRadius=5, borderWidth=1))
    styles.add(ParagraphStyle(name='Right-Bold-Titr', alignment=TA_RIGHT, fontName='Persian-Bold', fontSize=12))
    styles.add(ParagraphStyle(name='Right-small', alignment=TA_RIGHT, fontName='Persian', fontSize=8,
                              rightIndent=20,
                              wordWrap='CJK'))
    styles.add(ParagraphStyle(name='Centre', alignment=TA_CENTER, fontName='Persian', fontSize=10))
    styles.add(ParagraphStyle(name='Centre-Bold', alignment=TA_CENTER, fontName='Persian-Bold', fontSize=10))
    return styles


def create_pdf_resume(user):
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
    from reportlab.lib.units import inch

    doc = SimpleDocTemplate("farsi_resume.pdf", pagesize=letter, rightMargin=110, leftMargin=72, topMargin=72,
                            bottomMargin=18)

    story = []

    styles = add_styles()
    # bold_style = styles['Justify-Bold']
    # normal_style = styles['Justify']
    right_bold_style = styles['Right-Bold']
    right_normal_indented_style = styles['Right-indented']
    right_normal_style = styles['Right']
    right_small_style = styles['Right-small']
    # right_bold_titr_style = styles['Right-Bold-Titr']
    # centre_bold_style = styles['Centre-Bold']
    # centre_normal_style = styles['Centre']

    # story.append(Paragraph(get_farsi_formatted_text('بسمه تعالی'), centre_normal_style))
    # story.append(Spacer(1, 15))

    d = Drawing(100, 1)
    line = Line(0, 0, 450, 0, strokeColor=colors.lavender)
    d.add(line)
    story.append(d)
    story.append(Spacer(1, 15))

    # p_img = ImageReader(logo)
    # p_img = Paragraph('<img src=\"./{}\" valign=\"top\"/>'.format(logo), right_normal_style)
    logo = 'python_logo.png'
    p_img = Image(logo, 1.2*inch, .3*inch, hAlign='LEFT')
    story.append(p_img)
    req = urllib.request.Request("http://tipn.parsadp.com/api/v1.0{}".format(user['image']))
    req.add_header('token', 'og4ZNFIdbDW9sahj3DqWpVgSA2YiPVtuCBqbYhbx5QuZ2qH47syY2eazArK6HKujtF+w1GUBI1L1J7xeXPmBFDv4j45gubO2CX8qxmuYs3u31RgfdbK+cW3JdezhAoEG')
    p_img = urllib.request.urlopen(req)
    img = Image(p_img, 1*inch, 1*inch, hAlign='RIGHT')
    #story.append(img)

    text = '{}<br/>{}<br/>{}<br/>{}<br/>{}<br/>'.format(
        get_farsi_formatted_text('نام و نام خانوادگی: {} {}'.format(user['name'], user['last_name'])),
        get_farsi_formatted_text('تاریخ تولد: {}'.format(get_jalali_date(user['birthday']))),
        get_farsi_formatted_text('وضعیت تاهل: {}'.format(user['is_married'])),
        get_farsi_formatted_text('ایمیل: {}'.format(user['email'])),
        get_farsi_formatted_text('آدرس: {}'.format(user['address'])))

    p = Paragraph(text, right_normal_style)
    colWidths = [5*inch, 2.5*inch]
    # rowHeights = []
    table = Table([[p, img]], colWidths=colWidths)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), colors.white),
                               ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                               ("VALIGN", (0, 1), (-1, -1), "CENTER"),
                               ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
                               # ('RIGHTPADDING', (0, 0), (0, 0), 0)
                               ('ALIGN', (-1, -1), (-1, -1), 'CENTER')
                               ]))
    story.append(table)
    story.append(Spacer(1, 15))
    d = Drawing(100, 1)
    line = Line(20, 0, 430, 0, strokeColor=colors.lavender)
    d.add(line)
    # r = Rect(0, 0, 450, 3, fillColor=colors.lavenderblush, strokeColor=colors.red)
    # d.add(r)
    story.append(d)

    # p2 = Paragraph('{}{}'.format(text, '<img src="./python_logo.png" valign="top"/>'), right_normal_style)
    # story.append(p2)

    # p3 = Paragraph('{}{}'.format('<img src="./python_logo.png" valign="top" width="100" height="100"/>', text),
    #                right_normal_style)
    # story.append(p3)

    # story.append(Spacer(1, 12))
    # story.append(Paragraph(get_farsi_formatted_text('نام و نام خانوادگی: {} {}'.format(user['name'],
    #                                                                                    user['last_name'])),
    #                        right_normal_indented_style))
    # story.append(Paragraph(get_farsi_formatted_text('تاریخ تولد: {}'.format(get_jalali_date(user['birthday']))), right_normal_indented_style))
    # story.append(Paragraph(get_farsi_formatted_text('وضعیت تاهل: {}'.format(user['is_married'])), right_normal_indented_style))
    # story.append(Paragraph(get_farsi_formatted_text('آدرس ایمیل: {}'.format(user['email'])), right_normal_indented_style))
    # story.append(Paragraph(get_farsi_formatted_text('آدرس: {}'.format(user['address'])), right_normal_indented_style))
    # story.append(Spacer(1, 10))

    if user['proficiencies']:
        story.append(Paragraph(get_farsi_formatted_text('مهارت ها :'), right_bold_style))
        story.append(Spacer(1, 3))
        story.append(d)
        story.append(Spacer(1, 3))

        profs = []
        for prof in user['proficiencies']:
            # story.append(Paragraph(get_farsi_formatted_text(' - {}  در سطح {}'.format(prof['skill']['title'],
            #                                                                           prof['skill_level'])),
            #                        right_normal_indented_style))
            # story.append(Spacer(1, 5))
            profs.append([Paragraph(get_farsi_formatted_text(prof['skill_level']),
                                    right_normal_indented_style),
                          Paragraph(get_farsi_formatted_text(' - %s' % prof['skill']['title']), right_normal_style)])

        # colWidths = [2*inch, 3*inch, 2*inch]
        # rowHeights = []
        # table = Table(profs, colWidths=colWidths, rowHeights=rowHeights)
        table = Table(profs)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), colors.white),
                                   ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                                   ("VALIGN", (0, 0), (-1, -1), "RIGHT"),
                                   ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                                   # ('RIGHTPADDING', (0, 0), (0, 0), 0)
                                   # ,('ALIGN', (-1, -1), (-1, -1), 'CENTER')
                                   ]))
        story.append(table)
        # story.append(Paragraph('<html><head><style>.rightToleft{text-align:right;direction:rtl;float:right}</style>'
        #                        '</head><body><div class="rightToleft">', right_normal_indented_style))
        # for prof in user['proficiencies']:
        #     story.append(Paragraph(get_farsi_list_item(' - {}  در سطح {}'.format(prof['skill']['title'],
        #                                                prof['skill_level'])), right_normal_indented_style))
        # story.append(Paragraph('</ul></div></body></html>', right_normal_indented_style))  # dont work
        #
        # story.append(Paragraph('<div  align="right" dir="rtl"><ul>', right_normal_indented_style))
        # for prof in user['proficiencies']:
        #     story.append(Paragraph(get_farsi_list_item(' - {}  در سطح {}'.format(prof['skill']['title'],
        #                                                   prof['skill_level'])), right_normal_indented_style))
        # story.append(Paragraph('</ul></div>', right_normal_indented_style)) # dont work

        # list_f = ListFlowable([
        #     ListItem(Paragraph(get_farsi_formatted_text(' - {}  در سطح {}'.format(prof['skill']['title'],
        #                                                                                   prof['skill_level'])),
        #                                right_normal_indented_style)) for prof in user['proficiencies']], bulletType='bullet',
        #                       start='square', align='right')
        # story.append(list_f)
        story.append(Spacer(1, 5))

    if user['experiences']:
        story.append(d)
        story.append(Paragraph(get_farsi_formatted_text('تجربیات کاری :'), right_bold_style))
        story.append(Spacer(1, 3))
        story.append(d)
        story.append(Spacer(1, 3))

        expes = []
        for exp in user['experiences']:
            # story.append(Paragraph(get_farsi_formatted_text(' - {} در {}'.format(exp['title'], exp['company']['name'])),
            #                        right_normal_indented_style))
            # story.append(Paragraph(get_farsi_formatted_text('{}'.format(exp['description'])),
            #                        right_normal_indented_style))
            p1 = [Paragraph(get_farsi_formatted_text('- {} در {}'.format(exp['title'],
                             exp['company']['name'])), right_normal_style),
                                   Paragraph(get_farsi_formatted_text(exp['description']), right_small_style)]

            if exp['currently_work_here']:
                p2 = Paragraph(get_farsi_formatted_text('از تاریخ: {}    تاکنون').format(
                        get_jalali_date(exp['from_date'])), right_small_style)
            else:
                p2 = Paragraph(get_farsi_formatted_text('از تاریخ: {}    تا تاریخ: {}').format(
                    get_jalali_date(exp['from_date']), get_jalali_date(exp['to_date'])), right_small_style)
            # story.append(Spacer(1, 5))
            expes.append([p2, p1])
        # colWidths = [2*inch, 3*inch, 2*inch]
        # rowHeights = []
        # table = Table(expes, colWidths=colWidths, rowHeights=rowHeights)
        table = Table(expes)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), colors.white),
                                   ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                                   ("VALIGN", (0, 0), (-1, -1), "RIGHT"),
                                   ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                                   # ('RIGHTPADDING', (0, 0), (0, 0), 0)
                                   # ,('ALIGN', (-1, -1), (-1, -1), 'CENTER')
                                   ]))
        story.append(table)
        story.append(Spacer(1, 5))

    if user['educations']:
        story.append(d)
        story.append(Paragraph(get_farsi_formatted_text('سوابق تحصیلی :'), right_bold_style))
        story.append(Spacer(1, 3))
        story.append(d)
        story.append(Spacer(1, 3))

        edus = []
        for edu in user['educations']:
            # p1 = [Paragraph(get_farsi_formatted_text(edu['school']['title']),
            #                         right_normal_indented_style),
            #               Paragraph(get_farsi_formatted_text('- {} {}'.format(edu['degree'], edu['field_of_study'])),
            #                         right_normal_style)]
            p1 = Paragraph(get_farsi_formatted_text(' - {}  {} از {}'.format(edu['degree'], edu['field_of_study'],
                                             edu['school']['title'])), right_normal_style)
            p4 = ''
            if edu['date_attended_from'] and edu['date_attended_to']:
                p4 = Paragraph(get_farsi_formatted_text('از تاریخ: {}    تا تاریخ: {}').format(
                    get_jalali_date(edu['date_attended_from']), get_jalali_date(edu['date_attended_to'])), right_small_style)
            edus.append([p4, p1])
            # story.append(Paragraph(get_farsi_formatted_text(' - {}  {} از {}'.format(edu['degree'], edu['field_of_study'],
            #                                                                        edu['school']['title'])), right_normal_indented_style))
            if edu['grade']:
                p2 = Paragraph(get_farsi_formatted_text('معدل: {}'.format(get_farsi_numbers(edu['grade']))),
                                                                right_small_style)
                edus.append(["", p2])
            if edu['description']:
                p3 = Paragraph(get_farsi_formatted_text('{}'.format(edu['description'])),
                                   right_normal_indented_style)
                edus.append(["", p3])
            # story.append(Spacer(1, 5))
        table = Table(edus)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), colors.white),
                                   ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                                   # ("VALIGN", (0, 0), (-1, -1), "CENTER"),
                                   ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                                   # ('RIGHTPADDING', (0, 0), (0, 0), 0)
                                   # ,('ALIGN', (-1, -1), (-1, -1), 'CENTER')
                                   ]))
        story.append(table)
        story.append(Spacer(1, 5))

    if user['languages']:
        story.append(d)
        story.append(Paragraph(get_farsi_formatted_text('زبان ها:'), right_bold_style))
        story.append(Spacer(1, 3))
        story.append(d)
        story.append(Spacer(1, 3))

        langs = []
        for lang in user['languages']:
            # story.append(Paragraph(get_farsi_formatted_text('{}  در سطح {}'.format(lang['name'], lang['proficiency'])),
            #                        right_normal_indented_style))
            langs.append([Paragraph(get_farsi_formatted_text(lang['proficiency']),
                                    right_normal_indented_style),
                          Paragraph(get_farsi_formatted_text(' - %s' % lang['name']), right_normal_style)])

        table = Table(langs)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), colors.white),
                                   ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                                   ("VALIGN", (0, 0), (-1, -1), "RIGHT"),
                                   ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                                   ]))
        story.append(table)
        story.append(Spacer(1, 5))

    if user['interest']:
        story.append(d)
        story.append(Paragraph(get_farsi_formatted_text('علاقمندی ها :'), right_bold_style))
        story.append(Spacer(1, 3))
        story.append(d)
        story.append(Paragraph(get_farsi_formatted_text('- {}'.format(user['interest'])), right_normal_indented_style))
        story.append(Spacer(1, 10))

    # doc.build(story)
    doc.watermark = 'MOTANAWEB'
    # logo = 'python_logo.png'
    # p_img = Paragraph('<img src=\"./{}\" width="265" height="75"/>'.format(logo), right_normal_style)
    # p_img = Paragraph('<img src=\"./{}\" width="132" height="37"/>'.format(logo), right_normal_style)
    # p_img_ = ParagraphAndImage()
    # story.append(p_img)
    doc.multiBuild(story, canvasmaker=FooterCanvas)


class FooterCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_canvas(page_count)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_canvas(self, page_count):
        from reportlab.lib.units import inch

        page = get_farsi_text("صفحه {} از {}".format(get_farsi_numbers(str(self._pageNumber)),
                                                          get_farsi_numbers(str(page_count))))
        copyright_text = 'generated by {}'.format('Motanaweb Co.')
        x = 128
        self.saveState()
        self.setStrokeColor(colors.lavender)
        self.setLineWidth(0.3)
        self.line(66, 78, A4[0] - 66, 78)
        self.setStrokeColorRGB(0, 0, 0)
        # self.setLineWidth(0.3)
        # self.line(66, 78, A4[0] - 66, 78)
        self.setFont('Persian', 8)
        self.drawString(A4[0]/2 - len(page)/2, 65, page)
        # self.drawString(A4[0]-x, 67, copyright_text )
        self.drawString(A4[0]/2 - len(copyright_text), 55, copyright_text)
        self.restoreState()
        # self.drawImage(self, p_img, x, y, width=None, height=None, mask=None)
        # self.drawInlineImage(self, p_img, y=100, width=5*inch, height=1*inch, mask='auto')

create_pdf_resume(get_user_data())