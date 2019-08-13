from django.core.management.base import BaseCommand, CommandError
from TestPython.test_django.test_django.polls.models import Question as Poll
from django.utils import translation
__author__ = 'R.Azh'

# custom django-admin commands
#  Applications can register their own actions with manage.py.
# To do this, just add a management/commands directory to the application. Django will register a manage.py command
#  for each Python module in that directory whose name doesn’t begin with an underscore.

# Custom management commands are especially useful for running standalone scripts or for scripts that are periodically
# executed from the UNIX crontab or from Windows scheduled tasks control panel.


class Command(BaseCommand):
    help = 'Close the specified poll for voting'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('poll_id', nargs='+', type=int)

        # Named (optional) arguments
        parser.add_argument('--delete',
                            action='store_true',
                            dest='delete',
                            default=False,
                            help='Delete poll instead of closing it',)

    def handle(self, *args, **options):
        # Activate a fixed locale, e.g. Russian
        translation.activate('ru')

        # Or you can activate the LANGUAGE_CODE # chosen in the settings:
        from django.conf import settings
        translation.activate(settings.LANGUAGE_CODE)
        for poll_id in options['poll_id']:
            try:
                poll = Poll.objects.get(pk=poll_id)
            except Poll.DoesNotExist:
                raise CommandError('Poll "%s" does not exist' % poll_id)
            poll.opened = False
            poll.save()

            if options['delete']:
                poll.delete()

            self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))

            translation.deactivate()


# you don’t need to end messages with a newline character, it will be added automatically, unless you specify the
# ending parameter:
# self.stdout.write("Unterminated line", ending='')

# If, for some reason, your custom management command needs to use a fixed locale, you should manually activate and \
#         deactivate it in your handle() method using the functions provided by the I18N support code

