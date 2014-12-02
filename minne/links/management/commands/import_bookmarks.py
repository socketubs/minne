import datetime
from optparse import make_option

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from minne.links.models import Link
from bs4 import BeautifulSoup


class Command(BaseCommand):
    args = '<bookmark_file>'
    help = 'Import a bookmarks file'
    option_list = BaseCommand.option_list + (
        make_option(
            '--user-id',
            action='store',
            type='int',
            dest='user_id',
            help='Set owner of imported links'))

    def handle(self, *args, **options):
        file_path = args[0]
        file = open(file_path, 'rb')
        self.stdout.write('=> Importing %s...' % file_path.split('/')[-1])
        soup = BeautifulSoup(file.read())
        user_id = options['user_id']
        if not user_id:
            user_id = 1
        user = User.objects.get(user_id)

        for td in soup.find_all('dt')[::-1]:
            self.stdout.write(td.a.get('href'))
            link = Link()
            link.title = td.a.text
            link.url = td.a.get('href')
            link.added = datetime.datetime.fromtimestamp(int(td.a.get('add_date')))
            link.tags = td.a.get('tags').replace(',', ' ')
            link.user = user
            link.save()

        self.stdout.write('Successfully import all bookmarks!')
