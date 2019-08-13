mention = {
    'summary': {
        'text': '#هشتگ 🔴چرا سفر به عراق باید از افزایش عوارض خروج مستثنی شود؟ 🔸بر پایه لایحه بودجه سال 1397، عوارض خروج از کشور از 75 هزار تومان کنونی، تا 440 هزار تومان افزایش خواهد یافت. 🔸برخی منتقد این حجم از افزایش عوارض خروج از کشور هستند، اما در این باره نکاتی قابل تامل وجود دارد که شاید در اظهارنظرها موثر باشد.…',
        'highlights': [
            {'keyword': 'عوارض', 'type': 'keyword_main', 'offset': 38, 'length': 5},
            {'keyword': 'خروج', 'type': 'keyword_required', 'offset': 44, 'length': 4},
            {'keyword': 'عوارض', 'type': 'keyword_main', 'offset': 92, 'length': 5},
            {'keyword': 'خروج', 'type': 'keyword_required', 'offset': 98, 'length': 4},
            {'keyword': 'عوارض', 'type': 'keyword_main', 'offset': 202, 'length': 5},
            {'keyword': 'خروج', 'type': 'keyword_required', 'offset': 208, 'length': 4}]},
    'body': {
        'text': '#هشتگ\n\n🔴چرا سفر به عراق باید از افزایش عوارض خروج مستثنی شود؟\n\n🔸بر پایه لایحه بودجه سال 1397، عوارض خروج از کشور از 75 هزار تومان کنونی، تا 440 هزار تومان افزایش خواهد یافت.\n🔸برخی منتقد این حجم از افزایش عوارض خروج از کشور هستند، اما در این باره نکاتی قابل تامل وجود دارد که شاید در اظهارنظرها موثر باشد.\n🔸در سال 95 بیش از 9 میلیون نفر/سفر خارجی توسط ایرانیان انجام شده که بر اساس برخی برآوردها، بالغ بر 7 میلیارد دلار خروج ارز در پی داشته است.\n🔸طبیعتا بخشی از هزینه های تحمیل شده به کشور از ناحیه خروج ارز، باید از محل عوارض جبران شود و تعرفه کنونی، در مقایسه با هزینه\u200cها قابل مقایسه نیست. لذا از این جهت باید از افزایش تعرفه ها دفاع کرد.\n🔸اما در این میان یک نکته بسیار مهم وجود دارد و آن، مسئله سفر به عتبات عالیات در کشور عراق است. درباره عراق، جز اینکه دولت اسلامی وظیفه تسهیل امر زیارت را به عهده دارد و افزایش عوارض خروج، با این رویکرد در تضاد است، باید دقت داشت که ریال ایران در عراق معتبر است و بسیاری از زائران خریدهای خود را به ریال انجام می\u200cدهند.\n🔸وقتی مردم ایران در عراق ریال هزینه می\u200cکنند، در واقع در حال تقویت ارزش ریال هستند، چرا که این ریال\u200cها نهایتا در بازار ایران هزینه می\u200cشود.\n🔸این است که نمایندگان محترم مجلس ضمن حمایت از افزایش عوارض خروج از کشور، باید سفر به عتبات کشور عراق را از فرمول ارائه شده در جدول شماره 16 از تعرفه\u200cهای درآمدهای موضوع جدول شماره 5 مستثنی کنند.\n\n@jebraily\n@www_snn_ir\n',
        'highlights': [
            {'keyword': 'عوارض', 'type': 'keyword_main', 'offset': 39, 'length': 5},
            {'keyword': 'خروج', 'type': 'keyword_required', 'offset': 45, 'length': 4},
            {'keyword': 'عوارض', 'type': 'keyword_main', 'offset': 94, 'length': 5},
            {'keyword': 'خروج', 'type': 'keyword_required', 'offset': 100, 'length': 4},
            {'keyword': 'عوارض', 'type': 'keyword_main', 'offset': 204, 'length': 5},
            {'keyword': 'خروج', 'type': 'keyword_required', 'offset': 210, 'length': 4},
            {'keyword': 'خروج', 'type': 'keyword_required', 'offset': 419, 'length': 4},
            {'keyword': 'خروج', 'type': 'keyword_required', 'offset': 498, 'length': 4},
            {'keyword': 'عوارض', 'type': 'keyword_main', 'offset': 520, 'length': 5},
            {'keyword': 'عوارض', 'type': 'keyword_main', 'offset': 816, 'length': 5},
            {'keyword': 'خروج', 'type': 'keyword_required', 'offset': 822, 'length': 4},
            {'keyword': 'عوارض', 'type': 'keyword_main', 'offset': 1149, 'length': 5},
            {'keyword': 'خروج', 'type': 'keyword_required', 'offset': 1155, 'length': 4}
        ]
    }
}


def tag_highlights_in_text(input):
    text = input['text']
    highlights = input['highlights']

    marked_text_array = []
    marked_text = text
    actual_start = 0

    for h in highlights:
        start = h['offset'] - actual_start
        part_one = marked_text[0:start]
        part_two = marked_text[start: start + h['length']]
        marked_text = marked_text[start + h['length']:]
        actual_start = len(text) - len(marked_text)
        style_class = h['type']
        marked_text_array.append(f'{part_one}<b class="{style_class}">{part_two}</b>')
    marked_text_array.append(marked_text)
    return ''.join(marked_text_array)

result = tag_highlights_in_text(mention['summary'])
print(result)