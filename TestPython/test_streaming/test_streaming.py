import base64
import mimetypes
import os
import re
from flask import Response, request, send_file, Flask

__author__ = 'R.Azh'
app = Flask(__name__)


@app.route('/files/video_files/<file_name>', methods=['GET'])
def video_download(file_name):
    bytes_indicator = request.headers.get('Range', None)
    dto = {"storage_name": 'video_files', "file_name": file_name, "bytes_indicator": bytes_indicator}
    file_download_reader = FileDownload(dto)
    file_content, file_path = file_download_reader.execute()
    if not bytes_indicator:
        return send_file(file_path)
    path, mimetype, file_size, from_bytes, to_bytes, read_length = file_path
    response = Response(file_content, 206, mimetype=mimetype, direct_passthrough=True)
    response.headers.add('Content-Range', 'bytes {0}-{1}/{2}'.format(from_bytes, from_bytes + read_length - 1, file_size))
    return response


class FileDownload:
    storage_name = None
    file_name = None
    bytes_indicator = None

    def __init__(self, dto):
        self.__dict__.update(dto)

    def execute(self):
        from_bytes = to_bytes = None
        if self.bytes_indicator:
            from_bytes, to_bytes = 0, None
            m = re.search('(\d+)-(\d*)', self.bytes_indicator)
            g = m.groups()
            if g[0]: from_bytes = int(g[0])
            if g[1]: to_bytes = int(g[1])

        file_content, path = File.get_by_storage_name_file_name(self.storage_name, self.file_name, from_bytes, to_bytes)

        # return FileDownloadDetail.create_from_file(file_content, self.file_name)
        if self.bytes_indicator:
            os_path, mimetype, file_size, read_length = path
            return file_content, (path, mimetype, file_size, from_bytes, to_bytes, read_length)
        return file_content, path


