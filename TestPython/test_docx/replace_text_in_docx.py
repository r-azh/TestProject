from docx import Document


def replace_text_in_docx(file_path: str, filename: str, text_to_find: str, text_to_replace: str):
    if not file_path.endswith('\\'):
        file_path += '\\'
    # try:
    document = Document(file_path + filename)
    # except Exception as ex:
    #     print('Problem openning file: ', filename, ex)
    #     return

    # Paragraph-level formatting, such as style, is preserved. All run-level formatting, such as bold or italic, is
    # removed so we use runs
    for paragraph in document.paragraphs:
        if text_to_find in paragraph.text:
            inline = paragraph.runs
            # Loop added to work with runs (strings with same style)
            for i in range(len(inline)):
                if text_to_find in inline[i].text:
                    text = inline[i].text.replace(text_to_find, text_to_replace)
                    inline[i].text = text

    document.save(file_path + 'edited_' + filename)
    print('Replaced all in document')


if __name__ == '__main__':
    replace_text_in_docx(
        file_path='C:\\_Data_\\affirmations',
        filename='affirmations.docx',
        text_to_find=u'سلام',
        text_to_replace=u'خداحافظ'
    )

# مقادیر بعد از if رو عوض کن و فایل رو سیو کن و بعد با پایتون 3 اجراش کن رو سیستمت
# cd to path_to_this_script
# python replace_text_in_docx.py
