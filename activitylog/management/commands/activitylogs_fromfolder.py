import fnmatch
import os
import time

from django.core.management.base import BaseCommand

from activitylog.views import process_activitylog
from helpers.messages import MessagesDelegate


class Command(BaseCommand):
    help = 'Script to process activity log files from a source directory'

    def add_arguments(self, parser):

        parser.add_argument(
            'source',
            type=str,
            help=("Source folder that contains the activity log JSON files to "
                  "process")
        )

    def get_files(self, path):
        if not os.path.exists(path):
            print('Error: File "{}" does not exist'.format(path))
            return False

        if not os.path.isdir(path):
            print('Error: "{}" is not a directory'.format(path))
            return False

        if not os.access(path, os.R_OK):
            print('Error: You don\'t have read permission to access "{}"'
                  .format(path))
            return False

        jsonfiles = [f for f in os.listdir(path) if
                     os.path.isfile(
                         os.path.join(path, f)) and fnmatch.fnmatch(f,
                                                                    '*.json')]

        if len(jsonfiles) == 0:
            print('Source folder does not contain any JSON file')

        return jsonfiles

    def handle(self, *args, **options):
        sourcedir = options['source']
        jsonfiles = self.get_files(sourcedir)

        if not jsonfiles:
            exit(-1)

        start_time = time.time()
        messages_delegate = MessagesDelegate()
        for json in jsonfiles:
            filename = os.path.join(sourcedir, json)
            print('Processing {}:'.format(filename))
            with open(filename, 'rb') as file:
                file_data = file.read()
                success, errors = process_activitylog(messages_delegate, file_data)
                if success:
                    print("Success!")
                else:
                    print("Errors: " + str(errors))

        print("Process finished. Time taken: %s seconds"
              % (time.time() - start_time))
