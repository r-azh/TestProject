from __future__ import unicode_literals

__author__ = 'R.Azh'
from hazm import *

normalizer = Normalizer()
text = normalizer.normalize('اصلاح نویسه ها و استفاده از نیم فاصله پردازش را آسان می کند')
print(text)

text = sent_tokenize('ما هم برای وصل کردن آمدیم! ولی برای پردازش، جدا بهتر نیست؟')
print(text)

text = word_tokenize('ولی برای پردازش، جدا بهتر نیست؟')
print(text)

stemmer = Stemmer()
text = stemmer.stem('کتاب‌ها')
print(text)

lemmatizer = Lemmatizer()
text = lemmatizer.lemmatize('می‌روم')
print(text)

# tagger = POSTagger(model='resources/postagger.model')
# text = tagger.tag(word_tokenize('ما بسیار کتاب می‌خوانیم'))
# print(text)

# chunker = Chunker(model='resources/chunker.model')
# tagged = tagger.tag(word_tokenize('کتاب خواندن را دوست داریم'))
# txt = tree2brackets(chunker.parse(tagged))
# print(txt)

# parser = DependencyParser(tagger=tagger, lemmatizer=lemmatizer)
# parser.parse(word_tokenize('زنگ‌ها برای که به صدا درمی‌آید؟'))

text = "سلامخداحافظ نتاناkhgjhgg نتالتنار"
txt = normalizer.normalize(text)
print(txt)
