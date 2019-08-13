# -*- coding: utf-8 -*-
import urllib
from urllib.request import urlretrieve
from bson import ObjectId
from pymongo import MongoClient
from bidi.algorithm import get_display
from reportlab.graphics.shapes import Line, Drawing, Rect
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from rtl import reshaper

__author__ = 'R.Azh'


def get_user_data():
    dbClient = MongoClient('localhost', 27017)
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
    return reshaper.replace_digits('{}-{}-{}'.format(jalai_date['jd'], jalai_date['jm'], jalai_date['jy']))


def get_farsi_numbers(text):
    return reshaper.replace_digits(text)


def create_pdf_resume(user):
    from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_CENTER
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    doc = SimpleDocTemplate("farsi_resume.pdf", pagesize=letter, rightMargin=110, leftMargin=72, topMargin=72,
                            bottomMargin=18)
    pdfmetrics.registerFont(TTFont('Persian', 'Bahij-Nazanin-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('Persian-Bold', 'Bahij-Nazanin-Bold.ttf'))

    story = []

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontName='Persian', fontSize=10))
    styles.add(ParagraphStyle(name='Justify-Bold', alignment=TA_JUSTIFY, fontName='Persian-Bold', fontSize=10))
    bold_style = styles['Justify-Bold']
    normal_style = styles['Justify']
    styles.add(ParagraphStyle(name='Right-indented', alignment=TA_RIGHT, fontName='Persian', fontSize=10,
                              rightIndent=10, wordWrap='CJK'))
    styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT, fontName='Persian', fontSize=10,
                              rightIndent=10,
                              wordWrap='CJK'))
    styles.add(ParagraphStyle(name='Right-Bold', alignment=TA_RIGHT, fontName='Persian-Bold', fontSize=10))
    # styles.add(ParagraphStyle(name='Right-Bold-Titr', alignment=TA_RIGHT, fontName='Persian-Bold', fontSize=12,
    #                           backColor=colors.lavender, borderPadding=5, borderRadius=5, borderWidth=1))
    styles.add(ParagraphStyle(name='Right-Bold-Titr', alignment=TA_RIGHT, fontName='Persian-Bold', fontSize=12))
    styles.add(ParagraphStyle(name='Right-small', alignment=TA_RIGHT, fontName='Persian', fontSize=8,
                              rightIndent=20,
                              wordWrap='CJK'))
    right_bold_style = styles['Right-Bold']
    right_normal_indented_style = styles['Right-indented']
    right_normal_style = styles['Right']
    right_small_style = styles['Right-small']
    right_bold_titr_style = styles['Right-Bold-Titr']
    styles.add(ParagraphStyle(name='Centre', alignment=TA_CENTER, fontName='Persian', fontSize=10))
    styles.add(ParagraphStyle(name='Centre-Bold', alignment=TA_CENTER, fontName='Persian-Bold', fontSize=10))
    centre_bold_style = styles['Centre-Bold']
    centre_normal_style = styles['Centre']

    # story.append(Paragraph(get_farsi_formatted_text('بسمه تعالی'), centre_normal_style))
    # story.append(Spacer(1, 15))

    d = Drawing(100, 1)
    line = Line(0, 0, 450, 0)
    d.add(line)
    story.append(d)
    story.append(Spacer(1, 15))

    # logo = 'python_logo.png'
    req = urllib.request.Request("http://tipn.parsadp.com/api/v1.0{}".format(user['image']))
    req.add_header('token', 'og4ZNFIdbDW9sahj3DqWpVgSA2YiPVtuCBqbYhbx5QuZ2qH47syY2eazArK6HKujtF+w1GUBI1L1J7xeXPmBFDv4j45gubO2CX8qxmuYs3u31RgfdbK+cW3JdezhAoEG')
    logo = urllib.request.urlopen(req)
    img = Image(logo, 1*inch, 1*inch, hAlign='RIGHT')
    # story.append(img)

    text = '{}<br/>{}<br/>{}<br/>{}<br/>{}<br/>'.format(
        get_farsi_formatted_text('نام و نام خانوادگی: {} {}'.format(user['name'], user['last_name'])),
        get_farsi_formatted_text('تاریخ تولد: {}'.format(get_jalali_date(user['birthday']))),
        get_farsi_formatted_text('وضعیت تاهل: {}'.format(user['is_married'])),
        get_farsi_formatted_text('ایمیل: {}'.format(user['email'])),
        get_farsi_formatted_text('آدرس: {}'.format(user['address'])))

    p = Paragraph(text, right_normal_style)
    table = Table([['', p, img]])
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), colors.white),
                               ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                               ("VALIGN", (0, 1), (-1, -1), "CENTER"),
                               ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                               ('RIGHTPADDING', (0, 0), (0, 0), 0)
                               # ,('ALIGN', (-1, -1), (-1, -1), 'CENTER')
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

        for prof in user['proficiencies']:
            story.append(Paragraph(get_farsi_formatted_text(' - {}  در سطح {}'.format(prof['skill']['title'],
                                                                                      prof['skill_level'])),
                                   right_normal_indented_style))
            story.append(Spacer(1, 5))

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
        for exp in user['experiences']:
            story.append(Paragraph(get_farsi_formatted_text(' - {} در {}'.format(exp['title'], exp['company']['name'])),
                                   right_normal_indented_style))
            story.append(Paragraph(get_farsi_formatted_text('{}'.format(exp['description'])),
                                   right_normal_indented_style))
            if exp['currently_work_here']:
                story.append(Paragraph(get_farsi_formatted_text('از تاریخ: {}    تاکنون').format(
                    get_jalali_date(exp['from_date'])), right_small_style))
            else:
                story.append(Paragraph(get_farsi_formatted_text('از تاریخ: {}    تا تاریخ: {}').format(
                    get_jalali_date(exp['from_date']), get_jalali_date(exp['to_date'])), right_small_style))
            story.append(Spacer(1, 5))
        story.append(Spacer(1, 5))

    if user['educations']:
        story.append(d)
        story.append(Paragraph(get_farsi_formatted_text('سوابق تحصیلی :'), right_bold_style))
        story.append(Spacer(1, 3))
        story.append(d)
        for edu in user['educations']:
            story.append(Paragraph(get_farsi_formatted_text(' - {}  {} از {}'.format(edu['degree'], edu['field_of_study'],
                                                                                   edu['school']['title'])), right_normal_indented_style))
            if edu['grade']:
                story.append(Paragraph(get_farsi_formatted_text('معدل: {}'.format(get_farsi_numbers(edu['grade']))),
                                                                right_small_style))
            if edu['description']:
                story.append(Paragraph(get_farsi_formatted_text('{}'.format(edu['description'])),
                                   right_normal_indented_style))
            story.append(Paragraph(get_farsi_formatted_text('از تاریخ: {}    تا تاریخ: {}').format(
                get_jalali_date(edu['date_attended_from']), get_jalali_date(edu['date_attended_to'])), right_small_style))
            story.append(Spacer(1, 5))
        story.append(Spacer(1, 5))

    if user['languages']:
        story.append(d)
        story.append(Paragraph(get_farsi_formatted_text('زبان ها:'), right_bold_style))
        story.append(Spacer(1, 3))
        story.append(d)
        for lang in user['languages']:
            story.append(Paragraph(get_farsi_formatted_text('{}  در سطح {}'.format(lang['name'], lang['proficiency'])),
                                   right_normal_indented_style))
        story.append(Spacer(1, 5))

    if user['interest']:
        story.append(d)
        story.append(Paragraph(get_farsi_formatted_text('علاقمندی ها :'), right_bold_style))
        story.append(Spacer(1, 3))
        story.append(d)
        story.append(Paragraph(get_farsi_formatted_text('- {}'.format(user['interest'])), right_normal_indented_style))
        story.append(Spacer(1, 10))

    doc.build(story)

create_pdf_resume(get_user_data())