class File:
    @classmethod
    def get_by_storage_name_file_name(cls, storage_name, file_name, from_bytes=None, to_bytes=None):
        file_content, path = cls.get_content_by_path(cls._path_create(storage_name, file_name), from_bytes, to_bytes)
        return file_content, path

    @classmethod
    def _path_create(cls, storage_name, file_id):
        return "/files/{}/{}".format(storage_name, file_id)

    @classmethod
    def get_content_by_path(self, path, from_bytes=None, to_bytes=None):
            try:
                os_path = "{}{}".format(os.curdir, path)
                with open(os_path, 'rb') as file:
                    if from_bytes is not None:
                        mimetype = mimetypes.guess_type(os_path)[0]
                        file_size = os.path.getsize(os_path)
                        read_length = file_size - from_bytes
                        if to_bytes is not None:
                            read_length = to_bytes - from_bytes
                        file.seek(from_bytes)
                        encoded_string = file.read(read_length)
                        os_path = (os_path, mimetype, file_size, read_length)
                    else:
                        encoded_string = file.read()
            except:
                mimetype = 'image/png'
                encoded_string = \
                    'iVBORw0KGgoAAAANSUhEUgAAAMwAAADMCAMAAAAI/LzAAAAAXVBMVEWZmZn///+AgICWlpaLi4t9fX2SkpLs7OyQkJB5eXnv7+/7' \
                    '+/vy8vKcnJx0dHTj4+OoqKi+vr7Q0NDIyMiioqKurq7Y2Njd3d22trbExMSysrLMzMyFhYW6urrh4eFZXkG8AAAGJElEQVR4nO2d' \
                    'W3ujOAxA4yiBNMBwCTAkpP3/P3NgGTaXgvBFst1dn7f2qeeT5Buyu9sFAoFAIBAIBAKBQCAQCAQCgUAgEAgEAoFA4L8AAET/Mvzg' \
                    '+u/RZdCAuuzbPP5L3vZlPfzypxnBLqu7NhULpG1XZ7sfIwRQ3y75kshMfrnVPyJAEBV9vhiTl/jkfRH5rjOoLGfXUr75rQNZg6bX' \
                    't3RrMm91oGlVVEbaxk8byCrJBHsmrXwMTnQ7q6uMnG+R67/9DaiVM+xBW3sVHFAr/HdynyoHPjVTbOb86Y0NXBMzFyGSqy82lanK' \
                    'SOXa4h8yEhch+sy1yZBjRC5DbJxnGlyoXIRwXTfQ07kIcXFqA5+ULkJ0DhcD0GisxjBSd2sBqI3m/SW+nG1AM4P12Br9wY0LlPQu' \
                    'QjR3NzbGi5glkr2L2EQMSTbSf9i3gY4lMENo6qN1G/qRbOb3wbYNlEyBGULTHC3XDV9gxtDsrdpQr2NeKY57m5kWxZwyXx97izZQ' \
                    'cLoIcTru7WUa3Y5smcsQGms2NdtQNpEeRhk7mcY4Lk8ktzHP7MQGfvO6CNFOMjZsCtaxbCSObNmwZ9m0CtjbqRvSU4xlrn9l2GOT' \
                    'ffHLtPe9HZuC+BhjifR0tGIDDb+LENlDhrNuePb+7zQPGc7YcK9lJqYVDbtNZKH+hxHgRYbNJjL8TCZH/CrDVTcR+5Q5kv7a7y3E' \
                    '5mTDRYh3GR4bVzIsNs5kOOrGmQxHbBzK0Nu4lCG3cSpDXTdOZahj41iG1sbScmZVhtSG92h2Jv9YlaGsG/6DppFqXYYyNpQdJut8' \
                    'HhEZOhvobMjUqAyZDRQW9gBJhMuQ1U1tYQTID6gLXWw4OjPeqe5bMkQ2cOWX6fAso8s0uLGfAqYb9U9ow/mpeeJrO8uoMo3/5OyC' \
                    'TZm0NtBwfwbcSWQZVaYB8+CcS7qQ2HAfNzfSMhSZBqwuiYILgQ1tC/A7pZKMcaYB5wenFJRkCOqGcXS+KKmMGNqQtzQ/OGdqgSGw' \
                    'idiqppScMJ8xzbSM6VwjllvJ0NpwbThllphLGNqwbGsqTRdTG44dZ37QljHLNPgkX2+mhbbLgFFo6JtorgYqpjJA/BW9NYmLqQzx' \
                    'XkB+5c8j0xDa5IprMmqZwYZs7oxlt5dsMjuoiRZpZ/1BmUxmsCGJTWzuQiBDUzfG9UIkMywFjEfo9kTgQiNjfJB2PVK4EMkMKxuD' \
                    'YSAuNHYwjDLjMy2aC7WkoigXWplIdx8dwy+vZGCXdQYjWl7c/akZKK6Gg3PenSh0CFTqnmKeKQ/mo4Cxyu5KtDiLO+PgmKqYvjjz' \
                    'olPsXe5nGuJmjQpcyUB2IT/VPJd3g+AYuLC0AyS5wUCgrbLj+n6edNqVo+tSMLY2VRutJsQyoPsymxxxppdqWi5RydzVkDZaNjph' \
                    'oXpqCuOiM6rpuFjoAxo7gdRt1F1qK12Nw05a/YRDPS6WXMbbjao2qi6FlT7giVh1C6oaFwtXNJ9sFGOj5mKrXmYU60YtLpZdVOtG' \
                    'RcbOmPyKRK+mlkxk5bLpO7JtdGoydm4Bf0dhZSPvwt9lukwq330iLWNzgnlFfrqRlrE+kD2oiCNjoy97nU6ybCRdapcuIpGcO+Vk' \
                    'MiuXmdbJ5WYbORkr138QkpJMhrHrTxa5rm2pwDgcyWZaosjwvjIni0y7k0xgnE2Xz8QkkXE7xTyQmGy2ZWgaMMyRaOHYDoyFV6bk' \
                    '2G6q33Thf8tMlnyzi2MzMp5UzMjmpbotF9cLmWc2FzVbWebFHDOzNddsyNi5Li8Lcq1eQob7JVNVNr5Cbcg4OFzC6PHQ4DK+TJgz' \
                    'MX59Gw8M/xuTaswvn2pFxrMsG/JMOzIezf4zMToEoDJeTTIT6FSDZpmTw2Uc9KYg5uLTUmYGXdJgMm4Py1bAdjVYyTg69sfB7nBj' \
                    'Mt4NzCPYS0GIzMmzGXPi25OUcjJelsxQNDoydl4xUge5lIrIeHOS8QryItW6TOTBoewS7foIgETGwylzBNluIvXv2V5mBtnTrAfG' \
                    '/XeMZc7rXzfWZVx9Kt8C+ZS+LmP+70t5QHab6zK+bZlntGQ8nWawA/R1GQ93ZhPrrUFBxi3/dxn/zsxm1mX+ABXVkCtbgdBdAAAA' \
                    'AElFTkSuQmCC'
                encoded_string = base64.b64decode(encoded_string)
            finally:
                return encoded_string, os_path
                # return {'file_content': encoded_string, 'mimetype': mimetype}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)