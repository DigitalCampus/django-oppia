from django.db.migrations.executor import MigrationExecutor
from django.db import connection
from django.test import TestCase


class QuizTestMigrations(TestCase):

    @property
    def app(self):
        return 'quiz'

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


class QuizDictsTestCase(QuizTestMigrations):

    migrate_from = '0012_merge_20191228_1740'
    migrate_to = '0013_cleanup_quiz_dicts'

    def setUpBeforeMigration(self, apps):
        quiz_model = apps.get_model('quiz', 'Quiz')
        self.quiz_id_1 = quiz_model.objects.create(
            title="{u'en': u'Substance Abuse'}",
            description="{u'en': u'A long description about the quiz'}"
        ).id

        self.quiz_id_2 = quiz_model.objects.create(
            title="Substance Abuse",
            description="A long description about the quiz"
        ).id

        question_model = apps.get_model('quiz', 'Question')
        self.question_1 = question_model.objects.create(
            title="{u'en': u'my question about stuff'}"
        )
        self.question_id_1 = self.question_1.id

        self.question_id_2 = question_model.objects.create(
            title="my question about stuff"
        ).id

        response_model = apps.get_model('quiz', 'Response')
        self.response_id_1 = response_model.objects.create(
            title="{u'en': u'option 1'}",
            question=self.question_1
        ).id

        self.response_id_2 = response_model.objects.create(
            title="option 2",
            question=self.question_1
        ).id

        self.response_id_3 = response_model.objects.create(
            title="100",
            question=self.question_1
        ).id
