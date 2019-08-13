from jinja2 import Template
from pdfkit import pdfkit

__author__ = 'R.Azh'

sample_data = [{'url': 'http://www.google.com/', 'title': 'گوگل'},
               {'url': 'http://www.yahoo.com/fa/', 'title': 'یاهو'},
               {'url': 'http://www.amazon.com/', 'title': 'آمازون'}]

with open('template.html', 'r') as template_file:
    template_str = template_file.read()
    template = Template(template_str)
    resume_str = template.render({'experiences': sample_data})

    options = {'encoding': "UTF-8", 'quiet': ''}
    bytes_array = pdfkit.PDFKit(resume_str, 'string', options=options).to_pdf()
    with open('result.pdf', 'wb') as output:
        output.write(bytes_array)