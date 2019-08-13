from jinja2 import Template
import pdfkit


def load_template_from_file(file_name):
    with open(file_name, 'r') as template_file:
        return template_file.read()


def fulfill_template(template_str, data):
    template = Template(template_str)
    string_array = template.render(**data)
    return string_array


def convert_into_pdf_stream(string_array, options=None):
    if not options:
        options = dict()
    options.update({'quiet': ''})
    bytes_array = pdfkit.PDFKit(string_array, 'string', options=options).to_pdf()
    return bytes_array


def save_into_file(file_fullname, bytes_stream):
    with open(file_fullname, 'wb') as output:
        output.write(bytes_stream)