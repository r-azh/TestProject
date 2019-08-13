import re

text = "… 🔸برخی منتقد این حجم از افزایش عوارض خروج از کشور هستند، اما در این باره نکاتی قابل تامل وجود دارد که شاید در اظهارنظرها موثر باشد. 🔸در سال 95 بیش از 9 میلیون نفر/سفر خارجی توسط ایرانیان انجام شده که بر اساس برخی برآوردها، بالغ بر 7 میلیارد دلار خروج ارز در پی داشته است. 🔸طبیعتا بخشی از هزینه های تحمیل شده به کشور از ناحیه خروج ارز، باید از محل عوارض جبران شود و تعرفه کنونی، در مقایسه با هزینه‌ها قابل مقایسه نیست.…"

keyword = 'کشور'

keyword_regex = re.compile(r'\b%s\b' % keyword)

result = keyword_regex.finditer(text)

for match in result:
    print(f'starts {match.span()[0]}, len {len(keyword)}')


def _convert_keyword_to_list(keyword):
    result = list()
    prev_char = ""
    characters = list(keyword)
    for character in characters:
        if character == "\\" and prev_char == "":
            prev_char = character
            continue

        result.append(prev_char + character)
        prev_char = ""

    return result

# keyword = 'قابل مقایسه'
keyword = 'قابل مقــــــــــایسه'
# keyword = 'قابل     مقایسه'

pattern = re.escape(keyword)
# pattern = ''.join(_convert_keyword_to_list(normalized_keyword))

print(pattern)
result = re.compile(pattern).finditer(text)

for match in result:
    print(f'starts {match.span()[0]}, len {len(keyword)}')


def get_keyword_regex(keyword):
    separators = [r'\s', u'\u200c', 'ـ']
    separators_pattern = "[%s]*"%("".join(separators))
    normalized_keyword = re.escape(re.sub(re.compile(separators_pattern), r'', keyword))
    pattern = separators_pattern.join(_convert_keyword_to_list(normalized_keyword))
    print(pattern)
    return pattern

pattern = get_keyword_regex(keyword)
result = re.compile(pattern).finditer(text)
for match in result:
    print(f'starts {match.span()[0]}, len {len(keyword)}')


text2 = 'اکران فیلم‌های جـــار به کارگردانی حسین شمس (رییس جار) هر شب از صدا و سیما'
keyword2 = ' صدا  و  سیما'
pattern = get_keyword_regex(keyword2)
result = re.compile(pattern).finditer(text2)
for match in result:
    print(f'starts {match.span()[0]}, len {len(keyword2)}')