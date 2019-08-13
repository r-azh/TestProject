# mock is a library for testing in Python. It allows you to replace parts of your system under test with mock objects
# and make assertions about how they have been used.
# https://docs.python.org/dev/library/unittest.mock.html


from unittest import mock

m = mock.Mock()

assert isinstance(m.foo, mock.Mock)
assert isinstance(m.bar, mock.Mock)
assert isinstance(m(), mock.Mock)

assert m.foo is not m.bar is not m()


m.foo = 'bar'
assert m.foo == 'bar'

m.configure_mock(bar='baz')
assert m.bar == 'baz'

m.return_value = 42
assert m() == 42

m.side_effect = ['foo', 'bar', 'baz']
assert m() == 'foo'
assert m() == 'bar'
assert m() == 'baz'

try:
    m()
except StopIteration:
    assert True
else:
    assert False

m.side_effect = RuntimeError('Boom')
try:
    m()
except RuntimeError:
    assert True
else:
    assert False

m.assert_called()

try:
    m.assert_called_once()
except AssertionError:
    assert True
else:
    assert False

try:
    m(1, foo='bar')
except RuntimeError:
    assert True
else:
    assert False

assert m.call_args == mock.call(1, foo='bar')
assert len(m.call_args_list) > 1

m.reset_mock()
assert m.call_args is None


# @mock.patch("app.pandora.models.Medium")
# # @mock.patch("flask_sqlalchemy.SignallingSession", autospec=True)
# # @mock.patch('flask_sqlalchemy._QueryProperty.__get__')
# def test_should_return_list_of_medias_when_media_exists(self, mocked_medium):
#     # mocked_medium = mock.create_autospec("app.pandora.models.Medium")
#     # mocked_medium = mock.magic
#     medium = mocked_medium()
#     medium.name = "Telegram_test"
#     medium.label = "تلگرام"
#
#     mocked_medium.all.return_value = [medium]
#     response = self.get('api.list_media')
#     assert response.status_code == HTTPStatus.OK
#     assert response.data['list'] == []