from html2text import HTML2Text

__html_normalizer = HTML2Text()
__html_normalizer.ignore_links = True
__html_normalizer.style = 'pretty'
__html_normalizer.body_width = 0

def patched_handle_tag(tag, attrs, start):
    if tag == "br" and start:
        if __html_normalizer.blockquote > 0:
            __html_normalizer.o("\n>")
        else:
            __html_normalizer.o("\n")
    else:
        __original_handle_tag(tag, attrs, start)


__original_handle_tag = __html_normalizer.handle_tag
# __html_normalizer.handle_tag = patched_handle_tag

text = '''
        یک شهر پر از آدم و این حجم پر از درد  
لعنت شود آن شب که تو را برد و نیاورد ...  

 _ **✍ 🏼**_ #مهتاب_بهشتی  
 _ **🔸 ️**_ #كافه_كتاب _**☕ ️**_ _ **📚**_  

[@CafeKetab_Channe](https://t.me/CafeKetab_Channe)


        '''

# __html_normalizer.unicode_snob = True  # Prevents accents removing
__html_normalizer.ignore_anchors = True  # Prevents accents removing
result = __html_normalizer.handle(text)
result = __html_normalizer.handle(text.replace('\r\n', '<br>').replace('\n', '<br>'))
# result = __html_normalizer.unescape(result)

print(result)
