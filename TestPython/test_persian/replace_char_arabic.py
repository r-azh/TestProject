text ="… حتماً فاز دوم اين طرح اجرا خواهد شد و اجراي کامل این طرح از تعهدات دولت و مورد تاکید مقام معظم رهبری است. 🔹 تاکنون 1 میلیارد و 150 میلیون دلار ریال از منابع برداشت شده از صندوق توسعه ملی برای اجرای این طرح هزینه شده و حدود 350 میلیون دلار دیگر باقی مانده است و اگر با کسری منابع مواجه شویم، دولت راهکاری پیدا خواهد کرد.…"

__Alphabets = {
    '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4', '٥': '5', '٦': '6', '٧': '7', '٨': '8',
    '٩': '9', '۱': '1', '۲': '2', '۳': '3', '۴': '4', '۵': '5', '۶': '6', '۷': '7', '۸': '8',
    '۹': '9', '۰': '0',
    'ك': 'ک',
    'ى': 'ی',
    'ي': 'ی',
    'ة': 'ه',
}

text = text.replace('ک', 'ك')
# text = text.replace('ی', 'ى')
text = text.replace('ی', 'ي')
# text = text.replace('ه', 'ة')
print(text)