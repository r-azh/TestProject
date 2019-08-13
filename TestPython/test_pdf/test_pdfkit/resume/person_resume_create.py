import base64
from os.path import dirname, realpath, sep
from bson import ObjectId
from jinja2 import Template
import pdfkit
from pymongo import MongoClient
from rtl import reshaper

__author__ = 'R.Azh'


def load_template_from_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as template_file:
        return template_file.read()


def fulfill_template(template_str, data):
    template = Template(template_str)
    string_array = template.render(**data)
    return string_array


def convert_into_pdf_stream(string_array, options=None, css=None, config=None):
    if config:
        config = pdfkit.configuration(**config)
    if not options:
        options = dict()
    options.update({'quiet': ''})
    bytes_array = pdfkit.PDFKit(url_or_file=string_array, type_='string', options=options, css=css,
                                configuration=config).to_pdf()
    return bytes_array


def save_into_file(file_fullname, bytes_stream):
    with open(file_fullname, 'wb') as output:
        output.write(bytes_stream)


def get_jalali_date_from_isoformat_date(isoformat_date):
    import dateutil.parser
    import jalaali

    _date = dateutil.parser.parse(isoformat_date)
    jalai_date = jalaali.Jalaali().to_jalaali(_date.year, _date.month, _date.day)
    return reshaper.replace_digits('{}/{}/{}'.format(jalai_date['jy'], jalai_date['jm'], jalai_date['jd']))


def pdf_resume_stream(person_info):
    path = dirname(realpath(__file__))
    if person_info['birthday']:
        person_info['birthday'] = get_jalali_date_from_isoformat_date(person_info['birthday'])
    for exp in person_info['experiences']:
        exp['from_date'] = get_jalali_date_from_isoformat_date(exp['from_date'])
        if exp['to_date']:
            exp['to_date'] = get_jalali_date_from_isoformat_date(exp['to_date'])
    for edu in person_info['educations']:
        if edu['date_attended_from']:
            edu['date_attended_from'] = get_jalali_date_from_isoformat_date(edu['date_attended_from'])
        if edu['date_attended_to']:
            edu['date_attended_to'] = get_jalali_date_from_isoformat_date(edu['date_attended_to'])
    if person_info['image']:
        person_info['image'] = '{}/{}'.format(path, 'images/avatar.jpg')
    else:                                                   # another way
        f = open('images/avatar.jpg', 'rb')
        image_file = f.read()
        img_byte = base64.b64encode(image_file)
        person_info['image'] = "data:image/{};base64,{}".format('jpg', img_byte.decode('utf8'))

    template_str = load_template_from_file('{}{}resume_template.html'.format(path, sep))
    resume_str = fulfill_template(template_str, {'person': person_info, "path": path})
    options = {'encoding': "UTF-8"}
    wkhtmltopdf_path = "/usr/bin/wkhtmltopdf"
    config = {'wkhtmltopdf': wkhtmltopdf_path}
    resume_bytes = convert_into_pdf_stream(string_array=resume_str, options=options, config=config)
    file_name = '{}_{}.pdf'.format(person_info['name'], person_info['last_name'])
    save_into_file('resume.html', bytes(resume_str, encoding='utf8'))
    save_into_file(file_name, resume_bytes)


dbClient = MongoClient('localhost', 27017)
db = dbClient.ipn
user = db.person.find({'_id': ObjectId('560121abcbf62c13d4567f0d')})

pdf_resume_stream(user[0])



