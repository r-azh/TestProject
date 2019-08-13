__author__ = 'Nejati'
from flask import Flask, make_response

from TestPython.test_pdf.test_pdfkit.test_pdf_api.pdf_utility import *

app = Flask(__name__)

sample_data = [{'url': 'http://dlmo.asiatech.ir/', 'title': 'DLMO @ MotanaWeb'},
               {'url': 'http://www.rahyabtelecom.com/fa/', 'title': 'Team Lead @ Rahyab-Telecom'},
               {'url': 'http://tamir.parsadp.com/', 'title': 'IPN @ ParsaDP'}]


@app.route('/resume')
def generate_resume():
    template_str = load_template_from_file('resume_template.html')
    resume_str = fulfill_template(template_str, {'experiences': sample_data})
    options = {'encoding': "UTF-8"}
    resume_bytes = convert_into_pdf_stream(resume_str, options)

    response = make_response(resume_bytes)
    response.headers['Content-Type'] = 'application/pdf; charset=utf-8'
    response.headers['Content-Disposition'] = 'attachment; filename=resume.pdf'
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)