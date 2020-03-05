
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.migrations.executor import MigrationExecutor
from django.db import connection
from django.test import TestCase


class OppiaTestMigrations(TestCase):

    @property
    def app(self):
        return 'oppia'

    migrate_from = None
    migrate_to = None

    def setUp(self):
        assert self.migrate_from and self.migrate_to, \
            "TestCase '{}' must define migrate_from and migrate_to " \
            "properties".format(type(self).__name__)
        self.migrate_from = [(self.app, self.migrate_from)]
        self.migrate_to = [(self.app, self.migrate_to)]
        executor = MigrationExecutor(connection)
        old_apps = executor.loader.project_state(self.migrate_from).apps

        # Reverse to the original migration
        executor.migrate(self.migrate_from)

        self.setUpBeforeMigration(old_apps)

        # Run the migration to test
        executor = MigrationExecutor(connection)
        executor.loader.build_graph()  # reload.
        executor.migrate(self.migrate_to)

        self.apps = executor.loader.project_state(self.migrate_to).apps

    def setUpBeforeMigration(self, apps):
        # will be defined in the implementation class
        pass


class TrackerMigrationTestCase(OppiaTestMigrations):

    migrate_from = '0011_auto_20170620_1722'
    migrate_to = '0012_fix_future_tracker_dates'

    def setUpBeforeMigration(self, apps):
        tracker_model = apps.get_model('oppia', 'Tracker')
        future_date = datetime.today() + relativedelta(months=1)
        self.tracker_id = tracker_model.objects.create(
            submitted_date=future_date
        ).id

    '''
    @pytest.mark.xfail(reason="doesn't work on SQLite, so then doesn't work \
        for github workflows")
    def test_trackers_migrated(self):
        tracker_model = apps.get_model('oppia', 'Tracker')

        tracker = tracker_model.objects.get(id=self.tracker_id)
        self.assertEqual(datetime.today(), tracker.submitted_date)
    '''
