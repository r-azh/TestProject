# pip install email-normalize

from email_normalize import normalize
# from email_normalizer import normalize

normalized = normalize('f.o.o+bar@gmail.com')
print(normalized)

normalized = normalize('test_s@hotmail.com')
print(normalized)

normalized = normalize('test-s@hotmail.com')
print(normalized)


