from flask import g, request, json
from TestPython.test_flask.test_flask_locale.test_flask_babel.app import babel, app
from flask_babel import gettext, _

@app.route('/hello', methods=['GET'])
def hello():
    return json.dumps({
        "locale_language": get_locale(),
        "timezone": get_timezone()
    })


@app.route('/texts')
def retrieve_text():
    string1 = gettext('this is a text messgae')
    string2 = gettext('this is second text messgae')
    string3 = _('this is third text messgae')
    str4 = _("text 4")

    return "{}\n{}\n{}\n{}".format(string1, string2, string3, str4)


# Use the browser's language preferences to select an available translation
@babel.localeselector
def get_locale():
    # if a user is logged in, use the locale from the user settings
    user = getattr(g, 'user', None)
    if user is not None:
        return user.locale
    # otherwise try to guess the language from the user accept
    # header the browser transmits.  We support de/fr/en in this
    # example.  The best match wins.
    available_locale = ['de', 'fr', 'en', 'fa']
    # available_locale = [str(translation) for translation in babel.list_translations()]
    return request.accept_languages.best_match(available_locale)


@babel.timezoneselector
def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone

